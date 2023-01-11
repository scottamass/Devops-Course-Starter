terraform {
 required_providers {
 azurerm = {
 source = "hashicorp/azurerm"
 version = ">= 3.8"
 }
 }
}
provider "azurerm" {
 features {}
}
data "azurerm_resource_group" "main" {
 name = "LV21_ScottAtkinson_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
 name = "terraformed-asp" 
 location = data.azurerm_resource_group.main.location 
 resource_group_name = data.azurerm_resource_group.main.name 
 os_type = "Linux"
 sku_name = "B1"
}
resource "azurerm_linux_web_app" "main" {
 name = "scottamass-todohub-2" 
 location = data.azurerm_resource_group.main.location 
 resource_group_name = data.azurerm_resource_group.main.name 
 service_plan_id = azurerm_service_plan.main.id 
 site_config { 
 application_stack { 
 docker_image = "appsvcsample/python-helloworld" 
 docker_image_tag = "latest" 
 } 
 } 
 app_settings = { 
 "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io" 
 }
}
