# Intel Generative AI Rockstar Contest

![Generative AI Rockstar](images/ai-rockstar.png)

## Contest Details

- Deploy the [gen-ai-fastchat](https://github.com/intel/terraform-intel-aws-vm/tree/main/examples/gen-ai-fastchat) Terraform module using an AWS Cloud account
- The module will create an EC2 Instance with an  Intel 4th Generation Xeon CPU
- Access your EC2 instance via a web URL to create AI generated lyrics
- Post your results for a chance to win a Beelink Mini S12 Pro Mini PC
- See Contest [Guidelines](guidelines.md) for complete details

## Requirements
- AWS Cloud Account

## Contest Participation Overview

* Deploy the Terraform Module in your AWS account
* Connect to the public ip of your EC2 instance to access the Fast Chat UI
* Enter in the prompt to generate song lyrics

    **[Click here for detailed Rock Star Contest Instructions](Instructions.md)**
* Submit your entry to X.com

Refer to the [Official Rules](terms.md)

## How to enter your submission

Submissions for this contest will be done via X.com (aka Twitter)
1. You must have an X.com account
2. Submit a post on X.com
    Included in the post must be:<br>
        1) A screenshot of your Terraform code output successfully deployment<br>
        2) A screenshot of your song lyrics that were generated <br>
3. Use the #IntelGenAI as the hashtag in your x.com post<br>



## Module Overview
You will need an AWS account as this terraform module will launch a M7i.4xlarge instance on AWS. These instances use the latest [Intel 4th Generation Xeon CPUs](https://www.intel.com/content/www/us/en/products/docs/processors/xeon-accelerated/4th-gen-xeon-scalable-processors.html), which include new accelerators that help speed up AI and other workloads. This event will focus on taking advantage of the [Intel AMX](https://www.intel.com/content/www/us/en/products/docs/accelerator-engines/advanced-matrix-extensions/overview.html) accelerator to do AI inferencing on CPUs.

### Components of the Module
- [Intel Optimized Cloud Recipes](https://github.com/intel/optimized-cloud-recipes)
- [Intel Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch)
- [FastChat](https://github.com/lm-sys/FastChat)

This contest leverages the [Intel Cloud Optimization Modules](https://www.intel.com/content/www/us/en/developer/topic-technology/cloud-optimization.html) to provision the VM. <br>
This contest requires you to use the [AWS VM Module](https://github.com/intel/terraform-intel-aws-vm) and the 

---