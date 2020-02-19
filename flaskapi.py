# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import pymongo
from flask import Flask, request,url_for,render_template
app = Flask(__name__)
import pymongo
from flask_cors import CORS, cross_origin
CORS(app)
from bson import json_util, ObjectId
import json
import urllib
class aipassflask :
        def _init_(self):

        pass
        @app.route('/user/login',methods = ['POST','GET'])
        @cross_origin()
        def login():
                client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
                db = client['test']
                collect=db['logincollection']
                val = request.get_json('email')
                collect.insert_one(val)
                page_sanitized = json.loads(json_util.dumps(val))
                return(page_sanitized)
        @app.route('/user/register',methods = ['POST','GET'])
        @cross_origin()
        def register():
                client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
                db = client['test']
                collect=db['registercollection']
                val=request.get_json('First_Name')
                collect.insert_one(val)
                page_sanitized = json.loads(json_util.dumps(val))
                return(page_sanitized)
        @app.route('/homepage/home',methods = ['POST','GET'])
        @cross_origin()
        def project():
                client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
                db = client['test']
                collect=db['homepagecollection']
                val = request.get_json('project')
                collect.insert_one(val)
                page_sanitized = json.loads(json_util.dumps(val))
                return(page_sanitized)
        @app.route('/connectionsnew',methods = ['POST','GET'])
        @cross_origin()
        def project():
                client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
                db = client['test']
                collect=db['connectionscollection']
                val = request.get_json('host')
                collect.insert_one(val)
                page_sanitized = json.loads(json_util.dumps(val))
                return(page_sanitized)
        @app.route('/datasourcenew',methods = ['POST','GET'])
        @cross_origin()
        def project():
                client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
                db = client['test']
                collect=db['datasourceconnection']
                val = request.get_json('selectDataType')
                collect.insert_one(val)
                page_sanitized = json.loads(json_util.dumps(val))
                return(page_sanitized)

if _name_ == '__main__':
app.run()
