import time
import torch
import intel_extension_for_pytorch as ipex
from diffusers import StableDiffusionPipeline
from typing import List, Dict, Tuple
import pathlib
from flask import Flask

def inference_loop(pipe, prompt, num_inference_steps, num_images, output_folder, output_type = "pil" ):
    '''
    Loop to run inference
    ''' 
    print(f'Starting inference')
    start = time.time()
    for i in range(num_images):
        output = pipe(prompt,num_inference_steps = num_inference_steps, output_type="pil").images[0]
        t1 = time.strftime("%Y%m%d_%H%M%S")
        save_path = f"{output_folder}/{t1}_SD_image.png"
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
        img = output.save(save_path)
    end_time = time.time()       
    return output,save_path,start,end_time,

def run_stable_diffusion(
    prompt: str,
    model_id: str = "runwayml/stable-diffusion-v1-5",
    device: str = 'cpu',
    torch_dtype: torch.dtype = torch.bfloat16,
    num_inference_steps: int = 5,
    num_images: int = 1,
    output_folder: str = 'output_images'
    ):
    '''
    The main function to run stable diffusion. Arguments:
    
    - model_id: The stable diffusion model ID from Hugging Face
    - prompt: A string prompt to build the image
    - device: 'cpu' for an Intel CPU,  'xpu' for an Intel GPU
    - torch_dtype: torch.bfloat16 or torch.float32
    - num_inference_steps: number of noise removal steps
    - num_images: how many images to create
    - output_folder: The local folder to save the images to.
    '''
    
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    
    # to channels last
    print(f'To channels last')
    pipe.unet = pipe.unet.to(memory_format=torch.channels_last)
    pipe.vae = pipe.vae.to(memory_format=torch.channels_last)
    pipe.text_encoder = pipe.text_encoder.to(memory_format=torch.channels_last)
    pipe.safety_checker = pipe.safety_checker.to(memory_format=torch.channels_last)

    # # optimize with IPEX
    if torch_dtype == torch.bfloat16:
        # Create random input to enable JIT compilation
        sample = torch.randn(2,4,64,64)
        timestep = torch.rand(1)*999
        encoder_hidden_status = torch.randn(2,77,768)
        input_example = (sample, timestep, encoder_hidden_status)
        
        print(f'Optimizing pipeline with Intel Extension for PyTorch')
        pipe.unet = ipex.optimize(pipe.unet.eval(), dtype=torch_dtype, inplace=True, sample_input=input_example)
        pipe.vae = ipex.optimize(pipe.vae.eval(), dtype=torch_dtype, inplace=True)
        pipe.text_encoder = ipex.optimize(pipe.text_encoder.eval(), dtype=torch_dtype, inplace=True)
        pipe.safety_checker = ipex.optimize(pipe.safety_checker.eval(), dtype=torch_dtype, inplace=True)

        with torch.cpu.amp.autocast(enabled=True, dtype=torch_dtype):
            output,save_path,start,end_time = inference_loop(pipe,prompt,num_inference_steps,num_images,output_folder)

    else:
        output,save_path,start,end_time = inference_loop(pipe,prompt,num_inference_steps,num_images,output_folder)
    
    inference_time = (end_time - start) / num_images
    print(f'inference_time = {inference_time}')  
    return save_path

# output_image = run_stable_diffusion(
#     model_id =  "runwayml/stable-diffusion-v1-5",
#     prompt = "giraffe climbing a mountain",
#     device = 'cpu',
#     torch_dtype = torch.bfloat16,
#     num_inference_steps = 25,
#     num_images = 1,
#     output_folder = 'output_images'
# )


