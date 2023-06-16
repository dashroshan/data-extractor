# Importing required libraries
import os
import time
import requests
import string
import random
import argparse
from dotenv import load_dotenv
from process import processDataToCSV

# Loading environment variables
load_dotenv()

# Getting environment variables
ENDPOINT = os.getenv("ENDPOINT")
KEY = os.getenv("KEY")
BLOB_ENDPOINT = os.getenv("BLOB_ENDPOINT")
BLOB_QUERY = os.getenv("BLOB_QUERY")


# Uploads the file to Azure blob storage and returns the file url
def uploadToAzureBlob(fileName):
    with open(fileName, "rb") as finput:
        data = finput.read()
    randomStr = "".join(random.choices(string.ascii_letters, k=15))
    requests.put(
        url=BLOB_ENDPOINT + randomStr + fileName + BLOB_QUERY,
        data=data,
        headers={
            "Content-type": "image/jpeg",
            "x-ms-blob-type": "BlockBlob",
        },
    )
    return BLOB_ENDPOINT + randomStr + fileName


# Deletes the file at the given url in Azure blob storage
def deleteFromAzureBlob(fileUrl):
    r = requests.delete(
        url=fileUrl + BLOB_QUERY,
        headers={
            "Content-type": "image/jpeg",
            "x-ms-blob-type": "BlockBlob",
        },
    )


# Send the document to the Azure form recognizer service for analysis
# This returns a URL that we can use to get the results of the analysis when it is done
def analyze(fileName):
    # Azure form analyzer can only work with a file URL and doesn't supporting binary data directly
    # So we upload the file to azure blob storage and get the link
    fileUrl = uploadToAzureBlob(fileName)

    res = requests.post(
        url=f"{ENDPOINT}/formrecognizer/documentModels/prebuilt-document:analyze?api-version=2022-08-31",
        headers={"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": KEY},
        json={"urlSource": fileUrl},
    )
    return (res.headers["Operation-Location"], fileUrl)


# Analyze a given document
def getAnalyzeResult(filename):
    # Send the file to Azure to start analyzing
    analyze_url, fileUrl = analyze(filename)

    # It takes a while to complete analyzing so we keep on re-requesting every 1 second
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
            # If analyzing is completed, we delete the file from Azure blob storage and return the data
            deleteFromAzureBlob(fileUrl)
            return {
                "tables": result["analyzeResult"]["tables"],
                "keyValuePairs": result["analyzeResult"]["keyValuePairs"],
                "paragraphs": result["analyzeResult"]["paragraphs"],
            }
        else:
            # Else we wait 1s and try again
            time.sleep(1)


# Covert the data from the provided form into CSV
def formToCSV(formName, csvName):
    data = getAnalyzeResult(formName)  # Get the data from Azure form analyzer as JSON
    processDataToCSV(data, csvName)  # Process the data and write it into a CSV


# Run if the file is executed directly
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i")
    parser.add_argument("-o")
    args = parser.parse_args()

    if args.i and args.o:
        formToCSV(args.i, args.o)
        print("Done!")
    else:
        print(
            "Arguments missing!\nUse the format given below:\npy main.py -i input.xyz -o output.csv"
        )
