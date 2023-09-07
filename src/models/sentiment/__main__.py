from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
pipe = pipeline("text-classification", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Check if 'to_predict' key exists in the JSON data
        if 'to_predict' not in data:
            return jsonify({"error": "Missing 'to_predict' key in JSON data"}), 400

        # Perform your prediction here (replace this with your actual prediction logic)
        input_string = data['to_predict']
        response = pipe(input_string)[0]

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
