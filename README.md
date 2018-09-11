Secrets
===

Easily and securely store and retrieve secrets like API tokens so that they don't end up in git repos.

Secrets Architecture
---

Secrets are stored using "application level encryption". That is, secrets are stored in Google Cloud Storage, encrypted by a key before they are uploaded (versus using Google-provided encryption in Cloud Storage). Encryption keys are generated and retrieved from Google Key Management Service (KMS).

Deployment and Configuration
---

Create a keyring, key, and bucket.

Add a file `keyring.json` into the bucket with the keyring details:

```
{
	"location": "us-central1",
	"keyring": "my-key-ring",
	"key": "my-crypto-key"
}
```

Library
---

```
import gsecrets

# Get a single secret
gsecrets.get("slack/token")

# Get a dictionary of gsecrets 
gsecrets.get("manifests/admiral/env.json")

# Get a single secret from a dictionary of secrets 
gsecrets.get("manifests/admiral/env.json.airflow_fernet_key")


# Create or update a secret
gsecrets.put("slack/token", "AAABBBCCC")

# Create or update a secret, uses Python `dictionary.update` semantics for the update
gsecrets.put("manifests/admiral/env.json", {airflow_fernet_key: "AAABBBCCC"})

# Replace an entire dictionary of secrets
gsecrets.put("manifests/admiral/env.json", {airflow_fernet_key: "AAABBBCCC"}, replace=True)
```

CLI
---

The library commands map to CLI actions:

```
gsecrets get my-project/my-bucket/slack/token

gsecrets put my-project/my-bucket/slack/token AAABBBCCC

gsecrets put my-project/my-bucket/slack/env.json.FERNET_KEY AAABBBCCC

# etc.

# For a full list:
gsecrets --help
```

Development
---

Run the CLI inside a container

```
./cli.sh --help
```

Release
---

```
pip install twine

python setup.py upload
```

TODO
---

* Is this gonna need Python 2 support?
* Specify a Pipfile for version pinning in Dockerfile?


