import pandas as pd
from flask import Flask, jsonify, request, url_for
import requests
import pickle
import json
from src.errors import WrongInput


# with open("models/SOMENAME.pkl", "rb") as f:
#    MODEL = pickle.load(f)

app = Flask(__name__)


def convert_data(json_raw):
    """
    Some function to maybe do some data wrangeling with the json file
    """
    try:
        sample = pd.DataFrame(json_raw, index=[0]).rename(columns=str.lower)
        return sample
    except:
        raise WrongInput(
            "Payload should be json with all titanic headers except" " survived as keys"
        )
    pass


# routes
@app.route("/", methods=["POST"])
def predict():
    json_row = request.get_json()
    converted_data = convert_data(json_row)

    prediction = MODEL.predict(converted_data)[0]
    return str(prediction)  # , response_shap_api
