from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter # routing

from blog.api.views import (
  PostList, 
  PostDetail, 
  UserDetail, 
  TagViewSet,
  PostViewSet,
)

from django.urls import path, include

# Swagger
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import os


urlpatterns = [
    # Removed paths using views (we'll use the viewSet)
    #path("posts/", PostList.as_view(), name="api_post_list"),
    #path("posts/<int:pk>", PostDetail.as_view(), name="api_post_detail"),
    path("users/<str:email>", UserDetail.as_view(), name="api_user_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# updated below
# urlpatterns += [
#     path("auth/", include("rest_framework.urls")),
#     path("token-auth/", views.obtain_auth_token)
# ]

# customizing API html view 
schema_view = get_schema_view(
    openapi.Info(
        title="Blango API",
        default_version="v1",
        description="API for Blango Blog",
    ),
    url=f"https://{os.environ.get('CODIO_HOSTNAME')}-8000.codio.io/api/v1/",
    public=True,
)

# Using swagger UI 
urlpatterns += [
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", views.obtain_auth_token),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

# router for tags
router = DefaultRouter()
router.register("tags", TagViewSet)   # registering tags 
router.register("posts", PostViewSet) # registering posts 

urlpatterns += [
    path("", include(router.urls)),
]