from src.examples.shot_learning import ShotPromptingMode, example1_map, example2_map
from data_model import APIMapping
from src.tools import api_list_to_string
from src.llm_clients import generate_response
def generate_mapping_apis_goals(lowLevelGoals, apiList, mode=ShotPromptingMode.ZERO_SHOT):
    
    sys_prompt = (
        "You are a helpful assistant that helps developers to map low-level goals to APIs."
        " You will be given a low-level goal and a list of APIs. Your task is to identify which APIs best satisfies each low-level goal."        
        "Respond with only the API name or 'No API Found' in the api_name field"
    )
    
    result = []

    for lowLevelgoal in lowLevelGoals.low_level_goals:
        
        #print(f"Doing: {lowLevelgoal.get('description')} .." )
        
        prompt = f"""
            Given the following goal:
            {lowLevelgoal}

            And the list of APIs below:
            {apiList}

            Identify the single API that best satisfies the goal. Maximum three APIs satisfy the goal. If no API satisfies the goal, return exactly "No API Found".
            Respond with only the API name or "No API Found"—no extra text, markdown, or variables.

            {(example1_map if mode == ShotPromptingMode.ONE_SHOT else f"{example1_map}, {example2_map}" if mode == ShotPromptingMode.FEW_SHOT else "")}\n

            **Output:**\n
        """

        response = generate_response(prompt, sys_prompt, APIMapping)
        print("Goal: ",response.low_level_goal.description)
        print("APIs: ", api_list_to_string(response.APIs))
        result.append(response)

        
    return result



from tabulate import tabulate # Import tabulate for nice table formatting

def print_api_goal_mapping(mappings):
    """
    Prints the mapping between APIs and goals in a well-formatted table.

    Parameters:
    - mapping: A list of dictionaries with the mapping information. Each dictionary contains:
        - 'low_level_goal': The goal.
        - 'api': The API satisfying the goal or 'No API Found'.
    """
    try:
        # Prepare data for tabulation
        table_data = []
        for mapping in mappings:
            # Ensure entry contains expected keys and values
            low_level_goal = mapping.low_level_goal.description
            table_data.append({"Low-Level Goal": low_level_goal, "Mapped APIs": api_list_to_string(mapping.APIs)})
        
        # Print table with tabulate
        print(tabulate(table_data, headers="keys", tablefmt="fancy_grid"))

    except Exception as e:
        print(f"Error while printing mapping: {e}")