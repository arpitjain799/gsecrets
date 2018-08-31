import base64
import warnings
import googleapiclient.discovery
from google.cloud import storage


# Suppress this warning as this tool is intended to be authenticated
# using user credentials. May revisit this decision in the future.
warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")

# Google Cloud KMS configuration
project_id = "oee-secrets"
location = "us-central1"
keyring = "oee-key-ring"
key = "oee-crypto-key"

resource = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
    project_id,
    location,
    keyring,
    key
)

# Google Cloud Storage configuration
storage_client = storage.Client(project=project_id)
bucket_name = "oee-secrets"
bucket = storage_client.bucket(bucket_name)

def put(path, content):
    """Put a secret with value `content` at `path`

    Examples:

        put("slack/token", "AABBBCCC")

    """
    kms_client = googleapiclient.discovery.build('cloudkms','v1')
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    encoded = base64.b64encode(content.encode('utf-8'))
    request = crypto_keys.encrypt(
        name=resource,
        body={
            'plaintext': encoded.decode('utf-8')
        }
    )
    response = request.execute()

    ciphertext = response['ciphertext']

    blob = bucket.blob(path)
    blob.upload_from_string(ciphertext)

def get(path):
    """Retrieve a secret

    Examples:

        get("slack/token") -> "AAABBBCCC"

    """
    blob = bucket.blob(path)
    ciphertext = blob.download_as_string()
    kms_client = googleapiclient.discovery.build('cloudkms','v1')
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = crypto_keys.decrypt(
        name=resource,
        body={
            'ciphertext': ciphertext.decode('utf-8')
        }
    )
    response = request.execute()
    plaintext = base64.b64decode(response['plaintext'].encode('utf-8'))
    return plaintext






