import yaml
import os

from ttrack.repository.database import Database
from ttrack.repository.storage import StorageType
from ttrack.repository.yaml import Yaml

class Configuration:
    def __init__(self, file_path, yaml: Yaml):
        self.file_path = file_path
        self.yaml = yaml
        
        config = {}
        if self.yaml.file_exists(file_path):
            config = self.yaml.read_file(file_path)

        self.storage_type = StorageType(config["storage_type"]) if "storage_type" in config else None
        self.connection = config["connection"] if "connection" in config else None

    def instance_database(self):
        return self._mount_database()

    def create_or_update(self, uri, path, storage):
        config = {
            'storage_type': storage,
            'connection': self._mount_connection_data(uri, path, storage)
        }

        self.yaml.write_file(self.file_path, config)

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
