from rest_framework.pagination import PageNumberPagination

class TransactionPagination(PageNumberPagination):
    """
    Custom pagination class for Transaction endpoints.

    This paginator controls how transaction records are divided into pages
    when retrieving large datasets. It supports specifying a custom page size
    via query parameters.

    Attributes:
        page_size (int): Default number of items returned per page.
        page_size_query_param (str): Name of the query parameter that allows
            the client to define a custom page size (e.g., `?size=20`).
        max_page_size (int): Maximum allowed number of items per page to
            prevent excessive load on the API.
    """

    page_size = 10
    page_size_query_param = "size"
    max_page_size = 50
