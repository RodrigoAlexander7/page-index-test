# 1. Configuracion del Proveedor
provider "google" {
  project = "page-index-489500"
  region  = "us-central1"
}

# 2. Habilitar las APIs necesarias en el proyecto 
resource "google_project_service" "run_api" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifactregistry_api" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "secretmanager_api" {
  service            = "secretmanager.googleapis.com"
  disable_on_destroy = false
}

# 3. Artifact Registry
resource "google_artifact_registry_repository" "mi_repo" {
  location      = "us-central1"
  repository_id = "mi-app-repo"
  description   = "Repositorio para mis imágenes de FastAPI y NextJS"
  format        = "DOCKER"

  # Le decimos a Terraform que espere a que la API esté activa
  depends_on = [google_project_service.artifactregistry_api]
}

# 4. Secret Manager: La caja fuerte para GEMINI_API_KEY
resource "google_secret_manager_secret" "gemini_key" {
# establece el nombre (secret_id) pero no el contenido aun, eso se hace despues
  secret_id = "gemini-api-key"

  replication {
    auto {}
  }

  depends_on = [google_project_service.secretmanager_api]
}