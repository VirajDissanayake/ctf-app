import pymsteams
from flask import session
import os

myTeamsMessage = pymsteams.connectorcard(os.environ["WEB_HOOK_URL"])#(os.environ["WEB_HOOK_URL"])
def snednotice():

    myTeamsMessage.text("The Admin user "+session["username"]+" has logged in")
    myTeamsMessage.send()

def senderror(user, email):
    myTeamsMessage.text(user+ "is having issues - contact email: "+email)
    myTeamsMessage.send()