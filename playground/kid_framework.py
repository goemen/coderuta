import ast

import streamlit as st
from streamlit_monaco import st_monaco


class PendingInput(Exception):
    def __init__(self, prompt_text: str):
        super().__init__(prompt_text)
        self.prompt_text = prompt_text


class KidRuntime:
    def __init__(self):
        self.lines = []

    def show(self, *values):
        text = " ".join(str(value) for value in values)
        self.lines.append(text)
        return text


def validate_exercise_result(outputs, validation=None, reward=None):
    if not validation:
        return {"passed": False, "message": "", "stars": 0}

    output_text = "\n".join(str(item) for item in outputs).strip()
    validation_type = validation.get("type", "contains")
    expected_value = str(validation.get("value", ""))

    if validation_type == "exact":
        passed = output_text == expected_value
    else:
        passed = expected_value in output_text

    default_reward = {"stars": 10, "message": f"Great job! You earned 10 stars."}
    reward = reward or default_reward if passed else reward
    stars = reward.get("stars", 0) if passed and reward else 0
    if passed:
        message = reward.get("message", f"Great job! You earned {stars} stars.") if reward else "Great job!"
    else:
        message = reward.get("retry_message", "Try again — your output is not quite there yet.") if reward else "Try again."

    return {"passed": passed, "message": message, "stars": stars}


def update_progress(exercise_id: str, stars: int):
    if stars <= 0:
        return

    st.session_state.setdefault("total_stars", 0)
    st.session_state.setdefault("completed_exercises", [])
    st.session_state["total_stars"] += stars

    if exercise_id not in st.session_state["completed_exercises"]:
        st.session_state["completed_exercises"].append(exercise_id)


def get_prompt_input_key(exercise_id: str) -> str:
    prompt_count = st.session_state.get(f"{exercise_id}-prompt-count", 0) + 1
    st.session_state[f"{exercise_id}-prompt-count"] = prompt_count
    return f"{exercise_id}-dialog-input-{prompt_count}"


