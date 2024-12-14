import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

def get_date():
  date_str = input("What date did you buy Bitcoin? (MM-DD-YYYY): ")
  try:
      chosen_date = datetime.strptime(date_str, "%m-%d-%Y")
      chosen_timestamp = int(chosen_date.timestamp())
      return chosen_timestamp
  except ValueError:
      print("Invalid date format. Please enter the date in MM-DD-YYYY format.")
      return None

def get_bitcoin_price(timestamp=None):
  try:
      if timestamp:  # Fetch historical price
          url = 'https://min-api.cryptocompare.com/data/pricehistorical'
          params = {
              'fsym': 'BTC',
              'tsyms': 'USD',
              'ts': timestamp,
              'api_key': API_KEY
          }
      else:  # Fetch current price
          url = 'https://min-api.cryptocompare.com/data/price'
          params = {
              'fsym': 'BTC',
              'tsyms': 'USD',
              'api_key': API_KEY
          }
      
      response = requests.get(url, params=params)
      response.raise_for_status()  # Raise exception for HTTP errors
      data = response.json()
      
      if timestamp:
          return data['BTC']['USD']
      return data['USD']
  except Exception as e:
      print(f"Error fetching Bitcoin price: {e}")
      return None

def get_deposit_amount():
  amount = input("How much did you buy? ($): ")
  return int(amount)

def calculate_amount_gained():
  current_price = get_bitcoin_price()
  date = None
  while not date:
      date = get_date()
  
  historic_price = get_bitcoin_price(date)

  rate = int(current_price) / int(historic_price)
  deposit_amount = get_deposit_amount()

  amount_gained = (rate * deposit_amount) - deposit_amount
  print(f"Bitcoin cost {historic_price} when you bought it. It now costs {current_price}")
  return f"{amount_gained:.2f}"
