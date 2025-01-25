from mira_sdk import MiraClient
import dotenv
import os
dotenv.load_dotenv()
client = MiraClient(config={"API_KEY": os.getenv('DISCORD_BOT_KEY')})        # Initialize client

# Create a new dataset
client.dataset.create(
    "anshkarwasra/gpu-benchmark",                                     # Unique identifier
    "Its a collection of bechmarks of different games on bunch of gpus"        # Dataset purpose
)

client.dataset.add_source('anshkarwasra/GPU_benchMark',file_path='gpu_game_benchmarks.csv')
client.dataset.add_source('anshkarwasra/GPU_benchMark',url='https://gpu.userbenchmark.com/')


