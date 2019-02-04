from pathlib import Path
import yaml

# Read game images configuration
img_config_file_path = Path("configuration/game_images.yml")
with open(img_config_file_path, "r") as img_yaml:
    img_cfg = yaml.load(img_yaml)
# Read game objects sizes configuration
size_config_file_path = Path("configuration/size_conf.yml")
with open(size_config_file_path, "r") as size_yaml:
    size_cfg = yaml.load(size_yaml)
