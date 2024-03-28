import subprocess

def execute_command(command, capture_output=False):
    """Execute a shell command."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    if process.returncode == 0 and capture_output:
        return stdout
    elif process.returncode == 0:
        print(f"Success: {stdout}")
    else:
        print(f"Error: {stderr}")
    return None

def create_database(user, password, port, name, host):
    sql_command=f"CREATE DATABASE {name};"
    command = f"mysqlsh -u {user} -h {host} -P {port} --sql -p{password} -e \"{sql_command}\""
    execute_command(command)

def create_tables():
    """CONTINUE ON HERE TO INITIALISE TABLES WITH SCHEMA"""



if __name__ == "__main__":
    user="isabelle"
    password="password"
    port = "3304"
    db_name = "Loyalty_Scheme"
    create_database( user, password, port, db_name, "localhost")
    create_tables()
