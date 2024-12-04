import configparser

# Path to your config.ini file
CONFIG_FILE_PATH = "config.ini"

# Read and parse the configuration
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

# Accessing the properties from the file
try:
    SERVER_ADDRESS = config.get("settings", "server_address")
except (configparser.NoSectionError, configparser.NoOptionError) as e:
    raise RuntimeError(f"Error in config file: {e}")

# Optional: Print the constants for verification during development
if __name__ == "__main__":
    print(f"SERVER_ADDRESS = {SERVER_ADDRESS}")