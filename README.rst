============
LTI Producer
============

This is a Django project that makes it easy to develop pluggable `LTI <https://en.wikipedia.org/wiki/Learning_Tools_Interoperability>`__ 1.1 applications in Python. Behind the scenes, LTI authentication is handled by the `django-lti-toolbox <https://github.com/openfun/django-lti-toolbox/>`__ library.

Installation
============

::

    pip install -e .
    pip install -r requirements/dev.txt

Create a private settings file in ``standalone/producer/settings/private.py`` with the following contents::

    from .dev import *

Apply migrations::

    ./standalone/producer/manage.py migrate

Running in development
======================

Producer
--------

Run a producer::

    make producer

Run a worker to consume asynchronous tasks::

    make worker

Create an admin user::

    ./standalone/producer/manage.py createsuperuser

Go to http://localhost:9630/admin/lti_toolbox/ltipassport/ and create an LTI consumer and passport.

Consumer
--------

Create a ``standalone/consumer/settings/private.py`` file and add your ``LTI_*`` settings, similar to ``standalone/consumer/settings/base.py``.

Launch a consumer::

    make consumer

Then open the following url in a browser: http://localhost:9631

LTI application development
===========================

The process to add new LTI application to this Django project is fairly simple. As an example, you can check out the `Mux videos LTI producer <https://github.com/strata-kk/mux-videos-lti-producer>`__.

The LTI producer application should be created as a `Django reusable app <https://docs.djangoproject.com/en/dev/intro/reusable-apps/>`__. Then, the app is installed and added to the project ``INSTALLED_APPS``. For example if you created "myltiapp", add to ``standalone/producer/settings/private.py``::

    INSTALLED_APPS.append("myltiapp")

Then, the app urls module is added to ``LTI_PRODUCER_URLS`` and the name of the LTI app launch url to ``LTI_LAUNCH_VIEWS``::

    LTI_PRODUCER_URLS = {
        "myltiapp": "myltiapp.urls"
    }
    LTI_LAUNCH_VIEWS = {
        "myltiapp": "myltiapp:launch",
    }

This configuration assumes that the ``myltiapp/urls.py`` file includes a url named "launch". Thus, the ``myltiapp/urls.py`` will be similar to::

    from django.urls import path

    from . import views

    app_name = "myltiapp"
    urlpatterns = [
        path(
            "launch/<str:lti_session_id>",
            views.launch,
            name="launch",
        ),
        ...
    ]

The ``lti_session_id`` url argument, along with the contents of the session cookie, will be used to maintain session state between the different pages. The ``myltiapp/views.py`` module will contain the following view::

    from django.http import HttpResponse
    from ltiproducer import ltiviews

    @ltiviews.view
    def launch(request: ltiviews.HttpLtiRequest) -> HttpResponse:
        my_custom_parameter = request.lti_params.get("custom_my_parameter", "")
        ...
        return HttpResponse(f"Hello {my_custom_parameter}!")

The ``@ltiviews.view`` decorator swallows the ``lti_session_id`` argument and adds two attributes to the ``request`` object:

- ``request.lti_params`` (``ltiviews.params.LtiParams``): contains the parameters sent by the client when they called the "launch" url, such as "context_id", "roles", etc.
- ``request.lti_session_id`` (str): this is the randomly-generated string that is used to maintain states between different pages. Thus, it should be passed between views as a url argument for authentication.

Views that should be limited to instructors are decorated with ``@ltiviews.instructor_required``.

When the LMS makes a request to the LTI producer, it should include a "custom_app" parameter which is equal to "myltiapp". The LTI producer will then redirect the launch request to the ``myltiapp.views.launch`` view.

LMS Integration
===============

Open edX
--------

1. Copy the LTI passport ID and secret from the producer admin (see above). Then, in the Open edX Studio, go to your course advanced settings. Create an LTI passport with the same ID and secret.
2. In the advanced settings, add "lti_consumer" to the list of advanced modules.
3. Back to your course content, add an advanced "LTI module" unit.
4. In the unit settings, use the following launch url: http(s)://yourhost/lti/1.1/launch. Note that in order to work inside an iframe, the LTI producer will have to run in a subdomain of the LMS/CMS.

Development
===========

Run tests::

    make test

Format your code::

    make format

Compile or upgrade requirements::

    make compile-requirements
    make upgrade-requirements


Deployment
==========

Notes:
Final deployment settings should be in the private.py. All additional custom configurations should be listed there.
Installation of mux-videos-lti-producer performs in the CI by::

    pip install -e git+https://github.com/strata-kk/mux-videos-lti-producer#egg=mux-lti-producer


License
=======

The code in this repository is licensed under version 3 of the AGPL unless otherwise noted. See the LICENSE.txt file for details.
