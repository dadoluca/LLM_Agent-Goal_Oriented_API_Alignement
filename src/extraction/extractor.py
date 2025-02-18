from  src.examples.shot_learning import ShotPromptingMode, example1_actors, example2_actors, example3_actors, example1_hl, example2_hl, example3_hl, example1_ll, example2_ll, example3_ll
from src.data_model import DocumentDescription,  Actors,  LowLevelGoals,  HighLevelGoals
from src.tools import get_markdown
from src.llm_clients import generate_response

def generate_description(documentation_link=None):
    if documentation_link == None:
        raise Exception("No documentation link provided")
    
    sys_prompt = (
        "You are a technical writing assistant specialized in summarizing software documentation. "
        "Your goal is to extract a clear, well-written, and accurate description of a project from its README file. "
        "The description should be natural and informative, without unnecessary details or implementation specifics. "
        "Avoid marketing language, vague claims, or filler content. "
        "Write in a neutral, professional tone, ensuring that the description is easy to understand for someone unfamiliar with the project."
    )

    prompt = (
        f"Here is the README file of a software project:\n\n{get_markdown(link=documentation_link)}\n\n"
        "Based on this README, write a concise and well-structured description of the project. "
        "Explain its purpose, the problem it addresses (if mentioned), and its main functionalities. "
        "Do not include implementation details, generic statements, or assumptions not explicitly stated in the README."
    )
    
    response = generate_response(prompt, sys_prompt, DocumentDescription)
    
    return response


def generate_actors(project_description, feedback=None, mode=ShotPromptingMode.ZERO_SHOT):
    #if project_description == None:
    #    raise Exception("No project description provided")
    
    sys_prompt = (
        "You are a helpful assistant expert in software engineering tasks, specialized in extracting user roles from a high level description of a software project. \n"
        "Your task is to extract the actors (user roles of end users) of the system from the given description.\n"
        "Don't make up information that does not exist, just take information from the given text. \n"
        "Each extracted actor name should be accompained by a very short description.\n"
    )

    if feedback != None:
        print("Feedback provided!")
        sys_prompt += f"""

        The task given to you was already attempted but its output was flawed. You're provided with a critique on the previous attempt.
        The critique contains comments about actors, please take it into account when generating actors.

        **Critique:**
        {feedback.critique}
        **Previous attempt:**
        {feedback.previous_output}
        """
    else:
        print("No feedback provided!")
    
    prompt = f"""
        {(example1_actors if mode == ShotPromptingMode.ONE_SHOT else f"{example1_actors}, {example2_actors}, {example3_actors}" if mode == ShotPromptingMode.FEW_SHOT else "")}\n

        Now extract actors from the following software description.

        **Description:**
        {project_description}

        **Output:**
    """

    actors = generate_response(prompt, sys_prompt, Actors)

    return actors


#------------------------------------------- Define high level goals from description
def generate_high_level_goals(project_description, actors, feedback=None, mode=ShotPromptingMode.ZERO_SHOT):
    sys_prompt = (
        "You are a helpful assistant that helps developers to extract high-level goals from software descriptions."
        " You're tasked with extracting high level goals from a software description, you're also provided with actors that are expected to interact with the software."
        " MUST focus only on functional requirements and ignore non-functional requirements. Focus only on requirements that benefit the end user of the software."
        #" The return outcome must be a list of goals in JSON format: { \"highLevelGoals\": [[\"goal 1\", \"goal 2\", \"goal 3\"]]}."
        #" Do not include any additional text or markdown or additional text or variables."
        " The returned high-level goals should be specific and focused on functional user needs.\n"
    )


    if feedback != None:
        print("Feedback provided!")
        sys_prompt += f"""

        The task given to you was already attempted but its output was flawed. You're provided with a critique on the previous attempt.
        The critique contains comments about high level goals, please take it into account when generating high level goals.

        **Critique:**
        {feedback.critique}
        **Previous attempt:**
        {feedback.previous_output}
        """
    else:
        print("No feedback provided!")

    print("This is the provided sys prompt: ", sys_prompt)

    prompt = f"""
        {(example1_hl if mode == ShotPromptingMode.ONE_SHOT else f"{example1_hl}, {example2_hl}, {example3_hl}" if mode == ShotPromptingMode.FEW_SHOT else "")}\n
        Proceed defining the high level goals for the following software description and actors:\n

        **Description:** \n\n
        {project_description}\n

        **Actors:**\n
        {actors}\n

        **Output:**
        """

    high_level_goals = generate_response(prompt, sys_prompt, HighLevelGoals)

    return high_level_goals


#------------------------------------------- Define low level goals from high level goals
def generate_low_level_goals(highLevelGoals, feedback=None, mode=ShotPromptingMode.ZERO_SHOT):
    sys_prompt = (
        "You are a helpful assistant that helps developers to extract low-level goals from high-level goals."
        " The low-level goals that you create MUST be structured to match against a set of API calls. Don't be too generic, for example, avoid goals like 'make the software fast', 'develop a web interface' etc."
        " MUST focus only on functional requirements and ignore non-functional requirements. Focus only on requirements that benefit the end user of the software."
        #" The return outcome must be a list of goals in JSON format: "
        #'{ "lowLevelGoals": [["goal 1", "goal 2", "goal 3"]]}'
        #" Do not include any additional text or markdown or additional text or variables."
        " The returned low-level goals should be specific and focused on the user's needs.\n"
    )

    if feedback != None:
        print("Feedback provided!")
        sys_prompt += f"""

        The task given to you was already attempted but its output was flawed. You're provided with a critique on the previous attempt.
        The critique contains comments about low-level goals, please take it into account when generating low-level goals.

        **Critique:**
        {feedback.critique}\n
        **Previous attempt:**
        {feedback.previous_output}\n
        """
    else:
        print("No feedback provided!")

    print("This is the provided sys prompt: ", sys_prompt)

    prompt = f""" 

        {(example1_ll if mode == ShotPromptingMode.ONE_SHOT else f"{example1_ll}, {example2_ll}, {example3_ll}" if mode == ShotPromptingMode.FEW_SHOT else "")}\n
        Based on your understanding of the typical tasks that compose the sequence of high-level goal,
        provide if possible a decomposition of goals into sub-goals. 
        Each low-level goal should theoretically correspond to a single action of the actor with the software.
        **High-level goals:**\n\n
        {highLevelGoals}\n

        **Output:**
    """

    lowLevelGoals = generate_response(prompt, sys_prompt, LowLevelGoals)

    return lowLevelGoals