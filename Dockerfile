# Usa una imagen base oficial de Python
FROM python:3.9

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la aplicación al directorio de trabajo
COPY . /src

# Expone el puerto en el que la aplicación correrá
EXPOSE 5000

# Define el comando por defecto para correr la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
