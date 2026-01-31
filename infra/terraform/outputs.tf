locals {
  port_map = {
    dev  = 8002
    qa   = 8001
    prod = 8000
  }
}

output "app_url" {
  value = "http://localhost:${local.port_map[var.environment]}/ui"
}
