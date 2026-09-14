mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ minikube start --driver=docker --cpus=4 --memory=4096
😄  minikube v1.39.0 on Ubuntu 26.04 (kvm/amd64)
✨  Using the docker driver based on user configuration

💣  Exiting due to PROVIDER_DOCKER_NEWGRP: "docker version --format <no value>-<no value>:<no value>" exit status 1: permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
💡  Suggestion: Add your user to the 'docker' group: 'sudo usermod -aG docker $USER && newgrp docker'
📘  Documentation: https://docs.docker.com/engine/install/linux-postinstall/

mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  --name rancher \
  rancher/rancher:v2.9.2
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo !!
sudo docker run -d --restart=unless-stopped   -p 80:80 -p 443:443   --name rancher   rancher/rancher:v2.9.2
Unable to find image 'rancher/rancher:v2.9.2' locally
v2.9.2: Pulling from rancher/rancher
83a83d08b76a: Pull complete
4f4fb700ef54: Pull complete
f29d8c2c0a8a: Pull complete
f9b52d555bc3: Pull complete
ee78742af818: Pull complete
967086fd121e: Pull complete
708002f0f717: Pull complete
9b1f5f3a8e71: Pull complete
e50df727d370: Pull complete
ccd876f3e682: Pull complete
8d71b8d4e7bb: Pull complete
5973bb25bfb0: Pull complete
9fb2942ef2e1: Pull complete
935e3e307a66: Pull complete
1155075e238c: Pull complete
c502336bf586: Pull complete
7e727bd9e2db: Pull complete
e3f06fff7244: Pull complete
3568bc303555: Pull complete
b3a6ad6d7cf4: Pull complete
b99d4ccaf6b7: Pull complete
bb60c5e7735b: Pull complete
7fdf77566dc6: Pull complete
Digest: sha256:9c2435827884627a3f7472f63b87989724a1229079654e83073ac9160b8dbd08
Status: Downloaded newer image for rancher/rancher:v2.9.2
90a66f343cf7851b9adcd2b325fd14d70761b97ee87e49d7154b28be0d2c12bb
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED              STATUS                  PORTS                                                                          NAMES
90a66f343cf7   rancher/rancher:v2.9.2   "entrypoint.sh"          About a minute ago   Up Less than a second   0.0.0.0:80->80/tcp, [::]:80->80/tcp, 0.0.0.0:443->443/tcp, [::]:443->443/tcp   rancher
bd250f5d6665   postgres:16              "docker-entrypoint.s…"   20 minutes ago       Up 20 minutes           0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp                                    minipay-db
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo docker ps
\\CONTAINER ID   IMAGE                    COMMAND                  CREATED              STATUS                          PORTS                                         NAMES
90a66f343cf7   rancher/rancher:v2.9.2   "entrypoint.sh"          About a minute ago   Restarting (1) 39 seconds ago                                                 rancher
bd250f5d6665   postgres:16              "docker-entrypoint.s…"   21 minutes ago       Up 21 minutes                   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   minipay-db
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo docker logs rancher --tail 100
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
ERROR: Rancher must be ran with the --privileged flag when running outside of Kubernetes
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo docker rm -f rancher
rancher
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo docker run -d --restart=unless-stopped \
  --privileged \
  -p 80:80 -p 443:443 \
  --name rancher \
  rancher/rancher:v2.9.2
682d164ba64d50f7e2dde066a377db8fc88a7266c2595387db52833f4df1c6e6
mahad@DESKTOP-BFCF70D:/mnt/g/Paysus/paysys-implementation-l2-assessment$ sudo docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS          PORTS                                                                          NAMES
682d164ba64d   rancher/rancher:v2.9.2   "entrypoint.sh"          14 seconds ago   Up 3 seconds    0.0.0.0:80->80/tcp, [::]:80->80/tcp, 0.0.0.0:443->443/tcp, [::]:443->443/tcp   rancher
bd250f5d6665   postgres:16              "docker-entrypoint.s…"   22 minutes ago   Up 22 minutes   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp                                    minipay-db
