# -*- coding: utf-8 -*-
"""
application hooks module.
"""

import pyrin.application.services as application_services

from pyrin.core.structs import Hook
from pyrin.configuration import ConfigurationPackage
from pyrin.packaging.hooks import PackagingHookBase


class ApplicationHookBase(Hook):
    """
    application hook base class.

    all packages that need to be hooked into application business must
    implement this class and register it in application hooks.
    """

    def after_application_loaded(self):
        """
        this method will be called after application has been loaded.
        """
        pass

    def application_initialized(self):
        """
        this method will be get called after application has been fully initialized.
        """
        pass

    def prepare_runtime_data(self):
        """
        this method will be get called after application has been fully initialized.

        note that this method will not get called when
        application starts in scripting mode.
        """
        pass

    def before_application_run(self):
        """
        this method will be get called just before application gets running.

        note that this method will not get called when
        application starts in scripting mode.
        """
        pass

    def application_status_changed(self, old_status, new_status):
        """
        this method will be called whenever application status changes.

        :param str old_status: old application status.
        :param str new_status: new application status.

        :enum status:
            INITIALIZING = 'Initializing'
            LOADING = 'Loading'
            READY = 'Ready'
            RUNNING = 'Running'
            TERMINATED = 'Terminated'
        """
        pass

    def provide_response_headers(self, headers, endpoint,
                                 status_code, method, **options):
        """
        this method will be called whenever a response is going to be returned from server.

        subclasses could override this to provide custom or modified response headers.
        they must modify or extend headers in-place.

        :param dict | Headers headers: current response headers.

        :param str endpoint: the endpoint of the route that
                             handled the current request.
                             by default, it is the fully qualified
                             name of the view function.

        :param int status_code: response status code.
                                it could be None if not provided.

        :param str method: the http method of current request.

        :keyword str url: the url of the route that handled this request.

        :keyword user: the user of current request.
                       it could be None.
        """
        pass


class PackagingHook(PackagingHookBase):
    """
    packaging hook class.
    """

    def package_loaded(self, package_name, **options):
        """
        this method will be called after each application package has been loaded.

        :param str package_name: name of the loaded package.
        """

        # we should call this method as soon as configuration package is
        # loaded, to make sure application configs are loaded before any
        # other package needs them.
        if package_name == ConfigurationPackage.NAME:
            application_services.load_configs(**options)
