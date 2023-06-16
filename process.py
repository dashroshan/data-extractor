import csv
from io import StringIO


# Converts table data returned by Form recognizer into CSV data
def makeTableCSV(tablesData):
    data2d = [
        ["" for x in range(tablesData["columnCount"])]
        for y in range(tablesData["rowCount"])
    ]
    for cell in tablesData["cells"]:
        data2d[cell["rowIndex"]][cell["columnIndex"]] = cell["content"]
    return data2d


# Converts the key value data returned by Form recognizer into CSV data
def makeKeyValueCSV(data):
    pairs = []
    for pair in data:
        key = pair["key"]["content"]
        if key[-1] == ":":
            key = key[:-1]
        pairs.append([key, pair["value"]["content"]])
    pairs.insert(0, ["Key", "Value"])
    return pairs


# Converts the paragraphs data returned by Form recognizer into CSV data
def makeParagraphsCSV(data):
    paras = []
    for p in data:
        paras.append([p["content"]])
    paras.insert(0, ["Paragraphs"])
    return paras


# Merges all the 2d CSV data tables in the provided list into a single 2d CSV data table
def mergeCSV(datas):
    colmax = 0
    rowmax = 0
    for data in datas:
        cols = len(data[0])
        rows = len(data)
        if cols > colmax:
            colmax = cols
        rowmax += rows

    rowmax += (len(datas) - 1) * 3

    data2d = [["" for x in range(colmax)] for y in range(rowmax)]
    rowIndex = -1
    for data in datas:
        if rowIndex != -1:
            rowIndex += 3
        for row in data:
            rowIndex += 1
            for i in range(len(row)):
                data2d[rowIndex][i] = row[i]

    return data2d


# Extracts all the table, key-value, and paragraph data from Form recognizer and writes it to a CSV string
def processDataToCSV(data):
    csvData = []
    csvData.append(makeKeyValueCSV(data["keyValuePairs"]))

    for table in data["tables"]:
        csvData.append(makeTableCSV(table))

    csvData.append(makeParagraphsCSV(data["paragraphs"]))

    f = StringIO()
    csv.writer(f).writerows(mergeCSV(csvData))
    return f.getvalue()


# Extracts all the table, key-value, and paragraph data from Form recognizer and returns it as a dictionary
def processDataToObj(data):
    processedData = {"tables": []}
    processedData["keyValuePairs"] = makeKeyValueCSV(data["keyValuePairs"])

    for table in data["tables"]:
        processedData["tables"].append(makeTableCSV(table))

    processedData["paragraphs"] = makeParagraphsCSV(data["paragraphs"])

    return processedData
