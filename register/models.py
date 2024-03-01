from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    """
    Account model for storing user account information.

    Attributes:
    - user: OneToOneField to User model
    - balance: DecimalField to store account balance
    - CURRENCY_CHOICES: Tuple of tuples to store currency choices
    - currency: CharField to store currency type
    - created_at: DateTimeField to store account creation date
    - STATUS_CHOICES: Tuple of tuples to store account status choices
    - status: CharField to store account status

    Methods:
    - __str__: Returns the username of the user linked to the account

    """
    class Meta:
        db_table = 'account'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, related_name='account')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    CURRENCY_CHOICES = (
        ('gdp','GBP'),
        ('usd', 'USD'),
        ('eur', 'EUR'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='gdp')
    created_at = models.DateTimeField(auto_now_add=True) #
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        """
        Returns the username of the user linked to the account.

        :return: str: The username of the user linked to the account
        """
        return self.user.username

    def change_balance(self, amount):
        """
    Modifies the account balance by a specified amount. The amount can be positive (for deposits)
    or negative (for withdrawals).

    :param amount: The amount to adjust the balance by. Can be positive or negative.
    :type amount: Decimal

    :return: The updated account balance after applying the change.
    :rtype: Decimal
    """
        self.balance += amount
        self.save()
        return self.balance


class Transaction(models.Model):
    """
    Transaction model for storing transaction information.

    Attributes:
    - sender: ForeignKey to Account model for the sender account
    - receiver: ForeignKey to Account model for the receiver account
    - amount: DecimalField to store transaction amount
    - created_at: DateTimeField to store transaction creation date

    Methods:
    - __str__: Returns the transaction type and amount


    """
    class Meta:
        db_table = 'transaction'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    sender = models.ForeignKey(Account, on_delete=models.CASCADE,
                               related_name='sent_transactions')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE,
                                 related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns the transaction type and amount.

        :return: str: The transaction type and amount
        """
        return f'{self.sender.user.username} sent {self.amount} to {self.receiver.user.username}'


class Request(models.Model):
    """
    Request model for storing request information.

    Attributes:
    - sender: ForeignKey to Account model for the sender account
    - receiver: ForeignKey to Account model for the receiver account
    - amount: DecimalField to store request amount
    - created_at: DateTimeField to store request creation date

    Methods:
    - __str__: Returns the request type and amount
    - accept_request: Accepts a request and transfers the requested amount from the receiver's account to the
     sender's account
    - decline_request: Declines a request and deletes the request from the database


    """

    class Meta:
        db_table = 'request'
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'

    sender = models.ForeignKey(Account, on_delete=models.CASCADE,
                               related_name='sent_requests')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE,
                                 related_name='received_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns the request type and amount.

        :return: str: The request type and amount
        """
        return f'{self.sender.user.username} requested {self.amount} from {self.receiver.user.username}'

    def accept_request(self):
        """
        Accepts a request and transfers the requested amount from the receiver's account to the sender's account.

        :return: The updated account balance of the sender's account after the transfer.
        :rtype: Decimal
        """
        self.sender.change_balance(self.amount)
        self.receiver.change_balance(-self.amount)
        self.delete()
        return self.sender.balance

    def decline_request(self):
        """
        Declines a request and deletes the request from the database.

        :return: None
        """
        self.delete()
        return None

