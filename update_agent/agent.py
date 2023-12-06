import subprocess
import os

def start():
      repo_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
      process = subprocess.Popen(["docker-compose", "up", "-d"], cwd=repo_path, stdout=subprocess.PIPE)
      for line in process.stdout:
          print(line.decode())
      process.wait()

if __name__ == "__main__":
    start()
