# Initialize blockchain list
blockchain = [[0]]
open_tansactions = []
owner = "Robinson"


def get_last_blockchain_value():
    """ Return the last value of the current blockchain."""
    if len(blockchain) >= 1:
        return blockchain[-1]
    return [1]


def add_transaction(recipient, amount = 1.0, sender = owner):
    """ Return the last value of the current blockchain.
        Arguments:
            :sender: The sender of the coins
            :recipient: The recipient of the coins
            :amount: Amount of coins. Default to 1.0
    """

    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
    }
    open_tansactions.append(transaction)



def mine_block():
    pass

def get_transaction_value():
    """ Returns a tuple(tx_recipient, tx_amount) with the information for a transaction"""
    tx_recipient =  input('Please, the name of the recipient: ')
    tx_amount = float(input('Your transaction amount please: '))

    return tx_recipient, tx_amount #could be also like parethesis (tx_recipient, tx_amount)


def get_user_choice():
    user_option = input('Your choice: ')
    return user_option


def print_blockchain_elements():
    # Output blockchain list to console
    for block in blockchain:
        print('Outputing Blocks:')
        print(block)


def verify_chain():
    is_valid = True
    
    for index in range(len(blockchain)):
        block = blockchain[index]
        if index == 0:
            continue

        if block[0] != blockchain[index - 1]:
            is_valid = False
            break
    else:
        print("-" * 40)

    # Without range
    # index = 0
    # for block in blockchain:
    #     if index == 0:
    #         index += 1
    #         continue

    #     if block[0] != blockchain[index - 1]:
    #         is_valid = False
    #         break

    #     index += 1
    # else:
    #     print("-" * 40)

    return is_valid


def display_wrong_option_message():
    print('--------Input invalid, please pick a value from list--------')


waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add new transaction value')
    print('2: Output blockchain blocks')
    print('Q: Exit the program')
    print('H: Manipulate the chain')
    option = get_user_choice()

    try:
        if option.isnumeric() and int(option) == 1:
            recipient, amount  = get_transaction_value()
            # last_value = get_last_blockchain_value()

            add_transaction(recipient, amount)
            print(open_tansactions)
        elif option.isnumeric() and int(option) == 2:
            print_blockchain_elements()
        elif option == 'H' or option == 'q':
            if len(blockchain) >= 1:
                blockchain[0] = [2]
        elif option == 'Q' or option == 'h':
            waiting_for_input = False
        else:
            display_wrong_option_message()

        if not verify_chain():
            print('Invalid blockchain!')
            break

    except ValueError:
        display_wrong_option_message()

else:
    print('User left')


print('Done!')

print(blockchain)
