from Crypto.Util.number import getPrime, inverse, GCD
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

# Function to generate RSA keys
def generate_rsa_keys(key_size=2048):
    # Generate two large prime numbers
    p = getPrime(key_size // 2)
    q = getPrime(key_size // 2)

    # Calculate modulus and totient
    n = p * q
    totient = (p - 1) * (q - 1)

    # Choose a public exponent (commonly 65537)
    e = 65537  # Commonly used for RSA

    # Ensure that e is relatively prime to the totient
    if GCD(e, totient) != 1:
        raise ValueError("The public exponent is not relatively prime to the totient.")

    # Calculate the private exponent
    d = inverse(e, totient)

    # Construct the RSA public and private keys
    public_key = RSA.construct((n, e))
    private_key = RSA.construct((n, e, d))

    return public_key, private_key

# Function to encrypt a message with RSA
def rsa_encrypt(plaintext, public_key):
    # Use a padding scheme (PKCS1_OAEP) with SHA-256 for secure encryption
    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
    encrypted = cipher.encrypt(plaintext)
    return encrypted

# Function to decrypt a message with RSA
def rsa_decrypt(encrypted, private_key):
    # Use the corresponding private key to decrypt the message
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    decrypted = cipher.decrypt(encrypted)
    return decrypted

# Generate RSA public and private keys
public_key, private_key = generate_rsa_keys(key_size=2048)

# Example plaintext message
plaintext = b'Hello, RSA!'

# Encrypt the plaintext message
encrypted_message = rsa_encrypt(plaintext, public_key)
print("Encrypted message:", encrypted_message)

# Decrypt the encrypted message
decrypted_message = rsa_decrypt(encrypted_message, private_key)
print("Decrypted message:", decrypted_message)

# Validate that the decrypted message matches the original plaintext
if decrypted_message == plaintext:
    print("Decryption successful. The messages match.")
else:
    print("Decryption failed. The messages do not match.")
