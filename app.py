#! /usr/bin/python3
# -*- coding:utf8 -*-

# @file : mogodb_writer.py
# @desc : Inilitize MongoDB data
# @author: jli3158
# @Reference: https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api

from flask import Flask, url_for, redirect, render_template, request, Response, abort, g, jsonify, session, flash
from flask_restful import reqparse, abort, Api, Resource
import glob
import json
from bing_image_urls import bing_image_urls
from flask_cors import CORS

from pymongo import MongoClient

DATABASE = 'mongodb://localhost:27017/'
PROJECT_NAME = 'vizthebookdatabase'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS=True

DQ_ISSUE_LIST = [
    "Crusaders of New France ...",
    "Origin and development of form and ....",
    "Stories of Georgia 1896",
    "Origin and development of form..",
    "Pioneers of the old south",
    "Ten Thousand Miles with a...",
    "The Forty-niners ..",
    "The Age of invention a chronicle...",
    "The New york and albany post road...",
    "A general history for colleges and high schools",
    "A study of pueblo architecture",
    "Between the lines secret service",
    "Current History Vol. VIII",
    "The government class book designed for the ...",
    "John Marshall and the Constitution",
    "New York Times Current History;",
    "Notable Voyagers from Colombus to..",
    "The Conquest of new france...",
    "The Prairie Traveler...",
    "A little journey to Puerto Rico...",
    "New York Times Current History Vol 2",
    "History of the United STates, Volume 2 (of 6)",
    "Captains of the Civil War A chronicle of hte blue and gray Vol 31",
    "Critical Miscellanies (vol 1 of 3",
    "Great Epochs in American History Vol 1",
    "Holland and the history of the netherlands",
    "Letters from Port Royal Written at the time of the civil war",
    "Stories of Ohio 1897",
    "The American Spirit in Literature",
    "The Canadian Dominion",
    "The land we live in the story of our country",
    "The Negro at work in New York City",
    "The Red Man's Continent",
    "History of the 159th regiment",
    "The life of William Ewart Gladstone",
    "Sinking of the titanic and great sea disasters",
    "The Hispanic Nations of the new world",
    "Prince Henry the Navigator, the hero of..",
    "The Every-day life of abraham Lincoln",
    "The Journals of lewis and clark",
    "The old merchant marine A chronicle...",
    "Ancient man thebeginning of",
    "Daniel Boone taming the wilds",
    "Archeological investigations bureau",
    "Reminiscences of tolstoy",
    "The constitution of the united states a brief study",
    "The Sequel of Appomattox",
    "A study of pueblo pottery",
    "Chaldea from the earliest times",
    "Declaration of independence of the United States of America",
    "Declaration of independence",
    "The Naval History of the United states vol 1 of 2",
    "The Quaker colonies a chronicle of the proprietors of the delaware",
    "The story of geographical discovery how the world",
    "Pioneers of the old southwest",
    "The anti-slavery alphabet",
    "Camps and trails in China a narrative ..."
]

app = Flask(__name__, static_folder="assets", template_folder="templates")
CORS(app)
app.config['DATABASE'] = DATABASE
app.config['PROJECT_NAME'] = PROJECT_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY']="secret-key"
query_limit=' LIMIT 2000'

api = Api(app)

def get_db():
    client = MongoClient("db", 27017)
    db = client["gutenberg"]
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.teardown_request
def teardown_request(exception):
    print("Tear down")

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route("/books")
def books():
    db = g.db
    collection = db["map_dataset_mongo"]
    cursor = collection.find({})

    books = []
    for doc in cursor:
        r = doc
        del r["_id"]
        clean_title = ''.join(e for e in r["title"] if e.isalnum()).lower()

        if not any([''.join(e for e in bad if e.isalnum()).lower() in clean_title for bad in DQ_ISSUE_LIST]):
            books.append(r["title"])
    return {"data": books}

@app.route("/keywords")
def keywords():
    db = g.db
    collection = db["image_cloud_mongo"]
    cursor = collection.find({})

    keywords = []
    for doc in cursor:
        for k in doc["keywords"]:
            if isinstance(k, dict) and not k["keyword"] in keywords:
                keywords.append(k["keyword"])

    cursor.close()
    return {"data": keywords}

@app.route("/streamgraph")
def streamgraph():
    db = g.db
    collection = db["streamgraph_dataset_mongo"]
    title = request.args["title"]
    thing = collection.find_one({"title": title})
    if thing:
        del thing["_id"]
        return thing
    return {"data": []}

