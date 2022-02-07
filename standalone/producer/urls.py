from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("lti/", include("ltiproducer.urls")),
    path("admin/", admin.site.urls),
]

# Automatically load urls from the LTI_PRODUCER_URLS setting
for app, urls_module in settings.LTI_PRODUCER_URLS.items():
    urlpatterns.append(
        path(f"{app}/", include(f"{urls_module}")),
    )

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
