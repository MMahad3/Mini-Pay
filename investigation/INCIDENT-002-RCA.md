# INCIDENT-002 RCA: Application Unavailable After Deployment

## Symptoms

Pods could start while the application remained unreachable or unready. The starter Kubernetes manifest contained a placeholder image, mismatched Service selectors, incorrect target/probe ports, no namespace or durable database configuration, and no resource sizing.

## Evidence and reproduction

The original defects and corrected output are recorded in [kubernetes-findings.md](kubernetes-findings.md). The key checks are:

```bash
kubectl get pods -n minipay
kubectl -n minipay get endpoints minipay-api
kubectl -n minipay describe pod <pod-name>
kubectl logs deployment/minipay-api -n minipay --tail=200
```

A Service with no matching endpoints cannot route traffic even if its Deployment has Running pods. A probe pointed at the wrong port keeps the pod unready. The application image also must exist in the cluster image environment.

## Root causes

1. The Service selector did not match the API pod labels.
2. Service target port and health probes referenced a port different from the container's 8080 listener.
3. The starter image was `YOUR_IMAGE_HERE` and could not run.
4. Database configuration lacked namespace/secret/PVC/resource controls.
5. No rollout and health validation procedure was included.

## Corrective action

The submission manifest now provides a `minipay` namespace, PostgreSQL Secret and ConfigMap, StatefulSet with PVC, matching labels, API Service, local image configuration, resource requests/limits, and HTTP/exec health probes. The API image is built with:

```bash
minikube image build -t minipay-api:local .
kubectl apply -f kubernetes/minipay.yaml
kubectl -n minipay rollout status statefulset/minipay-db --timeout=180s
kubectl -n minipay rollout status deployment/minipay-api --timeout=180s
```

## Validation

```bash
kubectl -n minipay port-forward svc/minipay-api 8080:80
curl http://127.0.0.1:8080/health
```

Recorded result: `{"status":"ok","database":"ok"}` with both API replicas and the database pod Ready. Full command/output evidence is in [evidence/kubernetes.md](../evidence/kubernetes.md).

## Preventive controls

- Run `kubectl apply --dry-run=client -f kubernetes/minipay.yaml`.
- Validate Service selectors and container/service/probe ports in CI.
- Require immutable images, resource requests/limits, and readiness/liveness probes.
- Check rollout status and `/health` after every deployment.
- Inspect endpoints before debugging application code.
- Keep production credentials in an external secret manager.
