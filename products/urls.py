from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, restore_product

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),


    # Custom route
    path(
        'products/restore/<int:pk>/',
        restore_product,
        name='restore-product'
    ),
]