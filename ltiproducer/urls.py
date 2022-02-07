from django.urls import path

from . import views

urlpatterns = [
    # LTI launch request handler
    path(
        "1.1/launch",
        views.Lti11LaunchView.as_view(),
        name="lti11.launch",
    ),
]
