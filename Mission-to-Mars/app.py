from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars
from pymongo import MongoClient

app = Flask(__name__)

#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)
client = MongoClient("localhost", 27017)
db = client["mars_db"]
collection = db["collections"]

@app.route("/scrape")
def scrape():
    mars_dict = scrape_mars.scrape_data()
    collection.insert_one(mars_dict)
    #client.close()
    #mars = mongo.db.mars_db
    #mars.update({}, mars_dict, upsert=True)
    return redirect('/', code=302)

@app.route("/")
def index():
    #mars_data = mongo.db.mars.find_one()
    mars_data = collection.find_one()
    return render_template("index.html", data=mars_data)

if __name__ == "__main__":
    app.run()
