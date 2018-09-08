import unittest
import gsecrets
from gsecrets.exceptions import SecretNotFound

# Safety check that we're not running against prod data
# assert gsecrets.bucket_name == "oee-test-secrets"

class TestCore(unittest.TestCase):

	def test_bare_put_and_get(self):
		gsecrets.put("test/foo", "bar")
		secret = gsecrets.get("test/foo")
		assert bytes(secret) == b"bar"

	def test_secret_not_found_error(self):
		with self.assertRaises(SecretNotFound):
			gsecrets.get("thissecretshouldnotexist")
