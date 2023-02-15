variable "prefix" {
  description = "The prefix used for all resources in this enviroment"
}

variable "DOCKER_REGISTRY_SERVER_URL" {
  default = "https://index.docker.io"
}

variable "GITHUB_CLIENT_ID" {
  sensitive = true
}

variable "FLASK_ENV" {
  default = "production"
}

variable "GITHUB_SECRET_ID" {
  sensitive = true
}

variable "LOGIN_DISABLED" {
  default = "false"
}