from mesop import App, State, View, Input, Button, Text

# State to hold questions, answers, and the current question index
state = State({
    "questions": [
        "What is your name?",
        "How old are you?",
        "What is your favorite color?",
        "Where do you live?",
        "What is your favorite hobby?",
    ],
    "current_question": 0,
    "answers": [],
    "current_answer": "",
})

# Function to handle moving to the next question
def next_question():
    current_index = state.get("current_question")
    answers = state.get("answers")
    current_answer = state.get("current_answer").strip()

    if not current_answer:
        state.set({"error": "Please provide an answer before proceeding!"})
        return

    state.set({"error": ""})  # Clear any previous error
    answers.append(current_answer)
    state.set({"answers": answers, "current_answer": ""})

    # Move to the next question or finalize
    if current_index < len(state.get("questions")) - 1:
        state.set({"current_question": current_index + 1})
    else:
        finalize_survey()

# Function to create a CSV and download it
def finalize_survey():
    import csv
    questions = state.get("questions")
    answers = state.get("answers")

    with open("survey_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Question", "Answer"])
        for question, answer in zip(questions, answers):
            writer.writerow([question, answer])

    state.set({"message": "Survey completed! Answers saved to 'survey_results.csv'."})

# Function to handle input changes
def handle_input(value):
    state.set({"current_answer": value})

# Define the survey app layout
def SurveyApp():
    questions = state.get("questions")
    current_index = state.get("current_question")
    error = state.get("error")
    message = state.get("message")

    if message:
        return View([
            Text(message),
            Button("Close", onClick=lambda: App.stop())
        ])

    return View([
        Text(f"Question {current_index + 1}: {questions[current_index]}"),
        Input(value=state.get("current_answer"), onChange=handle_input),
        Text(error, style={"color": "red"}) if error else None,
        Button("Next", onClick=next_question)
    ])

# Run the app
App(SurveyApp)
