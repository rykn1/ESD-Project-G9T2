# pip install exchangeratesapi    -> If not done yet

from flask import Flask, request, jsonify
from flask_cors import CORS
import exchangeratesapi

app = Flask(__name__)
CORS(app)

api_key = ""  # Get this from https://exchangeratesapi.io/ , create an account there. 250 Free Calls. 

@app.route('/exchange', methods=['GET'])
def get_exchange_rate():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    amount = float(request.args.get('amount', 1.0)) 

    try:
        response = exchangeratesapi.get_json(
            'https://api.exchangeratesapi.io/v1/convert?access_key=${api_key}&from=${from_currency}&to=${to_currency}&amount=${amount}'
            # params={
            #     'access_key': api_key,
            #     'from': from_currency,
            #     'to': to_currency,
            #     'amount': amount
            # }
        )

        if response['success']:
            rate = response['info']['rate']
            result = response['result']
            return jsonify({
                'from': from_currency,
                'to': to_currency,
                'amount': amount,
                'rate': rate, 
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