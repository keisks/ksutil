import os
import sys
import logging
import logging.handlers
from flask import Flask, jsonify, render_template, request
from scripts.answer import get_answer
from scripts.cat_facts import get_cat_facts

app = Flask(__name__)

handler = logging.handlers.RotatingFileHandler("my_log.log", "a+", maxBytes=3000, backupCount=5)
handler.setLevel(logging.INFO) 
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
app.logger.addHandler(handler)

 
# default page 
@app.route("/", methods=['GET', 'POST'])
def run_index(): # this function name can be arbitrary.
    if request.method == "POST":
        food = request.form["food_submitted"]
        drink = request.form["drink_submitted"]
        app.logger.info("query:{}".format(food))
        return "Oh, your favorite food is " + get_answer(food) + "and favorite drink is " + get_answer(drink)
    return render_template("index.html", header="Minimal demo for NLP.")

# run script in backend
@app.route("/scripts/cat_facts", methods=['GET', 'POST'])
def run_cat_facts(): # this function name can be arbitrary.
    if request.method == "GET":
        resp = get_cat_facts()
        text = resp["text"]
        logging.info("cat facts:\t {}".format(text))
        return jsonify(result = text)
    return render_template("index.html", header="HEADER!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

