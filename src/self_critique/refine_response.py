import sys
from enum import Enum
from  src.examples.shot_learning import ShotPromptingMode
from src.llm_clients import generate_response_llama

class EvalMode(Enum):
    ACTORS = "actors"
    HIGH_LEVEL = "high"
    LOW_LEVEL = "low"

class Feedback():
    def __init__(self, previous_output, critique):
        self.previous_output = previous_output
        self.critique = critique 

# evaluation by Llama
def get_evaluation(eval_mode: EvalMode, description, actors, high_level_goals=None, low_level_goals=None):
    if not isinstance(eval_mode, EvalMode):
        raise TypeError(f"Expected an instance of EvalMode, but got {type(eval_mode).__name__}")
    sys_prompt = (
        "You're an helpful assistant, expert in the field of software engineering."
        )

    assume_this_is_ok = ""
    additional_prompt = ""
    if eval_mode == EvalMode.ACTORS:
        if high_level_goals != None or low_level_goals != None:
            raise ValueError("EvalMode.ACTORS can only be used when high_level_goals and low_level_goals are both None.")
        provided_with = "a software description and the actors for said software"
        assume_this_is_ok = ""
        critique_this = "defining actors"
    elif eval_mode == EvalMode.HIGH_LEVEL:
        if low_level_goals != None or high_level_goals == None:
            raise ValueError("EvalMode.HIGH_LEVEL can only be used when low_level_goals is None and high_level_goals is not None.")
        provided_with = "a software description, actors and high-level goals for said software"
        assume_this_is_ok = "Assuming the work done on actors is ok,"
        critique_this = "defining high-level goals"
        additional_prompt = f"""
        **High-level goals:**\n\n
        {high_level_goals}

        """
    elif eval_mode == EvalMode.LOW_LEVEL:
        if low_level_goals == None or high_level_goals == None:
            raise ValueError("EvalMode.LOW_LEVEL can only be used when both low_level_goals and high_level_goals are not None.")
        provided_with = "a software description, actors, high-level goals and low-level goals for said software"
        assume_this_is_ok = "Assuming the work done on actors and high-level goals is ok,"
        critique_this = "defining low-level goals"
        additional_prompt =  f"""
        **High-level goals:**\n\n
        {high_level_goals}

        **Low-level goals:**\n\n
        {low_level_goals}

        """

    prompt = f"""
        You are provided with {provided_with}.\n
        These informations were extracted by another assistant from the software description.\n
        {assume_this_is_ok} your job is to critique the work done by the assistant on {critique_this}, scoring it on a scale from 0 to 10, assign a low score if you see any contradiction or important omissions.\n
        Just respond with a score and a feedback, like in this example:\n
        
        Score: [0-10]\n
        Feedback: [Feedback here]\n

        Do not add any other comments, just the above mentioned lines.\n

        **Description:** \n\n
        {description}

        **Actors:**\n\n
        {actors}

        {additional_prompt}
        **Output:**\n\n
    """

    critique = generate_response_llama(prompt, sys_prompt)
    return critique 

def parse_evaluation(evaluation):
    lines = evaluation.strip().split("\n")
    if len(lines) < 3:
            raise ValueError("Input text is not in the expected format.")
    score_line = lines[0]
    if not score_line.startswith("Score:"):
            raise ValueError("Input text does not contain a valid 'Score:' line.")
    feedback_line = " ".join(lines[2:])
    if not feedback_line.startswith("Feedback:"):
            raise ValueError("Input text does not contain a valid 'Feedback:' line.")
    score = int(score_line.split(":")[1].strip())
    feedback = feedback_line.split(":")[1].strip()
    return score, feedback



MAX_ATTEMPTS = 5
def generate_response_with_reflection(target_type, call_function, define_args, eval_mode, eval_args, shotPromptingMode=ShotPromptingMode.ZERO_SHOT, max_attempts=MAX_ATTEMPTS):
    feedback = None
    for attempt in range(1, max_attempts + 1):
        print(f"{target_type} STARTING... (attempt {attempt})")
        result = call_function(*define_args, feedback=feedback, mode = shotPromptingMode )
        print(f"{target_type} DONE...")
        print(result)

        print(f"Evaluation for {target_type} STARTING...")
        evaluation = get_evaluation(eval_mode, *eval_args, result)
        print(f"Evaluation for {target_type} DONE...")

        try:
            score, critique = parse_evaluation(evaluation)
            print(f"Score: {score}")
            print(f"Critique: {critique}")

            #log this to check output
            #with open("output.txt", "a") as file:  # Use "w" to overwrite or "a" to append
            #   file.write(f"Critique: {critique}\nScore: {score}\nHLG: 

            if score >= 8:
                print("Satisfactory score achieved! Breaking out of the loop.")
                return result, score, critique
            else:
                print("Unsatisfactory score. Retrying...")
                feedback = Feedback(previous_output=result, critique=critique)
        except ValueError as e:
            print(f"Error while parsing evaluation: {e}")
            sys.exit(1)  # Exit the program if parsing fails

    raise RuntimeError("Failed to achieve a satisfactory score within the maximum number of attempts.")