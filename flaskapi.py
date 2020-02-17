# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pymongo
from flask import Flask, request,url_for,render_template
app = Flask(__name__)
import pymongo

import urllib 
class aipassflask :
        def __init__(self):
            
            pass
        @app.route('/user/login',methods = ['POST','GET'])
        def login():
            client = pymongo.MongoClient("mongodb+srv://"+urllib.parse.quote("aditya")+':'+urllib.parse.quote("lokam001")+"@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
            db = client['test']
            collect=db['logincollection']
            username = request.form['username']
            password=request.form['password']
            doc={'username':username,
                 'password':password
                }
            collect.insert_one(doc)
            return('success')
        @app.route('/user/register',methods = ['POST','GET'])
        def register():
            client = pymongo.MongoClient("mongodb+srv://"+urllib.parse.quote("aditya")+':'+urllib.parse.quote("lokam001")+"@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
            db = client['test']
            collect=db['registercollection']
            First_Name=request.form['First_Name']
            Last_Name=request.form['Last_Name']
            Email=request.form['Email']
            U=request.form['U']
            Password=request.form['Password']
            doc={'First_Name':First_Name,
                      'Last_Name':Last_Name,
                      'Email':Email,
                      'U':U,
                      'Password':Password
                }
            
            collect.insert_one(doc)
            return('success')
        @app.route('/homepage/home',methods = ['POST','GET'])
        def project():
            client = pymongo.MongoClient("mongodb+srv://"+urllib.parse.quote("aditya")+':'+urllib.parse.quote("lokam001")+"@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
            db = client['test']
            collect=db['registercollection']
            project =  request.form['Project Name']
            owner= request.form['Owner']
            description = request.form['Description']
            doc={'project':project,
                 'owner':owner,
                 'Description':description
                }
            collect.insert_one(doc)
            return('success')
if __name__ == '__main__':
    app.run()
    

                
        