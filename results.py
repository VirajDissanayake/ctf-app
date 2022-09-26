import requests
from requests_aws4auth import AWS4Auth
import boto3
import json
from flask import session
import application
import os
import datetime

region = 'us-east-1'
service = 'es'
host = os.environ['HOST_URL']

def get_result():

    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                       region, service, session_token=credentials.token)

    url = host + 'ctf/_search?size=400'

    headers = {"Content-Type": "application/json"}

    query = json.dumps({
        "query": {
            "match_all": {}
        },
        "sort": [
            {"grpscore": "desc"},
            {"grouptime": "asc"},
            {"grouplvlcount": "desc"}
        ]
    })
    try:
        r = requests.get(url, auth=awsauth,
                         data=query, headers=headers).json()
        
        results = {}
        res1 = []
        i = 0
        myscore = 0
        lcount = 0
        myrank = 0
        mygrpscore = 0
        mygrplevelcount = 0
        mygrouptime = 0
        timetaken = ""
        for item in r["hits"]["hits"]:
           
            if session["username"] ==  item["_source"]["username"]:
                results["user"] = item["_source"]["username"]
                results["myctfgroup"] = item["_source"]["ctfgroup"]
                mygrpscore = int(item["_source"]["grpscore"])
                mygrplevelcount = item["_source"]["grouplvlcount"]
                mygrouptime = str(datetime.timedelta(seconds=item["_source"]["grouptime"]))
                myscore = int(item["_source"]["totalscore"])
                lcount = item["_source"]["completecount"]
                timetaken = str(datetime.timedelta(seconds=item["_source"]["totaltime"]))
                myrank = i+1
            else:
                results["user"] = item["_source"]["username"][0:3] + "####"
            results["score"] = int(item["_source"]["totalscore"])
            results["grpscore"] = int(item["_source"]["grpscore"])
            results["ctfgroup"] = item["_source"]["ctfgroup"]
            results["grouptime"] = str(datetime.timedelta(seconds=item["_source"]["grouptime"]))
            results["totaltime"] = str(datetime.timedelta(seconds=item["_source"]["totaltime"]))
            results["completelevelcount"] = item["_source"]["completecount"]
            results["grplevelcount"] = item["_source"]["grouplvlcount"]
            res1.append(results.copy())
            i += 1

        return res1, myscore, lcount, myrank, timetaken, mygrpscore, mygrplevelcount, mygrouptime
    except requests.exceptions.RequestException as e:
        return application.wentwrong(e)

def get_result_all():

    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                       region, service, session_token=credentials.token)

    url = host + 'ctf/_search?size=40'

    headers = {"Content-Type": "application/json"}

    query = json.dumps({

        "query": {
            "match_all": {}
        },
        "sort": [
            {"grpscore": "desc"},
            {"grouptime": "asc"},
            {"grouplvlcount": "desc"}
        ]

    })
    try:
        r = requests.get(url, auth=awsauth,
                         data=query, headers=headers).json()
        
        results = {}
        res1 = []
        i = 0
        myscore = 0
        lcount = 0
        myrank = 0
        for item in r["hits"]["hits"]:
            results["user"] = item["_source"]["username"]
            results["grpscore"] = int(item["_source"]["grpscore"])
            results["grouptime"] = str(datetime.timedelta(seconds=item["_source"]["grouptime"]))
            results["ctfgroup"] = item["_source"]["ctfgroup"]
            myscore = int(item["_source"]["totalscore"])
            lcount = item["_source"]["completecount"]
            results["email"] = item["_source"]["email"]
            try:
                results["lastsub"] = item["_source"]["lastsubmission"]
            except KeyError as e:
                results["lastsub"] = ""
            except IndexError as e:
                results["lastsub"] = ""
            myrank = i+1
            results["score"] = int(item["_source"]["totalscore"])
            results["totaltime"] = str(datetime.timedelta(seconds=item["_source"]["totaltime"]))
            results["completelevelcount"] = item["_source"]["completecount"]
            results["grplevelcount"] = item["_source"]["grouplvlcount"]
            res1.append(results.copy())
            i += 1
        return res1, myscore, lcount, myrank
    except requests.exceptions.RequestException as e:
        print(e)
        return e

def get_group_score(group):
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                       region, service, session_token=credentials.token)
    url = host + 'ctf/_search'

    headers = {"Content-Type": "application/json"}

    query = json.dumps({

        "query": {
            "term": {
                "ctfgroup": group
            }
        }
    })
    try:
        r = requests.get(url, auth=awsauth,
                         data=query, headers=headers).json()
        return(r["hits"]["hits"])
    except requests.exceptions.RequestException as e:
        print(e)
        return e

def get_level_stat(level, group):
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                       region, service, session_token=credentials.token)

    url = host + 'ctf/_search'

    headers = {"Content-Type": "application/json"}

    query = json.dumps({

        "query": {
            "bool": {
                "must": [
                    {
                        "term": {"ctfgroup": group}
                    },
                    {
                        "term": {level: "solved"}
                    }
                ]
            }
        }
    })
    try:
        r = requests.get(url, auth=awsauth,
                         data=query, headers=headers).json()
        print(r["hits"]["hits"])
        for n in r["hits"]["hits"]:
            if n["_source"]["username"] == session["username"]:
                print("you")
                return("You")
            else:
                print(n["_source"]["username"])
                return(n["_source"]["username"])

    except requests.exceptions.RequestException as e:
        return e
    except IndexError:
        return None
