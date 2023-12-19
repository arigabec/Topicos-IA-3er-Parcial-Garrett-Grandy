# Usa la imagen de node como base
FROM node:14

# Establece el directorio de trabajo en /app/frontend
WORKDIR /app/frontend

# Copia el archivo package.json e instala las dependencias
COPY package.json .
RUN npm install

# Copia el resto de la aplicación
COPY . .

# Expone el puerto 3000
EXPOSE 3000

# Comando por defecto para ejecutar la aplicación cuando se inicia el contenedor
CMD ["npm", "start"]
