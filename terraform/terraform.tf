terraform {
  required_version = ">= 1.5.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 3.0"
    }
  }
}

# Credentials are not stored in code. The provider reads them from either:
#   - a clouds.yaml entry selected with OS_CLOUD (or var.cloud), or
#   - the standard OS_* environment variables from an OpenStack RC file
#     (OS_AUTH_URL, OS_USERNAME, OS_PASSWORD, OS_PROJECT_NAME, ...).
provider "openstack" {
  cloud = var.cloud
}

variable "cloud" {
  description = "Name of the clouds.yaml entry to use. Leave null to use OS_* environment variables."
  type        = string
  default     = null
}

variable "image" {
  description = "Name of the Glance image to boot."
  type        = string
  default     = "cirros"
}

variable "flavor" {
  description = "Name of the Nova flavor."
  type        = string
  default     = "1c05r1d"
}

variable "network" {
  description = "Name of the network to attach the instance to."
  type        = string
  default     = "ext-net-154"
}

resource "openstack_compute_instance_v2" "vm_terraform" {
  name        = "vm-terraform"
  image_name  = var.image
  flavor_name = var.flavor

  network {
    name = var.network
  }
}

output "instance_ipv4" {
  description = "IPv4 address of the created instance."
  value       = openstack_compute_instance_v2.vm_terraform.access_ip_v4
}
