import os
import string
import logging
import random
import argparse
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


KEY_LENGTH = 32
IV_LENGTH = 16

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
        string.ascii_uppercase + string.digits)
        for _ in range(size)).encode('utf8')


def adjust_padding(data, block_size, unpad=False):

    if not unpad:
        padder = padding.PKCS7(block_size * 8).padder()
        padded_data = padder.update(data.encode('utf8'))
        padded_data += padder.finalize()
        return padded_data

    unpadder = padding.PKCS7(block_size * 8).unpadder()
    data = unpadder.update(data)
    data += unpadder.finalize()
    return data.decode('utf8')


def encrypt_file(params):

    filename = params.file
    if not os.path.isfile(filename):
        exit('File doesn\'t exist: %s' % (filename))

    if params.new:
        aes_key = get_random_string(KEY_LENGTH)
        aes_key += b'-' + get_random_string(IV_LENGTH)

    else:
        if not os.environ.get('AES_KEY'):
            exit('`AES_KEY` doesn\'t exist in environment variables.')

        aes_key = os.environ.get('AES_KEY').encode('utf8')
        if len(aes_key.split(b'-')) != 2:
            exit('Invalid AES key detected.')

    content = open(filename, 'r').read()
    content = adjust_padding(content, KEY_LENGTH)
    cipher = Cipher(
        algorithms.AES(aes_key.split(b'-')[0]),
        modes.CBC(aes_key.split(b'-')[-1]),
        backend=default_backend())

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(content) + encryptor.finalize()

    open('_' + filename, 'wb').write(ciphertext)
    open('_keys', 'wb').writelines([b'export AES_KEY=%s\n' % (aes_key)])

    logger.info('Successfully encrypted file in: %s' % ('_' + filename))
    logger.info('Encryption keys can be found in: %s' % ('_keys'))


def decrypt_file(filename, write_to_file=True, is_ciphertext=False):

    if not os.environ.get('AES_KEY'):
        exit('`AES_KEY` doesn\'t exist in environment variables.')
    aes_key = os.environ.get('AES_KEY').encode('utf8')

    if not is_ciphertext:
        if not os.path.isfile(filename):
            exit('File doesn\'t exist: %s' % (filename))
        ciphertext = open(filename, 'rb').read()

    else:
        ciphertext = filename

    cipher = Cipher(
        algorithms.AES(aes_key.split(b'-')[0]),
        modes.CBC(aes_key.split(b'-')[-1]),
        backend=default_backend())

    decryptor = cipher.decryptor()
    content = decryptor.update(ciphertext) + decryptor.finalize()
    content = adjust_padding(content, KEY_LENGTH, unpad=True)

    if write_to_file and not is_ciphertext:
        open('_decrypted_' + filename, 'w').write(content)
        logger.info('Successfully decrypted file in: %s' % (
            '_decrypted_' + filename))

    else:
        return content


def main():
    params = define_params()

    if params.e:
        encrypt_file(params)
    elif params.d:
        decrypt_file(params.file)


if __name__ == "__main__":
    main()
