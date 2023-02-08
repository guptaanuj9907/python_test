import os
import json
import logging
import datetime
import requests
import logging
import sys

logging.basicConfig(level=logging.INFO,stream=sys.stdout,format="%(message)s")
logger = logging.getLogger()


def opa_validate(files_changes):
    logger.info(files_changes)

if __name__ == "__main__":
    file_changes = sys.argv
    file_changes.pop(0)
    opa_validate(file_changes)