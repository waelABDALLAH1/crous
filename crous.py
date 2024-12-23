import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
sender_email = "wa5t5t5h@etuewetgdiant-enit.utm.tn"
receiver_emails = ["mail1@gmail.com", "mail2@gmail.com"]  # Recipients
password = " ytrtetrtretertcs"  # App Password

# List of URLs to check
urls = [
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.224122_48.902156_2.4697602_48.8155755",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.4130316_48.6485333_2.4705092_48.6109217",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.0699384_48.82861_2.1683504_48.7792297",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.4100426_48.9194431_2.4761969_48.8952245",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.169302_48.9205991_2.234232_48.8742291",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.0362453_49.0338281_2.0845719_49.00172",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.2873758_48.914015_2.3209014_48.8941707",
]

def send_test_email():
    subject = "Test Email"
    body = "This is a test email to verify the script is working."
    send_email(subject, body)
    print("Test email sent successfully.")


def send_email(subject, body):
    # Set up the SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    
    for receiver_email in receiver_emails:
        # Create the email
      msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email sent to {receiver_email}")
    
    # Close the server
    server.quit()

def check_urls():
    available_houses = []  # Replace with your actual scraping logic
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Process the page and check for availability
        if "Available" in response.text:  # Example check
            available_houses.append(url)
    if available_houses:
        subject = "Housing Availability Notification"
        body = f"The following houses are now available:\n\n" + "\n".join(available_houses)
        send_email(subject, body)
    else:
        print("No new housing available at this time.")




send_test_email()

# Schedule the task for every hour from 07:00 to 19:00
for hour in range(7, 20):  # 7 AM to 7 PM
    time_str = f"{hour:02}:00"
    schedule.every().day.at(time_str).do(check_urls)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)