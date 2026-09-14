1) OS/kernel identification 
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ uname -a
Linux DESKTOP-BFCF70D 6.18.33.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun 18 21:54:43 UTC 2026 x86_64 GNU/Linux

mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ cat /etc/os-release
PRETTY_NAME="Ubuntu 26.04 LTS"
NAME="Ubuntu"
VERSION_ID="26.04"
VERSION="26.04 (Resolute Raccoon)"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=resolute
LOGO=ubuntu-logo
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$

2) CPU, memory and disk utilization
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ nproc
12
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ free -h
               total        used        free      shared  buff/cache   available
Mem:           7.7Gi       558Mi       7.1Gi       3.5Mi       212Mi       7.2Gi
Swap:          2.0Gi          0B       2.0Gi

mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ df -h
Filesystem      Size  Used Avail Use% Mounted on
none            3.9G     0  3.9G   0% /usr/lib/modules/6.18.33.2-microsoft-standard-WSL2
none            3.9G  4.0K  3.9G   1% /mnt/wsl
drivers         238G  182G   57G  77% /usr/lib/wsl/drivers
/dev/sdd       1007G  1.3G  955G   1% /
none            3.9G   36K  3.9G   1% /mnt/wslg
none            3.9G     0  3.9G   0% /usr/lib/wsl/lib
rootfs          3.9G  2.8M  3.9G   1% /init
none            3.9G  504K  3.9G   1% /run
none            3.9G     0  3.9G   0% /run/lock
none            3.9G     0  3.9G   0% /run/shm
none            3.9G  100K  3.9G   1% /mnt/wslg/versions.txt
none            3.9G  100K  3.9G   1% /mnt/wslg/doc
C:\             238G  182G   57G  77% /mnt/c
D:\             477G  163G  315G  35% /mnt/d
E:\             443G  367G   77G  83% /mnt/e
F:\             489G  462G   27G  95% /mnt/f
G:\             932G  638G  295G  69% /mnt/g
tmpfs           3.9G     0  3.9G   0% /tmp
none            1.0M     0  1.0M   0% /run/credentials/systemd-journald.service
none            1.0M     0  1.0M   0% /run/credentials/systemd-resolved.service
none            1.0M     0  1.0M   0% /run/credentials/getty@tty1.service
tmpfs           791M   12K  791M   1% /run/user/1000

mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ uptime
 22:03:54 up 14 min,  1 user,  load average: 0.04, 0.04, 0.05

3) listening ports and relevant processes
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ ss -lntp
State             Recv-Q            Send-Q                        Local Address:Port                         Peer Address:Port            Process
LISTEN            0                 4096                          127.0.0.53%lo:53                                0.0.0.0:*
LISTEN            0                 4096                             127.0.0.54:53                                0.0.0.0:*
LISTEN            0                 1000                         10.255.255.254:53                                0.0.0.0:*

mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.1  24732 15680 ?        Ss   21:49   0:00 /sbin/init
root           2  0.0  0.0   3180  2208 hvc0     Sl+  21:49   0:00 /init
root          10  0.0  0.0   3212  2140 hvc0     Sl+  21:49   0:00 plan9 --control-socket 7 --log-level 4 --server-fd 8 --pipe-fd 10 --log-truncate
root          63  0.0  0.2  50392 16664 ?        S<s  21:49   0:00 /usr/lib/systemd/systemd-journald
systemd+      97  0.0  0.1  22540 14508 ?        Ss   21:49   0:00 /usr/lib/systemd/systemd-resolved
root         106  0.0  0.1  35392 12244 ?        Ss   21:49   0:00 /usr/lib/systemd/systemd-udevd
root         193  0.0  0.0   2888  1948 ?        Ss   21:49   0:00 /bin/sh /usr/lib/systemd/scripts/chronyd-starter.sh -n -F 1
root         194  0.0  0.0   4472  3024 ?        Ss   21:49   0:00 /usr/sbin/cron -f -P
message+     195  0.0  0.0   8828  5348 ?        Ss   21:49   0:00 @dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslo
root         199  0.0  0.3  44092 29592 ?        Ss   21:49   0:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
root         203  0.0  0.1  18452  9340 ?        Ss   21:49   0:00 /usr/lib/systemd/systemd-logind
syslog       223  0.0  0.0 220548  5628 ?        Ssl  21:49   0:00 /usr/sbin/rsyslogd -n -iNONE
root         225  0.0  0.0   5492  2724 tty1     Ss+  21:49   0:00 /usr/sbin/agetty --noreset --noclear --issue-file=/etc/issue:/etc/issue.d:/run/issue.d:/us
_chrony      247  0.0  0.1  24520 11868 ?        S    21:49   0:00 /usr/sbin/chronyd -n -F 1 -x
root         253  0.0  0.4 123456 32584 ?        Ssl  21:49   0:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-sig
_chrony      263  0.0  0.0  12092  2464 ?        S    21:49   0:00 /usr/sbin/chronyd -n -F 1 -x
root         445  0.0  0.0   3188  1112 ?        Ss   21:49   0:00 /init
root         446  0.0  0.0   3204  1248 ?        S    21:49   0:00 /init
mahad        447  0.0  0.0   6312  5656 pts/0    Ss   21:49   0:00 /bin/bash
mahad        533  0.0  0.1  22344 13536 ?        Ss   21:49   0:00 /usr/lib/systemd/systemd --user
mahad        535  0.0  0.0  22912  4092 ?        S    21:49   0:00 (sd-pam)
root         672  0.0  0.0   8648  5576 ?        Ss   21:50   0:00 login -- mahad
mahad        717  0.0  0.0   6136  5404 pts/1    Ss+  21:50   0:00 -bash
root         866  0.0  0.0   3188  1120 ?        Ss   21:57   0:00 /init
root         867  0.0  0.0   3204  1256 ?        S    21:57   0:00 /init
mahad        869  0.0  0.0   6268  5600 pts/2    Ss   21:57   0:00 -bash
mahad       1130  0.0  0.0   5916  5332 pts/0    S+   22:05   0:00 nano linux.md
mahad       1208  0.0  0.0   7160  4300 pts/2    R+   22:06   0:00 ps aux
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ 

