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
from flask import jsonify
# import feda_auto
# import featurenames
# import KafkaTopic
# import hdfs_connection
# import featurenames
# import dmp1
import glob
class aipassflask :
        def __init__(self):

            pass
        @app.route('/user/login',methods = ['POST','GET'])
        @cross_origin()
        def login():
            client = pymongo.MongoClient("mongodb+srv://karun:test123@cluster0-c1nc9.mongodb.net/test?retryWrites=true&w=majority")
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
            client = pymongo.MongoClient("mongodb+srv://karun:test123@cluster0-c1nc9.mongodb.net/test?retryWrites=true&w=majority")
            db = client['test']
            collect=db['connectionscollection']
            val = request.get_json('host')
            collect.insert_one(val)
            page_sanitized=json.loads(json_util.dumps(val))
#             sc=hdfs_connection.Connection(val)
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
            client = pymongo.MongoClient("mongodb+srv://karun:test123@cluster0-c1nc9.mongodb.net/test?retryWrites=true&w=majority")
            db = client['test']
            collect=db['connectionscollection']
            cursor = db.connectionscollection.find()
            response = []
            for document in cursor:
                document['_id'] = str(document['_id'])
                response.append(document)
            return json.dumps(response)

        @app.route('/delete',methods = ['DELETE'])
        @cross_origin()
        def delete():
            client = pymongo.MongoClient("mongodb+srv://karun:test123@cluster0-c1nc9.mongodb.net/test?retryWrites=true&w=majority")
            db = client['test']
            collect=db['connectionscollection']
            val = request.get_json('_id')
            cursor = db.connectionscollection.remove(val)
            response = []
            return json.dumps(response)
#             a=[]
#             for document in cursor:
#                 a.append(document)
#                 #val=session['myvar']
#             val=sorted(a,key= lambda x:x['_id'])[-1]
#             cols=val['cols']
#             return({cursor})
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
#                cursor = db.dmpfolderscollection.find({})
#                for document in cursor:
#                    a.append(document)
#                valnc=sorted(a,key= lambda x:x['_id'])[-1]
#                featurepath=valnc.get('featurepath')
#                do=glob(directory)
#                childdirectory=[x.split('\\')[-1] for x in do]
#                file=[]
#                di={}
#                for x in childdirectory:
#                    do=directory[:-1]+x+'\*'
#                    do=glob(do)
#                    di[str(x)]=[x.split('\\')[-1] for x in do]
#                di=[{'folder':{'id1':{'name':'file1'},'id2':{'name':'file2'}},'folder2':{'id3':{'name':'file21'},'id4':{'name':'file22'}}}]
               di= "[{'chicago_taxi': {'id1': {'name': 'chicago_taxi_2020-03-04_11-33-26.csv'}, 'id2': {'name': 'chicago_taxi_2020-03-04_11-47-49.csv'}, 'id3': {'name': 'chicago_taxi_2020-03-04_11-50-46.csv'}, 'id4': {'name': 'chicago_taxi_2020-03-04_11-56-20.csv'}, 'id5': {'name': 'chicago_taxi_2020-03-04_12-00-01.csv'}, 'id6': {'name': 'chicago_taxi_2020-03-04_12-01-27.csv'}, 'id7': {'name': 'chicago_taxi_2020-03-04_12-02-54.csv'}, 'id8': {'name': 'chicago_taxi_2020-03-04_12-03-13.csv'}, 'id9': {'name': 'chicago_taxi_2020-03-04_12-07-33.csv'}, 'id10': {'name': 'chicago_taxi_2020-03-04_12-12-03.csv'}, 'id11': {'name': 'chicago_taxi_2020-03-04_12-19-08.csv'}, 'id12': {'name': 'chicago_taxi_2020-03-04_12-24-12.csv'}}, 'testdd': {'id13': {'name': 'featurestorefiledd_2020-03-04_10-39-11.csv'}, 'id14': {'name': 'testdd_2020-03-04_10-47-19.csv'}}, 'testfile_demo_march4': {'id15': {'name': 'featurestorefile_demo_march4_2020-03-04_08-20-13.csv'}}, 'testqq': {'id16': {'name': 'qq_2020-03-04_09-06-26.csv'}}}]"
               page_sanitized=jsonify(di)
               return (page_sanitized)
        @app.route("/dmpreaddata",methods=['POST'])
        @cross_origin()
        def dmpreaddata():
