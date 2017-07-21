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
def index_page():
    return render_template('hello.html')


@app.route('/predict')
def predict(text=''):
    text = request.args.get('text')
    prediction_message = clf.get_prediction_message(text)
    print(prediction_message)
    return prediction_message


@app.route('/<path:path>')
def hello(path=''):
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
