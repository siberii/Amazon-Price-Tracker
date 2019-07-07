
# Access a url and retrieve data from that website
import requests
# Parse retrived data and pull out individual items from it
from bs4 import BeautifulSoup
# Send emails (Simple Mail Transfer Protocol)
import smtplib


URL = "https://www.amazon.ca/Ripple-Junction-Doctor-Adult-T-Shirt/dp/B00U0HS8JI/ref=sr_1_5?keywords=t-shirt&qid=1562456707&s=pc&sr=1-5&th=1&psc=1"

# Info on your browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


def check_price():
    # Return all data from URL
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_ourprice").get_text()

    converted_price = float(price[5:10])

    if converted_price > 15:
        send_email(title, converted_price)


def send_email(title, price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("enter@email.here", "enterpasswordhere")

    subject = "Price went down!"
    body = f"{title} went down to {price}$! Check the amazon link: {URL}"

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        "enter@sender.here", "enter@receiver.here", msg
    )
    print("EMAIL HAS BEEN SENT!")

    server.quit()


check_price()
