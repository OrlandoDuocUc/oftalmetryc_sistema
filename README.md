## Oftalmetryc - Instrucciones de Instalación y Despliegue

Estas instrucciones le permitirán obtener una copia del proyecto en funcionamiento en su equipo local para fines de desarrollo y pruebas. Consulte la sección de implementación para obtener instrucciones sobre cómo implementar el proyecto en un sistema en vivo.

### 🖥️  Ejecución Local 
> Requisitos: Python 3.13+, pip, SQL Server Managment Studio

# 1. Clona el repositorio
```
git clone --branch fix/implementation-products --single-branch https://github.com/sofiadonosoalarcon/optica-maipu.git 
cd optica-maipu
```
# 2. Crea un entorno virtual
```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```
# 3. Instala las dependencias
```
pip install -r requirements.txt
```
# 6. Ejecuta la app
```
python boot.py
```
### ☁️  Despliegue en Azure App Service
> Requisitos: Cuenta de Azure, CLI de Azure, App Service plan
# 1. Inicia sesión en Azure
```
az login
```
# 2. Crea un grupo de recursos (si no existe)
```
az group create --name optica-maipu-resource-group --location eastus
```
# 3. Crea el plan de App Service
```
az appservice plan create --name optica-maipu-plan --resource-group optica-maipu-resource-group --sku B1 --is-linux
```
# 4. Crea la Web App
```
az webapp create --resource-group optica-maipu-resource-group --plan optica-maipu-plan \
  --name optica-maipu-backend --runtime "PYTHON|3.13" 
```
# 5. Crear el workflow oara el despliegue
```
# Docs for the Azure Web Apps Deploy action: https://github.com/Azure/webapps-deploy
# More GitHub Actions for Azure: https://github.com/Azure/actions
# More info on Python, GitHub Actions, and Azure App Service: https://aka.ms/python-webapps-actions

name: Build and deploy Python app to Azure Web App - backend-optica-maipu

on:
  push:
    branches:
      - fix/implementation-products
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read #This is required for actions/checkout

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python version
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Create and start virtual environment
        run: |
          python -m venv venv
          source venv/bin/activate
      
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      # Optional: Add step to run tests here (PyTest, Django test suites, etc.)

      - name: Zip artifact for deployment
        run: zip release.zip ./* -r

      - name: Upload artifact for deployment jobs
        uses: actions/upload-artifact@v4
        with:
          name: python-app
          path: |
            release.zip
            !venv/

  deploy:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: 'Production'
      url: ${{ steps.deploy-to-webapp.outputs.webapp-url }}
    permissions:
      id-token: write #This is required for requesting the JWT
      contents: read #This is required for actions/checkout

    steps:
      - name: Download artifact from build job
        uses: actions/download-artifact@v4
        with:
          name: python-app

      - name: Unzip artifact for deployment
        run: unzip release.zip

      
      - name: Login to Azure
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZUREAPPSERVICE_CLIENTID_21EA4B01A2424270B42F4658AA862DD2 }}
          tenant-id: ${{ secrets.AZUREAPPSERVICE_TENANTID_64B68935BAEC466F9250B3EBA15078F5 }}
          subscription-id: ${{ secrets.AZUREAPPSERVICE_SUBSCRIPTIONID_D1459044535646BCB7C2DFF261D32825 }}

      - name: 'Deploy to Azure Web App'
        uses: azure/webapps-deploy@v3
        id: deploy-to-webapp
        with:
          app-name: 'backend-optica-maipu'
          slot-name: 'Production'
```

