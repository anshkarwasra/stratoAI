from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv
import os 
load_dotenv()
client = MiraClient(config={"API_KEY":os.getenv('DISCORD_BOT_KEY')})     # Initialize client

version = "1.2.3"                                           # Optional specific version
# Execution input

test_input = {'prompt': 'Mira AI Hackathon 2024, AI/LLM Agents, 48-hour event focusing on innovative AI agents using Mira SDK, looking for projects that demonstrate creativity in AI agent development'}


# If no version is provided, it'll use the latest version by default
if version:
    flow_name = f"r3bel/hackathon-mentor/{version}"
else:
    flow_name = "r3bel/hackathon-mentor"

result = client.flow.execute(flow_name,test_input)  # Execute flow
print(result['result'])
