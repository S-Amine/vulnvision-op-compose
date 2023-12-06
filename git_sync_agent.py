import os
import git
import time
from datetime import datetime
from update_agent.utils import init_logger, get_current_commit_hash
import subprocess

# Configuration
repo_path = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the script
sleep_interval_seconds = 30  # Set the sleep interval in seconds
log_file = "git_auto_updater.log"  # Specify the log file name
agent = "update_agent/agent.py"  # Specify the path to the update agent script

def update_repo(logger):
    try:
        # Initialize the Git repository and remote
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin

        # Get the current commit hash before the pull
        before_pull_commit = get_current_commit_hash(repo)

        # Pull changes from the remote repository (origin)
        origin.pull(force=True)

        # Get the current commit hash after the pull
        after_pull_commit = get_current_commit_hash(repo)

        if before_pull_commit != after_pull_commit:
            info = "Repository is updated. Running update script."
            print(info)
            logger.info(info)

            # Update Python packages based on requirements.txt
            process = subprocess.Popen(["pip", "install", "-r", "requirements.txt"], cwd=repo_path, stdout=subprocess.PIPE)
            for line in process.stdout:
                print(line.decode())
                logger.info(line.decode())
            process.wait()

            # Run the update agent script
            process = subprocess.Popen(["python3", agent], cwd=repo_path, stdout=subprocess.PIPE)
            for line in process.stdout:
                print(line.decode())
                logger.info(line.decode())
            process.wait()
        else:
            info = "No updates found in the repository."
            print(info)
            logger.info(info)
    except Exception as e:
        info = f"An error occurred: {str(e)}"
        print(info)
        logger.error(info)

if __name__ == "__main__":
    # Initialize the logger for logging
    logger = init_logger(log_file)
    try:
        info = "Starting update process at: " + str(datetime.now())
        print(info)
        logger.info(info)

        while True:
            # Perform the repository update
            update_repo(logger)

            # Sleep for the specified interval
            info = "Sleeping for {} seconds.".format(sleep_interval_seconds)
            print(info)
            logger.info(info)
            time.sleep(sleep_interval_seconds)
    except KeyboardInterrupt:
        info = "Script terminated by the user."
        print(info)
        logger.info(info)
