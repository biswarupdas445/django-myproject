from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    # queryset = Product.objects.all()
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer


    # Override the delete operations
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        product.is_deleted = False
        product.deleted_at = None
        product.save()
        return Response({"message": "Product restored"})