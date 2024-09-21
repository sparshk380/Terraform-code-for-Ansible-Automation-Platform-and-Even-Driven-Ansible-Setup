variable "digitalocean_token" {
  type        = string
  description = "DigitalOcean API token"
  sensitive   = true # Sensitive so that it won't be seen in the logs
}

variable "ssh_key_name" {
  description = "SSH key"
  type        = string
}

variable "ssh_public_key" {
  description = "The content of SSH public key"
  type        = string
  sensitive   = true
}

variable "create_ansible_droplet" {
  type        = bool
  default     = true
  description = "Whether to create the ansible droplet or not"
}

variable "create_event_driven_droplet" {
  type        = bool
  default     = true
  description = "Whether to create the event driven droplet."
}
