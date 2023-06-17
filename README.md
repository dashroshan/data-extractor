# Data Extractor

Extract and download key-value pairs, tables, and paragraphs from your scanned pdf, jpg, and png documents as CSV files.

## Tech stack

| Technology                 | Used for                      |
| -------------------------- | ----------------------------- |
| Flask                      | Backend                       |
| React + Tailwind + DaisyUI | Frontend                      |
| Azure FormRecognizer       | Extracting data from document |
| Azure BlobStorage          | Storing uploaded documents    |

## Usage (as a webapp)

1. Run `npm i` in frontend folder followed by `npm run build`
2. Run `pip install -r requirements.txt` in root folder
3. Create a `.env` file with the below content:

Create a Azure FormRecognizer service and copy the `Endpoint` and `KEY1` from `Keys and Endpoint`. These will be the ENDPOINT and KEY respectively. Next create an azure storage account, and create a container in it. Go to `Shared access tokens` and click `Generate SAS token and URL`. Copy the `Blod SAS URL`. The part to the left of `?` goes in `BLOB_ENDPOINT` and the part to the right goes in `BLOB_QUERY`

```
ENDPOINT = "https://xyz.cognitiveservices.azure.com"
KEY = "12345something"
BLOB_ENDPOINT = "https://xyz.blob.core.windows.net/containerName/"
BLOB_QUERY = "?xyz=xyz&xyz=xyz..."
```

4. Run with `py main.py`

## Usage (as a script)

Run `py extract.py -i "input/file/path.pdf" -o "output/file/path.csv"`