#                 input1=json.loads(request.data)
#                 folder=input1.get('folder')
#                 file=input1.get('file')
#                 client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
#                 db = client['test']
#                 a=[]
#                 cursor = db.datasourcecollection.find({})
#                 for document in cursor:
#                     a.append(document)
#                 #val=session['myvar']
#                 vald=sorted(a,key= lambda x:x['_id'])[-1]
#                 path=vald.get('feature_Store_Path')
#                 db = client['test']
#                 a=[]
#                 cursor = db.connectionscollection.find({})
#                 for document in cursor:
#                     a.append(document)
#                 #val=session['myvar']
#                 valc=sorted(a,key= lambda x:x['_id'])[-1]
#                 cols=featurenames.dataconn(valc.get('host'),valc.get('port'),valc.get('user'),path,folder,file)[1].tolist()
                cols=['col1','col2','col3','col4']
                return({'cols':cols})
        @app.route('/dmpfeatures',methods = ['POST','GET'])
        @cross_origin()
        def dmpfeatures():
#                client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
#                db = client['test']
#                collect=db['dmpfeaturescollection']
#                val_port=request.json
#                page_sanitized=json.loads(json_util.dumps(val_port))
#                client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
#                db = client['test']
#                a=[]
#                cursor = db.datasourcecollection.find({})
#                for document in cursor:
#                     a.append(document)
#                #val=session['myvar']
#                vald=sorted(a,key= lambda x:x['_id'])[-1]
#                path=vald.get('feature_Store_Path')
#                folder=vald.get('data_Store_Folder')
#                file=vald.get('data_Store_Filename')
#                db = client['test']
#                a=[]
#                cursor = db.connectionscollection.find({})
#                for document in cursor:
#                     a.append(document)
#                #val=session['myvar']
#                valc=sorted(a,key= lambda x:x['_id'])[-1]
#                df=featurenames.dataconn(valc.get('host'),valc.get('port'),valc.get('user'),path,folder,file)[0]
#                df=featurenames.dataconn(valc.get('host'),valc.get('port'),valc.get('user'),path,folder,file)[0]
#                dmp1.api1(df,val_port)
#                collect.insert_one(val_port)
               models={'LinearRegression()':['Max Features','criterion','Max Depth'], 'SVR()':['d','e','v'], 'DecisionTreeRegressor()': [], 'KNeighborsRegressor()': [], 'LinearSVR()': [], 'Ridge()': []}
               return ({'models':models})
        @app.route('/dmpselectmodels',methods = ['POST','GET'])
        @cross_origin()
        def dmpselectmodels():
#                client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
#                db = client['test']
#                cursor = db.initialmodelcollection.find({})
#                a=[]
#                for document in cursor:
#                     a.append(document)
#                 #val=session['myvar']
#                valc=sorted(a,key= lambda x:x['_id'])[-1]
#                selected=valc.get('models')
#                top3=dmp1.api22(selected)
               models = [{'name':'Mod11','value':'90%'},{'name':'Mod12','value':'79%'},{'name':'Mod13','value':'87%'}]
               return ({'models':models})
        @app.route('/dmprecommend',methods = ['POST','GET'])
        @cross_origin()
        def dmprecommend():
        #                client = pymongo.MongoClient("mongodb+srv://aditya:lokam001@cluster0-dikue.mongodb.net/test?retryWrites=true&w=majority")
        #                db = client['test']
        #                cursor = db.initialmodelcollection.find({})
        #                a=[]
        #                for document in cursor:
        #                     a.append(document)
        #                 #val=session['myvar']
        #                valc=sorted(a,key= lambda x:x['_id'])[-1]
        #                selected=valc.get('models')
        #                top3=dmp1.api22(selected)
                models = ['https://www.google.com']
                return ({'models':models})
if __name__ == '__main__':
        app.run()


