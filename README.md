# AUTOMATED CRYPTO WALLET MANAGER
This Python script automates the process of importing a seed phrase or private key into a crypto wallet, reading the wallet address, and retrieving the wallet balance.

## Features
- Automates Wallet Import: Handles the import of a seed phrase or private key.
- Retrieves Wallet Addresses: Extracts wallet addresses from the wallet extension.
- Fetches Wallet Balances: Retrieves and displays the balance for each wallet address.

## Prerequisites
- Python 3.x
- Selenium WebDriver
- Web3.py
- Chrome browser with the Rabby Wallet extension

## Setup
### 1. Clone the Repository: <br /> 
   > git clone https://github.com/yourusername/repository.git <br /> 
   > cd repository <br /> 

### 2. Install Required Packages: <br /> 
   > pip install selenium web3 python-dotenv

### 3. Create a .env File: <br /> 
  - In the root directory of the project, create a .env file with the following content:
   
  > SEED_PASSPHRASE="your_seed_phrase" <br /> 
  > WALLET_PASSWORD="your_wallet_password" <br /> 
  > EXTENSION_PATH="path_to_your_extension.crx" <br /> 
  > PROFILE_PATH="path_to_your_chrome_profile" <br /> 
  > EXTENSION_ID="your_extension_id" <br /> 
  > INFURA_API_KEY="your_infura_api_key" <br />
    
## Usage
  ### Run the script: <br />
  > python main.py <br />
  - The script will automate the wallet import process, retrieve wallet addresses, and display their balances. <br />

## Error Handling
  - Errors during execution will be printed to the terminal. Ensure all environment variables are correctly set and the wallet extension is properly     configured.
