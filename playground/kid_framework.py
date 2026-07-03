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


def run_kid_code(code: str, exercise_id: str):
    runtime = KidRuntime()

    def ask(prompt_text: str):
        answer_key = f"{exercise_id}-answer"
        pending_key = f"{exercise_id}-awaiting_input"
        if answer_key in st.session_state and st.session_state[answer_key] is not None:
            value = st.session_state[answer_key]
            st.session_state[answer_key] = None
            return value

        st.session_state[pending_key] = True
        st.session_state[f"{exercise_id}-active_prompt"] = prompt_text
        raise PendingInput(prompt_text)

    safe_globals = {
        "__builtins__": __builtins__,
        "show": runtime.show,
        "ask": ask,
        "button": lambda label: None,
        "print": runtime.show,
    }

    try:
        exec(code, safe_globals)
        return True, runtime.lines, None, False
    except PendingInput:
        return False, [], None, True
    except Exception as exc:
        return False, [], str(exc), False


def render_exercise(exercise: dict, editor_theme: str = "vs"):
    exercise_id = exercise["id"]
    st.subheader(exercise["title"])
    st.write(exercise["goal"])

    if st.session_state.get(f"{exercise_id}-awaiting_input"):
        @st.dialog("💬 Ask the robot")
        def prompt_dialog():
            answer = st.text_input(
                st.session_state.get(f"{exercise_id}-active_prompt", "What do you want to say?"),
                placeholder="Type your answer here",
                key=f"{exercise_id}-dialog-input",
            )
            if st.button("Use this answer", key=f"{exercise_id}-confirm"):
                st.session_state[f"{exercise_id}-answer"] = answer
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
            st.session_state[f"{exercise_id}-result"] = {
                "success": success,
                "outputs": outputs,
                "error": error,
            }
            st.session_state[f"{exercise_id}-run_requested"] = False
            if awaiting_input:
                st.session_state[f"{exercise_id}-run_requested"] = False

    with col_right:
        st.markdown("### Output")
        result = st.session_state.get(f"{exercise['id']}-result")
        if result:
            if result["success"]:
                if result["outputs"]:
                    for line in result["outputs"]:
                        st.success(line)
                else:
                    st.info("The code ran, but there is no output yet.")
            else:
                st.error(result["error"])
        else:
            st.info("Press Run the code to see the result here.")

    st.markdown("---")
    st.markdown("### Instructions")
    st.info(exercise["instructions"])

    st.markdown("### Hint")
    st.warning(exercise["hint"])
