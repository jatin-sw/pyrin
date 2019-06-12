# -*- coding: utf-8 -*-
"""
rsa256 encryption handler module.
"""

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

import pyrin.configuration.services as config_services

from pyrin.security.encryption.decorators import encrypter
from pyrin.security.encryption.handlers.base import RSAEncrypterBase
from pyrin.security.utils import key_helper
from pyrin.settings.static import APPLICATION_ENCODING


@encrypter()
class RSA256Encrypter(RSAEncrypterBase):
    """
    rsa256 encrypter class.
    """

    def __init__(self, **options):
        """
        initializes an instance of RSA256Encrypter.
        """

        RSAEncrypterBase.__init__(self, **options)

    def _get_algorithm(self, **options):
        """
        gets the algorithm used for encryption.

        :rtype: str
        """

        return 'RSA256'

    def _encrypt(self, text, **options):
        """
        encrypts the given value and returns the encrypted result.

        :param str text: text to be encrypted.

        :rtype: bytes
        """

        return self._public_key.encrypt(text.encode(APPLICATION_ENCODING),
                                        padding.OAEP(
                                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                            algorithm=hashes.SHA256(),
                                            label=None))

    def _decrypt(self, value, **options):
        """
        decrypts the given value and returns the decrypted result.

        :param bytes value: value to be decrypted.

        :rtype: str
        """

        return self._private_key.decrypt(value, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None)).decode(APPLICATION_ENCODING)

    def generate_key(self, **options):
        """
        generates a valid public/private key for this handler and returns it.

        :returns tuple(str public_key, str private_key)

        :rtype: tuple(str, str)
        """

        return RSAEncrypterBase.generate_key(self, length=2048)

    def _load_keys(self, **options):
        """
        loads public/private keys into this class's relevant attributes.
        """

        public_pem = config_services.get('security', 'encryption', 'rsa256_public_key')
        private_pem = config_services.get('security', 'encryption', 'rsa256_private_key')

        self._public_key, self._private_key = key_helper.load_rsa_key(public_pem,
                                                                      private_pem,
                                                                      **options)
