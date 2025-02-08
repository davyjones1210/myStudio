import os
import logging

logging.basicConfig(level=logging.INFO)
username = os.environ.get("USERNAME")  # Windows
# username = os.environ.get("USER")  # Mac/Linux

logging.info(f"Logged in as: {username}")


os.environ["MY_VAR"] = "Hello World"
logging.info(os.environ["MY_VAR"])  # Output: Hello World


logging.info(os.getcwd())  # Get Current Working Directory


# os.chdir("C:\\Users")  # Change to 'C:\Users' on Windows
# logging.info(os.getcwd())  # Verify new path

# os.mkdir("my_folder")  # Create folder

# os.rmdir("my_folder")  # Remove folder

file_path = "README.md"

if os.path.exists(file_path):
    logging.info("File exists")
else:
    logging.info("File not found")

files = os.listdir(".")  # List files in the current directory
logging.info(files)

file_path = os.path.join("C:\\Users", "example.txt")
logging.info(file_path)  # Output: C:\Users\example.txt


if os.path.exists("example.txt"):
    os.remove("example.txt")
    logging.info("File deleted")
else:
    logging.info("File not found")


# os.system("notepad")  # Opens Notepad (Windows)
# output = os.popen("dir").read()  # Windows (use "ls" for Mac/Linux)
# logging.info(output)
# os.startfile("C:\\Program Files\\Blender Foundation\\Blender 4.3\\blender.exe")  # Opens Blender

# system_info = os.popen("systeminfo").read()  # Windows
# logging.info(system_info)

python_version = os.popen("python --version").read()
logging.info(python_version)

logging.info(os.environ.get("USERNAME"))  # Get the username
os.environ["MY_VAR"] = "Hello World"
logging.info(os.environ["MY_VAR"])

# print(os.getpid())  # Current process ID
# print(os.getppid())  # Parent process ID

print(os.getlogin())  # Get the username (Windows/Linux)

print(os.name)  # 'nt' (Windows) or 'posix' (Linux/Mac)

print(os.cpu_count())  # Number of CPU cores

print(os.environ)  # Print all environment variables