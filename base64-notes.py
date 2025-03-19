#!/usr/bin/env python3

import base64
import random

# https://en.wikipedia.org/wiki/Base64
# Base64 encoding represents every 3 bytes of data using 4 Base64 characters
# Since each byte is 8 bits, 3 bytes (24 bits) are encoded into 4 Base64 characters (4 * 6 = 24 bits)
string_data = "This is a string to encode!"
encoded_bytes = base64.urlsafe_b64encode(string_data.encode('utf-8'))
encoded_string = encoded_bytes.decode('utf-8')

print(f"Encoded string: {encoded_string}")

# Encode bytes directly
bytes_data = b"Binary data to encode."
encoded_bytes = base64.urlsafe_b64encode(bytes_data)
encoded_string = encoded_bytes.decode('utf-8')

print(f"Encoded bytes: {encoded_string}")


num_bytes = 6
integer_value = random.randint(0,2**(num_bytes*8))
# Python defaults to big endian (first byte is most significant)
byte_representation = integer_value.to_bytes(num_bytes, byteorder='big')
print(byte_representation)

# Convert bytes to integer with big-endian byte order
integer_big_endian = int.from_bytes(byte_representation, byteorder='big')
print(f"Big-endian: {integer_big_endian}")

# Convert bytes to integer with little-endian byte order
integer_little_endian = int.from_bytes(byte_representation, byteorder='little')
print(f"Little-endian: {integer_little_endian}")

# Convert bytes to signed integer (two's complement)
# signed_bytes = b'\xfc\x00'
signed_bytes = byte_representation
signed_integer = int.from_bytes(signed_bytes, byteorder='big', signed=True)
print(f"Signed integer: {signed_integer}")

bytes_data = byte_representation
encoded_bytes = base64.urlsafe_b64encode(bytes_data)
encoded_string = encoded_bytes.decode('utf-8')

print(f"Encoded bytes: {encoded_string}")

