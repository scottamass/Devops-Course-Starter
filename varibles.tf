variable "prefix" {
  description = "The prefix used for all resources in this enviroment"
}

variable "DOCKER_REGISTRY_SERVER_URL"{
    default = ""
}

variable "GITHUB_CLIENT_ID"{
    sensitive = true
}

variable "FLASK_ENV"{
    default = "production"
}

variable "GIT_HUB_SECRET"{
    sensitive = true
}

variable "LOGIN_DISABLED"{
    default = "false"
}