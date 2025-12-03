from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def validate(self, attrs):
        required_fields = ["description", "amount", "type", "date"]

        for field in required_fields:
            if field not in attrs or attrs[field] in [None, ""]:
                raise serializers.ValidationError({field: f"{field} is required."})

        return attrs

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("amount must be greater than zero.")
        return value

    def validate_type(self, value):
        if value not in ["income", "expense"]:
            raise serializers.ValidationError("type must be 'income' or 'expense'.")
        return value
