***Create MySQL NDB cluster and initialise database + tables***

1. Install MySQL and Docker on your machine (add Docker and MySQL Shell to path).
2. Copy the folder DOCKER_CLUSTER to your local disk so that the path is C:\DOCKER_CLUSTER .
3. Run create_cluster.py to create the cluster
4. Run create_user.py to access the mysql server node and create a user (update username as required)
5. Run create_database_tables.py to create the database and tables with schema (Ayush can add the instantiate tables part).
6. Run delete_cluster.py to stop and delete all cluster container instances.


- mySQL server node 1 is available at port 3304
- mySQL server node 2 is available at port 3305
