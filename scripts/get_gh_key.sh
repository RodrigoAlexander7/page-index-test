#!/bin/bash
# usamos esto justo despues de cargar el main.tf (por segunda vez)
# 1. Crear la cuenta de servicio
gcloud iam service-accounts create github-actions-sa --display-name="GitHub Actions Deployer"

sleep 15

# 2. Darle permisos de Editor (para que pueda subir imágenes y desplegar)
gcloud projects add-iam-policy-binding page-index-489500 \
  --member="serviceAccount:github-actions-sa@page-index-489500.iam.gserviceaccount.com" \
  --role="roles/editor"

sleep 3

# 3. Crear el archivo de llave JSON
gcloud iam service-accounts keys create github-key.json \
  --iam-account=github-actions-sa@page-index-489500.iam.gserviceaccount.com