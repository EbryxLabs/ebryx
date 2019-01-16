# Installation
Download either the source code or .whl file from latest release and install using pip or python.
```
pip install ebryx-x.x-py3-none-any.whl
```
If you want build from source code, then.
```
cd /path/to/repo/code/
python setup.py install
```
You will have a package named **`ebryx`** installed for your python.

## Encryption / Decryption
You can encrypt / decrypt data using `ebcrypt` tool. **(AES-256 Encryption)**

For example, to encrypt you can do following:
```
ebcrypt <my-file.json> -e --new
# encrypts myfile.json using newly created crypto-secure key. Keys will be written to _keys file.

ebcrypt <my-file.json> -e
# encrypts using keys in AES_KEY environment variable.
# If your input file is myfile.json, encrypted file will be _myfile.json
```

For decryption, you'll need to have `AES_KEY` keys in your environment variables.
```
ebcrypt <my-file.json> -d
# decrypts my-file.json and write the unencrypted data to _decrypted_my-file.json.
```
> This is an optional step in case you want to decode your encrypted data explicitly for manual checking. Program decrypts your encrypted config file automatically.

You can get detailed help on crypto tool by typing.
```
ebcrypt -h
```

## Code Usage
You can also use it in your own code by importing the appropriate module.
```
# import main module.
import ebryx 

# import crypto submodule.
from ebryx import crypto
```
