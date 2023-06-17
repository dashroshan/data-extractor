# Importing required libraries
import os
import random
import string
from flask import *
from extract import formToData

# Set react build folder for static and template
app = Flask(
    __name__,
    static_folder=os.path.abspath("frontend/build/static"),
    template_folder=os.path.abspath("frontend/build"),
)


# Server react site at root
@app.route("/")
def hello():
    return render_template("index.html")


# Api for form to data
@app.route("/api/uploadForm", methods=["POST"])
def success():
    if request.method == "POST":
        f = request.files["file"]
        randomStr = "".join(random.choices(string.ascii_letters, k=5))
        filePath = os.path.abspath("upload/" + randomStr + f.filename)
        f.save(filePath)
        formData = formToData(filePath)
        os.remove(filePath)
        return formData
    else:
        return {"status": "failed"}


# Start flask server
if __name__ == "__main__":
    app.run(debug=False, port=5016)
