import smtplib
import ssl

import pandas as pd

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime

calendar = pd.read_csv("Calendar.csv")

calendar['date_difference'] = pd.to_datetime(
    calendar['last_date_appeals']) - pd.Timestamp.now().normalize()


def send_reassessment_notifications(time_d):
    sender_email = "schwapstest@gmail.com"
    receiver_email = ["rosyrozzah@gmail.com",]
    password = "qwerty@123"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Reassessment Notification"
    message["From"] = sender_email
    for email in receiver_email:
        message["To"] = email

    township = (calendar.loc[calendar['date_difference'].dt.days == time_d])[
        "township"].values[0]
    reassessment_date = (calendar.loc[calendar['date_difference'].dt.days == time_d])[
        "reassessment_mail_date"].values[0]

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,

    The Reasessment Notice Mail Date for {} Township was released on {} and it's appeal work is due in {} day(s).

    Regards,
    Justin,
    Schwaps Ltd
    """.format(township, reassessment_date, time_d)
    html = """\
    <html>
    <body>
        <p>Hi,<br><br>
        
        The Reasessment Notice Mail Date for <b>{} Township</b> was released on <b>{}</b> and it's appeal work is due in <b>{} day(s)</b>.<br>
        <br>
        <br>
        <br>
        Regards,<br>
        Justin,<br>
        Schwaps Ltd<br>
    </body>
    </html>
    """.format(township, reassessment_date, time_d)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    # Create secure connection with server and send email
    for email in receiver_email:

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, email, message.as_string()
            )


calendar['date_difference'] = calendar['date_difference'].dt.days.apply(
    lambda x: send_reassessment_notifications(x) if (x > 0 and x <= 2) else "No email")


# date a roll certified

# **************************************************
def send_aroll_notifications():
    sender_email = "schwapstest@gmail.com"
    receiver_email = ["rosyrozzah@gmail.com",]
    password = "qwerty@123"

    message = MIMEMultipart("alternative")
    message["Subject"] = "The (A)ssessor Roll Certified"
    message["From"] = sender_email
    for email in receiver_email:
        message["To"] = email

    
    data  = get_certified_date(pd.Timestamp.now().date())
    for k, v in data.items():
        text = """\
        The (A)ssessor Roll for {} Township has been <b>certified</b> as of {}. Expect the publishing of the A-Roll within the next two weeks.
        """.format(k, v.date())
        html = """\
        <html>
        <body>
            <p>Hi,<br><br>
            
            The (A)ssessor Roll for <b>{} Township</b> has been <b>certified</b> as of <b>{}</b>. Expect the publishing of the A-Roll within the next two weeks.
            <br>
            <br>
            <br>
            Regards,<br>
            Justin,<br>
            Schwaps Ltd<br>
        </body>
        </html>
        """.format(k, v.date())

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        # Create secure connection with server and send email
        for email in receiver_email:

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                with open("output.txt", 'r+') as output:
                    if not text in  output.read():
                        output.write(text)
                        
                        server.sendmail(
                            sender_email, email, message.as_string()
                        )
                        output.close()

calendar["date_a_roll_certified"] = calendar["date_a_roll_certified"].apply(lambda x: str(
    x).strip("*"))
calendar["date_a_roll_certified"] = pd.to_datetime(
    calendar["date_a_roll_certified"])

def get_certified_date(date):
    data = {}
    for index, row in calendar.iterrows():
        if row["date_a_roll_certified"].date() >= date:
            township = row["township"]
            data[township] = row["date_a_roll_certified"]
    return data

send_aroll_notifications()


def send_aroll_pub_notification():
    sender_email = "schwapstest@gmail.com"
    receiver_email = ["rosyrozzah@gmail.com", ]
    password = "qwerty@123"

    message = MIMEMultipart("alternative")
    message["Subject"] = "The (A)ssessor Roll Published"
    message["From"] = sender_email
    for email in receiver_email:
        message["To"] = email

    data  = get_date(pd.Timestamp.now().date())
    for k, v in data.items():
        text = """\
        The (A)ssessor Roll for {} Township has been <b>published</b> as of {}. Expect it to be included in a Board of Review "Group" release within the next week.
        """.format(k, v.date())
        html = """\
        <html>
        <body>
            <p>Hi,<br><br>
            
            The (A)ssessor Roll for <b>{} Township</b> has been <b>published</b> as of <b>{}</b>. Expect it to be included in a Board of Review "Group" release within the next week.

            <br>
            <br>
            <br>
            Regards,<br>
            Justin,<br>
            Schwaps Ltd<br>
        </body>
        </html>
        """.format(k, v.date())

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        # Create secure connection with server and send email
        for email in receiver_email:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                with open("output.txt", 'r+') as output:
                    if not text in  output.read():
                        output.write(text)
                        
                        server.sendmail(
                            sender_email, email, message.as_string()
                        )
                        output.close()

calendar["date_a_roll_published"] = calendar["date_a_roll_published"].apply(lambda x: str(
    x).strip("*"))
calendar["date_a_roll_published"] = pd.to_datetime(
    calendar["date_a_roll_published"])

def get_date(date):
    data = {}
    for index, row in calendar.iterrows():
        if row["date_a_roll_published"].date() >= date:
            township = row["township"]
            data[township] = row["date_a_roll_published"]
    return data

send_aroll_pub_notification()


# **************** [board of reveiw filling dates] ***************
def send_board_notification():
    sender_email = "schwapstest@gmail.com"
    receiver_email = ["rosyrozzah@gmail.com", ]
    password = "qwerty@123"

    message = MIMEMultipart("alternative")
    message["Subject"] = "The Board of Review"
    message["From"] = sender_email
    for email in receiver_email:
        message["To"] = email


    data  = get_board_date(pd.Timestamp.now().date())
    for k, v in data.items():
        text = """\
        The Board of Review has released the filing date window for {} Township, it is {}.
        """.format(k, v)
        html = """\
        <html>
        <body>
            <p>Hi,<br><br>
            
            The Board of Review has released the filing date window for <b>{} Township</b>, it is <b>{}</b>.

            <br>
            <br>
            <br>
            Regards,<br>
            Justin,<br>
            Schwaps Ltd<br>
        </body>
        </html>
        """.format(k, v)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        # Create secure connection with server and send email
        for email in receiver_email:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                with open("output.txt", 'r+') as output:
                    if not text in  output.read():
                        output.write(text)
                        
                        server.sendmail(
                            sender_email, email, message.as_string()
                        )
                        output.close()

def get_board_date(date):
    data = {}
    for index, row in calendar.iterrows():
        if str(row["board_of_review_filling_dates"]) != "nan" and str(row["board_of_review_filling_dates"]) != "TBD":
            board_dates = str(row["board_of_review_filling_dates"]).split("to")
            for board_date in board_dates:
                if datetime.strptime(board_date.replace("/", "").replace(" ", ""), "%m%d%Y").date()  >= date:
                    township = row["township"]
                    data[township] = row["board_of_review_filling_dates"]
    return data

send_board_notification()

