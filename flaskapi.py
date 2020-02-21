# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:21:55 2020

@author: adityaroyal
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
import hdfs_connection
class aipassflask :
        def __init__(self):

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
            return(sanitized)
        @app.route('/homepage/home',methods = ['POST','GET'])
        @cross_origin()
        def project():
            client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
            db = client['test']
            collect=db['homepagecollection']
            val =  request.get_json('project')
            collect.insert_one(val)
            page_sanitized = json.loads(json_util.dumps(val))
            return(page_sanitized)
        @app.route('/connections/new',methods = ['POST','GET'])
        @cross_origin()
        def connections():
            client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
            db = client['test']
            collect=db['connectionscollection']
            val = request.get_json('host')
            collect.insert_one(val)
            #input_json=json.loads(json_util.dumps(val))
            sc=hdfs_connection.someclass(val)
            a= sc.HDFSConnection()
            b=sc.KafkaConnection()
            return({'HDFS':a,'Kafka':b})
        @app.route('/datasource/new',methods = ['POST','GET'])
        @cross_origin()
        def datasource():
                        client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
                        db = client['test']
                        collect=db['datasourcecollection']
                        val = request.get_json('selectDataType')
                        collect.insert_one(val)
                        page_sanitized = json.loads(json_util.dumps(val))
                        return(page_sanitized)
        
        @app.route('/fengg/new',methods = ['POST','GET'])
        @cross_origin()
        def featureeng():
                        client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
                        db = client['test']
                        collect=db['fenggcollection']
                        val = request.get_json('options1.name')
                        collect.insert_one(val)
                        page_sanitized = json.loads(json_util.dumps(val))
                        return(page_sanitized)
                      
                        
if __name__ == '__main__':
        app.run()




