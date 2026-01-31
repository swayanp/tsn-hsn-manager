variable "environment" {
  description = "Deployment environment (dev / qa / prod)"
  type        = string
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
}
