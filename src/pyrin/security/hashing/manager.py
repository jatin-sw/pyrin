# -*- coding: utf-8 -*-
"""
hashing manager module.
"""

from pyrin.core.context import CoreObject, Context
from pyrin.security.hashing.exceptions import InvalidHashingHandlerTypeError, \
    InvalidHashingHandlerNameError, DuplicatedHashingHandlerError, HashingHandlerNotFoundError
from pyrin.security.hashing.handlers.base import HashingBase
from pyrin.utils.custom_print import print_warning


class HashingManager(CoreObject):
    """
    hashing manager class.
    """

    def __init__(self):
        """
        initializes an instance of HashingManager.
        """

        CoreObject.__init__(self)

        self._hashing_handlers = Context()

    def register_hashing_handler(self, instance, **options):
        """
        registers a new hashing handler or replaces the existing one
        if `replace=True` is provided. otherwise, it raises an error
        on adding an instance which it's name is already available
        in registered handlers.

        :param HashingBase instance: hashing handler to be registered.
                                     it must be an instance of HashingBase.

        :keyword bool replace: specifies that if there is another registered
                               handler with the same name, replace it with
                               the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidHashingHandlerTypeError: invalid hashing handler type error.
        :raises InvalidHashingHandlerNameError: invalid hashing handler name error.
        :raises DuplicatedHashingHandlerError: duplicated hashing handler error.
        """

        if not isinstance(instance, HashingBase):
            raise InvalidHashingHandlerTypeError('Input parameter [{instance}] is '
                                                 'not an instance of HashingBase.'
                                                 .format(instance=str(instance)))

        if instance.get_name() is None or len(instance.get_name().strip()) == 0:
            raise InvalidHashingHandlerNameError('Hashing handler [{instance}] '
                                                 'has invalid name.'
                                                 .format(instance=str(instance)))

        # checking whether is there any registered instance with the same name.
        if instance.get_name() in self._hashing_handlers.keys():
            replace = options.get('replace', False)

            if replace is not True:
                raise DuplicatedHashingHandlerError('There is another registered hashing '
                                                    'handler with name [{name}] but "replace" '
                                                    'option is not set, so handler '
                                                    '[{instance}] could not be registered.'
                                                    .format(name=instance.get_name(),
                                                            instance=str(instance)))

            old_instance = self._hashing_handlers[instance.get_name()]
            print_warning('Hashing handler [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=str(old_instance), new_instance=str(instance)))

        # registering new hashing handler.
        self._hashing_handlers[instance.get_name()] = instance

    def generate_hash(self, handler_name, text, **options):
        """
        gets the hash of input text using a random or specified salt.

        :param str handler_name: handler name to be used for hash generation.

        :param str text: text to be hashed.

        :keyword bytes salt: salt to be used for hashing.
                             if not provided, a random salt will be generated
                             considering `salt_length` option.

        :keyword str internal_algorithm: internal algorithm to be used
                                         for hashing. if not provided,
                                         default value from relevant
                                         config will be used.

        :keyword int rounds: rounds to perform for generating hash.
                             if not provided, default value from
                             relevant config will be used.

        :keyword int salt_length: salt length to be used for hashing.
                                  if `salt` option is provided, then
                                  this value will be ignored.
                                  if not provided, default value from
                                  relevant config will be used.

        :keyword str prefix: prefix to be used for bcrypt hashing.

        :rtype: bytes
        """

        return self._get_hashing_handler(handler_name).generate_hash(text, **options)

    def is_match(self, handler_name, text, full_hashed_value):
        """
        gets a value indicating that given text's
        hash is identical to given full hashed value.

        :param str handler_name: handler name to be used for hash generation.
        :param str text: text to be hashed.
        :param bytes full_hashed_value: full hashed value to compare with.

        :rtype: bool
        """

        return self._get_hashing_handler(handler_name).is_match(text, full_hashed_value)

    def _get_hashing_handler(self, name, **options):
        """
        gets the specified hashing handler.

        :param str name: name of hashing handler to get.

        :raises HashingHandlerNotFoundError: hashing handler not found error.

        :rtype: HashingBase
        """

        if name not in self._hashing_handlers.keys():
            raise HashingHandlerNotFoundError('Hashing handler [{name}] not found.'
                                              .format(name=name))

        return self._hashing_handlers[name]
