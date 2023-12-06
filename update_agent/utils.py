import logging

# Initialize logger
def init_logger(log_file):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

def get_current_commit_hash(repo):
    return repo.head.commit.hexsha
