import os
from bitarray import bitarray
from bitarray.util import ba2int, int2ba

# Define shift functions for bit-level manipulation
def right_shift(array, n):
    length = len(array)
    res = bitarray(length)
    res.setall(0)  # Initialize with zeros
    if n < length:
        res[n:] = array[:length - n]
    return res

def left_shift(array, n):
    length = len(array)
    res = bitarray(length)
    res.setall(0)
    if n < length:
        res[:length - n] = array[n:]
    return res

# Helper function to convert byte strings to bitarrays
def bytestring_to_bitarray(byte_string):
    bit_arr = bitarray()
    bit_arr.frombytes(byte_string)
    return bit_arr

# Custom transformation function for bit-level encryption
def transformation(left, key):
    shifted_left = left_shift(left, 3)  # Shift left by 3 bits
    shifted_right_key = right_shift(key, 2)  # Shift right by 2 bits
    result = shifted_left ^ shifted_right_key  # Apply XOR operation
    return result

# Block-based encryption with Feistel-like structure
def encrypt_block(block, key, num_rounds=2):
    block_size = len(block)
    for round_number in range(num_rounds):
        key_segment = right_shift(key, round_number * 8)[:32]
        left = block[:block_size // 2]
        right = block[block_size // 2:]

        transformed = transformation(left, key_segment) ^ right

        if round_number == num_rounds - 1:
            new_block = left + transformed
        else:
            new_block = transformed + left

        block = new_block
    return block

# Block-based decryption with reverse Feistel-like structure
def decrypt_block(block, key, num_rounds=2):
    block_size = len(block)
    for round_number in range(num_rounds):
        key_segment = right_shift(key, (num_rounds - round_number - 1) * 8)[:32]
        left = block[:block_size // 2]
        right = block[block_size // 2:]

        transformed = transformation(right, key_segment) ^ left

        if round_number == num_rounds - 1:
            new_block = right + transformed
        else:
            new_block = transformed + right

        block = new_block
    return block

# Cipher Block Chaining (CBC) encryption
def encrypt_CBC(plaintext, key, IV, num_rounds=2, block_size=64):
    encrypted_result = bitarray()  # Initialize bitarray

    for index in range(0, len(plaintext), block_size):
        block = plaintext[index:index + block_size]

        if index == 0:
            block ^= IV  # XOR with IV for the first block
        else:
            block ^= encrypted_result[index - block_size:index]

        encrypted_block = encrypt_block(block, key, num_rounds)  # Encrypt block
        encrypted_result += encrypted_block  # Append to result

    return encrypted_result

# Cipher Block Chaining (CBC) decryption
def decrypt_CBC(ciphertext, key, IV, num_rounds=2, block_size=64):
    decrypted_result = bitarray()  # Initialize bitarray

    for index in range(0, len(ciphertext), block_size):
        block = ciphertext[index:index + block_size]

        # Decrypt block
        decrypted_block = decrypt_block(block, key, num_rounds)

        if index == 0:
            decrypted_block ^= IV  # XOR with IV for the first block
        else:
            decrypted_block ^= ciphertext[index - block_size:index]

        decrypted_result += decrypted_block  # Append to result

    return decrypted_result

# Cipher Feedback (CFB) encryption
def encrypt_CFB(plaintext, key, IV, num_rounds=2, block_size=64):
    encrypted_result = bitarray()  # Initialize bitarray

    for index in range(0, len(plaintext), block_size):
        block = plaintext[index:index + block_size]

        if index == 0:
            encrypted_stream = encrypt_block(IV, key, num_rounds)  # Encrypt IV
        else:
            encrypted_stream = encrypt_block(encrypted_result[index - block_size:index], key, num_rounds)

        encrypted_block = encrypted_stream ^ block  # XOR with plaintext block
        encrypted_result += encrypted_block

    return encrypted_result

# Cipher Feedback (CFB) decryption
def decrypt_CFB(ciphertext, key, IV, num_rounds=2, block_size=64):
    decrypted_result = bitarray()  # Initialize bitarray

    for index in range(0, len(ciphertext), block_size):
        block = ciphertext[index:index + block_size]

        if index == 0:
            decrypted_stream = encrypt_block(IV, key, num_rounds)  # Encrypt IV
        else:
            decrypted_stream = encrypt_block(ciphertext[index - block_size:index], key, num_rounds)

        decrypted_block = decrypted_stream ^ block  # XOR with ciphertext block
        decrypted_result += decrypted_block

    return decrypted_result

# Test data and initialization
input_text = "Top Secret Data"
input_bytes = input_text.encode("utf-8")

# Ensure proper padding for block consistency
block_size = 64
padded_input = input_bytes + b"\x00" * (block_size - len(input_bytes) % block_size)

# Convert to bitarray
input_bitarray = bytestring_to_bitarray(padded_input)

# Generate random key and initialization vector
key_bytes = os.urandom(8)
key_bitarray = bytestring_to_bitarray(key_bytes)

IV_bytes = os.urandom(8)
IV_bitarray = bytestring_to_bitarray(IV_bytes)

# Encrypt using CFB mode
cfb_encrypted = encrypt_CFB(input_bitarray, key_bitarray, IV_bitarray, num_rounds=4)

# Decrypt using CFB mode
cfb_decrypted = decrypt_CFB(cfb_encrypted, key_bitarray, IV_bitarray, num_rounds=4)

# Convert decrypted result to bytes and attempt to decode
cfb_decrypted_bytes = cfb_decrypted.tobytes()

# Use UTF-8 decoding, fallback to latin-1 in case of error
try:
    cfb_decrypted_text = cfb_decrypted_bytes.decode("utf-8").rstrip("\x00")  # Remove padding
except UnicodeDecodeError:
    cfb_decrypted_text = cfb_decrypted_bytes.decode("latin-1").rstrip("\x00")  # Fallback to latin-1

print("CFB Encrypted:", cfb_encrypted)
print("CFB Decrypted:", cfb_decrypted_text)
