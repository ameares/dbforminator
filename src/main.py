import argparse
import yaml
import logging
import tkinter as tk
from app import FormApp

APPLICATION_NAME = 'DBForminator'
DEFAULT_CONFIG_PATH = './config/eqinspect.yml'

def parse_arguments():
    parser = argparse.ArgumentParser(description=APPLICATION_NAME)
    parser.add_argument('-c', '--config', type=str, default=DEFAULT_CONFIG_PATH,
                        help='Path to the YAML file for form configuration.')
    parser.add_argument('-t', '--dbtype', type=str, required=True,
                        choices=['sqlite', 'mysql'],
                        help='Type of the database to use (local SQLite or remote MySQL).')
    parser.add_argument('-cn', '--connection', type=str, required=True,
                        help='Connection string or file path for the database.')
    return parser.parse_args()

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def load_configuration(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        if config is None:
            raise ValueError(f"Config file '{file_path}' is empty or has invalid YAML.")
        return config
    except Exception as e:
        logging.error(f"Failed to load configuration file: {e}")
        raise

if __name__ == '__main__':
    args = parse_arguments()
    setup_logging()

    try:
        config = load_configuration(args.config)
    except Exception as e:
        logging.critical("Application cannot start due to configuration loading error.")
        exit(1)

    # Initialize the main Tkinter window
    app = FormApp(args, config)
    app.mainloop()
