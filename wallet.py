from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
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

    def sign_transaction(self, sender, recipient, amount):
        signer = PKCS1_v1_5.new(self.__import_key__(self.private_key))
        h = self.__generate_hash__(sender, recipient, amount)
        signature = signer.sign(h)

        return binascii.hexlify(signature).decode('ascii')

    @classmethod
    def verify_transaction(cls, transaction):
        pub_key = cls.__import_key__(transaction.sender)
        verifier = PKCS1_v1_5.new(pub_key)
        h = cls.__generate_hash__(
            transaction.sender, transaction.recipient, transaction.amount)

        return verifier.verify(h, binascii.unhexlify(transaction.signature))

    @staticmethod
    def __import_key__(key):
        return RSA.importKey(
            binascii.unhexlify(key))

    @staticmethod
    def __generate_hash__(sender, recipient, amount):
        return SHA256.new((str(sender) + str(recipient) + str(amount)).encode())