4) DNS/network connectivity checks
mahad@DESKTOP-BFCF70D:/mnt/c/WINDOWS/system32$ curl -I https://google.com
HTTP/2 301
location: https://www.google.com/
content-type: text/html; charset=UTF-8
content-security-policy-report-only: object-src 'none';base-uri 'self';script-src 'nonce-tSKhQM4rIaP9L3yPAJ4g_A' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
date: Mon, 14 Sep 2026 17:05:59 GMT
expires: Wed, 14 Oct 2026 17:05:59 GMT
cache-control: public, max-age=2592000
server: gws
content-length: 220
x-xss-protection: 0
x-frame-options: SAMEORIGIN
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000

5) application/container logs
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                                         NAMES
bd250f5d6665   postgres:16   "docker-entrypoint.s…"   12 minutes ago   Up 12 minutes   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   minipay-db
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo docker logs --tail=100 bd250f5d6665
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
selecting default time zone ... Etc/UTC
creating configuration files ... ok
running bootstrap script ... ok
performing post-bootstrap initialization ... ok
syncing data to disk ... ok


Success. You can now start the database server using:
initdb: warning: enabling "trust" authentication for local connections
initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.

    pg_ctl -D /var/lib/postgresql/data -l logfile start

waiting for server to start....2026-09-14 17:25:12.190 UTC [48] LOG:  starting PostgreSQL 16.15 (Debian 16.15-1.pgdg13+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
2026-09-14 17:25:12.192 UTC [48] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2026-09-14 17:25:12.198 UTC [51] LOG:  database system was shut down at 2026-09-14 17:25:11 UTC
2026-09-14 17:25:12.202 UTC [48] LOG:  database system is ready to accept connections
 done
server started
CREATE DATABASE


/usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*

waiting for server to shut down...2026-09-14 17:25:12.380 UTC [48] LOG:  received fast shutdown request
.2026-09-14 17:25:12.382 UTC [48] LOG:  aborting any active transactions
2026-09-14 17:25:12.383 UTC [48] LOG:  background worker "logical replication launcher" (PID 54) exited with exit code 1
2026-09-14 17:25:12.383 UTC [49] LOG:  shutting down
2026-09-14 17:25:12.385 UTC [49] LOG:  checkpoint starting: shutdown immediate
2026-09-14 17:25:12.470 UTC [49] LOG:  checkpoint complete: wrote 926 buffers (5.7%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.023 s, sync=0.058 s, total=0.088 s; sync files=301, longest=0.020 s, average=0.001 s; distance=4273 kB, estimate=4273 kB; lsn=0/191F0E0, redo lsn=0/191F0E0
2026-09-14 17:25:12.477 UTC [48] LOG:  database system is shut down
 done
server stopped

PostgreSQL init process complete; ready for start up.

2026-09-14 17:25:12.503 UTC [1] LOG:  starting PostgreSQL 16.15 (Debian 16.15-1.pgdg13+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
2026-09-14 17:25:12.503 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2026-09-14 17:25:12.503 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2026-09-14 17:25:12.506 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2026-09-14 17:25:12.512 UTC [64] LOG:  database system was shut down at 2026-09-14 17:25:12 UTC
2026-09-14 17:25:12.517 UTC [1] LOG:  database system is ready to accept connections
2026-09-14 17:30:12.600 UTC [62] LOG:  checkpoint starting: time
2026-09-14 17:32:54.582 UTC [62] LOG:  checkpoint complete: wrote 1619 buffers (9.9%); 0 WAL file(s) added, 0 removed, 2 recycled; write=161.550 s, sync=0.014 s, total=161.983 s; sync files=70, longest=0.004 s, average=0.001 s; distance=23925 kB, estimate=23925 kB; lsn=0/3303DC8, redo lsn=0/307C7D0
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$


