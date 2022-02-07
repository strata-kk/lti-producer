from django.urls import path

import views  # pylint: disable=import-error

urlpatterns = [
    path("", views.consumer),
]
