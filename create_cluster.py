
import subprocess

def execute_command(command):
    """Execute a shell command."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print(f"Success: {stdout.decode('utf-8')}")
    else:
        print(f"Error: {stderr.decode('utf-8')}")

def create_network(network_name, ip):
    """Create a Docker network."""
    command = f"docker network create {network_name} --subnet={ip}0/16"
    execute_command(command)

def run_mysql_container(container_name, network_name, node_type, node_id, connect_string, ip_addr, port):
    """Run a MySQL NDB Cluster container."""
    if node_type == "ndb_mgmd":
        command = f"docker run -d --net={network_name} --hostname {container_name}  -v \"C:/DOCKER_CLUSTER/mysql/my.cnf:/etc/my.cnf\" -v \"C:/DOCKER_CLUSTER/mysql/mysql-cluster.cnf:/etc/mysql-cluster.cnf\"   --name={container_name} --ip={ip_addr} mysql/mysql-cluster ndb_mgmd --ndb-nodeid=1 --reload --initial"
    elif node_type == "data":
        command = f"docker run -d --net={network_name}  -v \"C:/DOCKER_CLUSTER/mysql/mysql-cluster.cnf:/etc/mysql-cluster.cnf\" --name={container_name} --ip={ip_addr} mysql/mysql-cluster ndbd --ndb-nodeid={node_id} --connect-string {connect_string}"
    elif node_type == "sql":
        command = f"docker run -d -p {port}:3306  -v \"C:/DOCKER_CLUSTER/mysql/mysql-cluster.cnf:/etc/mysql-cluster.cnf\" --net={network_name} --name={container_name} --ip={ip_addr} -e MYSQL_RANDOM_ROOT_PASSWORD=true mysql/mysql-cluster mysqld --ndb-nodeid={node_id} --ndb-connectstring {connect_string}"
    else:
        print("Invalid node type specified.")
        return
    execute_command(command)

def setup_mysql_cluster():
    network_name = "cluster"
    management_node_name = "management1"
    data_node_names = ["ndb1", "ndb2"]
    sql_node_name = ["mysqld1", "mysqld2"]
    ip="10.100.0."


    # Create Docker network
    create_network(network_name, ip)

    # Start management node
    run_mysql_container(management_node_name, network_name, "ndb_mgmd", None, None, ip+"2", None)

    # Start data nodes
    run_mysql_container(data_node_names[0], network_name, "data", 2, ip+"2", ip+"3", None)

    run_mysql_container(data_node_names[1], network_name, "data", 3, ip+"2", ip+"4", None)

    # Start MySQL server node
    run_mysql_container(sql_node_name[0], network_name, "sql", 4, ip+"2", ip+"10", "3304")

    run_mysql_container(sql_node_name[1], network_name, "sql", 5, ip+"2", ip+"11", "3305")

if __name__ == "__main__":
    setup_mysql_cluster()
