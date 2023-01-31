terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
        resource_group_name  = "LV21_ScottAtkinson_ProjectExercise"
        storage_account_name = "tfstoragesma1337"
        container_name       = "tfstate"
        key                  = "terraform.tfstate"
    }
}
provider "azurerm" {
  features {}
}
data "azurerm_resource_group" "main" {
  name = "LV21_ScottAtkinson_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-terraasp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}
resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-terratodoappsa"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id
  site_config {
    application_stack {
      docker_image     = "scottamass/prod"
      docker_image_tag = "latest"
    }
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = var.DOCKER_REGISTRY_SERVER_URL
    "MONGO_CONNECTION_STRING"  = azurerm_cosmosdb_account.main.connection_strings[0]
    "MONGO_DATABASE_NAME"       = "testDb"
    "FLASK_APP"                  = "todo_app/app"
    "FLASK_ENV"                  = "production"
    "LOG_LEVEL"                  = "DEBUG"
    "SECRET_KEY"                 = 1234567
    "GITHUB_CLIENT_ID"           = var.GITHUB_CLIENT_ID
    "GITHUB_SECRET_ID"           = var.GITHUB_SECRET_ID
    
  }
}


resource "azurerm_cosmosdb_account" "main" {
  name                = "terracosmosacc"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"


  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }

  consistency_policy {
    consistency_level = "Session"

  }

}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-terramongodb"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name

}

