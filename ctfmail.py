import requests
import smtplib
from email.message import EmailMessage
import boto3

client = boto3.client('cognito-idp')  
msg = EmailMessage()
msg['Subject'] = 'Registration confirmed'
msg['From'] = 'youremail@.com'
ALLOWED_DOMAIN = "@abc.com"
msg.set_content('Pearson CTF challange 2021')

def lambda_handler(event, context):
    print("--------------------")
    print(type(event["request"]["userAttributes"]["email"]))
    email_address = event["request"]["userAttributes"]["email"]
    response = client.list_users(
        UserPoolId= "id",
        AttributesToGet=["email"],
        Filter="email = \"" + email_address + "\""
    )
    print(response)
    if len(response["Users"]) == 0:
     domain = email_address[ email_address.find("@") : ]
     response = requests.get("http://apilayer.net/api/-----",params = {'email': email_address})
     format_valid = response.json()["format_valid"]
     mx_found = response.json()["mx_found"]
     smtp_check = response.json()["smtp_check"]
     if format_valid == True and mx_found == True and domain == ALLOWED_DOMAIN:
        msg.add_alternative("""\
        <!DOCTYPE html>
        <html>
        <body>
            <h3 style="color:SlateGray;">Pearson CTF challange 2021</h3>
            <img src="https://drive.google.com/uc?export=view&id=1Ivau5jLtrpW9o2ZhTLbFtumaz4odHQQD">
        </body>
        </html>
        """, subtype='html')
        msg['To'] = event["request"]["userAttributes"]["email"] 
        event["response"]["autoConfirmUser"] = True
        event["response"]["autoVerifyEmail"] = True

        send_confirmed()
        print("email is valid")
        return event
     elif domain != ALLOWED_DOMAIN:
        raise Exception(" -- The provided email address domain is not valid --")
     elif mx_found == False: 
        print("email is invalid")
        raise Exception(" -- The provided email is invalid --")
        
     else:
        raise Exception(" -- Email verification failed, please check the provided email address-- ")
    else:
        raise Exception(" -- A user with this email address already exisits --")
    
def send_confirmed():
    with smtplib.SMTP('yoursmtpserver', 25) as smtp:
        smtp.send_message(msg)