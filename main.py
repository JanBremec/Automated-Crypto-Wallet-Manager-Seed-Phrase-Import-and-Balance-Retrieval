from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from web3 import Web3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

seed_passphrase = os.getenv('SEED_PASSPHRASE')
password = os.getenv('WALLET_PASSWORD')
EXTENSION_PATH = os.getenv('EXTENSION_PATH')
profile_path = os.getenv('PROFILE_PATH')
EXTENSION_ID = os.getenv('EXTENSION_ID')
infura_api_key = os.getenv('INFURA_API_KEY')

# Set up Chrome options to load the extension
chrome_options = Options()
chrome_options.add_extension(EXTENSION_PATH)
chrome_options.add_argument(f"user-data-dir={profile_path}")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)


def switch_window(target_url=None):
    """Switches to the desired window if the target URL matches."""
    if target_url:
        for win in driver.window_handles:
            driver.switch_to.window(win)
            if driver.current_url == target_url:
                return True
    return False


def send_to_input(xpath, value, wait_until=True, find_by=By.XPATH):
    """Sends input to a specified element."""
    try:
        if wait_until:
            wait.until(EC.presence_of_element_located((find_by, xpath))).send_keys(value)
        else:
            driver.find_element(find_by, xpath).send_keys(value)
    except Exception as e:
        print(f"Error sending input to {xpath}: {e}")


def handle_error(e):
    """Handles errors by printing them and closing the browser."""
    print(f"An error occurred: {e}")
    driver.quit()
    exit()


def get_wallet_addresses():
    """Fetches wallet addresses from the extension."""
    try:
        elements = driver.find_elements(By.CLASS_NAME, "cell-address")
        return [element.find_element(By.TAG_NAME, "span").text for element in elements]
    except Exception as e:
        handle_error(f"Error fetching wallet addresses: {e}")


def check_web3_connection():
    """Initializes a Web3 instance and checks the connection."""
    rpc_url = f"https://mainnet.infura.io/v3/{infura_api_key}"
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if web3.is_connected():
        print("Connected to the mainnet")
    else:
        handle_error("Failed to connect to mainnet")
    return web3


def display_wallet_balances(web3, addresses):
    """Displays the balance of each wallet address."""
    for addr in addresses:
        try:
            checksummed_address = web3.to_checksum_address(addr)
            balance_wei = web3.eth.get_balance(checksummed_address)
            balance_ether = web3.from_wei(balance_wei, 'ether')
            print(f"{checksummed_address} has {balance_ether} ETH.")
        except Exception as e:
            print(f"Error fetching balance for {addr}: {e}")


try:
    # Navigate to the extension's popup page
    wallet_url = f"chrome-extension://{EXTENSION_ID}/popup.html"
    driver.get(wallet_url)

    # Handle different stages of the wallet setup and interaction
    while True:
        try:
            current_url = driver.current_url

            if current_url.endswith("/import/mnemonics"):
                send_to_input("/html/body/div/main/div/form/div[1]/div[1]/div/div/div/div/div/div[2]/div[1]/input",
                              seed_passphrase)
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/div/main/div/form/div[2]/button").click()
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/main/div[3]/div[1]/div[1]/div/div[2]")))

            elif current_url.endswith("/unlock"):
                send_to_input("/html/body/div/div/form/div[1]/div/div/div/input", password)
                driver.find_element(By.XPATH, "/html/body/div/div/form/div[2]/div/div/div/button").click()
                time.sleep(2)

            elif current_url.endswith("/add-address"):
                wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[2]/div[1]"))).click()
                switch_window(f"chrome-extension://{EXTENSION_ID}/index.html#/import/mnemonics")

            elif current_url.endswith("/import/select-address"):
                addresses = get_wallet_addresses()
                break

        except Exception as e:
            handle_error(e)

    web3 = check_web3_connection()
    display_wallet_balances(web3, addresses)

except Exception as e:
    handle_error(e)

finally:
    driver.quit()
