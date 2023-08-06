# CaesarsCipher Documentation

## Introduction 

This is a simple python package built to Encrypt and Decrypt text using the Caesar's Cipher.

## Installation

Install the CaesarsCipher package using PIP

```python
pip install CaesarsCipher
```

## Usage

```python
# Import The Caesar Class From The CaesarsCipher Module
from CaesarsCipher import Caesar

# Encrypt Your Text Using Caesar.encrypt('your_text_here',shift_value)
print(Caesar.encrypt("Aaron Fritz",10))

# If You Don't Specify Shift Value In The Function For Encryption, The Default Shift Will Be 10
print(Caesar.encrypt("Aaron Fritz",10))

# Decrypt Your Text Using Caesar.decrypt('your_text_here',shift_value)
print(Caesar.decrypt("Kkbyx Pbsdj",10))

# If You Dont Know The Shift Value, Decrypt Your Text Using Caesar.decrypt('your_text_here') for Brute Force Decryption
print(Caesar.decrypt("Kkbyx Pbsdj"))
```



