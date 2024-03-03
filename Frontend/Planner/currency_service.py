# pip install exchangeratesapi    -> If not done yet

from flask import Flask, request, jsonify
from flask_cors import CORS
import exchangeratesapi
import requests

app = Flask(__name__)
CORS(app)

api_key = ""  # Get this from https://exchangeratesapi.io/ , create an account there. 250 Free Calls. 
@app.route('/exchange', methods=['GET'])
def get_exchange_rate():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    # amount = float(request.args.get('amount', 1.0)) 

    try:

        response = requests.get('http://api.exchangeratesapi.io/v1/latest?access_key=b03e781c96bd6d8f723f9845a764a569&symbols=SGD,AFN')
        response = response.json()
        print(response['success'])
        if response['success']:
            print(from_currency,to_currency)
            fromCurr = response['rates'][from_currency]
            toCurr = response['rates'][to_currency]
            result = (1/fromCurr)/(1/toCurr)
            return jsonify({
                'from': from_currency,
                'to': to_currency,
                # 'amount': amount,
                # 'rate': rate, 
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