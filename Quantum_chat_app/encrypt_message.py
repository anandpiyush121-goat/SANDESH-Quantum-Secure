def encrypt(message: str, key_bits: str) -> str:
    # 1. Message ko bytes mein convert karo
    msg_bytes = message.encode('utf-8')
    required_bits = len(msg_bytes) * 8
    
    # 2. STRICT OTP RULE CHECK: No looping allowed!
    if required_bits > len(key_bits):
        raise ValueError(f"Message requires {required_bits} bits, but Quantum Key has only {len(key_bits)} bits.")
    
    # 3. One-Time Pad XOR (Byte by Byte)
    cipher_bytes = bytearray()
    for i in range(len(msg_bytes)):
        # Key me se exactly 8 bits nikaalo
        key_byte_str = key_bits[i*8 : (i+1)*8]
        key_byte = int(key_byte_str, 2)
        
        # XOR operation
        cipher_byte = msg_bytes[i] ^ key_byte
        cipher_bytes.append(cipher_byte)
        
    return cipher_bytes.hex()

def decrypt(ciphertext_hex: str, key_bits: str) -> str:
    try:
        cipher_bytes = bytes.fromhex(ciphertext_hex)
        decrypted_bytes = bytearray()
        
        for i in range(len(cipher_bytes)):
            key_byte_str = key_bits[i*8 : (i+1)*8]
            
            if not key_byte_str or len(key_byte_str) < 8:
                return "[ERROR: KEY_EXHAUSTED]"
                
            key_byte = int(key_byte_str, 2)
            decrypted_byte = cipher_bytes[i] ^ key_byte
            decrypted_bytes.append(decrypted_byte)
        
        # Agar key galat hui toh ye line error degi, jise hum handle karenge
        return decrypted_bytes.decode('utf-8')
        
    except (UnicodeDecodeError, Exception):
        # Crash hone ke bajaye ye return karega
        return "[ALERT: INTEGRITY COMPROMISED - KEY MISMATCH]"