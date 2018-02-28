# coding:utf8


from flask import Flask
from flask import request
from utils import sqladvisor, inception

import logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)


@app.route('/sql', methods=['POST'])
def sql():
    if request.method == "POST":
        data = request.json
        res = sqladvisor.getResult(data["sql"])
        #logging.warning(res)
        return res


@app.route('/inception', methods=['POST'])
def sql_inception():
    if request.method == "POST":
        data = request.json
        res = inception.get_result(data["sql"])
        return res

if __name__ == "__main__":
    #app.debug = True
    app.run(host='0.0.0.0', port=5000)
