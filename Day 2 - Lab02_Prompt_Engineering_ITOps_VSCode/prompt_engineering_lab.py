from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
load_dotenv()
client=OpenAI()
df=pd.read_csv('data/sample_incidents_10000.csv')
incident=df.loc[0,'incident_description']
prompt=f'''You are a Senior IT Infrastructure Engineer.
Summarize the incident.
Identify the probable root cause.
Recommend next actions.

Incident:
{incident}
'''
response=client.responses.create(model='gpt-4.1-mini',input=prompt)
print(response.output_text)
