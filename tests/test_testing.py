import unittest
import gsecrets
from gsecrets.exceptions import SecretNotFound

# Safety check that we're not running against prod data
# assert gsecrets.bucket_name == "oee-test-secrets"

VAULT_LOCATION = "oee-dev-145623/oee-test-secrets"
client = gsecrets.Client(VAULT_LOCATION)

class TestCore(unittest.TestCase):

	def test_bare_put_and_get(self):
		client.put("test/foo", "bar")
		secret = client.get("test/foo")
		assert bytes(secret) == b"bar"

	def test_secret_not_found_error(self):
		with self.assertRaises(SecretNotFound):
			client.get("thissecretshouldnotexist")
