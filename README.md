# Análisis Elección Presidencial Argentina 2023

Este repositorio fue el precursor de [este artículo](https://medium.com/@tomas.piaggio12/analizando-las-elecciones-presidenciales-con-inteligencia-artificial-y-casi-arruinando-mi-pc-bc3f3e133671).


El repositorio contiene código que analiza los canales de televisión TN, C5N y A24 de Argentina. Son noticieros muy conocidos, 
los cuales tienen streams continuos en YouTube con el chat habilitado. Se toma la infromación del chat y se hacen diferentes análisis
para entender el comportamiento de las personas y la percepción de los partidos políticos.

## Repositorio

El repositorio contiene dos directorios principales: `notebooks` y `src`.

- `notebooks`: Contiene algunos Jupyter Notebooks que analizan el código.
  - [EDA](/notebooks/EDA.ipynb): Exploratory Data Analysis. Este es el notebook más importante. Es donde la mayor parte del análisis recae.
  - [PySpark](/notebooks/PySpark.ipynb): Este notebook no esta terminado pero consiste en la configuración inicial para transformar el código de EDA en PySpark para que pueda correr de manera escalable.
  - [Sentiment](/notebooks/Sentiment.ipynb): Este notebook es el que calcula el sentiment. Se puede correr numerosas veces sin que inserte o repita la información ya que la query que toma los datos chequea que no este ya presente en la tabla `messages`.
- `src`: Contiene parte necesaria del código. Aquí, las carpetas más importantes son `message_collector` y `models`. `message_collector` es la cual toma los mensajes de YouTube y los escribe en la base de datos Clickhouse. Si se ve el [`docker-compose`](/docker-compose.yml) se puede ver que se inicializan tres contenedores uno para cada canal. El `video-id` es simplemente el valor del video de YouTube despues de el `watch?v=`. La carpeta models contiene los modelos que se utilizaron y se exponen por http. La idea es que a través de PySpark se hicieran llamados http a estos para poder aumentar la data. No uso los modelos directamente desde PySpark proque cargarlos desde el file system es lo más costoso y esto lo tendría que hacer numerosas veces.

## Uso

Si todavía no construyeron la imagen del `message_collector` háganlo ahora con los siguientes comandos: 

```bash
# Cambiar de directorio a la ubicación del message_collector.
cd src/message_collector

# Construir la imagen para que sea usada por el docker compose.
docker build -t message_collector:1.0.0 .
```

Y finalmente para correr el software: 

```bash
docker-compose up
```

Este inicializará la base de datos, los collectors y un Jupyter Lab para poder hacer los análisis que se quisieran hacer. 
Como recomendación importante (si no leyeron la nota ahí descubrirán por qué), configuren un volumen para el Jupyter Lab.
