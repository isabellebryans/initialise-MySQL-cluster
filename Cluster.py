import subprocess

class Cluster():
    def __init__(self, name):
        self.name = name
        self.ip_prefix = "10.100.0."
        self.management_node_name = "management1"
        self.data_node_names = ["ndb1", "ndb2"]
        self.sql_node_names = ["mysqld1", "mysqld2"]
        self.create_network(self.name, self.prefix)

    def run_containers(self):
        self.run_mysql_container(self.management_node_name, self.name, "ndb_mgmd", None, None, self.ip_prefix+"2", None)
        self.run_mysql_container(self.data_node_names[0], self.name, "data", 2, self.ip_prefix+"2", self.ip_prefix+"3", None)
        self.run_mysql_container(self.data_node_names[1], self.name, "data", 3, self.ip_prefix+"2", self.ip_prefix+"4", None)
        # Start MySQL server node
        self.run_mysql_container(self.sql_node_name[0], self.name, "sql", 4, self.ip_prefix+"2", self.ip_prefix+"10", "3304")
        self.run_mysql_container(self.sql_node_name[1], self.name, "sql", 5, self.ip_prefix+"2", self.ip_prefix+"11", "3305")

    def execute_command(self,command):
        """Execute a shell command."""
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print(f"Success: {stdout.decode('utf-8')}")
        else:
            print(f"Error: {stderr.decode('utf-8')}")

    def create_network(self, network_name, ip):
        """Create a Docker network."""
        command = f"docker network create {network_name} --subnet={ip}0/16"
        self.execute_command(command)
        
    def run_mysql_container(self, container_name, node_type, node_id, connect_string, ip_addr, port):
        """Run a MySQL NDB Cluster container."""
        if node_type == "ndb_mgmd":
            command = f"docker run -d --net={self.name} --hostname {container_name}  -v \"C:/DOCKER_CLUSTER/mysql/my.cnf:/etc/my.cnf\" -v \"C:/DOCKER_CLUSTER/mysql/mysql-cluster.cnf:/etc/mysql-cluster.cnf\"   --name={container_name} --ip={ip_addr} mysql/mysql-cluster ndb_mgmd --ndb-nodeid=1 --reload --initial"
        elif node_type == "data":
            command = f"docker run -d --net={self.name}  -v \"C:/DOCKER_CLUSTER/mysql/mysql-cluster.cnf:/etc/mysql-cluster.cnf\" --name={container_name} --ip={ip_addr} mysql/mysql-cluster ndbd --ndb-nodeid={node_id} --connect-string {connect_string}"
        elif node_type == "sql":
            command = f"docker run -d -p {port}:3306  -v \"C:/DOCKER_CLUSTER/mysql/mysql-cluster.cnf:/etc/mysql-cluster.cnf\" --net={self.name} --name={container_name} --ip={ip_addr} -e MYSQL_RANDOM_ROOT_PASSWORD=true mysql/mysql-cluster mysqld --ndb-nodeid={node_id} --ndb-connectstring {connect_string}"
        else:
            print("Invalid node type specified.")
            return
        self.execute_command(command)

    def delete_mysql_cluster(self):
        all_container_names = [self.management_node_name] + self.data_node_names + self.sql_node_names

        # Delete Docker containers
        self.delete_docker_containers(all_container_names)

        # Delete Docker network
        self.delete_docker_network()


    def delete_docker_containers(self, container_names):
        """Stop and remove specified Docker containers."""
        for name in container_names:
            # Stop the container
            self.execute_command(f"docker stop {name}")
            # Remove the container
            self.execute_command(f"docker rm {name}")

    def delete_docker_network(self):
        """Remove Docker network."""
        self.execute_command(f"docker network rm {self.name}")

    