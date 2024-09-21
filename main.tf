resource "digitalocean_ssh_key" "my_key" {
  name       = var.ssh_key_name
  public_key = var.ssh_public_key
}
resource "digitalocean_droplet" "ansible_automation_platform_droplet" {
  count    = var.create_ansible_droplet ? 1 : 0
  image    = "164728761"
  name     = "ansible-automation-platform-tf"
  region   = "blr1"
  size     = "s-4vcpu-8gb"
  ssh_keys = [digitalocean_ssh_key.my_key.fingerprint]

  provisioner "local-exec" {
    command = "powershell -Command \"Start-Sleep -Seconds 60\""
  }

  provisioner "local-exec" {
    command = "scp -o StrictHostKeyChecking=no  D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\id_rsa.pub D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\id_rsa D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\script.sh D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\script.py D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\inventory D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\ansible-automation-platform-setup-bundle-2.4-1-x86_64.tar.gz root@${self.ipv4_address}:/root/"
  }

  connection {
    type        = "ssh"
    user        = "root"
    private_key = file("D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\id_rsa")
    host        = self.ipv4_address
  }
  provisioner "remote-exec" {
    inline = [
      "dnf install -y python3-pip python3 vim-enhanced",
      "pip install requests",
      "tar -xzvf /root/ansible-automation-platform-setup-bundle-2.4-1-x86_64.tar.gz",
      "ls -l /root/ansible-automation-platform-setup-bundle-2.4-1-x86_64",
      "rm /root/ansible-automation-platform-setup-bundle-2.4-1-x86_64/inventory",
      "mv /root/inventory /root/ansible-automation-platform-setup-bundle-2.4-1-x86_64/",
      "python3 /root/script.py",
      "rm /root/script.py",
      "chmod +x /root/script.sh",
      "bash /root/script.sh",
      "cd /root/ansible-automation-platform-setup-bundle-2.4-1-x86_64",
      "export ANSIBLE_SSH_ARGS='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'",
      "./setup.sh"
    ]
  }
}
resource "digitalocean_droplet" "event_driven_droplet" {
  count    = var.create_event_driven_droplet ? 1 : 0
  image    = "164728761"
  name     = "event-driven-droplet-tf"
  region   = "blr1"
  size     = "s-4vcpu-8gb"
  ssh_keys = [digitalocean_ssh_key.my_key.fingerprint]

  provisioner "local-exec" {
    command = "powershell -Command \"Start-Sleep -Seconds 60\""
  }
  provisioner "local-exec" {
    command = "scp -o StrictHostKeyChecking=no D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\eda_script.sh D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\eda_script.py D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\id_rsa D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\id_rsa.pub root@${self.ipv4_address}:/root/"
  }
  connection {
    type        = "ssh"
    user        = "root"
    private_key = file("D:\\Ini8_Labs\\Terraform\\Ansible_Automation_Platform\\id_rsa")
    host        = self.ipv4_address
  }
  provisioner "remote-exec" {
    inline = [
      "chmod +x /root/eda_script.sh",
      "bash /root/eda_script.sh",
    ]
  }
}
