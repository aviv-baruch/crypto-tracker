import logging
import time
import requests
import os
from dotenv import load_dotenv


def init_api():
    load_dotenv()
    return os.getenv("API_KEY")


def get_all_assets():
    """
    Fetches all available assets from the CoinAPI.
    """
    url = "https://rest.coinapi.io/v1/assets"
    headers = {
        'Accept': 'application/json',
        'X-CoinAPI-Key': API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)  # Use requests.get with a timeout for better control.
        response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful (status code >= 400).
        return response.json()  # Return the parsed JSON data.
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request failed: {req_err}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return None  # Return None to indicate failure.


def fetch_specific_rate(ticker, retries=3):
    """
    Fetches the exchange rate for a specific cryptocurrency (ticker) in USD.
    Retries up to `retries` times if the request fails.
    """
    url = f'https://rest.coinapi.io/v1/exchangerate/{ticker}/USD'
    headers = {
        'Accept': 'application/json',
        'X-CoinAPI-Key': API_KEY
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()  # Return the exchange rate data as JSON.
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error on attempt {attempt}: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request failed on attempt {attempt}: {req_err}")
        except Exception as e:
            logging.error(f"Unexpected error on attempt {attempt}: {e}")

        if attempt < retries:
            logging.info(f"Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)  # Exponential backoff for retries.

    logging.error(f"Failed to fetch rate for {ticker} after {retries} retries.")
    return None


def check_api_status():
    """
    Checks the API status and returns 1 if the service is operational, 0 otherwise.
    """
    url = "https://status.coinapi.io/api/v1/status"
    headers = {
        'Accept': 'application/json',
        'X-CoinAPI-Key': API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        status_data = response.json()
        # Safely access nested dictionary values
        if status_data.get("page", {}).get("state") == "operational":
            return 1
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error while checking API status: {req_err}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return 0  # Return 0 if the API is not operational or an error occurs.


API_KEY = init_api()
