# Служит для быстрого набора команд в терминале
import os
import fire

def docker_up():
    os.system("docker compose -f docker-compose.dev.yaml up")
    
def docker_build():
    os.system("docker compose -f docker-compose.dev.yaml build")

def docker_down():
    os.system("docker compose -f docker-compose.dev.yaml down")
    
if __name__ == "__main__":
    fire.Fire({"up": docker_up, "build": docker_build, "down": docker_down})