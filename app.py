# import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

# import the scraping.py tool we created
import scraping

# set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" #tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
mongo = PyMongo(app)

# define routes
# This route, @app.route("/"), tells Flask what to display when we're looking at the home page, 
# index.html (index.html is the default HTML file that we'll use to display the content we've scraped). 
# This means that when we visit our web app's HTML page, we will see the home page.
@app.route("/")
def index():
   mars = mongo.db.mars.find_one() #uses PyMongo to find the "mars" collection in our database, assign that path to themars variable for use later
   return render_template("index.html", mars=mars) #tells Flask to return an HTML template using an index.html file, , mars=mars) tells Python to use the "mars" collection in MongoDB

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars #assign a new variable that points to our Mongo database: mars = mongo.db.mars
   mars_data = scraping.scrape_all() #created a new variable to hold the newly scraped data: mars_data = scraping.scrape_all(). In this line, we're referencing the scrape_all function in the scraping.py file
   mars.update_one({}, {"$set":mars_data}, upsert=True) #update the database using .update_one(). Syntx: .update_one(query_parameter, {"$set": data}, options)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()

