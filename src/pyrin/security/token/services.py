# -*- coding: utf-8 -*-
"""
token services module.
"""

from pyrin.application.services import get_component
from pyrin.security.token import TokenPackage


def register_token_handler(instance, **options):
    """
    registers a new token handler or replaces the existing one
    if `replace=True` is provided. otherwise, it raises an error
    on adding an instance which it's name is already available
    in registered handlers.

    :param TokenBase instance: token handler to be registered.
                               it must be an instance of TokenBase.

    :keyword bool replace: specifies that if there is another registered
                           handler with the same name, replace it with
                           the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidTokenHandlerTypeError: invalid token handler type error.
    :raises InvalidTokenHandlerNameError: invalid token handler name error.
    :raises DuplicatedTokenHandlerError: duplicated token handler error.
    :raises DuplicatedTokenKidHeaderError: duplicated token kid header error.
    """

    return get_component(TokenPackage.COMPONENT_NAME).register_token_handler(instance,
                                                                             **options)


def generate_access_token(payload, **options):
    """
    generates an access token using specified handler from the given inputs and returns it.
    the generated token is in the form of `header_hash.payload_hash.signature_hash`
    and each part is encoded using a signing key.

    :param dict payload: a dictionary containing key/values as payload.
                         note that for better performance, keep payload
                         as small as possible.

    :keyword str handler_name: name of token handler to be used.
                               if not provided, default handler
                               from relevant configs will be used.

    :keyword dict custom_headers: a dictionary containing custom headers.

    :keyword bool is_fresh: indicates that this token is fresh.
                            being fresh means that token is generated by
                            providing user credentials to server.
                            if not provided, defaults to False.

    :raises TokenHandlerNotFoundError: token handler not found error.

    :returns: token.

    :rtype: str
    """

    return get_component(TokenPackage.COMPONENT_NAME).generate_access_token(payload, **options)


def generate_refresh_token(payload, **options):
    """
    generates a refresh token using specified handler from the given inputs and returns it.
    the generated token is in the form of `header_hash.payload_hash.signature_hash`
    and each part is encoded using a signing key.

    :param dict payload: a dictionary containing key/values as payload.
                         note that for better performance, keep payload
                         as small as possible.

    :keyword str handler_name: name of token handler to be used.
                               if not provided, default handler
                               from relevant configs will be used.

    :keyword dict custom_headers: a dictionary containing custom headers.

    :keyword bool is_fresh: indicates that this token is fresh.
                            being fresh means that token is generated by
                            providing user credentials to server.
                            if not provided, defaults to False.

    :raises TokenHandlerNotFoundError: token handler not found error.

    :returns: token.

    :rtype: str
    """

    return get_component(TokenPackage.COMPONENT_NAME).generate_refresh_token(payload, **options)


def get_payload(token, **options):
    """
    decodes token using correct handler and gets the payload data.

    :param str token: token to get it's payload.

    :raises TokenIsBlackListedError: token is black listed error.
    :raises TokenKidHeaderNotSpecifiedError: token kid header not specified error.
    :raises TokenKidHeaderNotFoundError: token kid header not found error.
    :raises TokenHandlerNotFoundError: token handler not found error.

    :rtype: dict
    """

    return get_component(TokenPackage.COMPONENT_NAME).get_payload(token, **options)


def get_unverified_payload(token, **options):
    """
    decodes token and gets the payload data without verifying the signature.
    note that returned payload must not be trusted for any critical operations.

    :param str token: token to get it's payload.

    :rtype: dict
    """

    return get_component(TokenPackage.COMPONENT_NAME).get_unverified_payload(token, **options)


def get_unverified_header(token, **options):
    """
    gets the header dict of token without verifying the signature.
    note that the returned header must not be trusted for critical operations.

    :param str token: token to get it's header.

    :rtype: dict
    """

    return get_component(TokenPackage.COMPONENT_NAME).get_unverified_header(token, **options)


def generate_key(handler_name, **options):
    """
    generates a valid key for the given handler and returns it.

    :param str handler_name: token handler name to be used.

    :keyword int length: the length of generated key in bytes.
                         note that some token handlers may not accept custom
                         key length so this value would be ignored on those handlers.

    :rtype: Union[str, tuple(str, str)]
    """

    return get_component(TokenPackage.COMPONENT_NAME).generate_key(handler_name, **options)


def add_to_blacklist(token, **options):
    """
    adds the given token into blacklist.

    :param str token: token to be added into blacklist.
    """

    return get_component(TokenPackage.COMPONENT_NAME).add_to_blacklist(token, **options)


def is_in_blacklist(token, **options):
    """
    gets a value indicating that given token is blacklisted.

    :param str token: token to be checked is blacklisted.

    :rtype: bool
    """

    return get_component(TokenPackage.COMPONENT_NAME).is_in_blacklist(token, **options)
