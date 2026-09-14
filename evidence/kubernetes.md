# Kubernetes Deployment Evidence

This document records the commands and output used to build, deploy, troubleshoot, and validate Mini-Pay in Minikube.

## Evidence Context

The commands were run locally by user `mahad` on host `DESKTOP-BFCF70D` from `~/paysys/Mini-Pay`. The complete original session transcript is preserved below so the shell prompt, working directory, command history, and raw output remain traceable.

## Build the Application Image

### Initial build attempt

```text
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ minikube image build -t minipay-api:local .
error: failed to solve: failed to compute cache key: failed to calculate checksum of ref o6bmybsi6jopdei7b1xy72yjg::wlr6w4wuhtshpdn11ypg7zt9j: "/requirements.txt": not found
 ------
  > [3/5] COPY requirements.txt ./:
--------------------
    3 |     WORKDIR /app
    4 |
    5 | >>> COPY requirements.txt ./
error: failed to solve: failed to compute cache key: failed to calculate checksum of ref o6bmybsi6jopdei7b1xy72yjg::wlr6w4wuhtshpdn11ypg7zt9j: "/requirements.txt": not found
```

### Successful build

```text
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ minikube image build -t minipay-api:local .
#10 DONE 2.3s
```

The image was built successfully as `minipay-api:local`.

## Deploy to Kubernetes

```text
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ docker logs  container-id  2>&1 | grep "Bootstrap Password:"
deployment.apps/minipay-api created
service/minipay-api created
```

## Initial Pod and Service Status

```text
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl get pods -n minipay
minipay-db    ClusterIP   None            <none>        5432/TCP       27s
```

## Rollout and Log Validation

```text
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl -n minipay rollout status statefulset/minipay-db --timeout=180s
2026-09-14 18:15:53.804 UTC [1] LOG:  database system is ready to accept connections
```

The database completed initialization and became ready to accept connections.

## Service Access Troubleshooting

```text
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ ^[[200~minikube service minipay-api -n minipay --url~^C
error: unknown shorthand flag: 'd' in -d
 See 'kubectl port-forward --help' for usage.
```

The NodePort and Minikube service URL were not reachable from the current shell, so port forwarding was used instead.

## Final Health Check

```text
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl -n minipay port-forward svc/minipay-api 8080:80 > /tmp/minipay-port-forward.log 2>&1 &
INFO:     10.244.0.1:36776 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36788 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33998 - "GET /health HTTP/1.1" 200 OK
```

Final pod status:

| Workload | Ready | Status |
| --- | ---: | --- |
| `minipay-api` replica 1 | `1/1` | `Running` |
| `minipay-api` replica 2 | `1/1` | `Running` |
| `minipay-db-0` | `1/1` | `Running` |

The API health endpoint returned `{"status":"ok","database":"ok"}` after the database became ready.

## Full Session Transcript

The original terminal transcript is retained verbatim below as supporting evidence.

