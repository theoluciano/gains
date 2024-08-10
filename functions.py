import requests
from datetime import datetime

def get_date():
  date_str = input("What date did you buy Bitcoin? (MM-DD-YYYY): ")
  try:
      chosen_date = datetime.strptime(date_str, "%m-%d-%Y")
      return chosen_date
  except ValueError:
      print("Invalid date format. Please enter the date in MM-DD-YYYY format.")
      return None

def get_current_bitcoin_price():
    # CoinGecko API URL for getting the current price of Bitcoin in USD
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    
    try:
      response = requests.get(url)
      response.raise_for_status()  # Raise an error for bad responses
      data = response.json()
      price = data['bitcoin']['usd']
      return price
    
    except requests.exceptions.RequestException as e:
      print("Error fetching data:", e)
      return None
    
def get_historic_bitcoin_price(date):
  formatted_date = date.strftime("%d-%m-%Y")
  url = f"https://api.coingecko.com/api/v3/coins/bitcoin/history?date={formatted_date}"

  try:
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    data = response.json()
    price = data['market_data']['current_price']['usd']
    return f"{price:.0f}"

  except requests.exceptions.RequestException as e:
    print("Error fetching data:", e)
    return None

  except KeyError:
    print("Price data not available for this date.")
    return None

def get_deposit_amount():
  amount = input("How much did you buy? ($): ")
  return int(amount)

def calculate_amount_gained():
  current_price = get_current_bitcoin_price()
  date = None
  while not date:
      date = get_date()
  
  historic_price = get_historic_bitcoin_price(date)

  rate = int(current_price) / int(historic_price)
  deposit_amount = get_deposit_amount()

  amount_gained = (rate * deposit_amount) - deposit_amount
  return f"{amount_gained:.2f}"
