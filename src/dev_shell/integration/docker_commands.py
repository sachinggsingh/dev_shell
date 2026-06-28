import shutil
import subprocess


class DockerCommands:

    @staticmethod
    def _run(command):

        if shutil.which("docker") is None:
            print("Docker is not installed.")
            return

        try:

            result = subprocess.run(
                command,
                text=True
            )

        except Exception as e:

            print(f"Error: {e}")

    @staticmethod
    def help():

        print("""
Docker Commands

Containers
----------
docker ps
docker ps -a
docker start <container>
docker stop <container>
docker restart <container>
docker rm <container>
docker logs <container>
docker exec -it <container> bash

Images
------
docker images
docker pull <image>
docker push <image>
docker build -t <tag> .
docker rmi <image>

Volumes
-------
docker volume ls
docker volume create
docker volume rm

Networks
--------
docker network ls
docker network create
docker network rm

Compose
-------
docker compose up
docker compose down
docker compose logs

System
------
docker info
docker version
docker stats
docker system df
docker system prune
""")

    def execute(self, args):

        if not args:
            self.help()
            return

        command = args[0]

        aliases = {

            "containers": ["ps", "-a"],

            "running": ["ps"],

            "images": ["images"],

            "volumes": ["volume", "ls"],

            "networks": ["network", "ls"],

            "stats": ["stats"],

            "system": ["system", "df"]

        }

        if command in aliases:

            self._run(
                ["docker"] +
                aliases[command] +
                args[1:]
            )

        else:

            self._run(
                ["docker"] + args
            )