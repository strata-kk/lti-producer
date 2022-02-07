import typing as t

from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from .params import LtiParams


class HttpLtiRequest(HttpRequest):
    lti_params: LtiParams
    lti_session_id: str


View = t.Callable[[HttpRequest, t.Any], HttpResponse]
LtiView = t.Callable[[HttpLtiRequest, t.Any], HttpResponse]


def view(view_func: View) -> LtiView:
    """
    LTI view decorator.

    This decorator will swallow the `lti_session_id` argument and add two attributes to the `request` object:

    - request.lti_params (LtiParams)
    - request.lti_session_id (str)
    """

    def inner(request: HttpRequest, lti_session_id: str, *args: t.Any, **kwargs: t.Any):
        lti_params = LtiParams.load_from_session(request.session, lti_session_id)
        setattr(request, "lti_params", lti_params)
        setattr(request, "lti_session_id", lti_session_id)
        return view_func(request, *args, **kwargs)

    return inner


def instructor_required(view_func: LtiView) -> LtiView:
    """
    Limit view access to instructors only.

    A 403 error is returned when not an instructor. Note that this decorator
    must be applied after @lti_view.
    """

    def inner(request, *args, **kwargs):
        if not request.lti_params.is_instructor:
            return HttpResponseForbidden("Access restricted to instructors")
        return view_func(request, *args, **kwargs)

    return inner
