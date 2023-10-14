import logging
import os
import pymongo
import pickle

from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file


from src.generate_shadow_matrix import generate_shadow_matrix_for_datetime
from src.utils.db import get_connection_string
from src.utils.helpers import save_shadow_matrix_as_image

app = Flask(__name__)
load_dotenv()

APP_SECRET = os.environ["APP_SECRET"]
SCRIPT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "src/generate_shadow_matrix.py"
)
IMAGES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "images"
)


# db connection
db_client = pymongo.MongoClient(get_connection_string())
db = db_client["smart_research"]
collection = db["shadow_matrix"]


@app.route('/shadow-matrix', methods=['POST'])
def generate_shadow_matrix():
    data = request.json
    if "TOKEN" not in data:
        return jsonify({"error": "Token is required to access the endpoint"}), 404

    if data.get("TOKEN") != APP_SECRET:
        return jsonify({"error": "Invalid token"}), 401

    current_datetime = datetime.now()
    stored_datetime = generate_shadow_matrix_for_datetime(current_datetime)

    # db_client, collection = create_db_client()
    print(f"Returned datetime: {stored_datetime}")
    query = {"datetime": stored_datetime}

    # this should return only one document
    documents = collection.find(query)

    image_paths = []
    for matrix_data in documents:
        sh_binary = matrix_data["shadow_matrix"]
        sh = pickle.loads(sh_binary)

        image_name = matrix_data["datetime"].strftime("%Y-%m-%d_%H-%M-%S-%f")
        image_path = os.path.join(IMAGES_DIR_PATH, f"{image_name}.png")
        print(f"Image path: {image_path}")

        save_shadow_matrix_as_image(sh, matrix_data["hour"], matrix_data["minute"], image_path)
        if os.path.exists(image_path):
            image_paths.append(image_path)
        else:
            return jsonify({"error": "Internal server error"}), 500

    return send_file(image_paths[0], as_attachment=True)


@app.teardown_appcontext
def close_mongo_connection(exception):
    db_client.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
