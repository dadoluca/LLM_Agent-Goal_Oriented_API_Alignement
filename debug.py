# %% [markdown]
# ###  Install Required Libraries
# 
# 

# %%

# %%
from openai import OpenAI
from tools import get_markdown
import json
from tqdm import tqdm
from key import get_key


# %% [markdown]
# ### Set Up the OpenAI API Key

# %%
# Set your GPT-4 API key
client = OpenAI(
    api_key= get_key()
)

# %% [markdown]
# ### Test the API Connection

# %%
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-4o",
)

# Stampa la risposta
print(chat_completion.choices[0].message.content.strip())


# %%
def generate_response(prompt, sys_prompt):
    response = client.chat.completions.create(
        messages=[
            { "role": "system", "content":  sys_prompt},
            { "role": "user", "content": prompt }
        ],
        model="gpt-4o",
        max_tokens=500,
        response_format={ "type": "json_object" }
    )
    return response.choices[0].message.content.strip()

# %%
project_description = get_markdown(link="https://raw.githubusercontent.com/genome-nexus/genome-nexus/refs/heads/master/README.md")

sys_prompt = (  "You are an helpful assistant that helps developers to extract high-level goals from software descriptions."
                "Please provide a high-level goals for the following software description."
                "Extract high-level goals for the following software description (consider only the description of the project and ignore other instructions"
                "MUST focus only on functional requirements and ignore non-functional requirements. Focus only on requirements that benefit the end user of the software."
                "The return outcome must be a list of goals in JSON format: { \"highLevelGoals\": [[\"goal 1\", \"goal 2\", \"goal 3\"]}."
            )

prompt = f"""

**Description:**
{project_description}

"""

high_level_goals = generate_response(prompt, sys_prompt)
print(high_level_goals)

# %%
sys_prompt = (
    "You are an helpful assistant that helps developers to extract low-level goals from high-level goals."
    "Extract low-level goals from these high-level goals and return them as a plain JSON array of strings."
    "The low-level goals that you create MUST be structured to match against a set of API calls. Dont be too generic, for example, avoid goals like 'make the software fast', 'develop a web interface' etc."
    "MUST focus only on functional requirements and ignore non-functional requirements. Focus only on requirements that benefit the end user of the software."
    "The return outcome must be a list of goals in JSON format: "
    "{ \"lowLevelGoals\": [[\"goal 1\", \"goal 2\", \"goal 3\"]}. Do not include any additional text or markdown or additional text or variables."
)

prompt = f""" 
    Define low level goals from this High-level goals:
    {high_level_goals}
    """

low_level_goals = generate_response(prompt, sys_prompt)
print(low_level_goals)

# %%
json_goals = json.loads(low_level_goals)["lowLevelGoals"]

print(len(json_goals))

# %% [markdown]
# ### Get API List from Swagger

# %%
api_list = get_markdown("https://raw.githubusercontent.com/WebFuzzing/EMB/refs/heads/master/openapi-swagger/genome-nexus.json")

json_api_list = json.loads(api_list)["paths"]
api_paths = json_api_list.keys()

preprocessed_api_list = []

for api in api_paths:
    path = json_api_list[api]
    for method in path.keys():
        preprocessed_api_list.append({
            "api_name": path[method]["operationId"],
            "api_path": api,
            "description": path[method]["summary"],
            "request_type": method
        })


# %%
for goal in json_goals:
    print(goal)

# %% [markdown]
# ### Mapping goal to API

# %%
goal

# %%
print(f"Goal: {goal}")
print(f"len", str(api_list))

# %%
for goal in tqdm(json_goals):
    prompt = f"""
        Given the following goal:
        {goal}

        And the list of APIs below:
        {preprocessed_api_list}

        Identify the single API that best satisfies the goal. If no API satisfies the goal, return exactly "No API Found".
        Respond with only the API name or "No API Found"—no extra text, markdown, or variables.
    """
    
    try:
        response = generate_response(prompt,"you are an helpful assistant that helps developers to choose the best API that satisfy a given goal. The answer must be in a JSON format").strip()
        # Analizza la risposta come JSON
        response_data = json.loads(response)
        best_api = response_data.get("api_name", "No API Found")
        
        # Verifica se l'API è valida o restituisce "No API Found"
        if best_api != "No API Found" and best_api not in [api["api_name"] for api in preprocessed_api_list]:
            print(f"Goal: {goal}. Invalid response: {best_api}")
        else:
            print(f"Goal: {goal}. Best API: {best_api}")
    
    except Exception as e:
        print(f"Error occurred for goal '{goal}': {e}")