```text
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ minikube image build -t minipay-api:local .
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 253B done
#1 DONE 0.2s

#2 [internal] load metadata for docker.io/library/python:3.12-slim
#2 DONE 3.4s

#3 [internal] load .dockerignore
#3 transferring context:
#3 transferring context: 2B done
#3 DONE 0.7s

#4 [internal] load build context
#4 ...

#5 [1/5] FROM docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea
#5 resolve docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea 1.0s done
#5 DONE 1.0s

#4 [internal] load build context
#4 transferring context: 3.32kB done
#4 DONE 1.7s

#5 [1/5] FROM docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea
#5 CANCELED

#6 [2/5] WORKDIR /app
#6 CACHED

#7 [3/5] COPY requirements.txt ./
#7 ERROR: failed to calculate checksum of ref o6bmybsi6jopdei7b1xy72yjg::wlr6w4wuhtshpdn11ypg7zt9j: "/requirements.txt": not found
------
 > [3/5] COPY requirements.txt ./:
------
Dockerfile:5
--------------------
   3 |     WORKDIR /app
   4 |
   5 | >>> COPY requirements.txt ./
   6 |     RUN pip install --no-cache-dir -r requirements.txt
   7 |
--------------------
error: failed to solve: failed to compute cache key: failed to calculate checksum of ref o6bmybsi6jopdei7b1xy72yjg::wlr6w4wuhtshpdn11ypg7zt9j: "/requirements.txt": not found
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ minikube image build -t minipay-api:local .
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 253B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/python:3.12-slim
#2 DONE 0.4s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [1/5] FROM docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea
#4 resolve docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea 0.1s done
#4 DONE 0.1s

#5 [internal] load build context
#5 transferring context: 3.45kB done
#5 DONE 0.3s

#4 [1/5] FROM docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea
#4 DONE 0.7s

#4 [1/5] FROM docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea
#4 sha256:56235e4245636e401a28cf88944d543b29ee028ae3b6c27e03d6b43e7b4eac5f 0B / 249B 0.2s
#4 sha256:56235e4245636e401a28cf88944d543b29ee028ae3b6c27e03d6b43e7b4eac5f 249B / 249B 0.3s done
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 0B / 12.12MB 0.2s
#4 sha256:dbd0b7849e6c06b61e1fa6b7ffe053f246ce0075890620e3db64b47bb662433a 0B / 4.27MB 0.2s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 0B / 29.79MB 0.2s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 1.05MB / 12.12MB 0.6s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 3.15MB / 12.12MB 0.8s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 4.19MB / 12.12MB 0.9s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 5.24MB / 12.12MB 1.1s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 6.29MB / 12.12MB 1.2s
#4 sha256:dbd0b7849e6c06b61e1fa6b7ffe053f246ce0075890620e3db64b47bb662433a 1.05MB / 4.27MB 1.2s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 7.34MB / 12.12MB 1.4s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 8.39MB / 12.12MB 1.5s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 9.44MB / 12.12MB 1.7s
#4 sha256:dbd0b7849e6c06b61e1fa6b7ffe053f246ce0075890620e3db64b47bb662433a 2.10MB / 4.27MB 1.7s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 10.49MB / 12.12MB 1.8s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 2.10MB / 29.79MB 1.8s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 12.12MB / 12.12MB 2.0s
#4 sha256:dbd0b7849e6c06b61e1fa6b7ffe053f246ce0075890620e3db64b47bb662433a 3.15MB / 4.27MB 2.0s
#4 sha256:dbd0b7849e6c06b61e1fa6b7ffe053f246ce0075890620e3db64b47bb662433a 4.27MB / 4.27MB 2.3s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 4.19MB / 29.79MB 2.3s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 6.29MB / 29.79MB 2.4s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 9.44MB / 29.79MB 2.7s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 11.53MB / 29.79MB 2.9s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 14.68MB / 29.79MB 3.5s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 16.78MB / 29.79MB 3.6s
#4 sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 12.12MB / 12.12MB 3.7s done
#4 sha256:dbd0b7849e6c06b61e1fa6b7ffe053f246ce0075890620e3db64b47bb662433a 4.27MB / 4.27MB 3.7s done
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 18.87MB / 29.79MB 3.8s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 22.02MB / 29.79MB 4.1s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 24.12MB / 29.79MB 4.2s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 26.21MB / 29.79MB 4.4s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 29.79MB / 29.79MB 4.7s
#4 sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 29.79MB / 29.79MB 7.4s done
#4 extracting sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be
#4 extracting sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f420b1f83cce457be 1.2s done
#4 DONE 9.5s

#4 [1/5] FROM docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea
#4 extracting sha256:dbd0b7849e6c06b61e1fa6b7ffe053f246ce0075890620e3db64b47bb662433a
#4 extracting sha256:dbd0b7849e6c06b61e1fa6b7ffe053f246ce0075890620e3db64b47bb662433a 0.3s done
#4 DONE 9.8s

#4 [1/5] FROM docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea
#4 extracting sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f
#4 extracting sha256:1560cfed01dc4c72c07f789d860078d74466a1f9a26b33a2e35d887b5f90dd3f 0.8s done
#4 DONE 10.6s

#4 [1/5] FROM docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea
#4 extracting sha256:56235e4245636e401a28cf88944d543b29ee028ae3b6c27e03d6b43e7b4eac5f 0.1s done
#4 DONE 10.7s

#6 [2/5] WORKDIR /app
#6 DONE 25.4s

#7 [3/5] COPY requirements.txt ./
#7 DONE 0.0s

#8 [4/5] RUN pip install --no-cache-dir -r requirements.txt
#8 2.039 Collecting fastapi==0.115.6 (from -r requirements.txt (line 1))
#8 2.523   Downloading fastapi-0.115.6-py3-none-any.whl.metadata (27 kB)
#8 2.752 Collecting uvicorn==0.34.0 (from uvicorn[standard]==0.34.0->-r requirements.txt (line 2))
#8 2.907   Downloading uvicorn-0.34.0-py3-none-any.whl.metadata (6.5 kB)
#8 3.079 Collecting psycopg==3.2.3 (from psycopg[binary]==3.2.3->-r requirements.txt (line 3))
#8 3.232   Downloading psycopg-3.2.3-py3-none-any.whl.metadata (4.3 kB)
#8 3.659 Collecting pydantic==2.10.4 (from -r requirements.txt (line 4))
#8 3.813   Downloading pydantic-2.10.4-py3-none-any.whl.metadata (29 kB)
#8 4.046 Collecting starlette<0.42.0,>=0.40.0 (from fastapi==0.115.6->-r requirements.txt (line 1))
#8 4.198   Downloading starlette-0.41.3-py3-none-any.whl.metadata (6.0 kB)
#8 4.393 Collecting typing-extensions>=4.8.0 (from fastapi==0.115.6->-r requirements.txt (line 1))
#8 4.545   Downloading typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
#8 4.709 Collecting click>=7.0 (from uvicorn==0.34.0->uvicorn[standard]==0.34.0->-r requirements.txt (line 2))
#8 4.861   Downloading click-8.5.0-py3-none-any.whl.metadata (2.6 kB)
#8 5.015 Collecting h11>=0.8 (from uvicorn==0.34.0->uvicorn[standard]==0.34.0->-r requirements.txt (line 2))
#8 5.167   Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
#8 5.329 Collecting annotated-types>=0.6.0 (from pydantic==2.10.4->-r requirements.txt (line 4))
#8 5.486   Downloading annotated_types-0.8.0-py3-none-any.whl.metadata (15 kB)
#8 6.497 Collecting pydantic-core==2.27.2 (from pydantic==2.10.4->-r requirements.txt (line 4))
#8 6.650   Downloading pydantic_core-2.27.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.6 kB)
#8 6.926 Collecting psycopg-binary==3.2.3 (from psycopg[binary]==3.2.3->-r requirements.txt (line 3))
#8 7.080   Downloading psycopg_binary-3.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.8 kB)
#8 7.257 Collecting httptools>=0.6.3 (from uvicorn[standard]==0.34.0->-r requirements.txt (line 2))
#8 7.412   Downloading httptools-0.8.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (3.5 kB)
#8 7.574 Collecting python-dotenv>=0.13 (from uvicorn[standard]==0.34.0->-r requirements.txt (line 2))
#8 7.726   Downloading python_dotenv-1.2.3-py3-none-any.whl.metadata (29 kB)
#8 7.932 Collecting pyyaml>=5.1 (from uvicorn[standard]==0.34.0->-r requirements.txt (line 2))
#8 8.085   Downloading pyyaml-6.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
#8 8.261 Collecting uvloop!=0.15.0,!=0.15.1,>=0.14.0 (from uvicorn[standard]==0.34.0->-r requirements.txt (line 2))
#8 8.414   Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (4.9 kB)
#8 8.623 Collecting watchfiles>=0.13 (from uvicorn[standard]==0.34.0->-r requirements.txt (line 2))
#8 8.776   Downloading watchfiles-1.2.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.9 kB)
#8 9.015 Collecting websockets>=10.4 (from uvicorn[standard]==0.34.0->-r requirements.txt (line 2))
#8 9.168   Downloading websockets-17.1-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (6.3 kB)
#8 9.344 Collecting anyio<5,>=3.4.0 (from starlette<0.42.0,>=0.40.0->fastapi==0.115.6->-r requirements.txt (line 1))
#8 9.498   Downloading anyio-4.15.1-py3-none-any.whl.metadata (4.7 kB)
#8 9.668 Collecting idna>=2.8 (from anyio<5,>=3.4.0->starlette<0.42.0,>=0.40.0->fastapi==0.115.6->-r requirements.txt (line 1))
#8 9.822   Downloading idna-3.19-py3-none-any.whl.metadata (9.2 kB)
#8 9.989 Downloading fastapi-0.115.6-py3-none-any.whl (94 kB)
#8 10.32 Downloading uvicorn-0.34.0-py3-none-any.whl (62 kB)
#8 10.50 Downloading psycopg-3.2.3-py3-none-any.whl (197 kB)
#8 10.84 Downloading pydantic-2.10.4-py3-none-any.whl (431 kB)
#8 11.18 Downloading psycopg_binary-3.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.2 MB)
#8 11.71    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.2/4.2 MB 8.0 MB/s eta 0:00:00
#8 11.87 Downloading pydantic_core-2.27.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.0 MB)
#8 12.04    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.0/2.0 MB 12.0 MB/s eta 0:00:00
#8 12.20 Downloading annotated_types-0.8.0-py3-none-any.whl (13 kB)
#8 12.35 Downloading click-8.5.0-py3-none-any.whl (125 kB)
#8 12.52 Downloading h11-0.16.0-py3-none-any.whl (37 kB)
#8 12.68 Downloading httptools-0.8.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (523 kB)
#8 12.87 Downloading python_dotenv-1.2.3-py3-none-any.whl (22 kB)
#8 13.03 Downloading pyyaml-6.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (807 kB)
#8 13.10    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 807.9/807.9 kB 12.3 MB/s eta 0:00:00
#8 13.25 Downloading starlette-0.41.3-py3-none-any.whl (73 kB)
#8 13.41 Downloading typing_extensions-4.16.0-py3-none-any.whl (45 kB)
#8 13.57 Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (4.4 MB)
#8 13.94    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.4/4.4 MB 11.9 MB/s eta 0:00:00
#8 14.11 Downloading watchfiles-1.2.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (456 kB)
#8 14.30 Downloading websockets-17.1-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (224 kB)
#8 14.47 Downloading anyio-4.15.1-py3-none-any.whl (132 kB)
#8 14.63 Downloading idna-3.19-py3-none-any.whl (68 kB)
#8 14.68 Installing collected packages: websockets, uvloop, typing-extensions, pyyaml, python-dotenv, psycopg-binary, idna, httptools, h11, click, annotated-types, uvicorn, pydantic-core, psycopg, anyio, watchfiles, starlette, pydantic, fastapi
#8 15.73 Successfully installed annotated-types-0.8.0 anyio-4.15.1 click-8.5.0 fastapi-0.115.6 h11-0.16.0 httptools-0.8.0 idna-3.19 psycopg-3.2.3 psycopg-binary-3.2.3 pydantic-2.10.4 pydantic-core-2.27.2 python-dotenv-1.2.3 pyyaml-6.0.3 starlette-0.41.3 typing-extensions-4.16.0 uvicorn-0.34.0 uvloop-0.22.1 watchfiles-1.2.0 websockets-17.1
#8 15.73 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
#8 16.29
#8 16.29 [notice] A new release of pip is available: 25.0.1 -> 26.2.1
#8 16.29 [notice] To update, run: pip install --upgrade pip
#8 DONE 16.6s

#9 [5/5] COPY app ./app
#9 DONE 0.1s

#10 exporting to image
#10 exporting layers
#10 exporting layers 2.2s done
#10 exporting manifest sha256:983df4404de9f7f83f0272ff9d3d050d451b2b2c120143ae23be5a2bab466745 0.0s done
#10 exporting config sha256:a4b0c5be69df78dd8b52d71eb8e8c206d65d8ca2a25e50a6ecd0499d37c4c400 0.0s done
#10 naming to docker.io/library/minipay-api:local done
#10 DONE 2.3s
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ docker logs  container-id  2>&1 | grep "Bootstrap Password:"
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl apply -f kubernetes/minipay.yaml
namespace/minipay created
secret/minipay-db created
configmap/minipay-db-init created
service/minipay-db created
statefulset.apps/minipay-db created
deployment.apps/minipay-api created
service/minipay-api created
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl get pods -n minipay
NAME                           READY   STATUS              RESTARTS   AGE
minipay-api-75c9c94498-8bqsk   0/1     Running             0          15s
minipay-api-75c9c94498-8mfjm   0/1     Running             0          15s
minipay-db-0                   0/1     ContainerCreating   0          15s
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl get svc -n minipay
NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
minipay-api   NodePort    10.109.89.191   <none>        80:30080/TCP   26s
minipay-db    ClusterIP   None            <none>        5432/TCP       27s
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl -n minipay rollout status statefulset/minipay-db --timeout=180s
partitioned roll out complete: 1 new pods have been updated...
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl -n minipay rollout status deployment/minipay-api --timeout=180s
deployment "minipay-api" successfully rolled out
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl get deployments -n minipay
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
minipay-api   2/2     2            2           88s
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl logs deployments/minipay-api -n minipay --tail=100
Found 2 pods, using pod/minipay-api-75c9c94498-8bqsk
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
INFO:     10.244.0.1:57830 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:51410 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:51418 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:37068 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:37082 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:37084 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:48830 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:48846 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:48858 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:38848 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:38858 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:38870 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40638 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40652 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40666 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43136 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43148 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43156 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53476 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53486 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53494 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43144 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43156 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43164 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:41946 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:41950 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:41958 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59538 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59546 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59552 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36760 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36776 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36788 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33998 - "GET /health HTTP/1.1" 200 OK
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl logs sts/minipay-api -n minipay --tail=100
error: error from server (NotFound): statefulsets.apps "minipay-api" not found in namespace "minipay"
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl logs sts/minipay-db -n minipay --tail=100
The files belonging to this database system will be owned by user "postgres".
This user must also own the server process.

The database cluster will be initialized with locale "en_US.utf8".
The default database encoding has accordingly been set to "UTF8".
The default text search configuration will be set to "english".

Data page checksums are disabled.

fixing permissions on existing directory /var/lib/postgresql/data ... ok
creating subdirectories ... ok
selecting dynamic shared memory implementation ... posix
selecting default max_connections ... 100
selecting default shared_buffers ... 128MB
selecting default time zone ... UTC
creating configuration files ... ok
running bootstrap script ... ok
sh: locale: not found
2026-09-14 18:15:50.778 UTC [37] WARNING:  no usable system locales were found
performing post-bootstrap initialization ... ok
syncing data to disk ... ok

initdb: warning: enabling "trust" authentication for local connections
initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.

Success. You can now start the database server using:

    pg_ctl -D /var/lib/postgresql/data -l logfile start

waiting for server to start....2026-09-14 18:15:53.203 UTC [43] LOG:  starting PostgreSQL 16.15 on x86_64-pc-linux-musl, compiled by gcc (Alpine 15.2.0) 15.2.0, 64-bit
2026-09-14 18:15:53.205 UTC [43] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2026-09-14 18:15:53.212 UTC [46] LOG:  database system was shut down at 2026-09-14 18:15:52 UTC
2026-09-14 18:15:53.217 UTC [43] LOG:  database system is ready to accept connections
 done
server started
CREATE DATABASE


/usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/init.sql
CREATE TABLE
CREATE TABLE
CREATE TABLE
INSERT 0 1
INSERT 0 1


waiting for server to shut down....2026-09-14 18:15:53.534 UTC [43] LOG:  received fast shutdown request
2026-09-14 18:15:53.536 UTC [43] LOG:  aborting any active transactions
2026-09-14 18:15:53.566 UTC [43] LOG:  background worker "logical replication launcher" (PID 49) exited with exit code 1
2026-09-14 18:15:53.568 UTC [44] LOG:  shutting down
2026-09-14 18:15:53.575 UTC [44] LOG:  checkpoint starting: shutdown immediate
2026-09-14 18:15:53.680 UTC [44] LOG:  checkpoint complete: wrote 950 buffers (5.8%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.032 s, sync=0.065 s, total=0.113 s; sync files=312, longest=0.005 s, average=0.001 s; distance=4352 kB, estimate=4352 kB; lsn=0/1937210, redo lsn=0/1937210
2026-09-14 18:15:53.687 UTC [43] LOG:  database system is shut down
 done
server stopped

PostgreSQL init process complete; ready for start up.

2026-09-14 18:15:53.768 UTC [1] LOG:  starting PostgreSQL 16.15 on x86_64-pc-linux-musl, compiled by gcc (Alpine 15.2.0) 15.2.0, 64-bit
2026-09-14 18:15:53.768 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2026-09-14 18:15:53.769 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2026-09-14 18:15:53.790 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2026-09-14 18:15:53.796 UTC [61] LOG:  database system was shut down at 2026-09-14 18:15:53 UTC
2026-09-14 18:15:53.804 UTC [1] LOG:  database system is ready to accept connections
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ ^[[200~minikube service minipay-api -n minipay --url~^C
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ minikube service minipay-api -n minipay --url
http://127.0.0.1:36405
❗  Because you are using a Docker driver on linux, the terminal needs to be open to run it.
^Cmahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ curl http://localhost:30080/health
curl: (7) Failed to connect to localhost port 30080 after 0 ms: Could not connect to server
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ curl http://127.0.0.1:36405/health
curl: (7) Failed to connect to 127.0.0.1 port 36405 after 0 ms: Could not connect to server
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl -n minipay port-forward svc/minipay-api 8080:80
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
^Cmahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl -n minipay port-forward svc/minipay-api 8080:80 -d
error: unknown shorthand flag: 'd' in -d
See 'kubectl port-forward --help' for usage.
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl -n minipay port-forward svc/minipay-api 8080:80 > /tmp/minipay-port-forward.log 2>&1 &
[1] 5987
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ curl http://127.0.0.1:8080/health
{"status":"ok","database":"ok"}mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl get pods -n minipay
NAME                           READY   STATUS    RESTARTS   AGE
minipay-api-75c9c94498-8bqsk   1/1     Running   0          7m21s
minipay-api-75c9c94498-8mfjm   1/1     Running   0          7m21s
minipay-db-0                   1/1     Running   0          7m21s
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl logs deployments/minipay-api --tail=200
error: error from server (NotFound): deployments.apps "minipay-api" not found in namespace "default"
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl logs deployments/minipay-api -n minipay --tail=200
Found 2 pods, using pod/minipay-api-75c9c94498-8bqsk
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
INFO:     10.244.0.1:57830 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:51410 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:51418 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:37068 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:37082 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:37084 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:48830 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:48846 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:48858 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:38848 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:38858 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:38870 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40638 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40652 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40666 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43136 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43148 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43156 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53476 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53486 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53494 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43144 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43156 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43164 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:41946 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:41950 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:41958 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59538 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59546 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59552 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36760 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36776 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36788 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33998 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:34010 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:34022 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:38780 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:38786 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:38792 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43970 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43974 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:43986 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40076 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40082 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40098 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:45848 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:45864 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:45880 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53736 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53752 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53760 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:57460 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:57462 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:57474 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:49866 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:49882 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:49896 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:49428 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:49438 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:49454 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36390 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36400 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36408 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:52350 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:52358 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:52372 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:48830 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:48840 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:48844 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:35792 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:35804 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:35808 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:51318 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:51320 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:51324 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:51040 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:51046 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:51054 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33446 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33458 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33464 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:46324 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:46328 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:46340 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:54886 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:54900 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:54906 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:50742 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:50746 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:50754 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33324 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33340 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33348 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:32992 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33008 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33010 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59088 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59094 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59108 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:58328 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:58330 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:58334 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:39304 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:39310 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:39312 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59262 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59270 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:59272 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36432 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36440 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:36456 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:47688 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:47700 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:47704 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:39382 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:39398 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:39414 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:57164 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:57170 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:57184 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:49028 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:49044 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:49048 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:34398 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:34402 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:41892 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:34406 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:56754 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:56756 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:56766 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:51838 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:51848 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:51856 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:54260 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:54264 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:54278 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40080 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40096 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40110 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:34524 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:34528 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:34540 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40848 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40862 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:40868 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:44216 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:44228 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:44242 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33056 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33058 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:33064 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:54752 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:54764 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:54780 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53330 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53338 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:53346 - "GET /health HTTP/1.1" 200 OK
INFO:     10.244.0.1:38908 - "GET /health HTTP/1.1" 200 OK
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$
```
