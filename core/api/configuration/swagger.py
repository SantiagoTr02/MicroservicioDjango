from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MicroService Genomic",
        default_version='v1',
        description="Microservice for analytics and treatment of data",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="trianacarvajalsantiago@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)