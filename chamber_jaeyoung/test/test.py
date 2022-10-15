import datetime
from flask import Flask, Response
from flask_cors import cross_origin

app = Flask(__name__)


@app.route('/time_feed')
@cross_origin(origin='*')
def time_feed():
    def generate():
        yield datetime.datetime.now().strftime("%Y.%m.%d|%H:%M:%S")  # return also will work
    return Response(generate(), mimetype='text')

app.run(host="0.0.0.0", threaded=True)