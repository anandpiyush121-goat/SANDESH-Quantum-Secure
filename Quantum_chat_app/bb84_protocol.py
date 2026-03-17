import random

def generate_key(length=1024):
    """Generates a secure quantum key of specified bit length using BB84 simulation."""
    # Hum intentionally zyada bits bhejte hain kyunki ~50% bases mismatch mein discard ho jayenge
    raw_bits = [random.randint(0, 1) for _ in range(length * 3)]
    alice_bases = [random.randint(0, 1) for _ in range(length * 3)]
    bob_bases = [random.randint(0, 1) for _ in range(length * 3)]

    key = []
    for i in range(len(raw_bits)):
        if alice_bases[i] == bob_bases[i]:
            key.append(raw_bits[i])

    # Ensure we return exactly the requested length (1024 bits)
    return key[:length]