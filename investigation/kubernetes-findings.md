# Kubernetes findings

## Summary
The supplied starter manifest was intentionally defective and would not produce a healthy application deployment. The final corrected deployment was validated in Minikube with the following evidence:

```bash
kubectl get pods -n minipay
NAME                           READY   STATUS    RESTARTS   AGE
minipay-api-75c9c94498-8bqsk   1/1     Running   0          7m21s
minipay-api-75c9c94498-8mfjm   1/1     Running   0          7m21s
minipay-db-0                   1/1     Running   0          7m21s
```

```bash
kubectl -n minipay port-forward svc/minipay-api 8080:80
curl http://127.0.0.1:8080/health
{"status":"ok","database":"ok"}
```

## Defects in the starter manifest

### 1. Service selector did not match the Deployment labels
The original manifest used:

```yaml
metadata:
  name: minipay-api
spec:
  selector:
    matchLabels:
      app: minipay-api
```

but the Service selected:

```yaml
selector:
  app: minipay-backend
```

This meant the Service had no endpoints, so the application could not be reached even though the Pod existed.

### 2. Readiness and liveness probes used the wrong port
The container exposed port `8080`, but the original readiness/liveness section referenced `8081` and the Service target port also pointed to `8081`.

This is a common configuration issue that causes probes to fail and prevents the application from becoming Ready.

### 3. Placeholder image was invalid
The image was set to:

```yaml
image: YOUR_IMAGE_HERE
```

This cannot pull or run successfully in any real cluster. A real image name or a locally built image is required.

### 4. No real namespace, secret, or configuration hygiene
The starter manifest lacked a proper namespace configuration and any secret handling for DB credentials. This is a production issue because secrets should not be embedded in plain YAML or committed as literal values.

### 5. No persistent database storage
The database was not configured with a PVC or a proper StatefulSet volume. In production, stateful workloads require persistent storage so data survives pod rescheduling.

### 6. Missing resource requests and limits
The starter manifest omitted CPU/memory sizing guidance. This can lead to noisy-neighbor problems and unpredictable behavior under load.

### 7. No rollout or log troubleshooting guidance
The required deployment and support workflow includes validating rollout status and inspecting logs. The starter manifest did not include any of that operational context.

## Corrective actions applied

1. Created a proper namespace: `minipay`
2. Added a Secret for DB credentials instead of hard-coded values in the app config
3. Added a ConfigMap to initialize the PostgreSQL schema
4. Used a StatefulSet for PostgreSQL with persistent storage
5. Fixed all matching labels and ports so the Service routes to the API correctly
6. Added readiness and liveness probes against the application port `8080`
7. Added CPU/memory requests and limits
8. Built the app image locally for Minikube and pulled it via `imagePullPolicy: Never`

## Validation performed

### Pod health
```bash
kubectl get pods -n minipay
```
Output showed both API replicas and the DB pod as `Running`.

### Service exposure
```bash
kubectl -n minipay port-forward svc/minipay-api 8080:80
curl http://127.0.0.1:8080/health
```
Output:
```json
{"status":"ok","database":"ok"}
```

### Log inspection
```bash
kubectl logs deployment/minipay-api -n minipay --tail=200
```
The logs showed successful startup and HTTP 200 responses on `/health` after the application became Ready.

## Preventive controls

- Use `kubectl apply --dry-run=client -f ...` before cluster changes
- Validate Service selectors against Deployment labels in CI
- Verify probes and ports in a pre-deploy check
- Add a basic smoke test that calls `/health` after deployment
- Require resource requests and limits for all workloads
- Keep secrets in Kubernetes Secret resources, not in plain YAML or application source

## Conclusion
The starter manifest was intentionally broken to demonstrate a realistic deployment failure. The corrected configuration restored application availability and validated the expected health and startup behavior in Minikube.
