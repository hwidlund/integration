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
'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
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
