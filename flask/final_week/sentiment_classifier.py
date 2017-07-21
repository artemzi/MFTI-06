from sklearn.externals import joblib


class SentimentClassifier(object):
    def __init__(self):
        self.model = joblib.load("./Classifier.pkl")
        self.classes_dict = {0: "negative", 1: "positive", -1: "prediction error"}

    def predict_text(self, text):
        try:
            text = text.split(" ")
            print("Passed to model: {}".format(text))
            return self.model.predict(text)

        except Exception as inst:
            print("prediction error")
            print(inst)
            return -1

    def get_prediction_message(self, text):
        prediction = list(self.predict_text(text))
        ones = prediction.count(1) or 0
        zeros = prediction.count(0) or 0
        print("Prediction: {}".format(prediction))
        if ones > zeros:
            return self.classes_dict[1]
        else:
            return self.classes_dict[0]

    def get_prediction(self, text):
        clazz = self.model.predict(text)
        proba = self.model.predict_proba(text).max()
        return clazz, 100 * proba
