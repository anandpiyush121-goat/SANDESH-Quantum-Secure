import random
from encrypt_message import encrypt, decrypt

# Step 1: Generate quantum key (simulate BB84 result)
key_bits = [random.randint(0,1) for _ in range(10)]
shared_key = ''.join(map(str, key_bits))

print("Generated Quantum Key:", shared_key)

# Step 2: Alice sends message
message = "HELLO BOB"

print("\nOriginal Message:", message)

# Step 3: Encrypt message
encrypted_message = encrypt(message, shared_key)

print("Encrypted Message:", encrypted_message)

# Step 4: Bob decrypts message
decrypted_message = decrypt(encrypted_message, shared_key)

print("Decrypted Message:", decrypted_message)