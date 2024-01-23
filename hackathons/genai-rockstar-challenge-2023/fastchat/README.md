# Generate Song Lyrics

For this portion of the activity we will be using one of Intel's Optimized Cloud Recipes. If you want to experiment with this on your own, you can find the recipe [here](https://github.com/intel/optimized-cloud-recipes/tree/main/recipes/ai-fastchat-amx-ubuntu).

This recipe pre-installed and configured [Fastchat](https://github.com/lm-sys/FastChat) on the VMs that have been provisioned. The [Intel Extension for Pytorch](https://github.com/intel/intel-extension-for-pytorch) has been deployed, along with a few other components, for full details, refer to the recipe.

Intel AMX has been enabled by default for this activity.

## Instructions

You should recieve information about how to login to your assigned VM via the email address that you used to register. If not, please check with the on-site staff.

- Login to the VM using the provided credentials
- Run the following command to start FastChat

```Shell
source /usr/local/bin/run_demo.sh
```

If this is successful you will see the following output:

```shell
ubuntu@ip-172-31-33-45:~$ source /usr/local/bin/run_demo.sh
2023-09-06 14:10:00 | INFO | gradio_web_server_multi | args: Namespace(host='0.0.0.0', port=None, share=True, controller_url='http://localhost:21001', concurrency_count=10, model_list_mode='once', moderate=False, add_chatgpt=False, add_claude=False, add_palm=False, anony_only_for_proprietary_model=False, register_openai_compatible_models=None, gradio_auth_path=None, elo_results_file=None, leaderboard_table_file=None)
2023-09-06 14:10:00 | INFO | gradio_web_server | Models: ['4th_GenXeon_Vicuna_7b']
2023-09-06 14:10:00 | INFO | stdout | Running on local URL:  http://0.0.0.0:7860
2023-09-06 14:10:02 | INFO | stdout | Running on public URL: https://64163ad5b65c927ff1.gradio.live
2023-09-06 14:10:02 | INFO | stdout |
2023-09-06 14:10:02 | INFO | stdout | This share link expires in 72 hours. For free permanent hosting and GPU upgrades, run `gradio deploy` from Terminal to deploy to Spaces (https://huggingface.co/spaces)
```

Open a browser and go to the public URL listed. This URL is randomly generated each time the script is run. 

**If you having trouble accessing the URL provided in the console, or the page is really slow to load, or you get errors while using FastChat, then try going to `http://public_ip:7860`.**

Once you get to the application, you will see a screen like this:

![Single Model Screen](images/fastchat-single.png)

You can now generate the lyrics for your song.

## Submitting Results

For this portion of the challenge, you will need to copy the prompt you used, the text output and take a screenshot of either the UI or the output on the console. Put the lyrics in a text file and use the title of your song as the name of the file. Upload all of these as part of your submission. Examples are below. Don't finalize your submission until you've completed the second portion of the challenge.

**For the prompt and lyrics:**

```text
Prompt: Write a song about Star Wars in the style of Frank Sinatra
Lyrics: 

Verse 1:
A long time ago, in a galaxy far, far away
A hero emerged, to save us all from the dark side
He fought against the evil Empire, with a lightsaber in hand
And brought hope to the galaxy, with a wave of his wand

Chorus:
Star Wars, Star Wars, the epic space saga
With heroes and villains, it's a story we all know
From a tiny planet, to the Death Star
The Force is strong, with our Jedi warriors
```

**Pick one of these two types of screenshots to provide with your results.**

![Lyrics UI Example](images/lyrics-ui-example.png)

![Lyrics Console Example](images/lyrics-console-example.png)

## Continue to Album Cover instructions

**[Album Cover Instructions](../stable-diffusion/README.md)**
