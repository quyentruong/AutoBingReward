import smtplib
import jsonconfig
import os

pathlib = os.path.dirname(__file__) if os.path.dirname(__file__) != "" else os.getcwd()
data = jsonconfig.readjson(pathlib + "/config.json")


def send(user, message):
    if data["email"] == str() or data["passwd"] == str():
        print("You didn't setup your email.")
        return
    TO = data["email"]
    SUBJECT = "Bing Reward Question for " + user
    TEXT = message

    gmail_sender = data["email"]
    gmail_passwd = data["passwd"]
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join([
        'TO: %s' % TO,
        'FROM: %s' % gmail_sender,
        'SUBJECT: %s' % SUBJECT,
        '',
        TEXT
    ])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print("email sent by " + user)
    except:
        print("error sending email")

    server.quit()
