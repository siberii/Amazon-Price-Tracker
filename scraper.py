
import getpass
import time
# Send emails (Simple Mail Transfer Protocol)
import smtplib

# Access a url and retrieve data from that website
import requests
# Parse retrived data and pull out individual items from it
from bs4 import BeautifulSoup


# Info on your browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


def check_price(sender, password, receiver, desired_price, URL):
    price_matched = False
    # Return all data from URL
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_ourprice").get_text().strip()
    print("\n Item: " + title + "\n Current Price: " + price)

    converted_price = float(price[5:13].replace(',', ''))

    if converted_price <= float(desired_price):
        send_email(title, converted_price, URL, sender, password, receiver)
        price_matched = True
    return price_matched


def send_email(title, price, URL, sender, password, receiver):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender, password)

    subject = "Price went down!"
    body = f"{title} went down to {price}$!\nCheck the amazon link: {URL}\n"

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        sender, receiver, msg
    )
    print("\nEMAIL HAS BEEN SENT!")

    server.quit()


print("~ Welcome to Amazon Price Tracker! ~")
sender = input("\nSender Email: ")
try:
    print("\n(Your password will be hidden.) ")
    password = getpass.getpass()
except Exception as error:
    print('ERROR', error)
receiver = input("\nReceiver Email: ")
product_url = input("\nPaste Product URL: ")
if product_url == "-":
    product_url = "https://www.amazon.ca/Ripple-Junction-Doctor-Adult-T-Shirt/dp/B00U0HS8JI/ref=sr_1_5?keywords=t-shirt&qid=1562456707&s=pc&sr=1-5&th=1&psc=1"
desired_price = input("\nDesired Price: ")
frequency = input("\nPrice Check Frequency (seconds): ")

price_matched = False
while not price_matched:
    price_matched = check_price(sender, password, receiver, desired_price,
                                product_url)
    if not price_matched:
        time.sleep(int(frequency))
