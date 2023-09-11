# Generate Album Cover

## Instructions

You should recieve information about how to login to your assigned VM via the email address that you used to register. If not, please check with the on-site staff.

- Login to the VM using the provided credentials
- Run the following commands

```shell
pip install diffusers
```

Now copy the two Python scripts in the `stable-diffusion` directory on Github onto your AWS VM.

The `sd_amx.py` script will generate an image using Intel AMX and the `sd_noamx.py` script will generate an image without using Intel AMX.

The images generated will be saved to the `output_images` on your AWS VM. You will need to download them in order to attach the image for your submission.

Experiment with running your prompt using each script to see the impact that Intel AMX can have on how quickly an image is generated. Once you've explored the difference, you can focus on generating your album cover using the `sd_amx.py` script.

## Adjusting Parameters

To modify the prompt and other settings the impact the image generation, the main section of the script to pay attention to is at the end of the script. The below example is from the `sd_amx.py` script, but both scripts are similar.

```python
output_image = run_stable_diffusion(
    model_id =  "runwayml/stable-diffusion-v1-5",
    prompt = "giraffe climbing a mountain",
    device = 'cpu',
    torch_dtype = torch.bfloat16,
    num_inference_steps = 25,
    num_images = 1,
    output_folder = 'output_images'
)
```

To change your prompt, you'll want to modify the `prompt` setting. If you want to change the model, modify the `model_id` setting. If you want to increase the number of inference steps used to generate your image, modify the `num_inference_steps` settings.

## Submitting Results

For this portion of the challenge, you will need to copy the prompt and settings you used, the image generated and take a screenshot of the output on the console. Include these in your submission email. Examples are below. Don't send your submission until you've completed both parts of the challenge. The image you submit should've been generated using the `sd_amx.py` script.

***For the prompt and settings***

For the prompt and settings you can copy the section from the end of the `sd_amx.py` script that you used to create the album cover image. An example is below:

```python
output_image = run_stable_diffusion(
    model_id =  "runwayml/stable-diffusion-v1-5",
    prompt = "giraffe climbing a mountain",
    device = 'cpu',
    torch_dtype = torch.bfloat16,
    num_inference_steps = 25,
    num_images = 1,
    output_folder = 'output_images'
)
```

For the image, just attach the image you want to use as your album cover.


# Stable Diffusion on Intel 4th Gen Xeon CPUs
Simple Stable Diffusion app using Flask

Run using 

```python
python app.py
```

Connect to your web UI with:

```
localhost:5000
```

This is what the Web UI should look like:

<img width="961" alt="image" src="https://github.com/bconsolvo/stable_diffusion_flask/assets/15691316/5f6ad3b7-f6db-4acb-b0f7-825364c54387">


