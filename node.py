from uuid import uuid4

from blockchain import Blockchain
from wallet import Wallet
from utility.verification import Verification


class Node:
    def __init__(self):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def display_wrong_option_message(self):
        print('--------Input invalid, please pick a value from list--------')

    def get_transaction_value(self):
        """ Returns a tuple(tx_recipient, tx_amount) with the information for a transaction"""
        tx_recipient = input('Please, the name of the recipient: ')
        tx_amount = float(input('Your transaction amount please: '))

        # could be also like parethesis (tx_recipient, tx_amount)
        return tx_recipient, tx_amount

    def get_user_choice(self):
        user_option = input('Your choice: ')
        return user_option

    def print_blockchain_elements(self):
        # Output blockchain list to console
        for block in self.blockchain.chain:
            print('Outputing Blocks:')
            print(block)

    def listen_for_input(self):
        waiting_for_input = True

        while waiting_for_input:
            print('Please choose')
            print('1: Add new transaction value')
            print('2: Mine block')
            print('3: Output blockchain blocks')
            print('4: Check transaction validity')
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save wallet keys')
            print('Q: Exit the program')
            option = self.get_user_choice()

            try:
                if option.isnumeric() and int(option) == 1:
                    recipient, amount = self.get_transaction_value()
                    signature = self.wallet.sign_transaction(
                        self.wallet.public_key, recipient, amount)
                    if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount):
                        print('Added transaction')
                    else:
                        print('Transaction Fail')
                elif option.isnumeric() and int(option) == 2:
                    if not self.blockchain.mine_block():
                        print('Mining failed. Got no wallet?')
                elif option.isnumeric() and int(option) == 3:
                    self.print_blockchain_elements()
                elif option.isnumeric() and int(option) == 4:
                    if Verification.verify_transactions(self.blockchain.open_tansactions, self.blockchain.get_balance):
                        print('All transactions are valid!')
                    else:
                        print('There are invalid transactions!')
                elif option.isnumeric() and int(option) == 5:
                    self.wallet.create_keys()
                    self.blockchain = Blockchain(self.wallet.public_key)
                elif option.isnumeric() and int(option) == 6:
                    self.wallet.load_keys()
                    self.blockchain = Blockchain(self.wallet.public_key)
                elif option.isnumeric() and int(option) == 7:
                    self.wallet.save_keys()
                elif option == 'Q' or option == 'q':
                    waiting_for_input = False
                else:
                    self.display_wrong_option_message()

                if not Verification.verify_chain(self.blockchain.chain):
                    print('Invalid blockchain!')
                    break

                print(
                    f'Balance of {self.wallet.public_key}: {self.blockchain.get_balance():6.2f}')

            except ValueError:
                self.display_wrong_option_message()
        else:
            print('User left')
        print('Done!')


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()

print(__name__)
