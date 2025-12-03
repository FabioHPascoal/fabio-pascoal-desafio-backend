from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction
from .serializers import TransactionSerializer

# ------------------------------------------------------
# 1. Create new transaction
# 2. List all transactions
#      Endpoint: /transactions/
# ------------------------------------------------------
@api_view(['GET', 'POST'])
def transaction_list(request):

    # Post - Create new transaction
    if request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # GET - List all transactions
    if request.method == 'GET':
        transactions = Transaction.objects.all()

        description = request.query_params.get("description")
        type_filter = request.query_params.get("type")

        if description:
            transactions = transactions.filter(description__icontains=description)

        if type_filter:
            transactions = transactions.filter(type=type_filter)

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ------------------------------------------------------
# 3. Get specific transaction
# 4. Update transaction
# 5. Delete transaction
#      Endpoint: /transactions/<id>/
# ------------------------------------------------------
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def transaction_detail(request, id):
    try:
        transaction = Transaction.objects.get(pk=id)
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found."},
                        status=status.HTTP_404_NOT_FOUND)

    # GET - Get specific transaction
    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT - Update transaction
    if request.method in ['PUT', 'PATCH']:
        serializer = TransactionSerializer(transaction, data=request.data, partial=(request.method == 'PATCH'))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE - Delete transaction
    if request.method == 'DELETE':
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
