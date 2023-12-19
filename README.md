# Tercer Parcial - Tópicos Selectos en IA

### Nombres: Ariane Garrett - Camila Grandy
### Código: 54617 - 56584

El proyecto en el que trabajamos es un Análisis de Textos Jurídicos, en el cual se utilizan modelos de NLP para realizar
un análisis de los textos y poder mostrar información relevante de estos como las entidades que se encuentran en el texto.
Para esto se utilizo OpenAI para el análisis de los textos y sacar las entidades. 

## Primeras configuraciones
Para iniciar el proyecto, debemos clonar el repositorio con el siguiente comando:

```bash
git clone https://github.com/arigabec/Topicos-IA-3er-Parcial-Garrett-Grandy.git
```
Una vez obtenido el proyecto completo debemos ejecutar los siguientes comandos en la rama *master*, en la carpeta donde 
clonamos el proyecto,
para poder visualizar el proyecto funcionando en un contenedor de Docker:

```bash
cd Topicos-IA-3er-Parcial-Garrett-Grandy
docker compose up
```

## Explicación de la API
La API se encuentra en el archivo main.py, y se utilizó el framework FastAPI para su desarrollo. La API cuenta con 5 endpoints:

- /status: devuelve el estado en el que se encuentra el servicio actualmente.
- /analysis: recibe un texto y devuelve la predicción del analisis NLP que se realizó sobre este texto, sacando las entidades
que se encuentran en el texto. para asi poder mostrar la información relevante de este.
- /reports: devuelve un archivo .csv con los registros de las últimas predicciones realizadas.

## Explicacion de los modelos de predicción
- SqlModel: SQLModel es una biblioteca para interactuar con bases de datos SQL desde código Python, con objetos Python. 
Está diseñado para ser intuitivo, fácil de usar, altamente compatible y robusto.
- Openai - gpt_4: este modelo nos permite realizar un análisis NLP del texto enviado en la petición, devolviendo como 
resultado el POS Tagging y NER del texto. En este caso, el uso de este modelo fue interesante ya que permite predecir el
sentimiento de los textos en diferentes idiomas (multilingue).

## Link de Google Cloud del Backend
https://topicos-ia-3er-parcial-garrett-grandy-h6vokikroq-ue.a.run.app/docs

## Link de Google Cloud del Frontend

https://topicos-ia-3er-parcial-garrett-grandy-frontend-h6vokikroq-ue.a.run.app
