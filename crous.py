import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
sender_email = "wael.fefgrhtr@etudiant-enit.utm.tn"
receiver_email = "waelabdthyfhdtgrseretyrallah846@gmail.com"
password = "czigdhtfgthfgfgtrhfg"  # App Password

# List of URLs to check
urls = [
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.224122_48.902156_2.4697602_48.8155755",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.4130316_48.6485333_2.4705092_48.6109217",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.0699384_48.82861_2.1683504_48.7792297",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.4100426_48.9194431_2.4761969_48.8952245",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.169302_48.9205991_2.234232_48.8742291",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.0362453_49.0338281_2.0845719_49.00172",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.2873758_48.914015_2.3209014_48.8941707",
    "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=6.9447513_43.574726_7.074185_43.505026"
]

def send_email(subject, body):
    """
    Send an email with the specified subject and body.
    """
    try:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def fetch_and_check():
    """
    Fetch and check all URLs for housing availability.
    """
    for url in urls:
        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                logement_element = soup.find('h2', class_='SearchResults-desktop fr-h4 svelte-11sc5my')

                if logement_element and "Aucun logement trouvé" not in logement_element.text:
                    logements_trouves = logement_element.text.strip()
                    message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Logements trouvés at {url}: {logements_trouves}"
                    print(message)

                    send_email("Logement Found", message)
                else:
                    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - No logement found at {url}")
            else:
                print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Failed to fetch data from {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")

def test_email():
    """
    Test the email-sending functionality.
    """
    subject = "Test Email"
    body = "This is a test email to verify the functionality of the email-sending feature."
    send_email(subject, body)

# Schedule checks for every hour from 09:00 to 18:00
schedule.every().day.at("09:00").do(fetch_and_check)
schedule.every().day.at("10:00").do(fetch_and_check)
schedule.every().day.at("11:00").do(fetch_and_check)
schedule.every().day.at("12:00").do(fetch_and_check)
schedule.every().day.at("13:00").do(fetch_and_check)
schedule.every().day.at("14:00").do(fetch_and_check)
schedule.every().day.at("15:00").do(fetch_and_check)
schedule.every().day.at("16:00").do(fetch_and_check)
schedule.every().day.at("17:00").do(fetch_and_check)
schedule.every().day.at("18:00").do(fetch_and_check)

if __name__ == "__main__":
    # Test email functionality first
    test_email()

    # Run scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)
