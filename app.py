import streamlit as st

from playground.kid_framework import render_exercise


EXERCISES = {
    "hello": {
        "id": "hello",
        "title": "🌟 Hello App",
        "goal": "Make the app say hello using simple words.",
        "instructions": "Type your name and see the greeting appear in the output area.",
        "hint": "Use the ask function to get the name and the show function to print the message.",
        "starter_code": 'name = ask("What is your name?")\nshow("Hello " + name + "!")\nshow("You are ready to code!")',
    }
}


def main():
    st.set_page_config(page_title="Kid Python Playground", page_icon="🧡", layout="wide")
    st.title("🧒 Kid Python Playground")
    st.caption("A friendly, reusable place to learn Python with instant browser results.")

    exercise_key = st.sidebar.selectbox(
        "Choose an exercise",
        options=list(EXERCISES.keys()),
        format_func=lambda key: EXERCISES[key]["title"],
    )
    editor_theme = st.sidebar.selectbox(
        "Editor theme",
        options=["vs", "vs-dark", "hc-black", "hc-light"],
        index=0,
        help="Pick a theme with better contrast for reading code.",
    )
    render_exercise(EXERCISES[exercise_key], editor_theme=editor_theme)


if __name__ == "__main__":
    main()
