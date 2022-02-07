"""
This entire module is strongly inspired by the demo consumer from lti_toolbox.sandbox.views.
"""

from typing import Any, Dict
from urllib.parse import unquote

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from oauthlib import oauth1


def consumer(request: HttpRequest) -> HttpResponse:
    """
    LTI consumer landing page.

    The LTI parameters defined in the Django setting will be forwarded to the
    LTI producer from inside an iframe.
    """
    user_id = settings.LTI_USER_ID
    lti_parameters = {
        "lti_message_type": "basic-lti-launch-request",
        "lti_version": "LTI-1p0",
        "resource_link_id": settings.LTI_RESOURCE_LINK_ID,
        "launch_presentation_locale": settings.LTI_LOCALE,
        "lis_person_contact_email_primary": settings.LTI_USER_EMAIL,
        "lis_person_sourcedid": user_id,
        "user_id": user_id,
        "context_id": settings.LTI_CONTEXT_ID,
        "context_title": settings.LTI_CONTEXT_TITLE,
        "roles": settings.LTI_ROLE,
    }
    lti_parameters.update(settings.LTI_EXTRA_PARAMETERS)
    launch_url = settings.LTI_LAUNCH_URL
    sign_parameters(launch_url, lti_parameters, settings.LTI_KEY, settings.LTI_SECRET)
    return render(
        request,
        "consumer/iframe.html",
        {"lti_params": lti_parameters, "launch_url": launch_url},
    )


def sign_parameters(
    url: str, parameters: Dict[str, Any], key: str, secret: str
) -> None:
    """
    OAuth1-sign url/parameters with key/secret.

    Note: this function should probably be part of lti_toolbox.
    """
    oauth_client = oauth1.Client(client_key=key, client_secret=secret)
    _uri, headers, _body = oauth_client.sign(
        url,
        http_method="POST",
        body=parameters,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    # Parse headers to pass to template as part of context:
    oauth_dict = dict(
        param.strip().replace('"', "").split("=")
        for param in headers["Authorization"].split(",")
    )

    signature = oauth_dict["oauth_signature"]
    oauth_dict["oauth_signature"] = unquote(signature)
    oauth_dict["oauth_nonce"] = oauth_dict.pop("OAuth oauth_nonce")
    parameters.update(oauth_dict)
