from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# Note that this is using the path to the mars_app db we set up
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define app routes so that users can navigate to our pages
# index.html is the default HTML file that we'll use to display the content we've scraped
@app.route("/")
def index():
   # Use pymongo to find the mars collection in our database
   mars = mongo.db.mars.find_one()
   # tells Flask to return an HTML template using an index.html file
   return render_template("index.html", mars=mars)

# This indicates that the path will run the function 'scrape' defined below

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   # call the scraping.py file to scrape the data
   mars_data = scraping.scrape_all()
   # update the database with the scraped data
   # function format .update(query_parameter, data, options)
   # note that the empty brackets indicate an empty JSON object
   # 'upsert' tells mongo to create a new document if one doesn't already exist
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# tell it to run!
if __name__ == "__main__":
   app.run()



