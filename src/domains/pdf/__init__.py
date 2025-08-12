from src.com.azure.openai import AzureOpenAI
from src.com.azure.documentintelligence import AzureDocumentIntelligence
from src.com.azure.blob import AzureStorageBlob
from .process import process_pdf

async def start(input_pdf_path, output_folder):
    docintelligence = AzureDocumentIntelligence()
    openai= AzureOpenAI()
    blob = AzureStorageBlob()
    await process_pdf(input_pdf_path, output_folder, docintelligence, openai, blob)
