from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import viewsets, status
from .models import Product
from .serializers import ProductSerializer
from decimal import Decimal, InvalidOperation

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
    
    # get the products by price range.
    @action(detail=False, methods=["get"], url_path="by-price")
    def by_price(self, request):

        print(request.query_params)
        print(request.query_params.dict())

        from_price = request.query_params.get("from_price")
        to_price = request.query_params.get("to_price")

        print("From Price: ", from_price, ", To Price: ", to_price)

        filters = {
            "is_deleted": False
        }

        try:
            if from_price:
                filters["price__gte"] = Decimal(from_price)

            if to_price:
                filters["price__lte"] = Decimal(to_price)

        except InvalidOperation:
            return Response(
                {"error": "from_price and to_price must be valid numbers"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not from_price and not to_price:
            return Response(
                {
                    "error": "At least one query parameter (from_price or to_price) is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        products = Product.objects.filter(**filters)

        print(products.query)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    

@api_view(["POST"])
def restore_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    product.is_deleted = False
    product.deleted_at = None
    product.save()

    return Response({"message": "Product restored"})