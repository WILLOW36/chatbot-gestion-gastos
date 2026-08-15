from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    # API de conductores.
    path("api/drivers/", include("drivers.urls")),

    # API de gastos.
    path("api/expenses/", include("expenses.urls")),

    # API de conversaciones.
    path("api/conversations/", include("conversations.urls")),
]


# Permite servir archivos multimedia durante el desarrollo local.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )