from django.db.models import Q
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.prefetch_related('positions__product').all()
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        products = self.request.query_params.get('products')
        if products:
            queryset = queryset.filter(positions__product_id=products).distinct()

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(positions__product__title__icontains=search)
                | Q(positions__product__description__icontains=search)
            ).distinct()

        return queryset
