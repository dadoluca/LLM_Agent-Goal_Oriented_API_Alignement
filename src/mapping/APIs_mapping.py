
from src.examples.shot_learning import ShotPromptingMode, example1_map, example2_map
from src.data_model import APIMapping
from src.tools import api_list_to_string
from src.llm_clients import generate_response
from tabulate import tabulate # Import tabulate for nice table formatting

def generate_mapping_apis_goals(lowLevelGoals, apiList, mode=ShotPromptingMode.ZERO_SHOT):
    
    sys_prompt = (
        "You are a helpful assistant that helps developers to map low-level goals to APIs."
        "You will be given a low-level goal and a list of APIs. Your task is to identify which APIs best satisfies each low-level goal."        
        #"Respond with only the API name or 'No API Found' in the api_name field"
        "If no API satisfies the goal, set the api_name field to exactly: 'No API Found'"
    )
    
    result = []

    for lowLevelgoal in lowLevelGoals.low_level_goals:
        
        #print(f"Doing: {lowLevelgoal.get('description')} .." )
        
        prompt = f"""
            {(example1_map if mode == ShotPromptingMode.ONE_SHOT else f"{example1_map}, {example2_map}" if mode == ShotPromptingMode.FEW_SHOT else "")}\n

            Given the following goal:
            {lowLevelgoal}

            And the list of APIs below:
            {apiList}

            Identify the single API that best satisfies the goal. Maximum three APIs satisfy the goal.

            **Output:**\n
        """

        response = generate_response(prompt, sys_prompt, APIMapping)
        print("hlg name: ", response.low_level_goal.high_level_associated.name)
        print("Goal name: ",response.low_level_goal.name)
        print("Goal description: ",response.low_level_goal.description)
        print("APIs: ", api_list_to_string(response.APIs))
        result.append(response)

        
    return result



#from tabulate import tabulate 

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
            associated_high_level = mapping.low_level_goal.high_level_associated.name
            low_level_goal_name = mapping.low_level_goal.name
            low_level_goal_description = mapping.low_level_goal.description
            table_data.append({"High-Level Goal name": associated_high_level,"Low-Level Goal name": low_level_goal_name, "Low-Level Goal description": low_level_goal_description, "Mapped APIs": api_list_to_string(mapping.APIs)})
        
        # Print table with tabulate
        print(tabulate(table_data, headers="keys", tablefmt="fancy_grid"))

    except Exception as e:
        print(f"Error while printing mapping: {e}")