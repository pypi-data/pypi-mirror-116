import os
import tempfile

import spell.cli.utils  # for __file__ introspection
from spell.cli.utils.cluster_utils import kubectl
from OpenSSL import crypto

runs_manifests_dir = os.path.join(
    os.path.dirname(spell.cli.utils.__file__), "kube_manifests", "spell-run"
)

#########################
# Runs
#########################


# must be executed with elevated permissions (crd)
def add_argo():
    kubectl(
        "apply",
        "-f",
        os.path.join(runs_manifests_dir, "argo"),
        "-n",
        "spell-run",
    )


def create_registry():
    # Create cert
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    cert = crypto.X509()
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
    cert.set_pubkey(k)
    sub = cert.get_subject()
    sub.CN = "docker-registry"
    cert.sign(k, 'sha256')

    with tempfile.NamedTemporaryFile(suffix=".crt", mode="wb") as cert_file:
        cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        cert_file.flush()
        with tempfile.NamedTemporaryFile(suffix=".key", mode="wb") as key_file:
            key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
            key_file.flush()
            cert_op = f"--cert={cert_file.name}"
            key_op = f"--key={key_file.name}"
            # Delete if secret exists
            kubectl(
                "delete",
                "secret",
                "tls",
                "certs-secret",
                "-n",
                "spell-run",
                "--ignore-not-found"
            )
            # Create secret
            kubectl(
                "create",
                "secret",
                "tls",
                "certs-secret",
                cert_op,
                key_op,
                "-n",
                "spell-run",
            )
            # Create registry stateful set
            kubectl(
                "create",
                "-f",
                os.path.join(runs_manifests_dir, "cluster-registry.yaml"),
                "-n",
                "spell-run",
            )
