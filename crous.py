import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_email = "wael.ddddd@etudiant-enit.utm.tn"
receiver_email = "ddddd@d.com"
password = "d"

def send_email(subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def fetch_and_check():
    url = "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=2.224122_48.902156_2.4697602_48.8155755" #change the location 

   
    response = requests.get(url)

   
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')

       
        logement_element = soup.find('h2', class_='SearchResults-desktop fr-h4 svelte-11sc5my')

        
        if logement_element and "Aucun logement trouvé" not in logement_element.text:
            logements_trouves = logement_element.text.strip()
            message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Logements trouvés: {logements_trouves}"
            print(message)

            
            send_email("Logement Found", message)
        else:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Aucun logement trouvé")
    else:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Failed to fetch data. Status code: {response.status_code}")


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


# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