def _eval_node(node, env, ask_fn):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return env[node.id]
    if isinstance(node, ast.Attribute):
        base = _eval_node(node.value, env, ask_fn)
        return getattr(base, node.attr)
    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(str(value.value))
            elif isinstance(value, ast.FormattedValue):
                parts.append(str(_eval_node(value.value, env, ask_fn)))
            else:
                raise NotImplementedError(f"Unsupported f-string part: {ast.dump(value)}")
        return "".join(parts)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, env, ask_fn)
        right = _eval_node(node.right, env, ask_fn)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
    if isinstance(node, ast.Compare):
        left = _eval_node(node.left, env, ask_fn)
        right = _eval_node(node.comparators[0], env, ask_fn)
        if isinstance(node.ops[0], ast.Eq):
            return left == right
        if isinstance(node.ops[0], ast.Gt):
            return left > right
        if isinstance(node.ops[0], ast.GtE):
            return left >= right
        if isinstance(node.ops[0], ast.Lt):
            return left < right
        if isinstance(node.ops[0], ast.LtE):
            return left <= right
    if isinstance(node, ast.Call):
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        if func_name == "ask":
            prompt_text = _eval_node(node.args[0], env, ask_fn)
            return ask_fn(prompt_text)
        if func_name in {"show", "print"}:
            values = [_eval_node(arg, env, ask_fn) for arg in node.args]
            return env.get("__runtime").show(*values)
        if func_name == "int":
            return int(_eval_node(node.args[0], env, ask_fn))
        if func_name == "float":
            return float(_eval_node(node.args[0], env, ask_fn))
        if func_name == "str":
            return str(_eval_node(node.args[0], env, ask_fn))

        if isinstance(node.func, ast.Attribute):
            func = _eval_node(node.func, env, ask_fn)
            args = [_eval_node(arg, env, ask_fn) for arg in node.args]
            return func(*args)
    if isinstance(node, ast.List):
        return [_eval_node(elt, env, ask_fn) for elt in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(_eval_node(elt, env, ask_fn) for elt in node.elts)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_node(node.operand, env, ask_fn)
    raise NotImplementedError(f"Unsupported expression: {ast.dump(node)}")


def _execute_statement(stmt, env, ask_fn):
    if isinstance(stmt, ast.Assign):
        value = _eval_node(stmt.value, env, ask_fn)
        for target in stmt.targets:
            if isinstance(target, ast.Name):
                env[target.id] = value
            else:
                raise NotImplementedError("Only simple variable assignment is supported")
        return None

    if isinstance(stmt, ast.Import):
        for alias_node in stmt.names:
            module_name = alias_node.name
            if module_name in env:
                continue
            try:
                env[module_name] = __import__(module_name)
            except ImportError:
                raise NotImplementedError(f"Unsupported import: {module_name}")
        return None

    if isinstance(stmt, ast.Expr):
        _eval_node(stmt.value, env, ask_fn)
        return None

    if isinstance(stmt, ast.If):
        condition = _eval_node(stmt.test, env, ask_fn)
        if condition:
            for child in stmt.body:
                _execute_statement(child, env, ask_fn)
        else:
            for child in stmt.orelse:
                _execute_statement(child, env, ask_fn)
        return None

    if isinstance(stmt, ast.For):
        iterable = _eval_node(stmt.iter, env, ask_fn)
        if isinstance(stmt.iter, ast.Call) and isinstance(stmt.iter.func, ast.Name) and stmt.iter.func.id == "range":
            values = list(iterable)
        else:
            values = list(iterable)
        for item in values:
            if isinstance(stmt.target, ast.Name):
                env[stmt.target.id] = item
            else:
                raise NotImplementedError("Only simple loop variables are supported")
            for child in stmt.body:
                _execute_statement(child, env, ask_fn)
        return None

    raise NotImplementedError(f"Unsupported statement: {ast.dump(stmt)}")


def run_kid_code(code: str, exercise_id: str):
    runtime = KidRuntime()
    answer_list_key = f"{exercise_id}-answers"
    execution_state_key = f"{exercise_id}-execution-state"
    prompt_index_key = f"{exercise_id}-prompt-index"

    if answer_list_key not in st.session_state:
        st.session_state[answer_list_key] = []
    if prompt_index_key not in st.session_state:
        st.session_state[prompt_index_key] = 0

    if st.session_state.get(f"{exercise_id}-fresh-run", False):
        st.session_state[answer_list_key] = []
        st.session_state[prompt_index_key] = 0
        st.session_state[execution_state_key] = None
        st.session_state[f"{exercise_id}-fresh-run"] = False

    state = st.session_state.get(execution_state_key)
    if state is None:
        state = {"code": code, "index": 0, "env": {"__runtime": runtime}}
        st.session_state[execution_state_key] = state
    elif state.get("code") != code:
        state = {"code": code, "index": 0, "env": {"__runtime": runtime}}
        st.session_state[execution_state_key] = state

    def ask(prompt_text: str):
        pending_key = f"{exercise_id}-awaiting_input"
        answers = list(st.session_state.get(answer_list_key, []))
        prompt_index = st.session_state.get(prompt_index_key, 0)

        if prompt_index < len(answers):
            value = answers[prompt_index]
            st.session_state[prompt_index_key] = prompt_index + 1
            return value

        st.session_state[pending_key] = True
        st.session_state[f"{exercise_id}-active_prompt"] = prompt_text
        st.session_state[f"{exercise_id}-prompt-input-key"] = get_prompt_input_key(exercise_id)
        raise PendingInput(prompt_text)

    env = state["env"]
    env["__runtime"] = runtime
    env["ask"] = ask
    env["show"] = runtime.show
    env["print"] = runtime.show
    env["__builtins__"] = __builtins__

    try:
        tree = ast.parse(code)
        statements = tree.body
        while state["index"] < len(statements):
            stmt = statements[state["index"]]
            _execute_statement(stmt, env, ask)
            state["index"] += 1
        return True, runtime.lines, None, False
    except PendingInput:
        return False, [], None, True
    except Exception as exc:
        return False, [], str(exc), False


def render_exercise(exercise: dict, editor_theme: str = "vs"):
    exercise_id = exercise["id"]
    st.subheader(exercise["title"])
    if exercise.get("intro"):
        st.write(exercise["intro"])
    if exercise.get("concept"):
        with st.expander("💡 What you are learning"):
            st.write(exercise["concept"])
    st.write(f"**Goal:** {exercise['goal']}")

    if st.session_state.get(f"{exercise_id}-awaiting_input"):
        @st.dialog("💬 Ask the robot")
        def prompt_dialog():
            prompt_key = st.session_state.get(f"{exercise_id}-prompt-input-key") or get_prompt_input_key(exercise_id)
            answer = st.text_input(
                st.session_state.get(f"{exercise_id}-active_prompt", "What do you want to say?"),
                placeholder="Type your answer here",
                key=prompt_key,
            )
            if st.button("Use this answer", key=f"{exercise_id}-confirm"):
                answer_list_key = f"{exercise_id}-answers"
                answers = list(st.session_state.get(answer_list_key, []))
                answers.append(answer)
                st.session_state[answer_list_key] = answers
                st.session_state[f"{exercise_id}-awaiting_input"] = False
                st.session_state[f"{exercise_id}-run_requested"] = True
                st.rerun()

        prompt_dialog()

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("### Try this")
        st.caption("Write your Python and press Run to see the magic happen.")
        code = st_monaco(
            value=exercise["starter_code"],
            language="python",
            height=280,
            theme=editor_theme,
        )
        if st.button("Run the code", key=f"{exercise_id}-run"):
            st.session_state[f"{exercise_id}-code"] = code
            st.session_state[f"{exercise_id}-run_requested"] = True

        if st.session_state.get(f"{exercise_id}-run_requested"):
            success, outputs, error, awaiting_input = run_kid_code(
                st.session_state.get(f"{exercise_id}-code", exercise["starter_code"]),
                exercise_id,
            )
            validation_result = validate_exercise_result(
                outputs,
                validation=exercise.get("validation"),
                reward=exercise.get("reward"),
            )
            st.session_state[f"{exercise_id}-result"] = {
                "success": success,
                "outputs": outputs,
                "error": error,
                "validation_result": validation_result,
            }
            st.session_state[f"{exercise_id}-run_requested"] = False
            if awaiting_input:
                st.rerun()
            if validation_result.get("passed"):
                update_progress(exercise_id, validation_result.get("stars", 0))

    with col_right:
        st.markdown("### Output")
        result = st.session_state.get(f"{exercise_id}-result")
        if result:
            if result["success"]:
                if result["outputs"]:
                    for line in result["outputs"]:
                        st.success(line)
                else:
                    st.info("The code ran, but there is no output yet.")

                validation_result = result.get("validation_result", {})
                if validation_result.get("passed"):
                    st.balloons()
                    st.success(f"🎉 {validation_result['message']}")
                    reward = exercise.get("reward", {})
                    if reward.get("badge"):
                        st.info(f"🏅 Badge unlocked: {reward['badge']}")
                elif validation_result:
                    st.warning(validation_result.get("message", "Keep trying!"))
            else:
                st.error(result["error"])
        else:
            st.info("Press Run the code to see the result here.")

    st.markdown("---")
    st.markdown("### Instructions")
    st.info(exercise["instructions"])

    st.markdown("### Hint")
    st.warning(exercise["hint"])
