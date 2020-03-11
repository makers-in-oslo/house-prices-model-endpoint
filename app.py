import pandas as pd
from flask import Flask, jsonify, request
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
            "Payload should be json with all house-price headers except 'price' as keys"
        )
    pass


# routes
@app.route("/", methods=["POST"])
def predict():
    json_row = request.get_json()
    converted_data = convert_data(json_row)
    # prediction = MODEL.predict(converted_data)[0]
    print(converted_data)
    return str(1)  ##jsonify(converted_data.to_json())  # str(prediction)


@app.errorhandler(WrongInput)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
