import yaml
import os

from ttrack.repository.database import Database
from ttrack.repository.storage import StorageType

class Configuration:
    def __init__(self, file_path):
        self.file_path = file_path
        
        config = {}
        if self._file_exists():
            config = self._read_config_file()

        self.storage_type = StorageType(config["storage_type"]) if "storage_type" in config else None
        self.connection = config["connection"] if "connection" in config else None

    def instance_database(self):
        return self._mount_database()

    def create_or_update(self, uri, path, storage):
        config = {
            'storage_type': storage,
            'connection': self._mount_connection_data(uri, path, storage)
        }

        self._write_config_file(config)

    def _mount_connection_data(self, uri, path, storage):
        connection = {}
        if StorageType(storage) == StorageType.DATABASE:
            connection = {
                'uri': uri
            }
        elif StorageType(storage) == StorageType.LOCAL:
            connection = {
                'path': path
            }
        elif StorageType(storage) == StorageType.BLOB:
            connection = {}
        else:
            raise Exception("Storage is not an option")

        return connection

    def _mount_database(self):
        s = StorageType(self.storage_type)
        if s == StorageType.DATABASE:
            return Database(self.connection)
        else:
            raise NotImplementedError("Storage were not implemented")

    def _read_config_file(self):
        with open(self.file_path) as f:
            return yaml.safe_load(f)

    def _file_exists(self):
        return os.path.exists(os.path.dirname(self.file_path))

    def _write_config_file(self, config):
        if not self._file_exists():
            os.makedirs(os.path.dirname(self.file_path))
            
        with open(self.file_path, 'w') as yaml_file:
            yaml.dump(config, yaml_file, default_flow_style=False)
