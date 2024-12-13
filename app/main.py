# Project Code: main.py
from fastapi import FastAPI
import requests
import pandas as pd
from pyngrok import ngrok
import uvicorn
import nest_asyncio
import openai

# Initialize FastAPI
app = FastAPI()

# connect Ngork
ngrok.set_auth_token("Your_Ngrok_Key")
# Get a list of all active tunnels
tunnels = ngrok.get_tunnels()

# Iterate through each tunnel and disconnect it
for tunnel in tunnels:
    print(f"Disconnecting tunnel: {tunnel.public_url}")
    ngrok.disconnect(tunnel.public_url)

print("All ngrok tunnels have been deleted.")

ngrok_tunnel = ngrok.connect(8000)
print(f"Public URL: {ngrok_tunnel.public_url}")

# Set OpenAI API Key
YOUR_OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.get("/fetch_data/")
def fetch_data(drug_name: str):
    url = f"https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{drug_name}&limit=10"
    response = requests.get(url).json()
    events = response.get("results", [])
    df = pd.DataFrame(events)
    return df.to_dict(orient="records")

@app.post("/summarize/")
def summarize_adverse_events(data: list):
    report_text = "\n".join([f"Event: {x['patient']['reaction'][0]['reactionmeddrapt']}" for x in data])
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize these adverse events: {report_text}",
        max_tokens=150
    )
    return {"summary": response["choices"][0]["text"].strip()}

if __name__ == "__main__":
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

