from flask import Flask,request
from mira_sdk import MiraClient
from dotenv import load_dotenv
from flask_cors import CORS
import os 
import json

app = Flask(__name__)
CORS(app)

load_dotenv()
client = MiraClient(config={"API_KEY":os.getenv('DISCORD_BOT_KEY')})     # Initialize client

versionPart = "1.0.0"   
versionOrg = '1.0.0'                                        # Optional specific version
# Execution input


# If no version is provided, it'll use the latest version by default
if versionPart:
    flow_name = f"anshkarwasra/hackathon-mentor/{versionPart}"
else:
    flow_name = "anshkarwasra/hackathon-mentor"

if versionOrg:
    flowOrg = f"anshkarwasra/hackathon-project-evaluator/{versionPart}"
else:
    flowOrg = "anshkarwasra/hackathon-project-evaluator"




@app.route('/getData',methods=['GET','POST'])
def getData():
    if request.method == 'POST':
        print('got a request')
        clientData = request.get_data()
        jsonData = json.loads(clientData)
        response = client.flow.execute(flow_name,{
            'userPrompt': jsonData['details']
        })
        print('sent following data to client:',response)
        return {
            'status': 'success',
            'data': response['result']
        }
 
@app.route('/getEvals',methods=['GET','POST'])
def getEvals():
    if request.method == 'POST':
        print('got a eval request')
        clientData = request.get_data()
        jsonData = json.loads(clientData)
        print(jsonData)
        response = client.flow.execute(flowOrg,{
            'readme_documents': jsonData['details']
        })
        return  {
            'status':'success',
            'content': response['result']
        }

app.run(debug=True,port=5000)