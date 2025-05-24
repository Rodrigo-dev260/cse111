def deposit(amount):
    # In order to this program to work correctly and
    # for the bank records to becorrect, we most not
    # allow someone to deposit a zero or negative amount.
    assert amount > 0