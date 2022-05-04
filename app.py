# Import dependencies
# use Flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for
# use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
# to use the scraping code, we will convert from Jupyter notebook to Python.
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#tells Python that our app will connect to Mongo using a URI, a uniform resource 
# identifier similar to a URL.

# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, 
# using a database named "mars_app".
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

# next function will set up our scraping route. This route will be the "button" of the web application, 
# the one that will scrape updated data when we tell it to from the homepage of our web app. It'll be 
# tied to a button that will run the code when it's clicked.

# defines the route that Flask will be using,“/scrape”, will run the function that we create just beneath it.
@app.route('/scrape')
# next lines allow us to access the database, scrape new data using our scraping.py script, update the database, 
# and return a message when successful. Let's break it down.
def scrape():
    # assign a new variable that points to our Mongo database
    mars = mongo.db.mars
    # created a new variable to hold the newly scraped data, we're referencing the scrape_all function in 
    # the scraping.py file exported from Jupyter Notebook.
    mars_data = scraping.scrape_all()
    # Now that we've gathered new data, we need to update the database using .update_one()
    mars.update_one({}, {'$set':mars_data}, upsert=True)
    # we will add a redirect after successfully scraping the data, This will navigate our page back to 
    # '/' where we can see the updated content.
    return redirect('/', code=302)
# final bit of code we need for Flask is to tell it to run
if __name__ == '__main__':
    app.run()