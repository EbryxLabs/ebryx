import os
import codecs
import base64
import string
import random
import logging
import argparse
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


KEY_LENGTH = 32
IV_LENGTH = 16
BLOCK_SIZE = 128

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handle = logging.StreamHandler()
handle.setLevel(logging.INFO)
handle.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
logger.addHandler(handle)


def define_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='path to file that you want to target.')
    parser.add_argument('-e', action='store_true',
                        help='encrypts the provided file.')
    parser.add_argument('-d', action='store_true',
                        help='decrypts the provided file.')
    parser.add_argument('--new', action='store_true', help='creates new ' +
                        'random keys in case of encryption.')

    return parser.parse_args()


# use this to generate new random keys.
def get_random_string(size):
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(size)) \
        .encode('utf8')


def adjust_padding(data, block_size, unpad=False):

    if not unpad:
        padder = padding.PKCS7(block_size).padder()
        padded_data = padder.update(data.encode('utf8'))
        padded_data += padder.finalize()
        return padded_data

    unpadder = padding.PKCS7(block_size).unpadder()
    data = unpadder.update(data)
    data += unpadder.finalize()
    return data.decode('utf8')


def encrypt_file(filename, new_keys=False):
    '''
    encrypts file.

    params
    ------
    filename: str
        path to filename to encrypt.

    new_keys: bool (default: False)
        creates new AES key if True, otherwise expects it from
        AES_KEY environment variable.
    '''

    if not os.path.isfile(filename):
        exit('File doesn\'t exist: %s' % (filename))

    if new_keys:
        aes_key = get_random_string(KEY_LENGTH)
        aes_iv = get_random_string(IV_LENGTH)

    else:
        if not os.environ.get('AES_KEY'):
            exit('`AES_KEY` doesn\'t exist in environment variables.')
        if not os.environ.get('AES_IV'):
            exit('`AES_IV` doesn\'t exist in environment variables.')

        aes_key = os.environ.get('AES_KEY').encode('utf8')
        aes_iv = os.environ.get('AES_IV').encode('utf8')

        try:
            aes_key = codecs.decode(aes_key, 'hex')
            aes_iv = codecs.decode(aes_iv, 'hex')
        except Exception as exc:
            exit('Could not convert hex keys to string.')

        if len(aes_key) != KEY_LENGTH or len(aes_iv) != IV_LENGTH:
            exit('Invalid AES key/iv detected.')

    content = open(filename, 'r').read()
    content = adjust_padding(content, BLOCK_SIZE)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(content) + encryptor.finalize()
    ciphertext = base64.b64encode(ciphertext)

    name, ext = os.path.splitext(filename)
    filename = filename + '.enc' if ext != '.enc' else name + '.enc'
    open(filename, 'wb').write(ciphertext + b'\n')
    open('_keys', 'w').writelines([
        'export AES_KEY=%s\n' % (aes_key.hex()),
        'export AES_IV=%s\n' % (aes_iv.hex())
    ])

    logger.info('Successfully encrypted file in: %s', filename)
    logger.info('Encryption keys can be found in: %s', '_keys')


def decrypt_file(filename, write_to_file=True, is_ciphertext=False):
    '''
    decrypts file.

    params
    ------
    filename: str
        path to filename to decrypt.

    write_to_file: bool (default: True)
        writes decrypted content to '_' + filename if True.
        Otherwise, prints to std.

    is_ciphertext: bool (default: False)
        skips reading filename and consider it a text string
        if True, otherwise reads file. 

    returns
    -------
    str
        if write_to_file is False
    '''

    if not os.environ.get('AES_KEY'):
        exit('`AES_KEY` doesn\'t exist in environment variables.')
    if not os.environ.get('AES_IV'):
        exit('`AES_IV` doesn\'t exist in environment variables.')

    aes_key = os.environ.get('AES_KEY').encode('utf8')
    aes_iv = os.environ.get('AES_IV').encode('utf8')

    try:
        aes_key = codecs.decode(aes_key, 'hex')
        aes_iv = codecs.decode(aes_iv, 'hex')
    except Exception as exc:
        exit('Could not convert hex keys to string.')

    if not is_ciphertext:
        if not os.path.isfile(filename):
            exit('File doesn\'t exist: %s' % (filename))
        ciphertext = open(filename, 'rb').read()

    else:
        ciphertext = filename

    ciphertext = base64.b64decode(ciphertext)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv),
                    backend=default_backend())

    decryptor = cipher.decryptor()
    try:
        content = decryptor.update(ciphertext) + decryptor.finalize()
    except ValueError as exc:
        exit('ValueError: %s\n' % (str(exc)))

    content = adjust_padding(content, BLOCK_SIZE, unpad=True)

    if write_to_file and not is_ciphertext:
        name, ext = os.path.splitext(filename)
        filename = name + '.dec' if ext != '.dec' else name
        open(filename, 'w').write(content)
        logger.info('Successfully decrypted file in: %s', filename)
    else:
        return content


def main():
    params = define_params()

    if params.e:
        encrypt_file(params.file, params.new)
    elif params.d:
        decrypt_file(params.file)
