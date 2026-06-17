variable "project_name" {
  description = "Project name used for tagging Azure resources."
  type        = string
  default     = "cloudwise-radar"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}

variable "location" {
  description = "Azure region for the dev environment."
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "Azure resource group name."
  type        = string
  default     = "rg-cloudwise-radar-dev"
}

variable "owner" {
  description = "Owner tag for FinOps accountability."
  type        = string
  default     = "nikhil"
}

variable "cost_center" {
  description = "Cost center tag for FinOps reporting."
  type        = string
  default     = "learning"
}

