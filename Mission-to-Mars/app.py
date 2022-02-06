from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars
from pymongo import MongoClient

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/scrape")
def scrape():
    mars_dict = scrape_mars.scrape_data()
    mars = mongo.db.mars_db
    mars.insert_one({}, mars_dict)
    return redirect('/', code=302)

@app.route("/")
def index():
    mars = mongo.db.mars_db
    mars_data = mars.find_one()
    return render_template("index.html", data=mars_data)

if __name__ == "__main__":
    app.run()
