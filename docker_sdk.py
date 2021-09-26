import docker


def run_container(container_name:str, command:list=[]) -> None:
    client = docker.from_env()
    print(client.containers.run(container_name, command))


def run_container_dateched(container_name:str) -> None:
    client = docker.from_env()
    container = client.containers.run(container_name, detach=True)
    print(container.id)


def list_containers() -> None:
    client = docker.from_env()
    for container in client.containers.list():
        print(container.id)
        print(container.name)


def stop_all_containers() -> None:
    client = docker.from_env()
    for container in client.containers.list():
        container.stop()


def print_logs(container_name:str) -> None:
    client = docker.from_env()
    container = client.containers.get(container_name)
    print(container.logs())


def list_image() -> None:
    client = docker.from_env()
    for image in client.images.list():
        print(image.id)
        print(image.tag)


def pull_image(image_name:str) -> None:
    client = docker.from_env()
    image = client.images.pull(image_name)
    print(image.id)
    print(image.tag)


def commit_container(image_name:str):
    client = docker.from_env()
    container = client.containers.run(image_name, [], detach=True)
    container.wait()
    image = container.commit("committed_1")
    print(image.id)


def main():
    # run_container("alpine", ["echo", "hello", "world"])
    commit_container("alpine")



if __name__ == "__main__":
    main()


#Docs: https://docs.docker.com/engine/api/sdk/examples/