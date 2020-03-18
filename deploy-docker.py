#!/usr/bin/env python
import subprocess
from pathlib import Path
import os

IP = "13.124.222.31"
HOST = "ubuntu"
TARGET = f'{HOST}@{IP}'  # ubuntu@15.165.204.55
HOME = str(Path.home())  # "/Users/hongbeen"
SSH_KEY = os.path.join(HOME, '.ssh', 'pb_nexflex.pem')
PROJECT_FILE = os.path.join(HOME, 'projects', 'wps12th', 'Netflex_Clone_Backend')
DOCKER_IMAGE_TAG = "fcnetflex/fc-netflex"
SECRETS = os.path.join(HOME, ".aws", "credentials")

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-d', ''),
    ('-p', '80:80'),
    ('--name', 'netflex_container'),
]


# Local Host 에서 실행
def run(cmd, ignore_error=False):  # ignore_error을 이용하면 오류를 무시하고 다음 단계를 진행함.
    process = subprocess.run(cmd, shell=True)
    if not ignore_error:
        process.check_returncode()


# EC2에서 실행
def ssh_run(cmd, ignore_error=False):
    run(f"ssh -o StrictHostKeyChecking=no -i {SSH_KEY} {TARGET} -C {cmd}", ignore_error=ignore_error)


# requirements.txt 생성, 이미지 생성, 이미지 Docker hub 에 올리기
def local_build_push():
    run(f'poetry export -f requirements.txt > requirements.txt')  # poetry.rock에 있는 내용을 requirments.txt로 옮겨줌
    run(f'docker build -t {DOCKER_IMAGE_TAG} .')  # Host Os 에서 Docker 이미지 생성
    run(f'docker push {DOCKER_IMAGE_TAG}')  # 생성한 Docker 이미지를 Docker hub 전달


# 서버 초기설정
def server_init():
    ssh_run(f'sudo apt update')
    ssh_run(f'sudo DEBIAN_FRONTED=noninteractive apt -y dist-upgrade -y')
    ssh_run(f'sudo apt -y install docker.io')


# 실행중인 컨테이너 stop, pull, run
def server_pull_run():
    ssh_run(f'sudo docker stop netflex_container', ignore_error=True)
    ssh_run(f'sudo docker pull {DOCKER_IMAGE_TAG}')  # Docker hub 에 있는 Docker이미지를 EC2 내부로 가져온다
    # 가져온 이미지를 실행
    ssh_run('sudo docker run {options} {tag} /bin/bash'.format(
        options=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTIONS
        ]),
        tag=DOCKER_IMAGE_TAG
    ))


def copy_server():
    run(f'scp -i {SSH_KEY} {SECRETS} {TARGET}:/tmp', ignore_error=True)
    ssh_run(f'sudo docker cp /tmp/credentials netflex_container:/root/.aws/')


def server_cmd():
    # ssh_run(f'sudo docker exec netflex_container /user/sbin/nginx -s stop', ignore_error=True)
    # ssh_run(f'sudo docker exec netflex_container python manage.py collectstatic --noinput')
    ssh_run(f'sudo docker exec netflex_container supervisord -c /srv/Netflex_Clone_Backend/.config/supervisord.conf -n')


if __name__ == '__main__':
    try:
        local_build_push()
        server_init()
        server_pull_run()
        copy_server()
        server_cmd()
    except subprocess.CalledProcessError as e:
        print('docker-deploy-error')
        print('cmd: ', e.cmd)
        print('return code: ', e.returncode)
        print('output: ', e.output)
        print('stdout: ', e.stdout)
        print('stderr: ', e.stderr)
