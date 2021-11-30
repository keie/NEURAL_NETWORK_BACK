from flask import Flask, request, Response, jsonify, json, send_from_directory, abort
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/test', methods= ['GET'])
def test():
    try:
        return Response(response=json.dumps("works!!"), status=200, mimetype='application/json')
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)