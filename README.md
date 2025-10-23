# Readme

## SECCIÓN : Dataset de Diabates e Insurance

### 1) ¿Cuál es el umbral ideal para el modelo de predicción de diabetes?

El umbral ideal se determina mediante el análisis de la curva ROC, seleccionando aquel que maximiza el índice de Youden (J = Sensibilidad - Tasa de falsos positivos). Este punto representa el equilibrio óptimo entre sensibilidad y especificidad, asegurando una clasificación más precisa entre pacientes con y sin diabetes. El umbral permite ajustar el comportamiento según la necesidad: valores más bajos priorizan la detección de casos positivos, mientras que valores más altos reducen los falsos positivos.

### 2) ¿Cuáles son los factores que más influyen en el precio de los costos asociados al seguro médico?

- Los factores que ejercen mayor influencia en el costo del seguro médico son principalmente:

- Condición de fumador: los fumadores presentan costos significativamente mayores debido al riesgo sanitario asociado.

- Índice de masa corporal (BMI): un valor elevado refleja posibles complicaciones médicas, incrementando los costos.

- Edad: a mayor edad, mayor riesgo y, por tanto, mayor gasto en atención médica.

- Número de hijos y región geográfica: influyen en menor medida, pero afectan el monto final debido a las políticas regionales y familiares.

### 3) Hacer un análisis comparativo de cada características de ambos modelos utilizando RandomForest.

En el caso del modelo de diabetes, las variables más relevantes suelen ser Glucose, BMI y Age, ya que reflejan directamente el estado metabólico y la predisposición a la enfermedad.
En el modelo de costos médicos, las variables de mayor peso son Smoker, BMI y Age.
El análisis comparativo muestra que tanto en el ámbito clínico como económico, los factores fisiológicos y de hábitos de vida son determinantes en la predicción.

### 4) ¿Qué técnica de optimización mejora el rendimiento de  ambos modelos?

Para mejorar el rendimiento de ambos modelos se recomienda aplicar optimización de hiperparámetros, mediante técnicas como: 
- GridSearchCV: Que prueba todas las combinaciones posibles de parámetros dentro de un rango que tú defines, y selecciona la mejor.  
- RandomizedSearchCV: que prueba combinaciones aleatorias, lo que reduce el tiempo de cómputo y a menudo encuentra buenos resultados más rápido.

Estos permiten ajustar parámetros clave del modelo.

En el modelo de diabetes, puede aplicarse regularización: 
- L1: Elimina variables poco relevantes.
- L2: Evita que el modelo dependa demasiado de algunas variables.

Y calibración de probabilidades para mejorar la sensibilidad.

En el modelo de seguro médico, la optimización se puede complementar con ensembles (como Gradient Boosting o XGBoost) que consiste en combinan varios arboles débiles para crear uno mas fuerte.

### 5) Explicar contexto de los datos.

El dataset de diabetes proviene de estudios clínicos que analizan factores fisiológicos y demográficos relacionados con la enfermedad. Incluye variables como glucosa, presión arterial, índice de masa corporal y edad, con el objetivo de predecir la probabilidad de desarrollar diabetes.
El dataset de seguro médico recopila información demográfica, económica y de salud de los beneficiarios, con el fin de estimar el costo asociado a la atención médica. Las variables reflejan el perfil de riesgo de cada individuo.
Ambos conjuntos de datos representan contextos reales donde el análisis predictivo contribuye a la toma de decisiones en salud pública y gestión financiera.


### 6) Analizar el sesgo que presentan los modelos y explicar porqué.

Ambos modelos presentan posibles sesgos de muestreo y representación.
En el modelo de diabetes, el desbalance de clases puede llevar a que el algoritmo priorice los casos negativos, disminuyendo la sensibilidad hacia los casos positivos.
En el modelo de seguro médico, las variables sexo, región o estado de fumador pueden actuar como proxies de condiciones socioeconómicas, introduciendo sesgo en la predicción de costos.

##

## SECCIÓN 2: Dataset Telco Churn

### 1) Definir umbral máximo (Regresión lineal)

En el modelo de regresión aplicado al dataset, el umbral máximo se define como el valor a partir del cual se consideran clientes con altos costos o facturación acumulada. Este valor corresponde al percentil superior de las predicciones, representando a los clientes con mayor gasto total.


## 2) Factores que más influyen en las predicciones

Los factores más influyentes en las predicciones del modelo Telco son:

- Tenure: tiempo que el cliente ha permanecido con la compañía, directamente proporcional al monto total facturado.

- MonthlyCharges: costo mensual del servicio, que determina gran parte del gasto acumulado.

- Otras variables como método de pago o tipo de contrato influyen en menor medida, pero pueden asociarse a la estabilidad del cliente.

En conjunto, estos factores explican la mayor parte de la variabilidad del costo total.

## 3) Contexto de las predicciones

El dataset corresponde a una empresa de telecomunicaciones y contiene información demográfica, contractual y financiera de los clientes.
El objetivo del modelo de regresión es estimar el valor total de los cargos facturados, lo cual refleja la lealtad del cliente y su contribución económica a la empresa.
Este tipo de análisis permite a la organización anticipar ingresos, identificar clientes de alto valor y diseñar estrategias preventivas frente al abandono (churn).
El contexto del modelo se enmarca en la gestión predictiva de clientes y la optimización de decisiones comerciales basadas en datos.



