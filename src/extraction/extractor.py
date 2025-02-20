from  src.examples.shot_learning import ShotPromptingMode, example1_actors, example2_actors, example3_actors, example1_hl, example2_hl, example3_hl, example1_ll, example2_ll, example3_ll
from src.data_model import DocumentDescription,  Actors,  LowLevelGoals,  HighLevelGoals
from src.utils import get_markdown
from src.llm_clients import generate_response

def generate_description(documentation_link=None):
    if documentation_link == None:
        raise Exception("No documentation link provided")
    
    sys_prompt = (
        "You are a technical writing assistant specialized in summarizing software documentation. "
        "Your goal is to extract a clear, well-written, and accurate description of a project from its README file. "
        "The description should be natural and informative, without unnecessary details or implementation specifics. "
        "Avoid marketing language, vague claims, or filler content. "
    )

    prompt = (
        f"Here is the README file of a software project:\n\n{get_markdown(link=documentation_link)}\n\n"
        "Based on this README, write a concise and well-structured description of the project. "
        "Explain its purpose, the problem it addresses (if mentioned), and its main functionalities. "
        "Do not include software implementation details"
        #"Do not include implementation details, generic statements, or assumptions not explicitly stated in the README."
    )
    
    response = generate_response(prompt, sys_prompt, DocumentDescription)
    
    return response


def generate_actors(project_description, feedback=None, mode=ShotPromptingMode.ZERO_SHOT):

    sys_prompt = (
        "You are a helpful assistant expert in software engineering tasks, specialized in extracting end-users roles from a high level description of a software project. \n"
        "Your task is to extract the actors (roles of end users of the system) from the given description.\n"
        "If actors are not explicitly mentioned, infer them based on typical users of similar software systems."
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
        {(example1_actors if mode == ShotPromptingMode.ONE_SHOT else f"{example1_actors}, {example2_actors}" if mode == ShotPromptingMode.FEW_SHOT else "")}\n

        Now extract the actors (roles of end users) from the following software description.

        **Description:**
        {project_description}

        **Output:**
    """

    actors = generate_response(prompt, sys_prompt, Actors)

    return actors


#------------------------------------------- Define high level goals from description
def generate_high_level_goals(project_description, actors, feedback=None, mode=ShotPromptingMode.ZERO_SHOT):
    sys_prompt = (
        "You are a helpful assistant expert in software engineering tasks"
        " You're tasked with extracting high level goals from a software description for each provided actor that is expected to interact with the software."
        " MUST focus only on functional requirements and ignore non-functional requirements. Focus only on requirements that benefit the end users of the software."
        #" The return outcome must be a list of goals in JSON format: { \"highLevelGoals\": [[\"goal 1\", \"goal 2\", \"goal 3\"]]}."
        #" Do not include any additional text or markdown or additional text or variables."
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
        {(example1_hl if mode == ShotPromptingMode.ONE_SHOT else f"{example1_hl}, {example2_hl}" if mode == ShotPromptingMode.FEW_SHOT else "")}\n
        
        \nYour task: based on your understanding of the typical needs and interests of the following actors in the following software project, help generate a list of higl level goals.\n

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
        "You are a helpful assistant expert in software engineering tasks"
        "Elicit low-level goals for a specific stakeholder in a software project "
        " The low-level goals that you create MUST be structured to match against a set of API calls. Don't be too generic, for example, avoid goals like 'make the software fast', 'develop a web interface' etc."
        "Each low-level goal MUST be phrased as an interaction with the system that could be implemented via an API call."
        "Avoid generic goals. Instead, break them down into atomic actions linked to system capabilities."
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

        {(example1_ll if mode == ShotPromptingMode.ONE_SHOT else f"{example1_ll}, {example2_ll}" if mode == ShotPromptingMode.FEW_SHOT else "")}\n
         \nYour task: based on your understanding of the typical tasks that compose the following sequence of high-level goals,
        provide if possible a decomposition of goals into sub-goals. 
        Each low-level goal should theoretically correspond to a single action of the actor with the software.
        **High-level goals:**\n\n
        {highLevelGoals}\n

        **Output:**
    """

    lowLevelGoals = generate_response(prompt, sys_prompt, LowLevelGoals)

    return lowLevelGoals