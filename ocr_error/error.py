from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/log_error', methods=['POST'])
def log_error():
    try:
        error_message = request.json.get('error_message', 'No error message provided.')
        # Here you can implement logging of the error_message to a file, database, etc.
        print("Error logged:", error_message)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5004, debug=True)
