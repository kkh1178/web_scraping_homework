from flask import Flask
from flask import render_template
import mission_to_mars
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_database"
mongo = PyMongo(app)


@app.route("/")
def index():
    # mars_data = mission_to_mars.scrape()
    # read the mongo database for the mars data
    mars_data = mongo.db.martian.find_one()
    print(mars_data)
    return render_template("index2.html", mars_data=mars_data)

@app.route("/scrape")
def get_data():
    mars_data = mission_to_mars.scrape()
    print(mars_data)
    mongo.db.martian.find_one_and_replace({}, mars_data)
    # store in mongo
    return "scraped some data"

@app.route("/test")
def test():
    data = {"news": "This is some news", "weather": "hot"}

    #@TODO: Try to save data to a mongo database
    # conn = 'mongodb://localhost:27017'
    # client = mongo.MongoClient(conn)

    # db = client.mars_database

    # martian  = db.martian_data.find()
    martian = mongo.db.martian.find_one_and_replace({}, data)
    print(martian)
    # martian.update(data) 
    # print(mongo.db.martian.find({}))


    return "test"

if __name__ == "__main__":
    app.run(debug=True)