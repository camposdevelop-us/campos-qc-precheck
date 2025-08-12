# Processing images with openai
import os
import json
import base64

from src.com.jinja import get_instructions, get_output_summary
from assets import AssetManager
from src.com.azure.openai import AzureOpenAI

async def start(pdf_name: str, output_folder: str, images_path: str, openai: AzureOpenAI, blob):  
    response_files = []  # Initialize as a list  
    # Render the prompt using the Jinja template  
    system_prompt = get_instructions()
    # print(system_prompt)  

    # get template assets
    asset_manager = AssetManager()
    # get encoded templates and logos
    encoded_template_1 = asset_manager.get_encoded("templates", "template_1.jpg")    
    encoded_template_2 = asset_manager.get_encoded("templates", "template_2.jpg")    
    encoded_campos_logo = asset_manager.get_encoded("logos", "campos.jpg")
    encoded_xcel_energy_logo = asset_manager.get_encoded("logos", "xcel_energy.png")
    # Iterate through each file in the directory  
    page_number = 1
    for file_name in os.listdir(images_path): 
        if not file_name: 
            continue
        # Construct the full path to the image  
        image_path = os.path.join(images_path, file_name)  
        print(image_path)
        # Check if the file is an image (simple check for extensions)  
        try:  
            print(f"Processing image: {file_name}")  

            # Extract page number from the filename (e.g., "page_4.jpg")  
            # page_number = file_name.split('-')[1].split('.')[0]  # Extract "4" from "page_4.jpg"  

            encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('ascii')  
            
            # Prepare the chat prompt  
            chat_prompt = [  
                {  
                    "role": "system",  
                    "content": [  
                        {  
                            "type": "text",  
                            "text": "You are an AI assistant that helps people verify specific information."  
                        }  
                    ]  
                },  
                {  
                    "role": "user",  
                    "content": [  
                        {  
                            "type": "text",  
                            "text": "For your reference, I have provided below a template for defining all the terms and visual representations of the figures used in our project. Please look for similar details when answering the checklist of instructions/explanations for the images."  
                        },  
                        {  
                            "type": "text",  
                            "text": "\n"  
                        },  
                        {  
                            "type": "image_url",  
                            "image_url": {  
                                "url": f"data:image/jpeg;base64,{encoded_template_1}"  
                            }  
                        },  
                        {  
                            "type": "image_url",  
                            "image_url": {  
                                "url": f"data:image/jpeg;base64,{encoded_template_2}"  
                            }  
                        },  
                        {  
                            "type": "text",  
                            "text": "Below is the LOGO that you should compare the image logo with"  
                        },  
                        {  
                            "type": "image_url",  
                            "image_url": {  
                                "url": f"data:image/jpeg;base64,{encoded_campos_logo}"  
                            }  
                        },  
                                                    {  
                            "type": "text",  
                            "text": "Below is the CLIENT LOGO that you should compare the image logo with"  
                        },  
                        {  
                            "type": "image_url",  
                            "image_url": {  
                                "url": f"data:image/jpeg;base64,{encoded_xcel_energy_logo}"  
                            }  
                        },
                        {  
                            "type": "text",  
                            "text": system_prompt  
                        },  
                        {  
                            "type": "image_url",  
                            "image_url": {  
                                "url": f"data:image/jpeg;base64,{encoded_image}"  
                            }  
                        }  
                    ]  
                }  
            ]  

            # Call Azure OpenAI model 
            openai_response = await openai.chat_completion(
                messages=chat_prompt,
                max_tokens=16000
            ) 
            json_file_name = file_name.split('.',1)[0] if '.' in file_name else file_name

            response_files.append({"Page Number": page_number, "Response": openai_response})

            # Upload intermediate responses to Azure Blob Storage  
            # intermediate_blob_name = f"Xcel/{pdf_name}/intermediate_responses/{json_file_name}.json"  
            # write_json_to_blob(blob_service_client, CONTAINER_NAME, intermediate_blob_name, openai_response)  
            
            #save intermediate responses in output folder  
            intermediate_response_file = os.path.join(output_folder, f"{json_file_name}.json")

            with open(intermediate_response_file , "w" , encoding="utf-8") as f: 
                json.dump(openai_response, f, ensure_ascii=False, indent=4)

                
            # response_files.append({"Page Number": page_number, "Response": openai_response}) 
            page_number = page_number + 1
        except Exception as e:  
            print(f"Error processing {file_name}: {e}")  
  
    # # Save final response directly to Azure Blob Storage  
    # final_blob_name = f"Xcel/{pdf_name}/final_summary.json"
    # write_json_to_blob(blob_service_client, CONTAINER_NAME, final_blob_name, response_files)  

 # Save final response in a text file  
    final_response_file = os.path.join(output_folder, "final_summary.json")  
    with open(final_response_file, "w", encoding="utf-8") as f:  
        json.dump(response_files, f, ensure_ascii=False, indent=4)  # Save as JSON for better formatting  

    await process_checklist(response_files, output_folder, get_output_summary(), openai)


async def process_checklist(response_files, output_folder, output_summary_prompt, openai: AzureOpenAI):    
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI assistant that helps people verify Specific information pass the information by each page to page Based on the details below categorize the answers/ observations into three categories also explain if falls under Failed  Explain the reason what condition was not met:Pass failed Not Found/ Not Applicated."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"{output_summary_prompt} details are; {response_files}"
                }
            ]
        }
    ]
    
    output_response = await openai.chat_completion(
        messages=chat_prompt,
        max_tokens=2000,
        # temperature=0.0,
        # top_p=0.95,
        # frequency_penalty=0,
        # presence_penalty=0,
        # stop=None,
        # stream=False
    )
    
    # ans=completion.choices[0].message.content
    # Write the AI response (checklist) to Azure Blob Storage  
    # write_text_to_blob(blob_service_client, container_name, blob_name, ans)
    # Write checklist to local output folder
    with open(os.path.join(output_folder,"checklist.txt"), "w", encoding="utf-8") as file: 
        file.write(output_response)
    
