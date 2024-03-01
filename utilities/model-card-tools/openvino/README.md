<p align="center">
  <img src="assets/openvino-logo-purple-black.png?raw=true" alt="OpenVINO" width="500"/>
</p>

# Hugging Face* LLM Optimizations with OpenVino™ on Intel® Core Ultra™ AI PC

© Copyright 2024, Intel® Corporation

## Table of Contents
- [Introduction](#introduction)
- [What is OpenVINO™ Toolkit?](#what-is-openvino™-toolkit)
- [System Requirements](#system-requirements)
- [How to use](#usage)
- [License](#license)
- [Next steps](#next-steps)

## Introduction

This repository contains the development tools to optimize LLMs sourced from Hugging Face* using the [OpenVINO™](https://www.intel.com/content/www/us/en/developer/tools/openvino-toolkit/overview.html) model optimizations and run comprehensive AI inference on an [Intel® Core Ultra™ AI PC](https://www.intel.com/content/www/us/en/products/docs/processors/core-ultra/ai-pc.html).

## What is OpenVINO™ Toolkit?

OpenVINO™ is an open-source toolkit for optimizing and deploying AI inference.
- Boost deep learning performance in computer vision, automatic speech recognition, natural language processing and other common tasks
- Use models trained with popular frameworks like TensorFlow, PyTorch and more
- Reduce resource demands and efficiently deploy on a range of Intel® platforms from edge to cloud  

This open-source version includes several components: namely OpenVINO™ Model Converter (OVC), OpenVINO™ Runtime, as well as CPU, GPU, multi device and heterogeneous plugins to accelerate deep learning inference on Intel® CPUs and Intel® Processor Graphics. It supports pre-trained models from [Open Model Zoo](https://github.com/openvinotoolkit/open_model_zoo), along with 100+ open source and public models in popular formats such as TensorFlow, ONNX, PaddlePaddle, MXNet, Caffe, Kaldi.

For more information on the OpenVINO™ Toolkit, please check out the [GitHub repository](https://github.com/openvinotoolkit/openvino).

## System requirements

Before running this application, please ensure your AI PC meets the OpenVINO™ [system requirements](https://www.intel.com/content/www/us/en/developer/tools/openvino-toolkit/system-requirements.html).

## Usage

### Install Dependencies

To use this application, first clone the repo and install the dependencies:

```bash
git clone https://github.com/intel/ai-innovation-bridge
cd ai-innovation-bridge/utilities/model-card-tools/openvino
pip install -r requirements.txt
```

Once you have successfully installed the dependencies, you are ready to optimize your Hugging Face LLMs with OpenVINO. 

### Supported LLM Tasks

The [`openvino_llm_optimizations.py`](openvino_llm_optimizations.py) script currently supports the following LLM tasks:
- [`text-generation`](https://huggingface.co/tasks/text-generation)
- [`translation_en_to_fr`](https://huggingface.co/tasks/translation)

### Model Optimization

You can customize the [`openvino_llm_optimizations.py`](openvino_llm_optimizations.py) script by modifying the following parameters:
- **`model_path`**: The model path to LLM on Hugging Face, e.g., `helenai/gpt2-ov`.
- **`task`**: The LLM task. The supported options include: `text-generation`, `translation_en_to_fr`.
- **`device`**: The device on the AI PC to optimize the LLM. The supported options include GPU, NPU, and CPU.
- **`prompt`**: The input prompt for the LLM inference task.

### Example Usage

#### Text Generation

To run optimized inference of a text generation LLM with OpenVINO, use the following command:

```python
python openvino_llm_optimizations.py --model_path=helenai/gpt2-ov --task=text-generation --device=gpu --prompt="In the spring, flowers bloom"
```

Your output should be similar to:

```text
GPU device selected is available. Compiling model to GPU.
Optimizing helenai/gpt2-ov LLM with OpenVINO.
helenai/gpt2-ov LLM optimized with OpenVINO on GPU and inference completed in 4.94 seconds!

Prompt entered: In the spring, flowers bloom
Response: In the spring, flowers bloom all over the land. The flowers bloom in summer, when the rains soak away. 
```

#### Text Translation

To run optimized inference of a text translation LLM with OpenVINO, use the following command:

```python
python openvino_llm_optimizations.py --model_path=t5-small --task=translation_en_to_fr --device=gpu --prompt="In the spring, flowers bloom"
```

Your output should be similar to:

```text
GPU device selected is available. Compiling model to GPU.
Optimizing t5-small LLM with OpenVINO.
t5-small LLM optimized with OpenVINO on GPU and inference completed in 21.335 seconds!

Text to translate: In the spring, flowers bloom
Translation: Au printemps, les fleurs fleurissent
```

## License

OpenVINO™ Toolkit is licensed under [Apache License Version 2.0](https://github.com/openvinotoolkit/openvino/blob/master/LICENSE). By contributing to the project, you agree to the license and copyright terms therein and release your contribution under these terms.

## Next steps

Visit the OpenVINO™ channels on the [Intel® DevHub Discord*](https://discord.com/invite/7pVRxUwdWG) server if you need help or wish to talk to OpenVINO™ developers. 

You may also report questions, issues, and suggestions using:

- [GitHub* Issues](https://github.com/intel/ai-innovation-bridge/issues)
- The [`openvino`](https://stackoverflow.com/questions/tagged/openvino) tag on StackOverflow*
- [Forum](https://community.intel.com/t5/Developer-Software-Forums/ct-p/developer-software-forums/computer-vision)