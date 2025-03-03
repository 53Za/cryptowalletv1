from bitcoinlib.keys import Key
from datetime import datetime

def generate_and_save_1000_keys(filename):
    print("Generating 1000 Bitcoin keypairs...")
    
    # Generate 1000 keypairs
    keypairs = []
    for _ in range(10):
        key = Key()
        private_key_wif = key.wif()
        address = key.address()
        keypairs.append((private_key_wif, address))
    
    # Save to file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'w', encoding='utf-8') as f:
        for idx, (private_key, address) in enumerate(keypairs, 1):
            
            f.write(f"{private_key}\n")
            
           
    
    print(f"Generated and saved 1000 keys to {filename}")
    print("\nFirst 5 keypairs (preview):")
    for i, (private_key, address) in enumerate(keypairs[:5], 1):
        
        print(f" {private_key}")
        

def main():
    print("Bitcoin Private Key Generator - 1000 Keys")
    print("----------------------------------------")
    
    default_filename = f"bitcoin_1000_keys_{datetime.now().strftime('%Y-%m-%d')}.txt"
    filename = input(f"Enter filename (default: {default_filename}): ").strip() or default_filename
    
    generate_and_save_1000_keys(filename)
    
    print("\nInstructions for BlueWallet:")
    print("1. Open BlueWallet.")
    print("2. Tap 'Add Wallet' > 'Import Wallet'.")
    print("3. Paste a Private Key (WIF) from the file.")
    print("\nWARNING: Store the file securely!")

if __name__ == "__main__":
    main()
