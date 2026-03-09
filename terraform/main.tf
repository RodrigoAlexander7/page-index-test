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
  secret_id = "GEMINI_API_KEY"

  replication {
    auto {}
  }

  depends_on = [google_project_service.secretmanager_api]
}

# **********************************
# Primero corremo hasta este punto
# para que google cloud cree el secret manager, luego lo llenamos y finalmente contruimos las imagenes
# si intentamos correr todo de golpe fallara pke el google secret manager no tiene nada (y google exige q tenga algo)
# por eso despues de la primera parte corremos el script upload_secrets

# ==========================================
# BACKEND: FASTAPI
# ==========================================

# 1. Identidad del Backend (Service Account)
resource "google_service_account" "backend_sa" {
  account_id   = "fastapi-backend-sa"
  display_name = "Service Account para FastAPI Backend"
}

# 2. Le damos permiso a la Service Account para leer secretos
resource "google_project_iam_member" "secret_accessor" {
  project = "page-index-489500" 
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}

# 3. El Servicio Cloud Run del Backend
resource "google_cloud_run_v2_service" "backend_api" {
  name     = "fastapi-backend"
  location = "us-central1"

  depends_on = [google_project_iam_member.secret_accessor]

  template {
    service_account = google_service_account.backend_sa.email
    
    containers {
      # Usamos la imagen "placeholder" temporalmente
      image = "us-docker.pkg.dev/cloudrun/container/hello" 
      
      # Inyectamos el secreto como variable de entorno
      env {
        name = "GEMINI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = "GEMINI_API_KEY" # El nombre que pusiste en tu .env.prod
            version = "latest"
          }
        }
      }
    }
  }
  
  # to say terraform do not re create the image if I upload another new (the changes with github actions)
  lifecycle {
    ignore_changes = [
      template[0].containers[0].image
    ]
  }
}

# 4. Hacemos que el Backend sea público (accesible desde internet)
resource "google_cloud_run_v2_service_iam_member" "backend_publico" {
  name     = google_cloud_run_v2_service.backend_api.name
  location = google_cloud_run_v2_service.backend_api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ==========================================
# FRONTEND: NEXT.JS
# ==========================================

# 5. El Servicio Cloud Run del Frontend
resource "google_cloud_run_v2_service" "frontend_app" {
  name     = "nextjs-frontend"
  location = "us-central1"  
  template {
    containers {
      # Imagen placeholder temporal
      image = "us-docker.pkg.dev/cloudrun/container/hello" 
      
      # Next.js no necesita leer secretos en tiempo de ejecución
      # porque las variables se inyectaron en el Docker build
    }
  }
  lifecycle {
    ignore_changes = [
      template[0].containers[0].image
    ]
  }
}

# 6. Hacemos que el Frontend sea público
resource "google_cloud_run_v2_service_iam_member" "frontend_publico" {
  name     = google_cloud_run_v2_service.frontend_app.name
  location = google_cloud_run_v2_service.frontend_app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ==========================================
# OUTPUTS (Para que Terraform nos dé las URLs al terminar)
# ==========================================
output "backend_url" {
  value = google_cloud_run_v2_service.backend_api.uri
}

output "frontend_url" {
  value = google_cloud_run_v2_service.frontend_app.uri
}