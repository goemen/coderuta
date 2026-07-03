import streamlit as st
from streamlit_monaco import st_monaco


class KidRuntime:
    def __init__(self):
        self.lines = []

    def show(self, *values):
        text = " ".join(str(value) for value in values)
        self.lines.append(text)
        return text


def run_kid_code(code: str, input_value: str):
    runtime = KidRuntime()

    safe_globals = {
        "__builtins__": __builtins__,
        "show": runtime.show,
        "ask": lambda prompt: input_value,
        "button": lambda label: None,
        "print": runtime.show,
    }

    try:
        exec(code, safe_globals)
        return True, runtime.lines, None
    except Exception as exc:
        return False, [], str(exc)


def render_exercise(exercise: dict, editor_theme: str = "vs"):
    st.subheader(exercise["title"])
    st.write(exercise["goal"])

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
        input_value = st.text_input(
            "Type something here if you want to answer the prompt",
            key=f"{exercise['id']}-input",
        )

        if st.button("Run the code", key=f"{exercise['id']}-run"):
            success, outputs, error = run_kid_code(code, input_value)
            st.session_state[f"{exercise['id']}-result"] = {
                "success": success,
                "outputs": outputs,
                "error": error,
            }

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
