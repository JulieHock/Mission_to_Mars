# Import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#Set up Flask
app=Flask(__name__)

#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"]='mongodb://localhost:2701/mars_app'
mongo=PyMongo(app)

#Set up route for html
@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#Add next route
@app.route("/scrape")
def scrape():
    mars=mongo.db.mars
    mars_data=scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

if __name__=='__main__':
    app.run()