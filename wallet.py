from Crypto.PublicKey import RSA
import Crypto.Random
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        if self.public_key is None and self.private_key is None:
            return
            
        try:
            with open('wallet.txt', 'w') as file:
                file.write(self.public_key)
                file.write('\n')
                file.write(self.private_key)
        except (IOError, IndexError):
            print('Saving wallet failed')

    def load_keys(self):
        try:
            with open('wallet.txt') as file:
                keys = file.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
        except (IOError, IndexError):
            print('Loading wallet failed')

    def generate_keys(self):
        priv_key = RSA.generate(1024, Crypto.Random.new().read)
        pub_key = priv_key.publickey()

        return (
            binascii.hexlify(priv_key.exportKey(format='DER')).decode('ascii'),
            binascii.hexlify(pub_key.exportKey(format='DER')).decode('ascii'),
        )
