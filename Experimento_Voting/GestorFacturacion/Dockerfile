# Dockerfile para APIGateway, ColaSolicitudes, y GestorFacturacion
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt
COPY ../requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el contenido de la aplicación
COPY . .

# Establecer la variable de entorno para Flask
ENV FLASK_APP=app.py

# Exponer el puerto necesario
EXPOSE 5000 

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]  # Cambia el puerto según el microservicio
