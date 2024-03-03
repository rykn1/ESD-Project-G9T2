# pip install exchangeratesapi    -> If not done yet

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

api_key = ""  # Get this from https://exchangeratesapi.io/ , create an account there. 250 Free Calls. 
@app.route('/exchange', methods=['GET'])
def get_exchange_rate():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')

    try:
        api_url = f'http://api.exchangeratesapi.io/v1/latest?access_key={api_key}&symbols=SGD,{to_currency}'

        response = requests.get(api_url)

        response = response.json()
        print(response['success'])
        print(response)
        if response['success']:
            print(from_currency,to_currency)
            fromCurr = response['rates'][from_currency]
            toCurr = response['rates'][to_currency]
            result = round((1/fromCurr)/(1/toCurr),2)
            return jsonify({
                'from': from_currency,
                'to': to_currency,
                'result': result
            })
        else:
            return jsonify({'error': response['error']['message']}), 400 

    except KeyError as e: 
        return jsonify({'error': f'Currency not supported: {to_currency}'}), 400
    except Exception as e:  
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5002)