@app.route("/graphrel")
def graph_relationship():
    db = g.db
    collection = db["book_rel_info_mongo"]
    title = request.args["title"]
    cursor = collection.find({"source": title})

    records = []
    for doc in cursor:
        r = doc
        del r["_id"]
        records.append(r)
    return {"data": records}

@app.route("/graphkey")
def graph_keywords():
    db = g.db
    collection = db["book_info_mongo"]
    title = request.args["title"]
    cursor = collection.find({"title": title})

    records = []
    for doc in cursor:
        r = doc
        del r["_id"]
        r["fixed"] = True
        records.append(r)
    return {"data": records}

@app.route("/map")
def map_data():
    db = g.db
    collection = db["map_dataset_mongo"]
    title = request.args["title"]

    thing = collection.find_one({"title": title})
    if thing:
        del thing["_id"]
        return thing
    return {"data": []}

@app.route("/image")
def image_cloud():
    db = g.db
    collection = db["image_cloud_mongo"]
    title = request.args["title"]

    thing = collection.find_one({"title": title})
    if thing:
        del thing["_id"]

        keywords = []
        keywords.append({"keyword": "root", "value": None})

        for r in thing["keywords"]:
            record = r
            try:
                record["img"] = glob.glob("assets/img/test/{}.*".format(r["keyword"]))[0]
                keywords.append(record)
            except:
                continue

        return {"data": keywords}
    return {"data": []}


restful_todos = {}

"""
You can try it like this:

# Image Cloud Value
$ curl http://localhost:5000/restful/imageCloud  -d "data={\"keyword\" : \"Lincoln\"}" -X POST
{ "keyword": "Lincoln", "value": 10}
# Image Cloud URL
$ curl http://localhost:5000/restful/imageCloudURLs  -d "data={\"keyword\" : \"Lincoln\"}" -X POST
{ "keyword": "Lincoln", "urls": []}
# book Info
$ curl http://localhost:5000/restful/bookInfo  -d "data={\"name\": \"Book1\"}" -X POST
{ "keyword": "Lincoln", "urls": []}
# bookRelInfo
$ curl http://localhost:5000/restful/bookRelInfo  -d "data={\"source\": \"Book1\"}" -X POST
{"data" :[
      {"source": "Book1", "target": "Book2", "value": 4, "keyword_id": 1},
      {"source": "Book1", "target": "Book2", "value": 5, "keyword_id": 1},
      {"source": "Book1", "target": "Book2", "value": 4, "keyword_id": 3},
      {"source": "Book1", "target": "Book3", "value": 4, "keyword_id": 2},
      {"source": "Book1", "target": "Book3", "value": 4, "keyword_id": 5},
      {"source": "Book1", "target": "Book4", "value": 5, "keyword_id": 4}]}
# streamChart
$ curl http://localhost:5000/restful/streamChart  -d "data={\"book\": \"Book1\"}" -X POST
      { "book": "Book1", "keyword_score": [
        {"decile":1,"Difficult":24,"Uncertain":0,"Challenging":18,"Trying":5},
        {"decile":2,"Difficult":20,"Uncertain":0,"Challenging":16,"Trying":8},
        ...
        }
# map
$ curl http://localhost:5000/restful/map  -d "data={\"keyword\": \"Lincoln\"}" -X POST
"""

parser = reqparse.RequestParser()
parser.add_argument('data', type=str, help='data')

class Restful(Resource):
    def post(self, function):
        print ("function is: ", function)
        args = parser.parse_args()
        print ("args are: ", args)
        mycol = g.db[function]
        data = json.loads(args['data'])
        rtn = {}
        if (function == "imageCloud" or function == "map"):
            rtn = mycol.find_one(data)
            del rtn['_id']
        elif (function == "bookInfo"):
            rtn = mycol.find_one(data)
            del rtn['_id']
        elif (function == "bookRelInfo"):
            temp = []
            for x in  mycol.find(data):
                del x['_id']
                print("x is", x)
                temp.append(str(x))
            rtn["data"] = temp
        elif (function == "streamChart"):
            rtn = mycol.find_one(data)
            del rtn['_id']
        elif (function == "imageCloudURLs"):
            rtn["data"] = bing_image_urls(data["keyword"], limit=5)
        else:
            rtn["data"] = "test"
        return str(rtn)

api.add_resource(Restful, '/restful/<function>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
