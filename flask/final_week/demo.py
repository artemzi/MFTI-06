from sentiment_classifier import SentimentClassifier
from codecs import open
import time
import sys
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

print("Preparing classifier")
start_time = time.time()
clf = SentimentClassifier()
print("Classifier is ready")
print(time.time() - start_time, "seconds")


@app.route("/", methods=["POST", "GET"])
def index_page(text="", prediction_message=""):
    if request.method == "POST":
        text = request.form["text"]
        sys.stdout = open("ydf_demo_logs.txt", "a", "utf-8")
        print(text)
        print("<response> sys.stdout")
        prediction_message = clf.get_prediction_message(text)
        print(prediction_message)
        print("<response> sys.stdout")

    return render_template('hello.html', text=text, prediction_message=prediction_message)


@app.route('/predict', methods=["POST"])
def predict(text=''):
    txt = request.args.get('text')
    return clf.get_prediction(txt)


@app.route('/<path:path>')
def hello(path=''):
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
