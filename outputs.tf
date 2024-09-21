output "automation_platform_droplet_ip" {
  value = var.create_ansible_droplet ? digitalocean_droplet.ansible_automation_platform_droplet[0].ipv4_address : null
}

output "event_driven_droplet_ip" {
  value = var.create_event_driven_droplet ? digitalocean_droplet.event_driven_droplet[0].ipv4_address : null
}

