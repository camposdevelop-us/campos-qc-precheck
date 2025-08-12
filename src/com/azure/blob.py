from flask import current_app
from azure.storage.blob import BlobServiceClient


class AzureStorageBlob(object):
    _url: str
    _client: BlobServiceClient | None = None
    def __init__(self):
        self._url = current_app.config['AZURE_STORAGE_CONNECTION_STRING']
        self._connect()

    @property
    def _isopen(self):
        return self._client is not None
    
    def _connect(self):
        if not self._isopen:
            return self._client
        
        self._client = BlobServiceClient.from_connection_string(self._url)
        return self._client
    
    def _close(self):
        if self._isopen:
            self._client.close()
            self._client = None
            return True
        return False
    def download_file(self, container_name, file_path):
        if not self._isopen:
            self._connect()
        blob_client = self._client.get_blob_client(
            container=container_name, blob=file_path
        )
        blob = blob_client.download_blob().content_as_bytes()
        try:
            return blob
        except Exception as e:
            print(e)
            raise Exception("File is not an excel file", e)
    def upload_file(self, container_name, file_path, local_file_path):
        if not self._isopen:
            self._connect()
        blob_client = self._client.get_blob_client(
            container=container_name, blob=file_path
        )
        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        return True
    def delete_file(self, container_name, file_path):
        if not self._isopen:
            self._connect()
        blob_client = self._client.get_blob_client(
            container=container_name,blob=file_path
        )
        blob_client.delete_blob()