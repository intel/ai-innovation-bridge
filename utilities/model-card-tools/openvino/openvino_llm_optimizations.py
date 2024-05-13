# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import sys
import time
import warnings
logging.disable(sys.maxsize)
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(
    description = "A script to automate optimization of Hugging Face LLMs " \
      "with OpenVINO on Intel Core Ultra AI PCs."
)

parser.add_argument(
  "--model_path", 
  required = True, 
  type = str, 
  help = "The model path to LLM on Hugging Face."
)

parser.add_argument(
  "--task", 
  required = True, 
  type = str, 
  help = "The LLM task, selected choices include: text-generation, translation_en_to_fr."
)

parser.add_argument(
  "--device", 
  required = True, 
  type = str,
  help = "The device on the AI PC to optimize the LLM: GPU, NPU, or CPU."
)

parser.add_argument(
  "--prompt", 
  required = True, 
  type = str,
  help = "The input prompt for LLM inference task."
)

args = parser.parse_args()
model_path = args.model_path.lower()
task = args.task.lower()
device = args.device.upper()
prompt = args.prompt

def check_device(
    device_type: str
):
  """Function to check if device selected is available.

  Parameters:
    device_type (str): Device on AI PC to optimize LLM, supported options include: GPU, NPU, or CPU.
  
  Returns:
    device_type (str): Returns selected device type, if available.
  
  Raises:
    ValueError: If selected device type is not found.
  """

  from openvino import Core
  devices = Core().available_devices

  try:
    if device_type not in devices:
      raise ValueError
  except ValueError:
    print("Unable to find device selected: {}. "\
          "Please select an option from the available devices: {}.".format(
            device_type, ', '.join(str(dev) for dev in devices)))
    sys.exit()
  else:
    print("{} device selected is available. Compiling model to {}.".format(
      device_type, device_type))
    return(device_type)

def llm_task_check(
    task: str
):
  """Function to check if LLM task selected is supported.

  Parameters:
    task (str): LLM task, supported options include: text-generation and translation_en_to_fr.
  
  Returns:
    task (str): Returns selected LLM task, if supported.
  
  Raises:
    ValueError: If LLM task is not currently supported.
  """

  task_list = ['text-generation', 
               'translation_en_to_fr']
  
  try:
    if task not in task_list:
      raise ValueError
  except ValueError:
    print("Automated OpenVINO LLM optimization support for additional LLM tasks coming soon. "\
          "Please select a task from one of the available options: {}.".format(
            ', '.join(str(t) for t in task_list))
          )
    sys.exit()
  else:
    return task

def openvino_text_generation_llm(
    model_id: str,
    device_type: str,
    prompt: str
):
  """Function to optimize text generation LLMs with OpenVINO on AI PC.

  Parameters:
    model_id (str): Path to LLM on Hugging Face, e.g., helenai/gpt2-ov.
    device_type (str): Device on AI PC to optimize LLM.
    prompt (str): Input prompt for LLM text generation.
  
  Returns:
    response (str): Response generated from optimized LLM.
  
  Raises:
    RuntimeError: If OpenVINO optimization for selected device is not currently supported.
  """

  try:  
    from optimum.intel import OVModelForCausalLM
    from transformers import AutoTokenizer, pipeline

    print("Optimizing {} LLM with OpenVINO.".format(model_id))
    
    start = time.time()

    model = OVModelForCausalLM.from_pretrained(model_id).to(device_type)
    tokenizer = AutoTokenizer.from_pretrained(model_id)  
    pipe = pipeline(task, model=model, tokenizer=tokenizer)
    response = pipe(prompt)
    
    end = time.time()
    total_time = end - start
    
    print("{} LLM optimized with OpenVINO on {} and inference completed in {} seconds!\n"\
          "\nPrompt entered: {}\nResponse: {}".format(
            model_id, device_type, round(total_time,3), prompt, response[0]['generated_text']))
  
  except RuntimeError:
    print("Support for {} LLM OpenVINO optimizations on {} coming soon. Please try another "\
          "supported device.".format(model_id, device_type))

def openvino_translation_llm(
    model_id: str,
    device_type: str,
    prompt: str
):
  """Function to optimize text translation LLMs with OpenVINO on AI PC.

  Parameters:
    model_id (str): Path to LLM on Hugging Face, e.g., t5-small.
    device_type (str): Device on AI PC to optimize LLM.
    prompt (str): Input prompt for LLM text translation.
  
  Returns:
    response (str): Response generated from optimized LLM.
  
  Raises:
    RuntimeError: If OpenVINO optimization for selected device is not currently supported.
  """

  try:  
    from optimum.intel import OVModelForSeq2SeqLM
    from transformers import AutoTokenizer, pipeline

    print("Optimizing {} LLM with OpenVINO.".format(model_id))

    start = time.time()

    model = OVModelForSeq2SeqLM.from_pretrained(model_id, export=True).to(device_type)
    tokenizer = AutoTokenizer.from_pretrained(model_id)  
    pipe = pipeline(task, model=model, tokenizer=tokenizer)
    response = pipe(prompt)
    
    end = time.time()
    total_time = end - start

    print("{} LLM optimized with OpenVINO on {} and inference completed in {} seconds!\n"\
          "\nText to translate: {}\nTranslation: {}".format(
            model_id, device_type, round(total_time,3), prompt, response[0]['translation_text']))

  except RuntimeError:
    print("Support for {} LLM OpenVINO optimizations on {} coming soon. Please try another "\
          "supported device.".format(model_id, device_type))
    
def optimize_llm_openvino(
    model_id: str,
    task: str,
    device_type: str, 
    prompt: str
):
  """
  Function to optimize Hugging Face LLMs with OpenVINO on Intel AI PC.

  Parameters:
    model_id (str): Path to LLM on Hugging Face, e.g., helenai/gpt2-ov.
    task (str): Selected LLM task, supported options include: text-generation and translation_en_to_fr.
    device_type (str): Device on AI PC to optimize LLM.
    prompt (str): Input prompt for LLM text translation.
  """
  
  device_type = check_device(device_type = device)
  
  task = llm_task_check(task = task)
  
  if task == "text-generation":
    openvino_text_generation_llm(
      model_id = model_id, 
      device_type = device_type, 
      prompt = prompt
    )
  
  elif task == "translation_en_to_fr":
    openvino_translation_llm(
      model_id = model_id, 
      device_type = device_type, 
      prompt = prompt
    )

if __name__ == "__main__":

  optimize_llm_openvino(
    device_type = device, 
    model_id = model_path,
    task = task,
    prompt = prompt
  )