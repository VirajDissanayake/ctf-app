import boto3
from decimal import Decimal
from botocore.exceptions import ClientError
import botocore
from boto3.dynamodb.conditions import Attr
import application

def update_data(user, email, score, totalsc, levelno, status, endtime, completecount, totaltime, groupscore, grouptime, grouplvlcount):
    dynamodb = boto3.resource('dynamodb', "us-east-1")
    table = dynamodb.Table('leaderboard')
    response = table.update_item(
        Key={
            'user': user,
            'email': email
        },
        UpdateExpression="set totalsc=:totalsc, chlevel= list_append(chlevel, :chlevel), completecount=:completecount, endtime=:endtime, totaltime=:totaltime, groupscore=:groupscore, grouptime=:grouptime, grouplvlcount=:grouplvlcount",
        ExpressionAttributeValues={
            ':totalsc': totalsc,
            ':chlevel':[{
                levelno:status,
                ':score': score,
                
            }],
            ':endtime':endtime,
            ':completecount': completecount,
            ':totaltime': totaltime,
            ':groupscore': groupscore,  
            ':grouptime': grouptime, 
            ':grouplvlcount': grouplvlcount  
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def cstat(user, email, cstate, starttime, ctfgroup):
    dynamodb = boto3.resource('dynamodb', "us-east-1")
    table = dynamodb.Table('leaderboard')
    response = table.update_item(
        Key={
            'user': user,
            'email': email
        },
        UpdateExpression="set cstate=:cstate, starttime=:starttime, ctfgroup=:ctfgroup",
        ExpressionAttributeValues={
            ':cstate': cstate,
            ':starttime':starttime,
            ':ctfgroup': ctfgroup,
            
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def add_user(user, email):
 try:
    dynamodb = boto3.resource('dynamodb', "us-east-1")
    table = dynamodb.Table('leaderboard')
    response = table.put_item(
       Item={
            'user': user,
            'email': email,
            'starttime': "",
            'endtime': "",
            'chlevel': [   
                ],
            'totalsc': 0,
            'cstate': "notstarted",
            'completecount': 0,
            'totaltime': 0,
            'ctfgroup': "",
            'groupscore': 0,
            'grouptime': 0, 
            'grouplvlcount': 0 
        },
        ConditionExpression='attribute_not_exists(email)'
    )
 except botocore.exceptions.ClientError as e:
     response = "user already exsists!"
 except botocore.exceptions.EndpointConnectionError as e:
        return application.wentwrong(e)
 return response

def get_score(user, email):

    dynamodb = boto3.resource('dynamodb', "us-east-1")
    table = dynamodb.Table('leaderboard')

    try:
        response = table.get_item(Key={'user': user, 'email': email})
    except ClientError as e:
        print(e.response['Error']['Message'])
        return application.wentwrong(e)
    except botocore.exceptions.EndpointConnectionError as e:
        return application.wentwrong(e)
    else:
        return response["Item"]

def updatescore(user, email, grouptime, groupscore, grouplvlcount):
    dynamodb = boto3.resource('dynamodb', "us-east-1")
    table = dynamodb.Table('leaderboard')
    response = table.update_item(
        Key={
            'user': user,
            'email': email
        },
        UpdateExpression="set grouptime=:grouptime, groupscore=:groupscore, grouplvlcount=:grouplvlcount",
        ExpressionAttributeValues={
            ':grouptime': grouptime,
            ':groupscore':groupscore,
            ':grouplvlcount': grouplvlcount,
            
        },
        ReturnValues="UPDATED_NEW"
    )
    return response