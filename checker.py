from bitcoinlib.keys import Key, Address
import requests
from datetime import datetime
def validate_private_key(private_key):
    """
    Validate if a private key is a valid Bitcoin key.
    Returns tuple: (is_valid, address, error_message)
    """
    try:
        key = Key(private_key, is_private=True)
        address_obj = Address(key.public())
        address = address_obj.address
        return True, address, None
    except Exception as e:
        return False, None, str(e)

def check_blockchain_activity(address):
    """
    Check if an address has activity on the blockchain using Blockchain.info API.
    Returns tuple: (balance_in_btc, total_received_in_btc, error_message)
    """
    url = f"https://blockchain.info/rawaddr/{address}"
    proxies = {
       'http': 'http://51.158.68.68:8811',
        'https': 'https://51.158.68.68:8811',
    }
    try:
        response = requests.get(url, timeout=5, proxies=proxies)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            balance = data.get("final_balance", 0) / 100000000  # Satoshis to BTC
            total_received = data.get("total_received", 0) / 100000000  # Satoshis to BTC
            return balance, total_received, None
        else:
            return 0, 0, f"API error: Status code {response.status_code}"
    except requests.RequestException as e:
        return 0, 0, f"Network error: {str(e)}"
def check_keys_from_file(filename):
    print(f"Checking private keys from {filename}...")
    
    # Read private keys from file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Filter out header lines and get private keys
    private_keys = [line.strip() for line in lines if line.strip() and not line.startswith(('Generated', 'Total', '='))]
    if not private_keys:
        print("No private keys found in the file.")
        return
    
    print(f"Found {len(private_keys)} private keys to check.")
    
    # Check each key
    valid_keys = 0
    used_keys = 0
    for idx, private_key in enumerate(private_keys, 1):
        print(f"\nChecking Key #{idx}: {private_key}")
        
        # Validate the key
        is_valid, address, error = validate_private_key(private_key)
        if not is_valid:
            print(f"  Status: INVALID - {error}")
            continue
        
        valid_keys += 1
        print(f"  Status: VALID")
        print(f"  Address: {address}")
        
        # Check blockchain activity
        balance, total_received, error = check_blockchain_activity(address)
        if error:
            print(f"  Blockchain Check: Failed - {error}")
        else:
            print(f"  Balance: {balance} BTC")
            print(f"  Total Received: {total_received} BTC")
            if balance > 0 or total_received > 0:
                print("  Usability: This key has been used and could access a wallet with funds!")
                used_keys += 1
            else:
                print("  Usability: Valid but no funds/activity detected.")
    
    # Summary
    print(f"\nSummary:")
    print(f"Total Keys Checked: {len(private_keys)}")
    print(f"Valid Keys: {valid_keys}")
    print(f"Keys with Activity (Usable): {used_keys}")

def main():
    print("Bitcoin Private Key Checker")
    print("---------------------------")
    
    default_filename = f"bitcoin_1000_privkeys_{datetime.now().strftime('%Y-%m-%d')}.txt"
    filename = input(f"Enter filename to check (default: {default_filename}): ").strip() or default_filename
    
    check_keys_from_file(filename)

if __name__ == "__main__":
    main()
