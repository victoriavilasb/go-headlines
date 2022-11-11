import os
import yaml

class Yaml:
    def read_config_file(file_path):
        with open(file_path) as f:
            return yaml.safe_load(f)

    def write_file(self, file_path, data):
        if not self.file_exists():
            os.makedirs(os.path.dirname(file_path))
            
        with open(self.file_path, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)

    def file_exists(file_path):
        return os.path.exists(os.path.dirname(file_path))
