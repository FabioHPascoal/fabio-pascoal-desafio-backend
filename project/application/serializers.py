from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer responsible for converting Transaction model instances
    to and from JSON representations.

    The `user` field is read-only and is automatically set to the
    authenticated user in the view layer.
    """

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        """
        Meta configuration for the TransactionSerializer.

        Attributes:
            model (Transaction): The model associated with this serializer.
            fields (list[str]): Fields to include in the serialized output.
        """
        model = Transaction
        fields = ["id", "user", "description", "amount", "type", "date"]

    def validate(self, attrs):
        """
        Performs general validation for required fields.

        Ensures that all required fields are present when creating a new
        transaction and that no field is null or empty.

        Args:
            attrs (dict): The serializer input data.

        Returns:
            dict: The validated and cleaned attributes.

        Raises:
            serializers.ValidationError: If any required field is missing
            or empty.
        """
        required_fields = ["description", "amount", "type", "date"]

        for field in required_fields:
            # Creating a new instance -> all fields required
            if self.instance is None and field not in attrs:
                raise serializers.ValidationError({field: f"{field} is required."})

            # Updating existing instance -> field provided but invalid
            if field in attrs and attrs[field] in [None, ""]:
                raise serializers.ValidationError({field: f"{field} is required."})

        return attrs

    def validate_amount(self, value):
        """
        Validates the `amount` field.

        Ensures that the amount is strictly greater than zero.

        Args:
            value (Decimal): The monetary amount.

        Returns:
            Decimal: The validated amount.

        Raises:
            serializers.ValidationError: If amount is zero or negative.
        """
        if value <= 0:
            raise serializers.ValidationError("amount must be greater than zero.")
        return value

    def validate_type(self, value):
        """
        Validates the `type` field.

        Ensures that the transaction type is one of the allowed values:
        'income' or 'expense'.

        Args:
            value (str): The transaction type.

        Returns:
            str: The validated type.

        Raises:
            serializers.ValidationError: If type is not allowed.
        """
        if value not in ["income", "expense"]:
            raise serializers.ValidationError("type must be 'income' or 'expense'.")
        return value
