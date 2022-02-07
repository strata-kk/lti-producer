import uuid
from typing import Any, Dict

from django.contrib.sessions.backends.base import SessionBase
from lti_toolbox.launch_params import LAUNCH_PARAMS_OAUTH


class LtiParams:
    ROOT_KEY = "lti_sessions"

    def __init__(self, launch_params: Dict[str, Any]) -> None:
        self._params = launch_params

    def as_dict(self):
        return self._params

    def get(self, key, default=None):
        return self._params.get(key, default)

    @property
    def context_id(self):
        return self._params["context_id"]

    @property
    def resource_link_id(self):
        return self._params["resource_link_id"]

    def save_to_session(self, session: SessionBase):
        """
        Save the LTI parameters to the session.

        This allows to maintain state between calls to different views in the
        LTI app. For every user session, the LTI parameters are stored in:

            session["lti_sessions"][<random LTI session ID>]

        All values are stored, except for oauth-related parameters.

        Return: lti_session_id (str)
        """
        session.setdefault(self.ROOT_KEY, {})
        lti_session_id = str(uuid.uuid4())
        session[self.ROOT_KEY].setdefault(lti_session_id, {})
        context_session = session[self.ROOT_KEY][lti_session_id]

        context_session.clear()
        for key, value in self._params.items():
            if key not in LAUNCH_PARAMS_OAUTH:
                context_session[key] = value
        session.modified = True
        return lti_session_id

    @classmethod
    def load_from_session(
        cls, session: SessionBase, lti_session_id: str
    ) -> "LtiParams":
        return cls(session.get(cls.ROOT_KEY, {}).get(lti_session_id, {}))

    @property
    def is_instructor(self):
        return "Instructor" in self._params.get("roles", [])
