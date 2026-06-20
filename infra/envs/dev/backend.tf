terraform {
  backend "azurerm" {
    resource_group_name  = "rg-cloudwise-radar-tfstate"
    storage_account_name = "stcwrtfstatenikhil79"
    container_name       = "tfstate"
    key                  = "dev.terraform.tfstate"
  }
}