from cloudant.client import cloudant
from cloudant.query import Query
from flask import Flask, jsonify, request
import atexit
from werkzeug.exceptions import abort
import json


#Add your Cloudant service credentials here
cloudant_username = 'd9e208c2-1e95-486d-b218-9ba6ae84adac-bluemix'
cloudant_api_key = 'TQHSOOB6wvN93tS8_Bbotnz2zwK0CaclQA3q81QM_qX5'
cloudant_url = 'https://d9e208c2-1e95-486d-b218-9ba6ae84adac-bluemix.cloudantnosqldb.appdomain.cloud'
client = Cloudant.iam(cloudant_username, cloudant_api_key, connect=True, url=cloudant_url)

session = client.session()
print('Databases:', client.all_dbs())

db = client['reviews']

app = Flask(__name__)

@app.route('/api/get_reviews', methods=['GET'])
def get_reviews():
    dealership_id = request.args.get('id')

    # Check if "id" parameter is missing
    if dealership_id is None:
        return jsonify({"error": "Missing 'id' parameter in the URL"}), 400

    # Convert the "id" parameter to an integer (assuming "id" should be an integer)
    try:
        dealership_id = int(dealership_id)
    except ValueError:
        return jsonify({"error": "'id' parameter must be an integer"}), 400

    # Define the query based on the 'dealership' ID
    selector = {
        'dealership': dealership_id
    }

    # Execute the query using the query method
    result = db.get_query_result(selector)

    # Create a list to store the documents
    data_list = []
    # Iterate through the results and add documents to the list
    for doc in result:
        data_list.append(doc)
    print(data_list)
    # Return the data as JSON
    return jsonify(data_list)


@app.route('/api/post_review', methods=['POST'])
def post_review():
    if not request.json:
        abort(400, description='Invalid JSON data')
    
    # Extract review data from the request JSON
    review_data = request.json

    # Validate that the required fields are present in the review data
    required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
    for field in required_fields:
        if field not in review_data:
            abort(400, description=f'Missing required field: {field}')

    # Save the review data as a new document in the Cloudant database
    print("review--------->", review_data)
    # Ensure review_data is a dictionary
    if not isinstance(review_data, dict):
        review_data = json.loads(review_data)  # Parse string as JSON
        if not isinstance(review_data, dict):
            abort(400, description='Invalid JSON data')

    db.create_document(review_data)

    return jsonify({"message": "Review posted successfully"}), 201


if __name__ == '__main__':
    app.run(debug=True)