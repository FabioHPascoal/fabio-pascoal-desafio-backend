from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Transaction
from .serializers import TransactionSerializer
from .pagination import TransactionPagination

# ------------------------------------------------------
# 1. Create new transaction
# 2. List all transactions
#      Endpoint: /transactions/
# ------------------------------------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def transaction_list(request):

    # POST - Create new transaction
    if request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # GET - List all transactions
    if request.method == 'GET':
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')

        description = request.query_params.get("description")
        type_filter = request.query_params.get("type")

        if description:
            transactions = transactions.filter(description__icontains=description)

        if type_filter:
            transactions = transactions.filter(type=type_filter)

        # pagination
        paginator = TransactionPagination()
        page = paginator.paginate_queryset(transactions, request)
        if page is not None:
            serializer = TransactionSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # fallback
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ------------------------------------------------------
# 3. Get specific transaction
# 4. Update transaction
# 5. Delete transaction
#      Endpoint: /transactions/<id>/
# ------------------------------------------------------
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def transaction_detail(request, id):
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)

    # GET - Get specific transaction
    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT - Update transaction
    if request.method in ['PUT', 'PATCH']:
        partial = (request.method == 'PATCH')
        serializer = TransactionSerializer(transaction, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE - Delete transaction
    if request.method == 'DELETE':
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------------
# 6. Get summary of all transactions
#      Endpoint: /summary/
# ------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_summary(request):
    # GET - Get summary of all transactions from the authenticated user
    if request.method == 'GET':
        transactions = Transaction.objects.filter(user=request.user)
        total_income = 0
        total_expense = 0
        for tran in transactions:
            if tran.type == "income":
                total_income += tran.amount
            elif tran.type == "expense":
                total_expense += tran.amount
        summary = {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': total_income - total_expense
        }
        return Response(summary, status=status.HTTP_200_OK)