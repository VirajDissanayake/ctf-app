from copy import Error
import DynamoDB_functions
from flask import request, session, redirect, url_for, Flask
from datetime import datetime, time, timedelta
from decimal import Decimal
import time
import boto3
import os
import results
def validate_result(flag, level, points):
    status = "unsolved"
    key = request.form.get("key")
    challange = request.form.get("level")
    print(level)
    print(session["ctfgroup"])
    clevel=[]
    clevel1=[]
    usr1=""
    levels = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10', 'level11', 'level12', 'level13', 'level14', 'level15']
    #lvlstat = results.get_level_stat(level, session["ctfgroup"])
    lvlstat = results.get_group_score(session["ctfgroup"])
    for n in lvlstat:
            
            if n["_source"]["username"] == session["username"]:
                res = DynamoDB_functions.get_score(n["_source"]["username"], n["_source"]["email"])
                for lvl in res['chlevel']:
                    
                    if list(lvl.keys())[0] in levels:
                       
                        clevel.append(list(lvl.keys())[0])
                    if list(lvl.keys())[1] in levels:
                      
                        clevel.append(list(lvl.keys())[1])
            else:
                res = DynamoDB_functions.get_score(n["_source"]["username"], n["_source"]["email"])
                for lvl in res['chlevel']:
                    usr1 = n["_source"]["username"]
                    eml1 = n["_source"]["email"]
                    if list(lvl.keys())[0] in levels:
                        
                        clevel1.append(list(lvl.keys())[0])
                    if list(lvl.keys())[1] in levels:
                        
                        clevel1.append(list(lvl.keys())[1])   
    if level in clevel:
         nm = "You"
    if level in clevel1:
         nm = n["_source"]["username"]

    group = session["ctfgroup"]
    if key == flag and level not in clevel and level not in clevel1:
        session["msg"] = "correct"
        response = DynamoDB_functions.get_score(
            session["username"], session["email"])
        currentTotal = int(response["totalsc"])
        print(request.get_data("starttime"))
        sttime = response["starttime"]
        ltime = response["endtime"]
        gap=0
        for val in response["chlevel"]:
          for key,vl in val.items():
          
            if key == level and vl == "solved":
                print(key,vl)   
                session["msg"] = "submitted"
                status = "solved"
                break
        
        completecount = len(response["chlevel"]) 
        groupscore=0
        grouptime=0
        grouplvlcount=0
        if status == "unsolved":
            now = datetime.now()
            endtime = now.strftime("%d/%m/%Y %H:%M:%S")
            start = datetime.strptime(sttime, "%d/%m/%Y %H:%M:%S")
            end =   datetime.strptime(endtime, "%d/%m/%Y %H:%M:%S")
            totaltime = Decimal((end - start).total_seconds())
            if ltime != '':
                etime = datetime.strptime(ltime, "%d/%m/%Y %H:%M:%S")
                print(start)
                totaltime = Decimal((end - start).total_seconds())
                gap = Decimal((end - etime).total_seconds())
            total = currentTotal + points
            ctfgroup = results.get_group_score(group)
            print(ctfgroup)
            
            for cgroup in ctfgroup:
                    groupscore += cgroup["_source"]["totalscore"]
                    grouptime += cgroup["_source"]["totaltime"]
                    grouplvlcount += cgroup["_source"]["completecount"]
            print(groupscore)
            print(grouptime)
            completecount+=1
            grouplvlcount +=1
            groupscore +=points
            grouptime +=gap
            valtime = countdown()
            if session["groups"] != ["admin"] and valtime >0:
                DynamoDB_functions.update_data(
                    session["username"], session["email"], points, total, level, "solved", endtime, completecount, totaltime, groupscore, grouptime, grouplvlcount)
                if usr1 != "":
                    DynamoDB_functions.updatescore(usr1,eml1,grouptime,groupscore, grouplvlcount)
        return True
    elif key == flag and level in clevel or level in clevel1:
        session["msg"] = "marked"
        session["player2"] = nm
        return False
    elif key != flag and level in clevel or level in clevel1:
        session["msg"] = "marked"
        session["player2"] = nm
        return False
    else:
        session["msg"] = "wrong"
        return False

def countdown():
    closetime = datetime.strptime(os.environ["CLOSE_TIME"], "%d/%m/%Y %H:%M:%S")
    now = datetime.now()
    gap = int((closetime - now).total_seconds())
    
    return gap
   
def golive():
    livetime = datetime.strptime(os.environ["CLOSE_TIME"], "%d/%m/%Y %H:%M:%S")
    now = datetime.now()
    gap = int((livetime - now).total_seconds())

    return gap      

client = boto3.client('ssm', region_name="us-east-1")


def get_secret(name):
    response = client.get_parameter(Name=name, WithDecryption=True)
    return response["Parameter"]["Value"]