import subprocess

def execute_command(command):
    """Execute a shell command."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print(f"Success: {stdout.decode('utf-8')}")
    else:
        print(f"Error: {stderr.decode('utf-8')}")

def delete_docker_containers(container_names):
    """Stop and remove specified Docker containers."""
    for name in container_names:
        # Stop the container
        execute_command(f"docker stop {name}")
        # Remove the container
        execute_command(f"docker rm {name}")

def delete_docker_network(network_name):
    """Remove Docker network."""
    execute_command(f"docker network rm {network_name}")

def cleanup_mysql_cluster():
    network_name = "cluster"
    management_node_name = "management1"
    data_node_names = ["ndb1", "ndb2"]
    sql_node_names = ["mysqld1", "mysqld2"]

    all_container_names = [management_node_name] + data_node_names + sql_node_names

    # Delete Docker containers
    delete_docker_containers(all_container_names)

    # Delete Docker network
    delete_docker_network(network_name)

if __name__ == "__main__":
    cleanup_mysql_cluster()
