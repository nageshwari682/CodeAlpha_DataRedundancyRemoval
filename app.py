from flask import Flask, request, jsonify, render_template
from database import init_db, insert_record
from redundancy_checker import validate_and_classify

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400

    result = validate_and_classify(name, email)

    if result['status'] == 'accepted':
        insert_record(name, email, result['hash'])
        return jsonify({"message": "Record added successfully", "status": "accepted"}), 201
    elif result['status'] == 'rejected':
        return jsonify({"message": "Exact duplicate rejected", "status": "rejected"}), 409
    else:
        return jsonify({
            "message": "Flagged as possible duplicate — needs review",
            "status": "flagged",
            "similar_record": result['similar_to']
        }), 202

if __name__ == '__main__':
    app.run(debug=True)