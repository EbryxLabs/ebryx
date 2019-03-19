# Installation
You can grab the latest .whl file from repository and install it via pip or just simply type:
```
pip install ebryx
```
If you want build from source code, then.
```
git clone https://github.com/EbryxLabs/ebryx
cd ebryx/
python setup.py install
```
You will have a package named **`ebryx`** installed for your python.

# Encryption / Decryption
You can encrypt / decrypt data using `ebcrypt` tool. **(AES-256 Encryption)**

For example, to encrypt you can do following:
```
ebcrypt <my-file.json> -e --new
# encrypts myfile.json using newly created crypto-secure key. Keys will be written to _keys file.

ebcrypt <my-file.json> -e
# encrypts using keys in AES_KEY, AES_IV environment variable.
```

For decryption, you'll need to have `AES_KEY` and `AES_IV` keys in your environment variables.
```
ebcrypt <my-file.json> -d
```
> This is an optional step in case you want to decode your encrypted data explicitly for manual checking. Program decrypts your encrypted config file automatically.

You can get detailed help on crypto tool by typing.
```
ebcrypt -h
```

## OpenSSL compatibility
Encryption done by openssl utility can be decrypted by `ebcrypt` utility and vice versa. For example, you can encrypt using openssl as follows.
```
openssl aes-256-cbc -a -e -K <hex-key> -iv <hex-iv> -in <input-file> -out <output-file>
```
`hex-key` and `hex-iv` should be replaced with actual keys in hex format. Using the same keys you used in openssl, you can decrypt using `ebcrypt` as follows.
```
ebcrypt <encrypted-file> -d
# AES_KEY environment variable should hold <hex-key>.
# AES_IV environment variable should hold <hex-iv>.
```
Similarly, you can encrypt using `ebcrypt` and decrypt the content using openssl, given that you're using the same keys.

# Code Usage
You can also use it in your own code by importing the appropriate module.
```
# import main module.
import ebryx 

# import crypto submodule.
from ebryx import crypto
```
