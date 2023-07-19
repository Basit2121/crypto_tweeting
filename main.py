import requests
import json
import time
from playwright.sync_api import sync_playwright
import random

api_key = ""
twitter_username = input("Enter Twitter Username : ")
twitter_password = input("Enter Twitter Password : ")

def fetch_coin_data(api_key):
    url = "https://api.livecoinwatch.com/coins/single"
    headers = {
        "content-type": "application/json",
        "x-api-key": api_key
    }
    payload = {
        "currency": "USD",
        "code": "VDO",
        "meta": True
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching coin data. Status code: {response.status_code}")
        return None

def print_coin_data(data):
    if data is None:
        return

    name = data["name"]
    rank = data["rank"]
    price = data["rate"]
    market_cap = data["cap"]
    volume = data["volume"]

    print("-------- Voodoo Coin Data --------")
    print(f"Name: {name}")
    print(f"Rank: {rank}")
    print(f"Price: ${price}")
    print(f"Market Capitalization: ${market_cap}")
    print(f"Trading Volume: ${volume}")
    print("----------------------------------\n")

def login_to_twitter(username, password):
    
    with sync_playwright() as playwright:
        
        print('Fetching Coin Data from Livecoinwatch API...\n')
    
        browser = playwright.chromium.launch(headless=True, channel='msedge')
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://twitter.com/login")
        # Fill in the login form
        page.fill('input[autocomplete="username"]', username)
        # Press the "Next" button
        page.click('text="Next"')
        # Wait for the password input field to appear
        page.wait_for_selector('input[autocomplete="current-password"]')
        # Fill in the password
        page.fill('input[autocomplete="current-password"]', password)
        # Submit the form
        page.click('div[data-testid="LoginForm_Login_Button"]')
        
        time.sleep(random.uniform(4,5))
        
        while True:
            
            coin_data = fetch_coin_data(api_key)
            print_coin_data(coin_data)
            
            page.goto("https://twitter.com/compose/tweet")
            
            tweet_message = f"-------- Voodoo Coin Data --------\nName: {coin_data['name']}\nTicker Symbol: $VDO\nBlockchain: Pulsechain\nPrice: ${coin_data['rate']}\nMarket Capitalization: ${coin_data['cap']}\nTrading Volume: ${coin_data['volume']}\n------------------------------------"

            time.sleep(random.uniform(4,5))
            
            textarea = page.query_selector('[data-testid="tweetTextarea_0"]')
            
            time.sleep(random.uniform(1,2))
            
            textarea.fill(tweet_message)
            
            time.sleep(random.uniform(4,5))
            
            # Fill in the tweet text area
            page.click('span:has-text("Tweet")')
            
            print("Tweeted!!!")
            
            print("Waiting an hour before tweeting again...")

            time.sleep(random.uniform(3600,3650))
            
while True:
    try:        
        login_to_twitter(twitter_username,twitter_password)    
    except:
        print('There was an Error, Retrying ...\n If the error Presists Restart the bot and make sure the entered Username and Password is Correct.')
        time.sleep(5)