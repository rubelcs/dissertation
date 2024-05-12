from web3 import Web3, Account
import json
from web3.middleware import geth_poa_middleware
from web3.exceptions import ExtraDataLengthError
from dotenv import load_dotenv
from tqdm import tqdm
import os
from eth_utils import to_checksum_address


load_dotenv()
CELO_PRIVATE_KEY = os.getenv('CELO_PRIVATE_KEY')

# Load ABI from the JSON file
with open("certificates_abi.json") as f:
    contract_abi = json.load(f)

provider_url = "https://alfajores-forno.celo-testnet.org"
web3 = Web3(Web3.HTTPProvider(provider_url))

deployer = web3.eth.account.from_key(CELO_PRIVATE_KEY)
account = deployer
print(f"Connected to Celo network. Address: {deployer.address}")
web3.middleware_onion.inject(geth_poa_middleware, layer=0)  
contract_abi = contract_abi
contract_address = "0xAd0EB497991273D9c57146b2112EB5a1CcAC7c88"
contract_address = to_checksum_address(contract_address)
certificate_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def add_record(patient_id, social_security_number, patient_name, date_of_admission, date_of_birth, gender, contact_number, insurer_name):
    try:
        # Encode the function call to addRecord
        transaction = certificate_contract.functions.addRecord(
            patient_id,
            social_security_number,
            patient_name,
            date_of_admission,
            date_of_birth,
            gender,
            contact_number,
            insurer_name
        ).build_transaction({
            'chainId': 44787,  # Alfajores testnet chainId
            'gas': 3000000,    # Adjust gas value as needed
            'gasPrice': web3.to_wei('10', 'gwei'),  # Adjust gasPrice as needed
            "nonce": web3.eth.get_transaction_count(account.address),
        })

        # Sign the transaction with the account's private key
        signed_transaction = web3.eth.account.sign_transaction(transaction, CELO_PRIVATE_KEY)

        # Send the signed transaction
        tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # Wait for the transaction to be mined
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        # Check if the transaction was successful
        if tx_receipt['status'] == 1:
            print("Health record added successfully.")
            return tx_receipt
        else:
            print("Failed to add health record.")
    except Exception as e:
        print(f"Error adding health record: {e}")
        return e


def record_exists(record_id):
    try:
        # Call the contract function
        return certificate_contract.functions.recordExists(record_id).call()
    except Exception as e:
        print(f"Error checking if record exists: {e}")
        return False

def get_record_by_patient_id(patient_id):
    try:
        # Call the contract function
        return certificate_contract.functions.getRecordByPatientId(patient_id).call()
    except Exception as e:
        print(f"Error retrieving health record: {e}")
        return None


if __name__ == "__main__":
    print("Connected to Celo network")
    print(f"Deployer address: {deployer.address}")
    print(f"Contract address: {certificate_contract.address}")
    add_record("1234","ss13548839r", "John Doe", "2021-09-01", "1990-01-01", "M", "1234567890", "XYZ Insurance")