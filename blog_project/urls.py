from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from schema_graph.views import Schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogs.urls')),
    path('', include('contactus.urls')),
    path('', include('about_us.urls')),
    path("schema/", Schema.as_view()),
    path('admin_tools_stats/', include('admin_tools_stats.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
