# 🐳 Despliegue con Docker y Kubernetes

## Docker

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando inicial
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "trazabilidad_agroindustrial.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgis/postgis:13
    environment:
      POSTGRES_DB: trazabilidad_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DB_NAME=trazabilidad_db
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_HOST=postgres
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
```

### Comandos Docker

```bash
# Construir imagen
docker build -t trazabilidad-backend:latest .

# Ejecutar con docker-compose
docker-compose up -d

# Ejecutar migraciones
docker-compose exec backend python manage.py migrate

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Ver logs
docker-compose logs -f backend

# Detener servicios
docker-compose down
```

## Kubernetes (AWS EKS)

### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trazabilidad-backend
  labels:
    app: trazabilidad-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: trazabilidad-backend
  template:
    metadata:
      labels:
        app: trazabilidad-backend
    spec:
      containers:
      - name: backend
        image: 123456789.dkr.ecr.us-east-1.amazonaws.com/trazabilidad-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DEBUG
          value: "False"
        - name: DB_HOST
          value: "postgres-service"
        - name: DB_NAME
          value: "trazabilidad_db"
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
        - name: DJANGO_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: django-secrets
              key: secret-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: trazabilidad-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  selector:
    app: trazabilidad-backend
```

### Comandos Kubernetes

```bash
# Crear namespace
kubectl create namespace trazabilidad

# Crear secretos
kubectl create secret generic db-credentials \
  --from-literal=username=postgres \
  --from-literal=password=tu_password \
  -n trazabilidad

kubectl create secret generic django-secrets \
  --from-literal=secret-key=tu_clave_secreta \
  -n trazabilidad

# Desplegar
kubectl apply -f deployment.yaml -n trazabilidad
kubectl apply -f service.yaml -n trazabilidad

# Ver estado
kubectl get pods -n trazabilidad
kubectl get svc -n trazabilidad

# Ver logs
kubectl logs -f deployment/trazabilidad-backend -n trazabilidad

# Ejecutar migraciones
kubectl exec -it deployment/trazabilidad-backend -n trazabilidad \
  -- python manage.py migrate
```

## CI/CD con GitHub Actions

### .github/workflows/deploy.yml

```yaml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths: ['backend/**']

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: trazabilidad-backend
  EKS_CLUSTER_NAME: trazabilidad-cluster

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Login to ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build, tag, and push image to ECR
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG backend/
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
    
    - name: Update deployment image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        aws eks update-kubeconfig --region ${{ env.AWS_REGION }} --name ${{ env.EKS_CLUSTER_NAME }}
        kubectl set image deployment/trazabilidad-backend \
          backend=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG \
          -n trazabilidad
        kubectl rollout status deployment/trazabilidad-backend -n trazabilidad
```

## Monitoreo y Logging

### CloudWatch Logs
```bash
# Ver logs en CloudWatch
aws logs tail /aws/eks/trazabilidad-cluster --follow

# Crear grupo de logs
aws logs create-log-group --log-group-name /trazabilidad/backend
```

### Prometheus y Grafana
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: trazabilidad
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'django'
      static_configs:
      - targets: ['trazabilidad-service:8000']
      metrics_path: '/metrics/'
```

## Checklist de Despliegue

- [ ] Variables de entorno configuradas
- [ ] Base de datos PostgreSQL + PostGIS lista
- [ ] Migraciones ejecutadas
- [ ] Archivos estáticos recolectados
- [ ] Usuarios admin creados
- [ ] Certificados SSL configurados
- [ ] Backups automatizados programados
- [ ] Logs centralizados configurados
- [ ] Monitoreo activado
- [ ] Health checks funcionando
- [ ] Rate limiting configurado
- [ ] CORS configurado correctamente

## Troubleshooting Producción

### Error: "Database connection refused"
```bash
# Verificar conexión a BD
python manage.py dbshell

# Crear user en PostgreSQL
createuser -P postgres
createdb -O postgres trazabilidad_db
```

### Error: "Static files not found"
```bash
python manage.py collectstatic --noinput --clear
```

### Error: "Out of memory"
```bash
# Aumentar límites en K8s
# En deployment.yaml, aumentar resources.limits.memory
```

---

Adaptado para despliegue en AWS con EKS y escalabilidad horizontal.
