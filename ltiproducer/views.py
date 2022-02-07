import logging

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from lti_toolbox.exceptions import LTIException
from lti_toolbox.lti import LTI

from ltiproducer.params import LtiParams

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class Lti11LaunchView(View):
    @xframe_options_exempt
    def post(self, request: HttpRequest) -> HttpResponse:
        """Handler for POST requests."""
        lti = LTI(request)
        try:
            lti.verify()
        except LTIException as error:
            logger.debug(error)
            return HttpResponseForbidden("Invalid LTI launch request")

        lti_params = LtiParams(lti._params)  # pylint: disable=protected-access
        lti_session_id = lti_params.save_to_session(request.session)

        # Redirect to the right LTI producer app
        app_name = lti.get_param(settings.LTI_APP_NAME_KEY)
        if not app_name:
            return HttpResponse(
                f"Missing LTI app parameter: '{settings.LTI_APP_NAME_KEY}'", status=400
            )
        try:
            view_name = settings.LTI_LAUNCH_VIEWS[app_name]
        except KeyError:
            return HttpResponse("Invalid LTI app: {app_name}", status=400)

        return redirect(view_name, lti_session_id=lti_session_id)
