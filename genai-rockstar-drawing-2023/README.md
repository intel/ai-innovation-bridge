# Intel Generative AI Rockstar HashiConf Drawing

![Generative AI Rockstar](images/ai-rockstar.png)

## Details

- Complete this module to get 5 extra ticket entries to the drawing at HashiConf 2023
- Deploy the [gen-ai-fastchat](https://github.com/intel/terraform-intel-aws-vm/tree/main/examples/gen-ai-fastchat) Terraform module using an AWS Cloud account
- The module will create an EC2 Instance with an Intel 4th Generation Xeon CPU in your AWS Account
- Access your EC2 instance via a web URL to create AI generated lyrics
- Screen shot or take a picture of your successful "terraform apply" results and your fastchat generated lyrics, and bring that to the Intel  Booth at HashiConf 2023, to pick up your 5 additional entries to win a Beelink Mini S12 Pro Mini PC
- See Contest [Guidelines](guidelines.md) for complete details

## Requirements
- AWS Cloud Account

## Participation Overview

* Deploy the Terraform Module in your AWS account
* Connect to the public ip of your EC2 instance to access the Fast Chat UI
* Enter in a prompt to generate song lyrics
* Bring a screenshot or picture of:
    1) Terraform output of the successful deployment he Module
    2) The song lyrics you generated using FastChat

Refer to the [Official Rules](terms.md)


## Instructions on how to deploy the GenAI FastChat Module

Open your AWS account and click the Cloudshell
At the command prompt enter
```Shell
terraform
```
If you get an error then you will need to install Terraform. Use these commands below to install Terraform into the AWS Cloudshell
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
Screen Capture the results of the Terraform Apply Command so you can bring that to us at the HashiConf Intel Booth <br>
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


5. Screen shot your lyrics as and bring both your terraform output results and your lyrics to the Intel booth at HashiConf 2023 between 8:00am PST October 10th and 5:00pm PST October 11th 

5. To delete the demo:<br>
  a. Exit the VM instance by pressing Ctrl-C to break out of fastchat<br>
  b. Then run Terraform destroy to delete all resources created<br>


## Module Overview
You will need an AWS account as this terraform module will launch a M7i.4xlarge instance on AWS. These instances use the latest [Intel 4th Generation Xeon CPUs](https://www.intel.com/content/www/us/en/products/docs/processors/xeon-accelerated/4th-gen-xeon-scalable-processors.html), which include new accelerators that help speed up AI and other workloads. This event will focus on taking advantage of the [Intel AMX](https://www.intel.com/content/www/us/en/products/docs/accelerator-engines/advanced-matrix-extensions/overview.html) accelerator to do AI inferencing on CPUs.

### Components of the Module
- [Intel Optimized Cloud Recipes](https://github.com/intel/optimized-cloud-recipes)
- [Intel Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch)
- [FastChat](https://github.com/lm-sys/FastChat)

For this you will be using one of the [Intel Cloud Optimization Modules](https://www.intel.com/content/www/us/en/developer/topic-technology/cloud-optimization.html) to provision the VM. <br>
You will be using the [AWS VM Module](https://github.com/intel/terraform-intel-aws-vm) and the gen-ai-fastchat example in that module.

The gen-ai-fastchat example leverages one of Intel's Optimized Cloud Recipes. If you want to experiment with this on your own, you can find the recipe [here](https://github.com/intel/optimized-cloud-recipes/tree/main/recipes/ai-fastchat-amx-ubuntu).

This recipe is included in the Terraform module you are deploying.  This installs and configures [Fastchat](https://github.com/lm-sys/FastChat) on the VM created in your AWS account. The [Intel Extension for Pytorch](https://github.com/intel/intel-extension-for-pytorch) also deploys onto the VM, along with a few other components, for full details, refer to the recipe.

Intel AMX has been enabled by default.

## Considerations
- The AWS region where this example is run should have a default VPC



