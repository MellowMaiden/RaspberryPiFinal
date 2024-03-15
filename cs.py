import datetime
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
import ssl

class WeatherAlarm:
    def __init__(self, weather_url, email_user, email_pass, recipient_email):
        self.weather_url = weather_url
        self.email_user = email_user
        self.email_pass = email_pass
        self.recipient_email = recipient_email

    def get_weather_from_web(self):
        page = requests.get(self.weather_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        weather_div = soup.find('section', id='National-Forecast-Map')
        for p in weather_div.find_all('p'):
            if "Issued at" not in p.text:
                return p.text
        return "No weather information found."

    def send_email(self, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_user
        msg['To'] = self.recipient_email
        server = "smtp.fastmail.com"
        port = 465

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(server, port, context=context) as server:
            server.set_debuglevel(1)
            server.login(self.email_user, self.email_pass)
            server.sendmail(self.email_user, self.recipient_email, msg.as_string())

    def play_alarm(self):
        os.system('mpg123 /home/pi/Leo/static/audio/warningvoice.mp3')


# Initialize the WeatherAlarm object with necessary info
alarm = WeatherAlarm(
    weather_url='https://www.met.ie/dublin-forecast.html',
    email_user="l2628787@fastmail.com",
    email_pass="ha2hjhvkcryqfzkd",
    recipient_email="l2628787@gmail.com"
)

# Set the alarm time
alarm_hour = 7
alarm_minute = 0

# Main loop to check the time and send weather email
while True:
    now = datetime.datetime.now()
    if now.hour == alarm_hour and now.minute == alarm_minute:
        alarm.play_alarm()
        weather_info = alarm.get_weather_from_web()
        alarm.send_email("Today's Weather", weather_info)
        print("Weather email sent.")
        time.sleep(60)  # Wait a minute to prevent multiple alerts
    time.sleep(10)  # Check every 10 seconds