import os
from bitarray import bitarray
from bitarray.util import ba2int, int2ba

# Shift functions
def right_shift(array, n):
    length = len(array)
    res = bitarray(length)
    res.setall(0)  # Initialize with zeros
    if n < length:
        res[n:] = array[:length - n]  # Shift bits to the right
    return res

def left_shift(array, n):
    length = len(array)
    res = bitarray(length)
    res.setall(0)  # Initialize with zeros
    if n < length:
        res[:length - n] = array[n:]  # Shift bits to the left
    return res

# Transformation function for Feistel-like structure
def F(left, key):
    shifted_left = left_shift(left, 3)  # Left shift
    shifted_right_key = right_shift(key, 2)  # Right shift key
    transformed = shifted_left ^ shifted_right_key  # XOR with shifted key
    return transformed

# Custom encryption and decryption functions (with block size checks)
def encrypt(plaintext, key, num_rounds=2, block_size=64):
    ciphertext = bitarray()  # Initialize ciphertext
    for index in range(0, len(plaintext), block_size):
        block = plaintext[index:index + block_size]
        half_size = block_size // 2
        left = block[:half_size]
        right = block[half_size:]

        # Perform multiple rounds of encryption
        for round_number in range(num_rounds):
            key_segment = right_shift(key, round_number * 8)[:32]
            transformed = F(left, key_segment)  # Apply transformation function
            new_right = transformed ^ right

            if round_number == num_rounds - 1:
                new_block = left + new_right  # Final round maintains order
            else:
                new_block = new_right + left  # Swap halves in intermediate rounds

            left, right = new_right, left  # Swap halves for next round

        ciphertext += new_block  # Append to ciphertext

    return ciphertext

def decrypt(ciphertext, key, num_rounds=2, block_size=64):
    plaintext = bitarray()  # Initialize plaintext
    for index in range(0, len(ciphertext), block_size):
        block = ciphertext[index:index + block_size]
        half_size = block_size // 2
        left = block[:half_size]
        right = block[half_size:]

        # Perform multiple rounds of decryption in reverse order
        for round_number in range(num_rounds - 1, -1, -1):
            key_segment = right_shift(key, round_number * 8)[:32]
            transformed = F(right, key_segment)  # Apply transformation
            new_left = transformed ^ left

            if round_number == 0:
                new_block = right + new_left  # Final round maintains order
            else:
                new_block = new_left + right  # Swap halves in intermediate rounds

            left, right = right, new_left  # Swap halves for next round

        plaintext += new_block  # Append to plaintext

    return plaintext

# Test data for encryption and decryption
original_text = "Secret message"
original_bytes = original_text.encode("utf-8")

# Ensure even block size with proper padding
padded_bytes = original_bytes + b"\x00" * (8 - len(original_bytes) % 8)

# Convert to bitarray
original_bitarray = bitarray()
original_bitarray.frombytes(padded_bytes)  # Convert to bitarray

# Generate a random key
key_bytes = os.urandom(8)  # Generate random 8-byte key
key_bitarray = bitarray()  # Initialize bitarray for key
key_bitarray.frombytes(key_bytes)

# Encrypt and decrypt
num_rounds = 4
encrypted = encrypt(original_bitarray, key_bitarray, num_rounds)

# Decrypt the ciphertext
decrypted = decrypt(encrypted, key_bitarray, num_rounds)

# Convert to bytes for decoding
decrypted_bytes = decrypted.tobytes()  # Use `tobytes()` to convert to bytes

# Attempt decoding with UTF-8, falling back to Latin-1 if needed
try:
    decrypted_text = decrypted_bytes.decode("utf-8")  # Try UTF-8
except UnicodeDecodeError:
    decrypted_text = decrypted_bytes.decode("latin-1")  # Fallback to Latin-1

# Display results
print("Original Text:", original_text)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
print("Decrypted Text:", decrypted_text)
