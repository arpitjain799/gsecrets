import base64
import json
import re
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

def put(path, content, replace=False):
    """Put a secret with value `content` at `path`

    Optional arguments:

        replace: if set to `False`, will do a dict.update if an object already
                 exists in GCS. If `True`, completely replaces the object.

    Examples:

        put("slack/token", "AABBBCCC")

    Replace an entire dictionary

        put("manifests/admiral/env.json", {airflow_fernet_key: "AAABBBCCC"}, replace=True)

    """
    dictionary_mode = path.endswith(".json")
    
    if dictionary_mode:
        existing_secret = get(path)
        if type(content) is not dict:
            new_secret = json.loads(content)

        if replace:
            content = json.dumps(new_secret)
        else:
            existing_secret.update(new_secret)
            content = json.dumps(existing_secret)

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
        
    Automatically parse json if the path ends with `.json`:

        get("manifests/admiral/env.json") -> "{'key': AAABBBCCC}"

    Retrieve a single value from a json file:
    
        get("manifests/admiral/env.json.key") -> "AAABBBCCC"

    """

    # Check if this is a json key path
    pattern = "(.+\.json)\.(.+)$"
    matches = re.search(pattern, path)
    json_extract_mode = False
    if matches:
        json_extract_mode = True
        path = matches.group(1)
        key = matches.group(2)

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

    if json_extract_mode:
        return json.loads(plaintext).get(key)

    if path.endswith(".json"):
        return json.loads(plaintext)

    return plaintext




