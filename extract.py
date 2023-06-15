# Importing required libraries
import os
import time
import json
import requests
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

# Getting environment variables
ENDPOINT = os.getenv("ENDPOINT")
KEY = os.getenv("KEY")


# Send the document to the Azure form recognizer service for analysis
# This returns a URL that we can use to get the results of the analysis when it is done
def analyze():
    res = requests.post(
        url=f"{ENDPOINT}/formrecognizer/documentModels/prebuilt-document:analyze?api-version=2022-08-31",
        headers={"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": KEY},
        json={"urlSource": "https://i.imgur.com/v2KqwxU.jpg"},
    )
    return res.headers["Operation-Location"]


def processData(data):
    return {
        "tables": data["tables"],
        "keyValuePairs": data["keyValuePairs"],
        "paragraphs": data["paragraphs"],
    }


def getAnalyzeResult():
    analyze_url = analyze()
    while True:
        res = requests.get(
            url=analyze_url,
            headers={
                "Content-Type": "application/json",
                "Ocp-Apim-Subscription-Key": KEY,
            },
        )
        result = res.json()
        if result["status"] == "succeeded":
            return processData(result["analyzeResult"])
        else:
            time.sleep(1)


result = getAnalyzeResult()
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
