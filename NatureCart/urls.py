"""
URL configuration for NatureCart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Customer_app.urls')),
    path('', include('Seller_app.urls')),
]

def case_insensitive_serve(request, path, document_root=None, **kwargs):
    import os
    from django.views.static import serve
    if document_root:
        full_path = os.path.join(document_root, path)
        if not os.path.exists(full_path):
            dir_name = os.path.dirname(full_path)
            base_name = os.path.basename(full_path).lower()
            if os.path.isdir(dir_name):
                for filename in os.listdir(dir_name):
                    if filename.lower() == base_name:
                        # Reconstruct path using the correct case on disk
                        path = os.path.join(os.path.dirname(path), filename).replace('\\', '/')
                        break
    return serve(request, path, document_root=document_root, **kwargs)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', case_insensitive_serve, {'document_root': settings.MEDIA_ROOT}),
    ]


