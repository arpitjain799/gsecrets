Secrets
===

Easily and securely store and retrieve secrets like API tokens so that they don't end up in git repos.

Comes preconfigured for OEE, pointing at the `oee-secrets` GCP project and `oee-secrets` bucket.

Secrets Architecture
---

Secrets are stored using "application level encryption". That is, secrets are stored in Google Cloud Storage, encrypted by a key before they are uploaded (versus using Google-provided encryption in Cloud Storagee). Encryption keys are generated and retrieved from Google Key Management Service (KMS).

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
gsecrets get slack/token

gsecrets put slack/token AAABBBCCC

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

TODO
---

* Is this gonna need Python 2 support?
* Specify a Pipfile for version pinning in Dockerfile?


