from dotenv import load_dotenv
from mira_sdk import MiraClient
from mira_sdk import Flow,CompoundFlow
from mira_sdk.exceptions import FlowError
import os

load_dotenv()
client = MiraClient(config={"API_KEY": os.getenv("DISCORD_BOT_KEY")})

    # Initialize Mira Client

# Basic test
flow = Flow(source="./modelData/hackscheme.yaml")# Load flow configuration

test_input = {"organizer_ideas":'''
   {
  "organizer_ideas": {
    "theme": "Future of Mobility",
    "target_audience": ["students", "startups", "tech enthusiasts"],
    "tracks": ["autonomous vehicles", "sustainable transportation", "urban mobility"],
    "duration": "72 hours",
    "prize_structure": "Cash prizes, incubator support, and certificates",
    "additional_goals": "Encourage innovation in clean energy solutions for transportation"
  }
}

'''}

try:
    response = client.flow.test(flow, test_input)           # Test entire pipeline
    print("Test response:", response)
except Exception as e:
    print("Test failed:", str(e))  

# try:
#     client.flow.deploy(flow)                                # Deploy to platform
# except FlowError as e:
#     print(f"Error occurred: {str(e)}") 

