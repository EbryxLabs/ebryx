## Encryption / Decryption
You can encrypt / decrypt data using `crypto.py` script. **(AES-256 Encryption)**

For example, to encrypt you can do following:
```
python crypto.py <my-file.json> -e --new
# encrypts myfile.json using newly created crypto-secure key. Keys will be written to _keys file.

python crypto.py <my-file.json> -e
# encrypts using keys in AES_KEY environment variable.

# If your input file is myfile.json, encrypted file will be _myfile.json
```

For decryption, you'll need to have `AES_KEY` keys in your environment variables.
```
python crypto.py <my-file.json> -d
# decrypts my-file.json and write the unencrypted data to _decrypted_my-file.json.
```
> This is an optional step in case you want to decode your encrypted data explicitly for manual checking. Program decrypts your encrypted config file automatically.
