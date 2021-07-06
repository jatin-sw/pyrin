# -*- coding: utf-8 -*-
"""
audit api module.
"""

import pyrin.audit.services as audit_services

from pyrin.api.router.decorators import get


audit_config = audit_services.get_audit_configurations()
is_enabled = audit_config.pop('enabled', False)

if is_enabled is True:
    @get(**audit_config, no_cache=True)
    def inspect(**options):
        """
        inspects all registered packages and gets inspection data.
        ---
        parameters:
          - name: application
            in: query
            type: boolean
            required: false
            description: specifies that application info must be included.
          - name: packages
            in: query
            type: boolean
            required: false
            description: specifies that loaded packages info must be included.
          - name: framework
            in: query
            type: boolean
            required: false
            description: specifies that framework info must be included.
          - name: python
            in: query
            type: boolean
            required: false
            description: specifies that python info must be included.
          - name: os
            in: query
            type: boolean
            required: false
            description: specifies that operating system info must be included.
          - name: hardware
            in: query
            type: boolean
            required: false
            description: specifies that hardware info must be included.
          - name: database
            in: query
            type: boolean
            required: false
            description: specifies that database info must be included.
          - name: caching
            in: query
            type: boolean
            required: false
            description: specifies that caching info must be included.
          - name: celery
            in: query
            type: boolean
            required: false
            description: specifies that celery info must be included.
          - name: traceback
            in: query
            type: boolean
            required: false
            description: specifies that on failure, it must include the traceback of errors.
        responses:
          200:
            description: all packages are working normally.
            schema:
              properties:
                application:
                  type: object
                  description: application info.
                packages:
                  type: object
                  description: loaded packages info.
                framework:
                  type: object
                  description: framework info.
                python:
                  type: object
                  description: python info.
                platform:
                  type: object
                  description: platform info.
                database:
                  type: object
                  description: database info.
                caching:
                  type: object
                  description: caching info.
                celery:
                  type: object
                  description: celery info.
          500:
            description: some packages have errors.
            schema:
              properties:
                application:
                  type: object
                  description: application info.
                packages:
                  type: object
                  description: loaded packages info.
                framework:
                  type: object
                  description: framework info.
                python:
                  type: object
                  description: python info.
                platform:
                  type: object
                  description: platform info.
                database:
                  type: object
                  description: database info.
                caching:
                  type: object
                  description: caching info.
                celery:
                  type: object
                  description: celery info.
        """

        return audit_services.inspect(**options)
