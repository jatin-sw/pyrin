# -*- coding: utf-8 -*-
"""
swagger enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class ParameterLocationEnum(CoreEnum):
    """
    parameter location enum.
    """

    PATH = 'path'
    QUERY = 'query'
    JSON = 'json'
    BODY = 'body'


class ParameterAttributeEnum(CoreEnum):
    """
    parameter attribute enum.
    """

    # name of the parameter.
    NAME = 'name'

    # description of the parameter.
    DESCRIPTION = 'description'

    # specifies that parameter is required.
    REQUIRED = 'required'

    # type of the parameter.
    # it could be from 'ParameterTypeEnum' values.
    TYPE = 'type'

    # the place of this parameter in request.
    # it could be from 'ParameterLocationEnum' values.
    IN = 'in'

    # the format of parameter for given type.
    # it could be from 'ParameterFormatEnum' values.
    FORMAT = 'format'

    # list of valid values for given parameter.
    ENUM = 'enum'

    # items of an array type parameter.
    ITEMS = 'items'

    # keys of an object type parameter.
    PROPERTIES = 'properties'


class ParameterFormatEnum(CoreEnum):
    """
    parameter format enum.
    """

    UUID = 'uuid'
    EMAIL = 'email'
    DATE = 'date'
    DATE_TIME = 'date-time'
    PASSWORD = 'password'
    BYTE = 'byte'
    URI = 'uri'
    HOSTNAME = 'hostname'
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
    DOUBLE = 'double'
    FLOAT = 'float'


class ParameterTypeEnum(CoreEnum):
    """
    parameter type enum.
    """

    INTEGER = 'integer'
    NUMBER = 'number'
    BOOLEAN = 'boolean'
    STRING = 'string'
    ARRAY = 'array'
    OBJECT = 'object'


class DocstringSectionEnum(CoreEnum):
    """
    docstring section enum.
    """

    # list of parameters.
    PARAMETERS = 'parameters'

    # dict of responses.
    RESPONSES = 'responses'

    # list of security definitions.
    SECURITY = 'security'

    # list of tags for each api to be categorized by tag in swagger ui.
    TAGS = 'tags'
