import os
import json
from .pdf2image import PDF2ImageConverter
from ..image.images import start


async def process_pdf(pdf_path, output_base_path, docintelligence, openai, blob, dpi=400):  
    """  
    Process a PDF file to:  
    1. Convert pages to images.  
    2. Extract markdowns for each page.  
    3. Extract font styles and save them as JSON files.  
    4. Extract page dimensions and save them as JSON files.  
  
    Args:  
        pdf_path (str): Path to the input PDF file.  
        output_base_path (str): Base directory where output files will be stored.  
        dpi (int): Resolution for image conversion (default: 400 DPI).  
    """  
    # get doc intelligence client
    docintelligence_client = docintelligence.get_client()
    # Extract the name of the PDF file (without extension)  
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]  
    main_folder = os.path.join(output_base_path, pdf_name)  
   
    # Step 1: Convert PDF pages to images
    output_images_path = os.path.join(main_folder, "Images")  
    images = convert_to_images(output_images_path, pdf_path, blob)
    # Step 2: Extract markdowns for each page  
    pages = extract_markdowns(main_folder, pdf_path, pdf_name, docintelligence_client, blob)  
    # Step 3: Extract page dimensions and save them as JSON files  
    dimensions = extract_dimensions(main_folder, pdf_path, pdf_name, docintelligence_client, blob)
    # Step 4: Process Images
    return await start(pdf_name, main_folder, output_images_path, openai, blob)
 
def convert_to_images(output_images_path: str, pdf_path: str, blob):
    os.makedirs(output_images_path, exist_ok=True)  
    pdf2image = PDF2ImageConverter(dpi=400, output_folder=output_images_path, fmt="jpeg")
    images = pdf2image.convert(pdf_path=pdf_path)
    # for i, image in enumerate(images):
    #     image_path = os.path.join(output_images_path, f'page_{i + 1}.jpg')  
    #     image.save(image_path, 'JPEG')  
    #     print(f"Saved Image: {image_path}")    
    #     image_blob_name = f"Xcel/{pdf_name}/Images/page_{i + 1}.jpg"  
    #     # image_blob_name = f"{pdf_name}/Images/page_{i + 1}.jpg"  
    #     image_stream = io.BytesIO()  
    #     image.save(image_stream, format="JPEG")  
    #     image_stream.seek(0)  # Reset the stream position to the beginning  
    #     upload_to_blob(container_client, image_blob_name, image_stream, content_type="image/jpeg")  
    return images

def extract_markdowns(main_path: str, pdf_path: str, pdf_name: str, docintelligence, blob):
    markdown_folder = os.path.join(main_path, "markdowns")
    os.makedirs(markdown_folder, exist_ok=True)  
  
    with open(pdf_path, "rb") as document_stream:  
        poller = docintelligence.begin_analyze_document(  
            "prebuilt-layout",  
            body=document_stream,  
            output_content_format="Markdown",  
            content_type="application/octet-stream"  
        )  
        result = poller.result()  
        content = result.content  # Complete content of the document  
        pages = content.split("<!-- PageBreak -->")  # Split content into pages using the marker  
        for page_num, page_content in enumerate(pages):  
            markdown_blob_name = f"Xcel/{pdf_name}/markdowns/page_{page_num + 1}.md"  
            # markdown_blob_name = f"{pdf_name}/markdowns/page_{page_num + 1}.md"
            # blob.upload_file()
            # upload_to_blob(container_client, markdown_blob_name, page_content.strip(), content_type="text/markdown")  
            markdown_file = os.path.join(markdown_folder, f'page_{page_num + 1}.md')  
            with open(markdown_file, "w", encoding="utf-8") as f:  
                f.write(page_content.strip())  # Save the page content  

            print(f"Saved Markdown: {markdown_file}") 
    return pages

def extract_fonts():
    pass

def extract_dimensions(main_path: str, pdf_path: str, pdf_name: str, docintelligence, blob):
    dimension_folder = os.path.join(main_path, "page_dimensions")  
    os.makedirs(dimension_folder, exist_ok=True)  
    with open(pdf_path, "rb") as document_stream:  
        poller = docintelligence.begin_analyze_document(  
            "prebuilt-layout",  
            body=document_stream  
        )  
        result = poller.result()  
        dimensions = []  
        for page in result.pages:  
            dimensions.append({  
                "page_number": page.page_number,  
                "width": page.width,  
                "height": page.height,  
                "unit": page.unit  
            })  
        # dimension_blob_name = f"Xcel/{pdf_name}/page_dimensions/{pdf_name}_dimensions.json"  
        # dimension_blob_name = f"{pdf_name}/page_dimensions/{pdf_name}_dimensions.json"  
        dimension_json = json.dumps(dimensions, indent=4)  
        # upload_to_blob(container_client, dimension_blob_name, dimension_json, content_type="application/json")
        dimension_file = os.path.join(dimension_folder, f'{pdf_name}_dimensions.json')  
        with open(dimension_file, "w", encoding="utf-8") as f:  
            json.dump(dimensions, f, indent=4)  
        print(f"Saved Page Dimensions: {dimension_file}")    
    return dimensions

