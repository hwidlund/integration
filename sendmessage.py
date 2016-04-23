#-------------------------------------------------------------------------------
# Name:        sendmessage.py
# Purpose:     Send a message on script error
#
# Author:      Heather Widlund, GIS Coordinator
#              heatherw@sanmiguelcountyco.gov
# Created:     Mar 2016
#-------------------------------------------------------------------------------
# Requirements
# SMTP server settings
# Parameters
# 0. Message to send

def SendEmail(message):
    import smtplib
    sender = ""
    recipient = ""
    subject = "Status message from script"
    # must include the from/to/subject text in message
    msg = "From: {0}\nTo: {1}\nSubject: {2}\n{3}".format(sender,recipient,subject,message)
    smtpServer = ""
    smtpPort = 25
    smtp = smtplib.SMTP(smtpServer,smtpPort)
    try:
        smtp.sendmail(sender,recipient,msg)
        return (True,"Success")
    except Exception as e:
        error = "Failed: send email notification " + str(e)
        return (False, error)
    finally:
        smtp.quit
