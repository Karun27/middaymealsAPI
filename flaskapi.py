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
import feda_auto
import featurenames
import KafkaTopic
import hdfs_connection
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
            path=page_sanitized.get('data_Store_Path')
            folder=page_sanitized.get('data_Store_Folder')
            file=page_sanitized.get('data_Store_Filename')
            cols=featurenames.dataconn(host,user,port,path,folder,file)[1].tolist()
            val_port['cols']=cols
            db = client['test']
            collect=db['datasourcecollection']
            collect.insert_one(val_port)
            
            return(page_sanitized)
        @app.route('/features',methods = ['POST','GET'])
        @cross_origin()
        def features():
            client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
            db = client['test']
            collect=db['datasourcecollection']
            cursor = db.datasourcecollection.find({})
            a=[]
            for document in cursor:
                a.append(document)
                #val=session['myvar']
            val=sorted(a,key= lambda x:x['_id'])[-1]
            cols=val['cols']
            return({'cols':cols})
        @app.route('/submit',methods = ['POST','GET'])
        @cross_origin()
        def submit():
           client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
           db = client['test']
           collect=db['columnscollection']
           val_port=request.json
           value=[k['name'] for k in val_port]
           di={}
           di['newcols']=value
           collect.insert_one(di)
           return ({'cols':value})
        @app.route('/feda',methods = ['POST','GET'])
        @cross_origin()
        def feda():
        
            a=request.json
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
            client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")

            db = client['test']
            a=[]
            cursor = db.connectionscollection.find({})
            for document in cursor:
                a.append(document)
            #val=session['myvar']
            valc=sorted(a,key= lambda x:x['_id'])[-1]
            a=[]
            cursor = db.datasourcecollection.find({})
            for document in cursor:
                a.append(document)
            #val=session['myvar']
            vald=sorted(a,key= lambda x:x['_id'])[-1]
            a=[]
            featurepath=vald.get('featurepath')
            collect=db['dmpfolderscollection']
            di={}
            di['featurepath']=featurepath
            collect.insert_one(di)
            featurenames.final(val,valc.get('host'),valc.get('user'),valc.get('port'),vald.get('path'),vald.get('file'),vald.get('folder'),vald.get('featurepath'),vald.get('featurefile'),vald.get('featurefolder'))
            return page_sanitized
        @app.route('/recommend',methods = ['POST','GET'])
        @cross_origin()
        def recommend():
            print('success5')
            client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")

            db = client['test']
            a=[]
            cursor = db.connectionscollection.find({})
            for document in cursor:
                a.append(document)
            #val=session['myvar']
            valc=sorted(a,key= lambda x:x['_id'])[-1]
            a=[]
            cursor = db.datasourcecollection.find({})
            for document in cursor:
                a.append(document)
            #val=session['myvar']
            vald=sorted(a,key= lambda x:x['_id'])[-1]
            a=[]
            cursor = db.columnscollection.find({})
            for document in cursor:
                a.append(document)
            valnc=sorted(a,key= lambda x:x['_id'])[-1]

            print('success6')
            print(vald.get('newcols'),valc.get('host'),valc.get('port'),valc.get('user'),vald.get('data_Store_Path'),vald.get('data_Store_Folder'),vald.get('data_Store_Filename'),vald.get('feature_Store_Path'),vald.get('feature_Store_Folder'),vald.get('feature_Store_Filename'))
            df=feda_auto.main(valnc.get('cols').tolist(),valc.get('host'),valc.get('port'),valc.get('user'),vald.get('data_Store_Path'),vald.get('data_Store_Folder'),vald.get('data_Store_Filename'),vald.get('feature_Store_Path'),vald.get('feature_Store_Folder'),vald.get('feature_Store_Filename'))    
            return (df)
            #self, column_list, host, webhdfs_default_port, user_ubuntu, datastore_path, datastore_foldername, datastore_filename, featurestore_path, featurestore_foldername, featurestore_filename
#[{"Feature_Engeneering_option":"Bucketing","Features":[{"name":"acds"},{"name":"asd"}]},{"Feature_Engeneering_option":"Handle missing data","Features":[{"name":"dsfsc"},{"name":"asd"}]},{"Feature_Engeneering_option":"Drop duplicate data","Features":[{"name":"asd"}]}]           
        @app.route('/dmpfolders',methods = ['POST','GET'])
        @cross_origin()
        def dmpfolders():
               client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
               db = client['test']
               a=[]
               cursor = db.dmpfolderscollection.find({})
               for document in cursor:
                   a.append(document)
               valnc=sorted(a,key= lambda x:x['_id'])[-1]
               featurepath=valnc.get('featurepath')
               do=glob(directory)
               childdirectory=[x.split('\\')[-1] for x in do]
               file=[]
               di={}
               for x in childdirectory:
                   do=directory[:-1]+x+'\*'
                   do=glob(do)
                   di[str(x)]=[x.split('\\')[-1] for x in do]
               return (di)
        @app.route("/dmpreaddata",methods=['POST'])
        @cross_origin()
        def dmpreaddata():
                input1=json.loads(request.data)
                folder=input1.get('folder')
                file=input1.get('file')  
                client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
                db = client['test']
                a=[]
                cursor = db.datasourcecollection.find({})
                for document in cursor:
                    a.append(document)
                #val=session['myvar']
                vald=sorted(a,key= lambda x:x['_id'])[-1]
                path=vald.get('featurepath')
                db = client['test']
                a=[]
                cursor = db.connectionscollection.find({})
                for document in cursor:
                    a.append(document)
                #val=session['myvar']
                valc=sorted(a,key= lambda x:x['_id'])[-1]
                cols=featurenames.dataconn(valc.get('host'),valc.get('port'),valc.get('user'),path,folder,file)[1].tolist()   
                return({'cols':cols})
        @app.route('/dmpfeatures',methods = ['POST','GET'])
        @cross_origin()
        def dmpfeatures():
               client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
               db = client['test']
               collect=db['dmpfeaturescollection']
               val_port=request.json
               page_sanitized=json.loads(json_util.dumps(val_port))
               collect.insert_one(val_port)
               return (page_sanitized)
        @app.route('/dmpmodels',methods = ['POST','GET'])
        @cross_origin()
        def dmpmodels():
               client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
               db = client['test']
               collect=db['dmpfeaturescollection']
               val_port=request.json
               models=dmp.main(val_port)
               collect=db['initialmodelcollection']
               collect.insert_one({'models':models})
               return ({'models':models})
        @app.route('/dmpselectmodels',methods = ['POST','GET'])
        @cross_origin()
        def dmpselectmodels():
               client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
               db = client['test']
               cursor = db.initialmodelcollection.find({})
               for document in cursor:
                    a.append(document)
                #val=session['myvar']
               valc=sorted(a,key= lambda x:x['_id'])[-1]
               selected=valc.get('models')
               top3=dmp.main2(selected)
               return ({'top3':top3})
if __name__ == '__main__':
        app.run()




