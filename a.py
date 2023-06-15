from data import data
import csv

# Writes the given CSV data into the given file
def writeCSV(data, filename):
    with open(filename, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)


# Converts table data returned by Form recognizer into a html table
def makeTableHTML(tablesData):
    prevRow = 0
    tableHtml = "<table><tr>"
    for cell in tablesData["cells"]:
        if cell["rowIndex"] != prevRow:
            tableHtml += "</tr><tr>"
            prevRow = cell["rowIndex"]
        colspan = cell.get("columnSpan", 1)
        if cell.get("kind", None) == "columnHeader":
            tableHtml += f"<th colspan='{colspan}'>{cell['content']}</th>"
        else:
            tableHtml += f"<td colspan='{colspan}'>{cell['content']}</td>"
    tableHtml += "</tr></table>"
    return tableHtml


# Converts table data returned by Form recognizer into CSV data
def makeTableCSV(tablesData):
    data2d = [
        ["" for x in range(tablesData["columnCount"])]
        for y in range(tablesData["rowCount"])
    ]
    for cell in tablesData["cells"]:
        data2d[cell["rowIndex"]][cell["columnIndex"]] = cell["content"]
    return data2d

# Returns key values detected as a 
def getKeyValue(data):
    pairs = []
    for pair in data:
        key = pair["key"]["content"]
        if key[-1] == ":":
            key = key[:-1]
        pairs.append([key, pair["value"]["content"]])
    return pairs


def makeKeyValueCSV(data):
    data.insert(0, ["Key", "Value"])
    return data


# tablesData = data["tables"][0]
# tableCSV = makeTableCSV(tablesData)
# tableHtml = makeTableHTML(tablesData)
# writeCSV(tableCSV, "table.csv")
kvPairData = getKeyValue(data["keyValuePairs"])
writeCSV(makeKeyValueCSV(kvPairData), "table.csv")
