
from django.contrib import admin

from django.urls import path, include
# from rest_framework.authtoken import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path

from paza.views import addInDiscussion, addInForum
# from Discussion_forum.views import *



schema_view = get_schema_view(
   openapi.Info(
      title="PAZA",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@Paza.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)







urlpatterns = [
   path('admin/', admin.site.urls),
   path('api-auth/', include('api.auth_api.urls')),
   path('api/',include('api.urls')),
   path('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('^redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('addInForum/',addInForum,name='addInForum'),
   path('addInDiscussion/',addInDiscussion,name='addInDiscussion')

]
