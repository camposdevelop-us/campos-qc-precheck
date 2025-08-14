import os
from dotenv import load_dotenv
from flask import current_app
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


class AzureDocumentIntelligence(object):
    _endpoint: str
    _key: str
    def __init__(self):
        self._endpoint = current_app.config["AZURE_DOC_ENDPOINT"]
        self._key = current_app.config["AZURE_DOC_KEY"]
        
        if not self._endpoint or not self._key:
            raise ValueError("Missing AZURE_DOC_ENDPOINT or AZURE_DOC_KEY in environment variables.")
        
        self._client = None
    
    def _connect(self):
        try:
            self._client = DocumentIntelligenceClient(
                endpoint=self._endpoint,
                credential=AzureKeyCredential(self._key)
            )
        except Exception as e:
            print(f'[azure doc service] Error connecting to Azure Doc Intelligence {str(e)}')
    
    def get_client(self):
        if self._client is None:
            self._connect()

        return self._client
        
