import streamlit as st

from playground.kid_framework import render_exercise


EXERCISES = {
    "hello": {
        "id": "hello",
        "title": "🌟 Hello App",
        "intro": "Your first robot friend is ready to say hello. This lesson teaches you how to make words appear on the screen.",
        "concept": "A variable is a box that holds information. You can store a name, a number, or a word inside it.",
        "goal": "Make the app say hello using simple words.",
        "instructions": "Write a friendly greeting so it appears in the output area.",
        "hint": "Use show() to print a sentence.",
        "starter_code": "show('Hello, coder!')\nshow('You are ready to begin!')",
        "validation": {"type": "contains", "value": "Hello"},
        "reward": {
            "stars": 10,
            "badge": "First Hello",
            "message": "Great job! You earned 10 stars.",
            "retry_message": "Almost there! Try adding a hello message to the output.",
        },
    },
    "data_types": {
        "id": "data_types",
        "title": "🌟 Data Types",
        "intro": "Data types are the different kinds of information you can use in programming. This lesson teaches you about numbers, text, and other data types in Python.",
        "concept": "In Python, there are several data types, including integers (whole numbers), floats (decimal numbers), strings (text), and booleans (True/False).",
        "goal": "Identify and use different data types in Python.",
        "instructions": "Create variables of different data types and display them.",
        "hint": "Use the assignment operator (=) to create a variable. For example: age = 10\nshow(age)\nname = 'Alice'\nshow(name)",
        "starter_code": "# Create a variable named age and assign it an integer value\nage = 10\n# Display the value of the variable\nshow(age)\n\n# Create a variable named name and assign it a string value\nname = 'Alice'\n# Display the value of the variable\nshow(name)\n\n# Create a variable named is_student and assign it a boolean value\nis_student = True\n# Display the value of the variable\nshow(is_student)",
        "validation": {"type": "contains", "value": "age ="},
        "reward": {
            "stars": 10,
            "badge": "Data Type Explorer",
            "message": "Great job! You earned 10 stars.",
            "retry_message": "Almost there! Try creating variables of different data types.",
        },
    },
    "variables": {
        "id": "variables",
        "title": "🌟 Variables",
        "intro": "Variables are like boxes where you can store information. This lesson teaches you how to create and use variables in Python. Variables can hold different types of data, such as numbers, text, or even more complex structures. You can change the value of a variable during the execution of your program.",
        "concept": "A variable is a named location in memory that stores a value. You can change the value of a variable during the execution of your program.",
        "goal": "Create and use variables to store and display information.",
        "instructions": "Define a variable and assign it a value, then display it.",
        "hint": "Use the assignment operator (=) to create a variable. For example: name = 'Alice'. Then use show(name) to display it. Or: score = 10\nshow(score)",
        "starter_code": "# Create a variable named name and assign it the value 'Alice'\nname = 'Alice'\n# Display the value of the variable\nshow(name)\n\n# Create a variable named score and assign it the value 10\nscore = 10\n# Display the value of the variable\nshow(score) \n\n# You can change the value of a variable\nscore = 20\nshow(score)",
        "validation": {"type": "contains", "value": "name ="},
        "reward": {
            "stars": 10,
            "badge": "Variable Master",
            "message": "Great job! You earned 10 stars.",
            "retry_message": "Almost there! Try creating a variable and assigning it a value.",
        },
    },
    "math": {
        "id": "math",
        "title": "🌟 Math Operations",
        "intro": "Math operations allow you to perform calculations with numbers. This lesson teaches you how to use basic math operators in Python.",
        "concept": "Math operations in Python use standard operators like +, -, *, /, and ** for addition, subtraction, multiplication, division, and exponentiation.",
        "goal": "Perform basic math operations with variables.",
        "instructions": "Create variables with numeric values and perform math operations on them.",
        "hint": "Use the assignment operator (=) to create a variable. For example: x = 5. Then use show(x) to display it. You can also perform math operations like: y = 10\nshow(y)",
        "starter_code": "# Create a variable named x and assign it the value 5\nx = 5\n# Display the value of the variable\nshow(x)\n\n# Create a variable named y and assign it the value 10\ny = 10\n# Display the value of the variable\nshow(y)\n\n# Perform a math operation\nz = x + y\nshow(z)",
        "validation": {"type": "contains", "value": "x ="},
        "reward": {
            "stars": 10,
            "badge": "Math Master",
            "message": "Great job! You earned 10 stars.",
            "retry_message": "Almost there! Try creating variables and performing math operations on them.",
        },
    },
    "strings": {
        "id": "strings",
        "title": "🌟 Strings",
        "intro": "Strings are sequences of characters. This lesson teaches you how to create and use strings in Python.",
        "concept": "In Python, strings are created by enclosing text in single or double quotes. You can perform various operations on strings, such as concatenation and formatting.",
        "goal": "Create and manipulate strings in Python.",
        "instructions": "Create string variables and perform operations on them.",
        "hint": "Use the assignment operator (=) to create a string variable. For example: name = 'Alice'. Then use show(name) to display it.",
        "starter_code": "# Create a variable named name and assign it the value 'Alice'\nname = 'Alice'\n# Display the value of the variable\nshow(name)\n\n# Create a variable named greeting and assign it a string value\ngreeting = 'Hello, ' + name + '!'\n# Display the value of the variable\nshow(greeting)",
        "validation": {"type": "contains", "value": "name ="},
        "reward": {
            "stars": 10,
            "badge": "String Master",
            "message": "Great job! You earned 10 stars.",
            "retry_message": "Almost there! Try creating string variables and performing operations on them.",
        },
    },
    "string_formatting": {
        "id": "string_formatting",
        "title": "🌟 String Formatting",
        "intro": "String formatting allows you to create dynamic strings by inserting values into placeholders. This lesson teaches you how to use string formatting in Python.",
        "concept": "In Python, you can format strings using the .format() method or f-strings. Both methods allow you to insert values into a string template.",
        "goal": "Format strings in Python using different methods.",
        "instructions": "Create formatted strings using the .format() method and f-strings.",
        "hint": "Use the .format() method or f-strings to create formatted strings. For example: name = 'Alice'\nage = 10\nmessage = 'Hello, {}! You are {} years old.'.format(name, age)\nshow(message)",
        "starter_code": "# Create a variable named name and assign it the value 'Alice'\nname = 'Alice'\n# Create a variable named age and assign it the value 10\nage = 10\n# Create a formatted string using the .format() method\nmessage = 'Hello, {}! You are {} years old.'.format(name, age)\n# Display the value of the variable\nshow(message)\n\n# Create a formatted string using f-strings\nmessage2 = f'Hello, {name}! You are {age} years old.'\n# Display the value of the variable\nshow(message2)",
        "validation": {"type": "contains", "value": "name ="},
        "reward": {
            "stars": 10,
            "badge": "String Formatter",
            "message": "Great job! You earned 10 stars.",
            "retry_message": "Almost there! Try creating formatted strings using different methods.",
        },
    },
    "checkpoint_1": {
        "id": "checkpoint_1",
        "title": "🌟 Checkpoint 1",
        "intro": "Congratulations on reaching Checkpoint 1! This checkpoint allows you to review and reinforce the concepts you've learned so far. You can revisit previous exercises and ensure you understand the material before moving on to the next set of lessons.",
        "concept": "Checkpoints are a way to review and reinforce the concepts you've learned in previous exercises. They allow you to revisit and practice the material before moving on to new lessons.",
        "goal": "Review and reinforce the concepts learned in previous exercises.",
        "instructions": "Revisit previous exercises and ensure you understand the material before moving on to the next set of lessons. You can also try creating your own exercises to test your understanding. For example: Create a program that asks the user for their name and age, then displays a greeting message using string formatting.",
        "hint": "Take your time to review the previous exercises and make sure you understand the concepts before moving on.",
        "starter_code": "# Review previous exercises and ensure you understand the material before moving on to the next set of lessons.\n# You can also try creating your own exercises to test your understanding.\n# For example: Create a program that asks the user for their name and age, then displays a greeting message using string formatting.\n\nname = ask('What is your name? ')\nage = int(ask('How old are you? '))\nmessage = f'Hello, {name}! You are {age} years old.'\nshow(message)",
        "validation": {"type": "contains", "value": "name ="},
        "reward": {
            "stars": 10,
            "badge": "Checkpoint 1 Achiever",
            "message": "Great job! You earned 10 stars.",
            "retry_message": "Almost there! Try reviewing the previous exercises and ensure you understand the material before moving on.",
        },
    },
    "conditional_statements": {
        "id": "conditional_statements",
        "title": "🌟 Conditional Statements",
        "intro": "Conditional statements allow your program to make decisions based on certain conditions. They are essential for creating dynamic and interactive programs.",
        "concept": "Conditional statements are used to execute different blocks of code depending on whether a condition is true or false.",
        "goal": "Understand and use conditional statements to control the flow of your program.",
        "instructions": "Create a program that uses conditional statements to make decisions based on user input. For example: Create a simple calculator that performs different operations based on the user's choice.",
        "hint": "Remember to use the 'if', 'elif', and 'else' keywords to create conditional logic.",
        "starter_code": "# Create a simple calculator that performs different operations based on the user's choice.\n\noperation = ask('Choose an operation (+, -, *, /): ')\nnum1 = float(ask('Enter the first number: '))\nnum2 = float(ask('Enter the second number: '))\n\nif operation == '+':\n    result = num1 + num2\nelif operation == '-':\n    result = num1 - num2\nelif operation == '*':\n    result = num1 * num2\nelif operation == '/':\n    result = num1 / num2\nelse:\n    result = 'Invalid operation'\n\nshow(result)",
        "validation": {"type": "contains", "value": "if operation =="},
        "reward": {
            "stars": 10,
            "badge": "Conditional Statements Master",
            "message": "Great job! You earned 10 stars.",
            "retry_message": "Almost there! Try reviewing the concept of conditional statements and ensure you understand how to use them.",
        },
    },
    "loops": {
        "id": "loops",
        "title": "🌟 Loops",
        "intro": "Loops allow you to repeat a block of code multiple times. They are essential for automating repetitive tasks.",
        "concept": "Loops are used to execute a block of code repeatedly until a certain condition is met.",
        "goal": "Understand and use loops to automate repetitive tasks.",
        "instructions": "Create a program that uses loops to repeat a task multiple times. For example: Create a program that prints the numbers from 1 to 10 using a loop.",
        "hint": "Remember to use the 'for' and 'while' keywords to create loops. For example: for i in range(1, 11):\n    show(i)",
        "starter_code": "# Create a program that prints the numbers from 1 to 10 using a loop.\n\nfor i in range(1, 11):\n    show(i)",
        "validation": {"type": "contains", "value": "for i in range"},
        "reward": {
            "stars": 10,
            "badge": "Loops Master",
            "message": "Great job! You earned 10 stars.",
            "retry_message": "Almost there! Try reviewing the concept of loops and ensure you understand how to use them.",
        },
    },
    "rock_paper_scissors": {
        "id": "rock_paper_scissors",
        "title": "🌟 Rock Paper Scissors Game",
        "intro": "Play the classic game of Rock Paper Scissors against the computer.",
        "concept": "The game involves choosing one of three options (rock, paper, or scissors) and comparing it with the computer's choice.",
        "goal": "Create a simple Rock Paper Scissors game in Python.",
        "instructions": "Create a program that allows the user to play Rock Paper Scissors against the computer. The program should display the user's choice, the computer's choice, and the result of the game.",
        "hint": "Use random.choice() to generate the computer's choice. For example: import random\nchoices = ['rock', 'paper', 'scissors']\ncomputer_choice = random.choice(choices)",
        "starter_code": "# Create a simple Rock Paper Scissors game in Python.\n\nimport random\n\nchoices = ['rock', 'paper', 'scissors']\nuser_choice = ask('Choose rock, paper, or scissors: ')\ncomputer_choice = random.choice(choices)\n\nprint(f'You chose {user_choice}.')\nprint(f'Computer chose {computer_choice}.')",
        "validation": {"type": "contains", "value": "import random"},
        "reward": {
            "stars": 10,
            "badge": "Rock Paper Scissors Master",
            "message": "Great job! You earned 10 stars.",
            "retry_message": "Almost there! Try reviewing the concept of loops and ensure you understand how to use them.",
        },
    }
}


def main():
    st.set_page_config(page_title="Kid Python Playground", page_icon="🧡", layout="wide")
    st.title("🧒 Kid Python Playground")
    st.caption("A friendly, reusable place to learn Python with instant browser results.")

    with st.sidebar:
        st.header("🏆 Adventure progress")
        st.metric("⭐ Total stars", st.session_state.get("total_stars", 0))
        st.metric("🎯 Completed lessons", len(st.session_state.get("completed_exercises", [])))
        st.caption("Each lesson rewards you with stars and a badge when you solve it.")

        exercise_key = st.selectbox(
            "Choose an lesson to explore",
            options=list(EXERCISES.keys()),
            format_func=lambda key: EXERCISES[key]["title"],
        )
        editor_theme = st.selectbox(
            "Editor theme",
            options=["vs", "vs-dark", "hc-black", "hc-light"],
            index=0,
            help="Pick a theme with better contrast for reading code.",
        )

    render_exercise(EXERCISES[exercise_key], editor_theme=editor_theme)


if __name__ == "__main__":
    main()
