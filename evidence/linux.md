# Linux Evidence

This document records host-level checks collected from the WSL2 environment used to run Mini-Pay.

## Evidence Context

The commands were run locally by user `mahad` on host `DESKTOP-BFCF70D` in Ubuntu under WSL2. The evidence includes commands run from `/mnt/c/WINDOWS/system32`, `/mnt/g/Paysus/paysys-implementation-l2-assessment`, and `~/paysys/Mini-Pay` so the original session and filesystem context remain traceable.

## OS and Kernel

```bash
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ uname -a
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ cat /etc/os-release
```

```text
Linux DESKTOP-BFCF70D 6.18.33.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun 18 21:54:43 UTC 2026 x86_64 GNU/Linux
PRETTY_NAME="Ubuntu 26.04 LTS"
NAME="Ubuntu"
VERSION_ID="26.04"
VERSION="26.04 (Resolute Raccoon)"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
UBUNTU_CODENAME=resolute
```

## CPU, Memory, and Disk

```bash
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ nproc
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ free -h
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ df -h
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ uptime
```

```text
12

               total        used        free      shared  buff/cache   available
Mem:           7.7Gi       558Mi       7.1Gi       3.5Mi       212Mi       7.1Gi
Swap:          2.0Gi          0B       2.0Gi

Filesystem      Size  Used Avail Use% Mounted on
/usr/lib/modules/6.18.33.2-microsoft-standard-WSL2  3.9G     0  3.9G   0% /usr/lib/modules/6.18.33.2-microsoft-standard-WSL2
/mnt/wsl          3.9G  4.0K  3.9G   1% /mnt/wsl
/usr/lib/wsl/drivers 238G 182G 57G 77% /usr/lib/wsl/drivers
/dev/sdd       1007G  1.3G  955G   1% /
/mnt/wslg         3.9G   36K  3.9G   1% /mnt/wslg
/usr/lib/wsl/lib  3.9G     0  3.9G   0% /usr/lib/wsl/lib
/init              3.9G  2.8M  3.9G   1% /init
/run               3.9G  504K  3.9G   1% /run
/run/lock          3.9G     0  3.9G   0% /run/lock
/run/shm           3.9G     0  3.9G   0% /run/shm
/mnt/wslg/versions.txt 3.9G 100K 3.9G 1% /mnt/wslg/versions.txt
/mnt/wslg/doc       3.9G  100K  3.9G   1% /mnt/wslg/doc
C:\             238G  182G   57G  77% /mnt/c
D:\             477G  163G  315G  35% /mnt/d
E:\             443G  367G   77G  83% /mnt/e
F:\             489G  462G   27G  95% /mnt/f
G:\             932G  638G  295G  69% /mnt/g
/tmp               3.9G     0  3.9G   0% /tmp
/run/user/1000      791M   12K  791M   1% /run/user/1000

22:03:54 up 14 min,  1 user,  load average: 0.04, 0.04, 0.05
```

## Listening Ports

```bash
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ ss -lntp
```

```text
State   Recv-Q  Send-Q  Local Address:Port       Peer Address:Port  Process
LISTEN  0       4096    127.0.0.53%lo:53        0.0.0.0:*
LISTEN  0       4096    127.0.0.54:53           0.0.0.0:*
LISTEN  0       1000    10.255.255.254:53       0.0.0.0:*
```

## DNS and Network Connectivity

```bash
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ curl -I https://google.com
```

```text
HTTP/2 301
location: https://www.google.com/
content-type: text/html; charset=UTF-8
server: gws
```

The HTTP 301 response confirms outbound HTTPS connectivity and DNS resolution.

## Docker and Application Logs

```bash
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo docker ps
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo docker logs --tail=100 bd250f5d6665
```

```text
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                                         NAMES
bd250f5d6665   postgres:16   "docker-entrypoint.s…"   12 minutes ago   Up 12 minutes   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   minipay-db

The database system is ready to accept connections
```

## Kubernetes API Logs

```bash
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl get deployments -n minipay
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ kubectl logs deployments/minipay-api -n minipay --tail=100
```

```text
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
minipay-api   2/2     2            2           88s

INFO:     Started server process [1]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
INFO:     10.244.0.1:57830 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO:     10.244.0.1:48830 - "GET /health HTTP/1.1" 200 OK
```

The API initially returned `503 Service Unavailable` while its dependency was starting, then returned `200 OK` after the database became ready.

## Highest Memory Consumer

```bash
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ ps aux --sort=-%mem | head
```

```text
USER         PID  %CPU  %MEM  VSZ      RSS    TTY   STAT  COMMAND
mahad       5987  0.0   0.6   1321044  52516  pts/2 Sl    kubectl -n minipay port-forward svc/minipay-api 8080:80
root        1788  0.0   0.3   1287532  29120  pts/3 Ssl+  /run/docker-desktop/docker-desktop-user-distro proxy
```

## Disk Usage by Directory

```bash
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ du -sh */
```

```text
16K     app/
64K     evidence/
12K     investigation/
12K     kubernetes/
12K     sql/
```

## Repeatable Health Check

The repository includes [`scripts/healthcheck.sh`](../scripts/healthcheck.sh), which checks the API health endpoint and returns a non-zero exit code on failure.

```bash
#!/usr/bin/env bash
set -u

URL="${1:-http://localhost:8080/health}"

if curl --fail --silent --show-error --max-time 5 "$URL" >/dev/null; then
    echo "Health check passed: $URL"
    exit 0
fi

echo "Health check failed: $URL" >&2
exit 1
```

Example execution:

```bash
mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay/scripts$ ./healthcheck.sh
```

```text
Health check passed: http://localhost:8080/health
```


