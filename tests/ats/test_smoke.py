"""app-test-suite smoke for the oncall-shift-reporter chart.

app-test-suite 1.x (the generated execute-chart-tests CircleCI job) creates a kind
cluster, installs the packaged chart with `helm upgrade --install --wait` (namespace and
values file: .ats/main.yaml) and then runs `pytest -m smoke` in this directory.

The chart ships a monthly CronJob and the Secret it reads its tokens from, no long-running
workload. The smoke proves that the chart installs on a bare cluster, that the CronJob is
armed, and that every Secret key the job's env references exists in the rendered Secret.
"""

import logging
import os

import pykube
import pytest
from pytest_helm_charts.clusters import Cluster

logger = logging.getLogger(__name__)

# app-test-suite exports the release namespace (app-tests-deploy-namespace in .ats/main.yaml).
namespace = os.environ.get("ATS_RELEASE_NAMESPACE", "oncall-shift-reporter")
cronjob_name = "oncall-shift-reporter"
image_repository = "gsoci.azurecr.io/giantswarm/oncall-shift-reporter"


@pytest.mark.smoke
def test_api_working(kube_cluster: Cluster) -> None:
    """The test cluster is reachable."""
    assert kube_cluster.kube_client is not None
    assert len(pykube.Node.objects(kube_cluster.kube_client)) >= 1


@pytest.mark.smoke
def test_cronjob_armed(kube_cluster: Cluster) -> None:
    """The CronJob exists, is scheduled and not suspended, and runs the reporter image."""
    cronjob = pykube.CronJob.objects(kube_cluster.kube_client, namespace=namespace).get(name=cronjob_name)
    spec = cronjob.obj["spec"]
    assert spec["schedule"], "CronJob has no schedule"
    assert spec.get("suspend", False) is False, "CronJob is suspended"
    containers = spec["jobTemplate"]["spec"]["template"]["spec"]["containers"]
    assert len(containers) == 1
    assert containers[0]["image"].startswith(f"{image_repository}:"), containers[0]["image"]
    logger.info("CronJob %s/%s armed with schedule %r", namespace, cronjob_name, spec["schedule"])


@pytest.mark.smoke
def test_secret_keys_match_cronjob_env(kube_cluster: Cluster) -> None:
    """Every secretKeyRef in the job's env resolves to a key of the chart's Secret."""
    cronjob = pykube.CronJob.objects(kube_cluster.kube_client, namespace=namespace).get(name=cronjob_name)
    container = cronjob.obj["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]
    refs = [e["valueFrom"]["secretKeyRef"] for e in container.get("env", []) if "secretKeyRef" in e.get("valueFrom", {})]
    assert refs, "the job's env references no Secret"
    for ref in refs:
        secret = pykube.Secret.objects(kube_cluster.kube_client, namespace=namespace).get(name=ref["name"])
        assert ref["key"] in secret.obj.get("data", {}), f"Secret {ref['name']} has no key {ref['key']}"
