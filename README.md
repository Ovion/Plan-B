# Plan-B

Predicción de acidentes de tráfico con involucración de bicicletas

## Introducción

Plan B nace con la idea de evitar los numerosos accidentes de tráfico que sufren los ciclistas en las calles de Madrid.

En esta aplicación podemos consultar en un mapa interactivo de calor el histórico de los accidentes de tráfico producidos en la ciudad de Madrid. Además, también se puede predecir futuros accidentes en función de:

- Condiciones meteorológicas

- Festividades, Vísperas, Laborables

- Rango horario: Mañana, Tarde, Noche

## Datos 

Los datos de accidentes de tráfico provienen de [datos abiertos de Madrid](https://datos.madrid.es/sites/v/index.jsp?vgnextoid=374512b9ace9f310VgnVCM100000171f5a0aRCRD&buscar=true&Texto=&Sector=comercio&Formato=&Periodicidad=&orderByCombo=CONTENT_INSTANCE_NAME_DECODE) de los cuales se cruzan los de accidentes de tráfico, meteorológicos y con el calendario laboral.

Además esta aplicación bebe de dos APIs:
- Google: Para el tema de coordenadas

- IQAir Visual: Para meteorología 

## Parte técnica

Librerías usadas en el proyecto:

- Pandas: Librería principal, con ella he limpiado y ordenado todos

- Scikit Learn: Para los modelos de predicción, en este caso se utilizan modelos de clasificación. Los mejores resultados se obtuvieron con KNNC brute 

- Folium: Con el fin de pintar los mapas de calor

- Flask: Como interfaz para el usuario

- MongoDB: Se utilizó como base de datos, tanto en local como en la nube (Atlas)
