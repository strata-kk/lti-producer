# Switch to dev in development
from .prod import *  # pylint: disable=wildcard-import,unused-wildcard-import

LTI_PRODUCER_URLS = {"appname": "myapp.urls"}
LTI_LAUNCH_VIEWS = {
    "appname": "myapp:launch",
}
