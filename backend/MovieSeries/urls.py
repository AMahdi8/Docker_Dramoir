"""
URL configuration for MovieSeries project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from movie.views import HomePageView
from django.views.static import serve

schema_view = get_schema_view(
    openapi.Info(
        title="Dramoir API Documentation",
        default_version='v1',
        description="""
## Authentication
This API uses JWT (JSON Web Token) for authentication.

### How to authenticate:
1. First, obtain tokens by sending a POST request to `/auth/login/` with your email and password.
2. You will receive `access` and `refresh` tokens in the response.
3. For protected endpoints, include the access token in the Authorization header:
   ```
   Authorization: Bearer {your_access_token}
   ```

### Headers for authenticated requests:
- **GET requests**: `Authorization: Bearer {your_access_token}`
- **POST requests**: `Authorization: Bearer {your_access_token}` and `Content-Type: application/json`
- **PUT/PATCH requests**: `Authorization: Bearer {your_access_token}` and `Content-Type: application/json`
- **DELETE requests**: `Authorization: Bearer {your_access_token}`

### Token refresh:
- If your access token expires, send a POST request to `/auth/token/refresh/` with your refresh token to get a new access token.
- Example: `{"refresh": "your_refresh_token"}`
        """,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('main/', include('movie.urls')),
    path('review/', include('review.urls')),
    path('auth/', include('authentication.urls')),
    path('ticket/', include('ticket.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
