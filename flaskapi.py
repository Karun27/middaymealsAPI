# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:21:55 2020

@author: adityaroyal
"""

import pymongo
from flask import Flask, request,url_for,render_template,session,redirect
app = Flask(__name__)
app.secret_key = "super secret key"
import pymongo
from flask_cors import CORS, cross_origin
CORS(app)
from bson import json_util, ObjectId
import json
import urllib
#import KafkaTopic
#import hdfs_connection
import featurenames
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
            return(page_sanitized)
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
            page_sanitized=json.loads(json_util.dumps(val))
            sc=hdfs_connection.Connection(val)
            a= 'True'
            b='False'
            session['my_var']=page_sanitized

            

            return(page_sanitized)
  

            
        @app.route('/datasource/new',methods = ['POST','GET'])
        @cross_origin()
        def datasource():
                        #connections()
            client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")

            db = client['test']
            a=[]
            cursor = db.connectionscollection.find({})
            for document in cursor:
                a.append(document)
            #val=session['myvar']
            val=sorted(a,key= lambda x:x['_id'])[-1]
            val_port = request.get_json('topic_Name')
            #session['my_var2'] = val_port
            
            page_sanitized= json.loads(json_util.dumps(val_port))
            sc=KafkaTopic.KafkaTopic(val,page_sanitized)
            sc.topic()
            sc.producer()
            sc.consumer()  
            host=val.get('host')
            user=val.get('user')
            port=val.get('port')
            path=page_sanitized.get('path')
            file=page_sanitized.get('file')
            cols=fedanew.dataconn(host,user,port,path,file)[1]
            val_port['cols']=cols
            db = client['test']
            collect=db['datasourcecollection']
            collect.insert_one(val_port)
            
            return(cols)
        @app.route('/features',methods = ['POST','GET'])
        @cross_origin()
        def features():
            client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
            db = client['test']
            cursor = db.datasourcecollection.find({})
            a=[]
            for document in cursor:
                a.append(document)
                #val=session['myvar']
            val=sorted(a,key= lambda x:x['_id'])[-1]
            cols=val['cols']
            return({'cols':cols})
        @app.route('/feda',methods = ['POST','GET'])
        @cross_origin()
        def feda():
            client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")

            db = client['test']
            a=[]
            cursor = db.connectionscollection.find({})
            for document in cursor:
                a.append(document)
                #val=session['myvar']
            a=sorted(a,key= lambda x:x['_id'])[-1]
            key=[]
            key_value=[]
            for i in range(len(a['val'])):
                print(a['val'])
                key.append(a['val'][i]['Feature_Engeneering_option'])
                value=[]
                for j in range(len(a['val'][i]['Features'])):
                    value.append(a['val'][i]['Features'][j]['name'])
                key_value.append(value)
            val={}
            for i,j in zip(key,key_value):
                val[i]=j
            valnew=request.json
            page_sanitized= json.loads(json_util.dumps(valnew))
            featurenames.final(page_sanitized,val.get('host'),val.get('user'),val.get('port'),val.get('path'),val.get('file'),val.get('folder'),val.get('featurepath'),val.get('featurefile'),val.get('featurefolder'))
            return page_sanitized
        @app.route('/recommend',methods = ['POST','GET'])
        @cross_origin()
        def recommend():
            client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")

            db = client['test']
            a=[]
            cursor = db.connectionscollection.find({})
            for document in cursor:
                a.append(document)
                #val=session['myvar']
            a=sorted(a,key= lambda x:x['_id'])[-1]
            key=[]
            key_value=[]
            for i in range(len(a['val'])):
                print(a['val'])
                key.append(a['val'][i]['Feature_Engeneering_option'])
                value=[]
                for j in range(len(a['val'][i]['Features'])):
                    value.append(a['val'][i]['Features'][j]['name'])
                key_value.append(value)
            val={}
            for i,j in zip(key,key_value):
                val[i]=j
            valnew=request.json
            valnew=valnew['cols']
            page_sanitized= json.loads(json_util.dumps(valnew))
            cursor = db.datasourcecollection.find({})
            a=[]
            for document in cursor:
                a.append(document)
                #val=session['myvar']
            vald=sorted(a,key= lambda x:x['_id'])[-1]
            featurenames.final(page_sanitized,val.get('host'),val.get('user'),val.get('port'),vald.get('data_Path'),vald.get('data_File'),vald.get('data_Folder'),vald.get('feature_Path'),vald.get('feature_Name'),vald.get('feature_Folder'))
            return page_sanitized
            
#[{"Feature_Engeneering_option":"Bucketing","Features":[{"name":"acds"},{"name":"asd"}]},{"Feature_Engeneering_option":"Handle missing data","Features":[{"name":"dsfsc"},{"name":"asd"}]},{"Feature_Engeneering_option":"Drop duplicate data","Features":[{"name":"asd"}]}]           
                        
if __name__ == '__main__':
        app.run()




