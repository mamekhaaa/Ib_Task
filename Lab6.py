# Import the necessary library for image processing
from PIL import Image

# Function to hide a secret message within an image
def hide_message(container_image_path, message, output_path):
    # Open the container image where the message will be hidden
    container_image = Image.open(container_image_path)

    # Convert the message into binary bits
    # Each character is converted to its ASCII binary representation (8 bits)
    message_bits = ''.join(format(ord(char), '08b') for char in message)

    # Append a termination marker to indicate the end of the message
    message_bits += "00000000"

    # Get the pixel data from the container image
    container_pixels = list(container_image.getdata())
    new_pixels = []  # To store modified pixel data
    message_index = 0  # Tracks the position in the message_bits
    message_length = len(message_bits)  # Total number of bits in the message

    # Embed the message bits into the least significant bit of the red channel
    for pixel in container_pixels:
        r, g, b = pixel  # Extract RGB values from the pixel

        if message_index < message_length:
            # Clear the least significant bit of the red channel
            r &= 0xFE  # Set the last bit to 0
            # Set the least significant bit to the corresponding message bit
            r |= int(message_bits[message_index])  # 1 or 0 based on the message
            message_index += 1  # Move to the next bit

        # Append the modified pixel to the new pixel list
        new_pixels.append((r, g, b))

    # Create a new image with the modified pixel data
    new_image = Image.new(container_image.mode, container_image.size)  # Same mode and size
    new_image.putdata(new_pixels)  # Apply modified pixel data
    new_image.save(output_path)  # Save the new image with the hidden message

# Function to extract the hidden message from an image
def extract_message(container_image_path):
    # Open the container image from which the message will be extracted
    container_image = Image.open(container_image_path)
    container_pixels = list(container_image.getdata())  # Get the pixel data

    message_bits = ''  # To store the extracted bits
    # Extract the least significant bit of the red channel from each pixel
    for pixel in container_pixels:
        r, _, _ = pixel  # Only interested in the red channel
        message_bits += str(r & 1)  # Get the LSB of the red channel

    # Find the index of the termination marker ("00000000")
    end_index = message_bits.find("00000000")
    if end_index == -1:
        return "Termination marker not found. Message extraction unsuccessful."  # No marker found

    # Extract only the message bits before the termination marker
    message_bits = message_bits[:end_index]

    # Convert the binary bits back into characters to reconstruct the hidden message
    decoded_message = ""  # Holds the decoded message
    for i in range(0, len(message_bits), 8):  # Process 8 bits at a time
        byte = message_bits[i:i + 8]  # Get a byte (8 bits)
        decoded_message += chr(int(byte, 2))  # Convert the byte to an ASCII character

    return decoded_message  # Return the decoded message

# Sample usage of the functions
# Define file paths
