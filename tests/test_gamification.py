import unittest

import streamlit as st

from playground.kid_framework import get_prompt_input_key, run_kid_code, validate_exercise_result


class GamificationValidationTests(unittest.TestCase):
    def test_contains_validator_matches_output(self):
        result = validate_exercise_result(
            outputs=["Hello Maya!", "You are ready to code!"],
            validation={"type": "contains", "value": "Hello"},
        )
        self.assertTrue(result["passed"])
        self.assertEqual(result["message"], "Great job! You earned 10 stars.")

    def test_contains_validator_fails_when_missing(self):
        result = validate_exercise_result(
            outputs=["Hi Maya!"],
            validation={"type": "contains", "value": "Hello"},
        )
        self.assertFalse(result["passed"])
        self.assertIn("Try again", result["message"])

    def test_exact_validator_matches_output(self):
        result = validate_exercise_result(
            outputs=["7"],
            validation={"type": "exact", "value": "7"},
        )
        self.assertTrue(result["passed"])

    def test_multiple_asks_can_be_satisfied_in_order(self):
        st.session_state.clear()
        st.session_state["demo-restart-execution"] = True

        success, outputs, error, awaiting_input = run_kid_code(
            "first = int(ask('first'))\nsecond = int(ask('second'))\nshow(first + second)",
            "demo",
        )
        self.assertFalse(success)
        self.assertTrue(awaiting_input)

        st.session_state["demo-answers"] = ["7"]
        success, outputs, error, awaiting_input = run_kid_code(
            "first = int(ask('first'))\nsecond = int(ask('second'))\nshow(first + second)",
            "demo",
        )
        self.assertFalse(success)
        self.assertTrue(awaiting_input)

        st.session_state["demo-answers"] = ["7", "3"]
        success, outputs, error, awaiting_input = run_kid_code(
            "first = int(ask('first'))\nsecond = int(ask('second'))\nshow(first + second)",
            "demo",
        )

        self.assertTrue(success)
        self.assertEqual(outputs, ["10"])
        self.assertIsNone(error)
        self.assertFalse(awaiting_input)

    def test_fstrings_are_supported(self):
        st.session_state.clear()

        success, outputs, error, awaiting_input = run_kid_code(
            "name = 'Maya'\nage = 10\nshow(f'Hello, {name}! You are {age} years old.')",
            "demo-fstring",
        )

        self.assertTrue(success)
        self.assertEqual(outputs, ["Hello, Maya! You are 10 years old."])
        self.assertIsNone(error)
        self.assertFalse(awaiting_input)

    def test_prompt_input_key_changes_for_each_new_prompt(self):
        st.session_state.clear()
        self.assertEqual(get_prompt_input_key("demo"), "demo-dialog-input-1")

        st.session_state["demo-prompt-sequence"] = 1
        self.assertEqual(get_prompt_input_key("demo"), "demo-dialog-input-2")

    def test_import_statements_are_supported(self):
        st.session_state.clear()

        success, outputs, error, awaiting_input = run_kid_code(
            "import random\nshow(random.__name__)",
            "demo-import",
        )

        self.assertTrue(success)
        self.assertEqual(outputs, ["random"])
        self.assertIsNone(error)
        self.assertFalse(awaiting_input)

    def test_attribute_calls_are_supported(self):
        st.session_state.clear()

        success, outputs, error, awaiting_input = run_kid_code(
            "import random\nchoices = ['rock', 'paper', 'scissors']\nshow(random.choice(choices))",
            "demo-attribute-call",
        )

        self.assertTrue(success)
        self.assertEqual(len(outputs), 1)
        self.assertIn(outputs[0], ["rock", "paper", "scissors"])
        self.assertIsNone(error)
        self.assertFalse(awaiting_input)

    def test_three_prompts_can_be_satisfied_in_order(self):
        st.session_state.clear()
        st.session_state["demo-three-prompts-restart-execution"] = True

        success, outputs, error, awaiting_input = run_kid_code(
            "operation = ask('Choose an operation (+, -, *, /): ')\n"
            "num1 = float(ask('Enter the first number: '))\n"
            "num2 = float(ask('Enter the second number: '))\n"
            "show(operation + ' ' + str(num1) + ' ' + str(num2))",
            "demo-three-prompts",
        )
        self.assertFalse(success)
        self.assertTrue(awaiting_input)

        st.session_state["demo-three-prompts-answers"] = ["+"]
        success, outputs, error, awaiting_input = run_kid_code(
            "operation = ask('Choose an operation (+, -, *, /): ')\n"
            "num1 = float(ask('Enter the first number: '))\n"
            "num2 = float(ask('Enter the second number: '))\n"
            "show(operation + ' ' + str(num1) + ' ' + str(num2))",
            "demo-three-prompts",
        )
        self.assertFalse(success)
        self.assertTrue(awaiting_input)

        st.session_state["demo-three-prompts-answers"] = ["+", "2"]
        success, outputs, error, awaiting_input = run_kid_code(
            "operation = ask('Choose an operation (+, -, *, /): ')\n"
            "num1 = float(ask('Enter the first number: '))\n"
            "num2 = float(ask('Enter the second number: '))\n"
            "show(operation + ' ' + str(num1) + ' ' + str(num2))",
            "demo-three-prompts",
        )
        self.assertFalse(success)
        self.assertTrue(awaiting_input)

        st.session_state["demo-three-prompts-answers"] = ["+", "2", "3"]
        success, outputs, error, awaiting_input = run_kid_code(
            "operation = ask('Choose an operation (+, -, *, /): ')\n"
            "num1 = float(ask('Enter the first number: '))\n"
            "num2 = float(ask('Enter the second number: '))\n"
            "show(operation + ' ' + str(num1) + ' ' + str(num2))",
            "demo-three-prompts",
        )
        self.assertTrue(success)
        self.assertEqual(outputs, ["+ 2.0 3.0"])
        self.assertIsNone(error)
        self.assertFalse(awaiting_input)


if __name__ == "__main__":
    unittest.main()
