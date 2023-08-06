# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_pay_token_decryption']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.4.7,<4.0.0']

setup_kwargs = {
    'name': 'google-pay-token-decryption',
    'version': '0.1.0',
    'description': 'Python package to verify and decrypt Google Pay tokens',
    'long_description': '# Google Pay token decryption\n\nA Python package to decrypt Google Pay tokens according to the [Google Pay docs](https://developers.google.com/pay/api/android/guides/resources/payment-data-cryptography#decrypt-token) using the [`pyca/cryptography`](https://cryptography.io/en/latest/) package.\n\n## System requirements\n\n- Python 3.8+\n\n## Usage\n\n1. Install the package using Pip: `pip install google-pay-token-decryption`.\n\n2. Get latest Google root signing keys [here](https://developers.google.com/pay/api/android/guides/resources/payment-data-cryptography#root-signing-keys).\n\n3. Get your **merchant ID/recipient ID** from the [Google Pay business console](https://pay.google.com/business/console). It should be in the format "merchant:<your merchant ID>". In Google\'s test environment it is always "merchant:12345678901234567890".\n\n4. Generate your merchant private and public keys by following [this documentation](https://developers.google.com/pay/api/android/guides/resources/payment-data-cryptography#using-openssl).\n\n5. Create a new `GooglePayTokenDecryptor` object and decrypt a token using the `decrypt_token` method:\n\n```python\nfrom google_pay_token_decryption import GooglePayTokenDecryptor\n\n# Instantiate using the a list of root signing keys, your recipient ID and private key\nroot_signing_keys = [{\n    "keyValue": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE/1+3HBVSbdv+j7NaArdgMyoSAM43yRydzqdg1TxodSzA96Dj4Mc1EiKroxxunavVIvdxGnJeFViTzFvzFRxyCw==",\n    "keyExpiration": "32506264800000",\n    "protocolVersion": "ECv2",\n}]\nrecipient_id = "someRecipient"\nprivate_key = "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgCPSuFr4iSIaQprjjchHPyDu2NXFe0vDBoTpPkYaK9dehRANCAATnaFz/vQKuO90pxsINyVNWojabHfbx9qIJ6uD7Q7ZSxmtyo/Ez3/o2kDT8g0pIdyVIYktCsq65VoQIDWSh2Bdm"\ndecryptor = GooglePayTokenDecryptor(root_signing_keys, recipient_id, private_key)\n\n# Verify and decrypt a token \nencrypted_token = {\n    "signature": "MEYCIQCbtFh9UIf1Ty3NKZ2z0ZmL0SHwR30uiRGuRXk9ghpyrwIhANiZQ0Df6noxkQ6M652PcIPkk2m1PQhqiq4UhzvPQOYf",\n    "intermediateSigningKey": {\n        "signedKey": "{\\"keyValue\\":\\"MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE/1+3HBVSbdv+j7NaArdgMyoSAM43yRydzqdg1TxodSzA96Dj4Mc1EiKroxxunavVIvdxGnJeFViTzFvzFRxyCw==\\",\\"keyExpiration\\":\\"1879409613939\\"}",\n        "signatures": [\n            "MEQCIFBle+JsfsovRBeoFEYKWFAeBYFAhq0S+GtusiosjV4lAiAGcK9qfVpnqG6Hw8cbGBQ79beiAs6IIkBxBfeKDBR+kA=="\n        ]\n    },\n    "protocolVersion": "ECv2",\n    "signedMessage": "{\\"encryptedMessage\\":\\"PeYi+ZnJs1Gei1dSOkItdfFG8Y81FvEI7dHE0sSrSU6OPnndftV/qDbbmXHmppoyP/2lhF+XsH93qzD3u46BRnxxPtetzGT0533rIraskTj8SZ6FVYY1Opfo7FECGk57FfF8aDaCSOoyTh1k0v6wdxVwEVvWqG1T/ij+u2KWOw5G1WSB/RVicni0Az13ModYb0KMdMws1USKlWxBfKU5PtxibVx4fZ95HYQ82qgHlV4ToKaUY7YWud1iEspmFsBMk0nh4t1hVxRzsxKUjMV1915qD5yq7k5n9YPao2mR9NJgLPDktsc4uf9bszzvnqhz3T1YID43QwX16yCyn/YxNVe3dJ1+S+BGyJ+vyKXp+Zh4SlIua2NFLwnR06Es3Kvl6LlOGasoPC/tMAWYLQlGsl+vHK3mrMZjC6KbOsXg+2mrlZwL+QOt3ih2jIPe\\",\\"ephemeralPublicKey\\":\\"BD6pQKpy7yDebAX4qV0u/AfMYNQhOD+teyoa/5SsxwTGCoC1ZKHxNMb5BXvRmBcYGPNTx8+fAkEwzJ8GqbX/Q7E=\\",\\"tag\\":\\"8gFteCvCuamX1RmL7ORdHqleyBf0N55OfAs80RYGgwc=\\"}"\n}\ndecrypted_token = decryptor.decrypt_token(encrypted_token)\nprint(decrypted_token)\n"""\n{\n    "messageExpiration": "32506264800000",\n    "messageId": "AH2EjtfkY514K5lmPF4NOP9lMR5tPedsjQR719hIzI-zB1g0A-TBlYInGQuEVQeIWGlajqEpvSyrl3r_iN0RxoV9RYjxqnzG-kXmcBNkferp4NfNjVqxYrVT0e5JRzU3dQjkb0tQWOxN",\n    "paymentMethod": "CARD",\n    "paymentMethodDetails": {\n        "expirationYear": 2026,\n        "expirationMonth": 12,\n        "pan": "4111111111111111",\n        "authMethod": "PAN_ONLY"\n    }\n}\n"""\n```\n\n## Contributing\n\nSee [Contributing](./CONTRIBUTING.md)',
    'author': 'Yoyo Wallet',
    'author_email': 'dev@yoyowallet.com',
    'maintainer': 'Yoyo Wallet',
    'maintainer_email': 'dev@yoyowallet.com',
    'url': 'https://github.com/yoyowallet/google-pay-token-decryption',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
