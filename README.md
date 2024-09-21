# This Terraform code allows you to automate the setup of Event Driven Ansible and Ansible Automation Platform.
# Before running this code, go through the code once, and go through this documentation.

## Step 1: Configure <b>terraform.tfvars</b>

In the root directory where you will run this terraform code , create file called <b>terraform.tfvars</b> with the following content:

```
digitalocean_token = "<Add the value of your digital ocean token here>"
ssh_key_name       = "<The name of your ssh-key>"
ssh_public_key     = "<your public ssh key>"
```


## Step 2: Configure the <b>script.py</b>, by adding the digital ocean token:

In the <b>script.py</b> file, consider adding your digital ocean token in this field:

![Screenshots](<Python Script.png>)

## Step 3: Create your ssh public key and private key in the root directory in order to enable inter droplet ssh connection [IMPORTANT].

```
ssh-keygen -t rsa -b 4096 -f ./id_rsa
```
## Step 4: Continue running the Terraform commands in your terminal:

```
terraform init
terraform plan
terraform apply
```

## Step 5: If you want to run either of the droplet not both then you can use this command:

  * Example: Suppose you want to create only the <b>ansible-automation-platform-tf</b> droplet and not the <b>event-driven-droplet-tf</b> droplet:
    
    ```
    terraform apply -var="create_event_driven_droplet=false"
    ```
