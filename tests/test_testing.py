import gsecrets

# Safety check that we're not running against prod data
# assert gsecrets.bucket_name == "oee-test-secrets"

def test_bare_put_and_get():
	gsecrets.put("test/foo", "bar")
	secret = gsecrets.get("test/foo")
	assert bytes(secret) == b"bar"