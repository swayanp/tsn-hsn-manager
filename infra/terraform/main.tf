resource "docker_image" "tsn_hsn_image" {
  name         = "swayanp/tsn-hsn-manager:${var.image_tag}"
  keep_locally = true
}

resource "docker_container" "tsn_hsn_app" {
  name  = "tsn-hsn-manager-${var.environment}"
  image = docker_image.tsn_hsn_image.image_id

  ports {
    internal = 8000
    external = var.environment == "prod" ? 8000 : (
               var.environment == "qa"   ? 8001 : 8002
    )
  }

  env = [
    "DATABASE_PATH=/data/identifiers.db",
    "ENVIRONMENT=${var.environment}"
  ]

  volumes {
    container_path = "/data"
    host_path      = "${path.cwd}/data-${var.environment}"
  }

  restart = "unless-stopped"
}
