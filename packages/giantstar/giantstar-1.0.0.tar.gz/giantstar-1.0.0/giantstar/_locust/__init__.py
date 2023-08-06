import sys

if "giantlocust" in sys.argv[1]:
    try:
        # monkey patch all at beginning to avoid RecursionError when running locust.
        # `from gevent import monkey; monkey.patch_all()` will be triggered when importing locust
        from locust import main as locust_main

        print("NOTICE: gevent monkey patches have been applied !!!")
    except ImportError:
        msg = """
Locust is not installed, install first and try again.
install with pip:
$ pip install locust
"""
        print(msg)
        sys.exit(1)

import os
from typing import List, Dict
import json

from giantstar.loader.locustLoader import LocustLoader
from giantstar.utils.download import build_file

""" converted pytest files from YAML/JSON testcases
"""
pytest_files: List = []

from giantstar.globalSetting import plus_setting
from giantstar.utils.logger import logger

project_path = plus_setting.BASE_DIR
locust_file = os.path.join(project_path, 'test_case/giant_locust.json')


def prepare_locust_tests() -> Dict:
    with open(locust_file, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    locust_tests = LocustLoader.load(raw)
    return locust_tests


def main_locusts():
    logger.remove()
    logger.add(sys.stderr, level="WARNING")

    sys.argv[0] = "locust"
    if len(sys.argv) == 1:
        sys.argv.extend(["-h"])

    if sys.argv[1] in ["-h", "--help", "-V", "--version"]:
        locust_main.main()

    def get_arg_index(*target_args):
        for arg in target_args:
            if arg not in sys.argv:
                continue
            return sys.argv.index(arg) + 1
        return None

    url_index = get_arg_index("--url", "-u")
    if url_index:
        url = sys.argv[url_index]
        build_file(url, 'giant_case.json')

    config_index = get_arg_index("--config", "-c")
    if config_index:
        config = sys.argv[config_index]
        build_file(config, 'projectSetting.json')
    command_index = get_arg_index("--args", "-a")
    command = sys.argv[command_index]
    command = command.replace(" ", "").split(',')
    if not config_index or not command_index:
        print("Testcase file is not specified, exit 1.")
        sys.exit(1)
    sys.argv = command
    sys.argv.extend(['-f', os.path.join(os.path.dirname(__file__), "locustfile.py")])

    locust_main.main()

