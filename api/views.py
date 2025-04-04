from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet

from api.serializers import (OrderCreateSerializer, OrderReadSerializer,
                             OrderUpdateSerializer, SalesRevenueSerializer)
from orders.models import Order


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer
    http_method_names = ['get', 'post',
                         'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('table_number', 'status')

    def get_serializer_class(self):
        """Select the suitable serializer for the request method."""
        if self.request.method == 'POST':
            return OrderCreateSerializer
        if self.request.method == 'PATCH':
            return OrderUpdateSerializer
        return OrderReadSerializer

    @action(methods=['get'], detail=False)
    def sales_revenue(self, request: Request) -> Response:
        """
        Get sales revenue.

        Query parameters:
            1) from_date (string represents date, format %Y-%m-%d);
            2) to_date (string represents date, format %Y-%m-%d).
        """
        try:
            sales_revenue_period = {
                'from_date': request.query_params.get('from_date'),
                'to_date': request.query_params.get('to_date'),
            }

            serializer = SalesRevenueSerializer(data=sales_revenue_period)
            if serializer.is_valid(raise_exception=True):
                return Response(
                    serializer.data, status=status.HTTP_200_OK
                )
        except ValidationError as e:
            return Response(
                {'Validation Error': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
