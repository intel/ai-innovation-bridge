# Model Evaluation on Gaudi Hardware

This repository contains code and instructions to evaluate the performance and compatibility of machine learning models on Gaudi hardware, specifically using the `meta-llama/Llama-2-7b-hf` model as an example. The evaluation process is facilitated by a Makefile that orchestrates the setup and execution of the model on Gaudi.

## Contents

- **Makefile**: Contains commands to run the model evaluation on Gaudi hardware.
- **run_generation.py**: A Python script for generating text using the model.

## Setup and Evaluation Process

Runs env setup and eval in sequence to facilitate a complete evaluation process.

```bash
make run-all
```

## Customization

You can customize the evaluation by modifying the following variables in the Makefile:

- MODEL_NAME: The model identifier from Hugging Face's model hub.
- TEST_PROMPT: The prompt text used for generating text.
- MAX_TOKENS: The maximum number of tokens to generate.
- BATCH_SIZE: The number of examples to process in parallel.

## Logs
The output of the evaluation, including execution time and any errors, will be saved in run-gaudi-eval.log.

## Note
Ensure that your system meets the prerequisites and that Gaudi hardware is properly configured before proceeding with the evaluation.