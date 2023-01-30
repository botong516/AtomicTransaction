import algosdk

# Generate a fresh private key and associated account address
private_key_A, account_address_A = algosdk.account.generate_account()
private_key_B, account_address_B = algosdk.account.generate_account()

# Convert the private key into a mnemonic which is easier to use
mnemonic_A = algosdk.mnemonic.from_private_key(private_key_A)
mnemonic_B = algosdk.mnemonic.from_private_key(private_key_B)

print("Private key mnemonic for A: " + mnemonic_A)
print("Account address for A: " + account_address_A)

print("Private key mnemonic for B: " + mnemonic_B)
print("Account address for B: " + account_address_B)