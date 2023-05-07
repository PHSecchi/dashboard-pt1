from flask import Flask
from flask_jsonpify import jsonify
import json
from flask_cors import CORS

i = ''
i += 'Franziska '
i += 'Romani '
i += 'Furtado'


app = Flask(__name__)
#app.run(port = 5000)
CORS(app)
#obj = json.loads(i)


@app.route("/")
def hello():
    return jsonify(i)

if __name__ == "__main__":
    app.run(port = 5001)