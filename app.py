import pandas as pd
from flask import Flask, jsonify, request
import pickle
import json
from src.errors import WrongInput
import os
from src.funcs import stream_pickle

app = Flask(__name__)

model_name_d = "model_d.pkl"
model_name_b = "model_b.pkl"


MODEL_DANIEL = stream_pickle(
    os.environ["ACCESS_KEY"],
    os.environ["SECRET_KEY"],
    "ds-lett",
    "house-prices/models/" + model_name_d,
)

MODEL_BJORNAR = stream_pickle(
    os.environ["ACCESS_KEY"],
    os.environ["SECRET_KEY"],
    "ds-lett",
    "house-prices/models/" + model_name_b,
)

# with open("models/model_bkm.pkl", "rb") as f:
#    MODEL_BJORNAR = pickle.load(f)


def convert_data(json_raw):
    """
    Some function to maybe do some data wrangeling with the json file
    """
    sample = pd.DataFrame(json_raw, index=[0]).rename(columns=str.lower)
    return sample


# routes
@app.route("/", methods=["POST"])
def to_row():
    try:
        json_row = request.get_json()
        converted_data = convert_data(json_row)
        print(converted_data)
        return jsonify(converted_data.to_json())
    except:
        raise WrongInput(
            "Payload should be JSON with all house-price headers except 'price' as keys"
        )


@app.route("/daniel", methods=["POST"])
def predict_daniel():
    try:
        json_row = request.get_json()
        # print(f"json: {json_row}")
        converted_data = convert_data(json_row)
        # print(f"pandas: {converted_data}")
        prediction = MODEL_DANIEL.predict(converted_data)[0]
        # print(f"prediction: {prediction}")
        return str(prediction)
    except:
        raise WrongInput(
            "Payload should be JSON with all house-price headers except 'price' as keys"
        )


@app.route("/bjornar", methods=["POST"])
def predict_bjornar():
    try:
        json_row = request.get_json()
        # print(f"json: {json_row}")
        converted_data = convert_data(json_row)
        # print(f"pandas: {converted_data}")
        prediction = MODEL_BJORNAR.predict(converted_data)[0]
        # print(f"prediction: {prediction}")
        return str(prediction)
    except:
        raise WrongInput(
            "Payload should be JSON with all house-price headers except 'price' as keys"
        )


@app.errorhandler(WrongInput)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(ValueError)
def handle_error_in_model(error):
    response = jsonify({"message": "ValueError", "status_code": 400})
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
