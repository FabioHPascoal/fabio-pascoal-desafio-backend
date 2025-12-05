from django.conf import settings
from django.db import models

class Transaction(models.Model):
    """
    Represents a financial transaction belonging to a user.

    Attributes:
        user (User): The owner of the transaction.
        description (str): A short text describing the transaction.
        amount (Decimal): The monetary value.
        type (str): Either 'income' or 'expense'.
        date (date): The date the transaction occurred.
    """
    
    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.description} - {self.amount}"
