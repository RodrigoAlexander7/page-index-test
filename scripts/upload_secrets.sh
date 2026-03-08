#!/bin/bash
# upload_secrets.sh

# Leemos el archivo línea por línea
while IFS='=' read -r key value; do
  # Ignoramos líneas vacías o comentarios
  [[ -z "$key" || "$key" == \#* ]] && continue
  
  echo "Subiendo secreto: $key..."
  # Sube el valor como una nueva versión
  echo -n "$value" | gcloud secrets versions add "$key" --data-file=-
done < .env.prod

echo "¡Todos los secretos subidos correctamente!"