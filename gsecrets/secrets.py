import googleapiclient.discovery
from google.cloud import storage
import base64

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
