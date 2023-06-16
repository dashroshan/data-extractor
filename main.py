from flask import Flask

app = Flask("Data Extractor")

if __name__ == "__main__":
    app.run(debug=True, port=4000)
