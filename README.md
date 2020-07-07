# AES
[AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) 128 bits implementation in python.

## Example
Text encryption and decryption
```Python
import aes

# generates new cipher key
key = aes.generate_cipher_key()

text = "YOUR_TEXT"

aes_object = aes.AES(key)
# encrypt text
encrypted_text = aes_object.encrypt(text)
# decrypt text
decrypted_text = aes_object.decrypt(encrypted_text)
```

File encryption and decryption
```Python
filename = "YOUR_FILE_PATH"
# encrypt file
aes_object.encrypt_file(filename)
# decrypt file
aes_object.decrypt_file(filename)
```
