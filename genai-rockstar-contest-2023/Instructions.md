# GenAI Rockstar Contest

We will be using one of Intel's Optimized Cloud Recipes. If you want to experiment with this on your own, you can find the recipe [here](https://github.com/intel/optimized-cloud-recipes/tree/main/recipes/ai-fastchat-amx-ubuntu).

This recipe is included in the Terraform module.  This installs and configures [Fastchat](https://github.com/lm-sys/FastChat) on the VM created in your AWS account. The [Intel Extension for Pytorch](https://github.com/intel/intel-extension-for-pytorch) also deploys onto the VM, along with a few other components, for full details, refer to the recipe.

Intel AMX has been enabled by default.

## Instructions

Open your AWS account and click the Cloudshell
At the command prompt enter in in these command promps to install Terraform into the AWS Cloudshell
```Shell
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
mkdir ~/bin
ln -s ~/.tfenv/bin/* ~/bin/
tfenv install 1.3.0
tfenv use 1.3.0
```
Download and run the [gen-ai-fastchat](https://github.com/intel/terraform-intel-aws-vm/tree/main/examples/gen-ai-fastchat) Terraform Module by typing this command
```Shell
git clone https://github.com/intel/terraform-intel-aws-vm.git
```
Change into the fastchat example folder
```Shell
cd terraform-intel-aws-vm/examples/gen-ai-fastchat
```

Run the Terraform Commands
```Shell
terraform init
terraform plan
terraform apply
```
Screen Capture the results of the Terraform Apply Command to submit for the contest<br>
Example :

![Module Success](images/genai-aws-success.png)
<br>

```Shell
WAIT 10 MINUTES
```
After the Terraform module successfully creates the EC2 instance, **wait ~10 minutes** for the recipe to download/install FastChat and the LLM model before continuing.

1. Connect to the newly created AWS EC2 instance using SSH<br>
  
      a. The terraform module creates a key pair and adds the public key to the EC2 instance. It keeps the private key in the same folder from where the **terraform apply** was run. File name = tfkey.private<br>
  
    b. At your Terraform prompt, nagivate to the folder from where you ran the **terraform apply** command and change the permissions of the file:
    ```hcl
    chmod 400 tfkey.private
    ```

    c. Run the ssh command as below:
    ```hcl
    ssh ubuntu@<Public_IP_Address_EC2_Instance> -i tfkey.private
    ```

2. Once you are logged into the EC2 instance, run the command
    ```hcl
    source /usr/local/bin/run_demo.sh
    ```
    If successful your prompt will look similar to this
    ```shell
    ubuntu@ip-172-31-33-45:~$ source /usr/local/bin/run_demo.sh
    2023-09-06 14:10:00 | INFO | gradio_web_server_multi | args: Namespace(host='0.0.0.0', port=None, share=True, controller_url='http://localhost:21001', concurrency_count=10, model_list_mode='once', moderate=False, add_chatgpt=False, add_claude=False, add_palm=False, anony_only_for_proprietary_model=False, register_openai_compatible_models=None, gradio_auth_path=None, elo_results_file=None, leaderboard_table_file=None)
    2023-09-06 14:10:00 | INFO | gradio_web_server | Models: ['4th_GenXeon_Vicuna_7b']
    2023-09-06 14:10:00 | INFO | stdout | Running on local URL:  http://0.0.0.0:7860
    2023-09-06 14:10:02 | INFO | stdout | Running on public URL: https://64163ad5b65c927ff1.gradio.live
    2023-09-06 14:10:02 | INFO | stdout |
    2023-09-06 14:10:02 | INFO | stdout | This share link expires in 72 hours. For free permanent hosting and GPU upgrades, run `gradio deploy` from Terminal to deploy to Spaces (https://huggingface.co/spaces)
    ```


3. Now you can access the Fastchat by opening your browser and entering the following URL     
http://yourpublicip:7860

4. Type in the prompt to interact with fastchat. Enter your message or question in the chat prompt to see the Fastchat in action?  Example:

    ```text
    Prompt: Write a song about Star Wars in the style of Frank Sinatra
    ```

    The output from FastChat:
    ```text
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

    ***Screenshot your lyrics***


5. Create an X.com Post under your account
  Included in the post must be:<br>
        1) A screenshot of your Terraform code output successfully deployment<br>
        2) A screenshot of your song lyrics that were generated <br>
        3) Use the ***#IntelGenAI*** as the hashtag in your x.com post<br>

5. To delete the demo:<br>
  a. Exit the VM instance by pressing Ctrl-C to break out of fastchat<br>
  b. Then run Terraform destroy to delete all resources created<br>

## Considerations
- The AWS region where this example is run should have a default VPC



