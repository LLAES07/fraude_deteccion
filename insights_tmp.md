# **0. Importar librerias**

---

# **1. CARGA Y EXPLORACIÓN INICIAL**

---

## 1.1 Revisión de columnas y tipo de datos

---

### 💾 **Observaciones**


Existe un total de **11 columnas** y **151112 registros**.

 - 10 son variables independientes
 - 1 variable dependiente (`class`)

Existen 2 columnas que parecen estar relacionadas con fechas pero están como str: `signup_time`, `purchase_time`.

Hay 5 columnas **numéricas** (`user_id`, `purchase_value`, `user_id`, `age`,`ip_address` y `class`), las 6 restantes son **str**.


No existen datos nulos aparentes.





---

### 💾 **Observaciones**


Existe un total de 3 columnas y 138846.

- 2 son numéricas relacionadas con limites de ip
- 1 de estas es str relacionada con el país de donde se efectuo la compra.



📢 **Conclusión**

Según lo señalado se debe revisar las columnas para ver si es necesario transformar alguna columna. En cuanto a las features relacionadas con tiempo deben ser cambiadas a su tipo correcto.

Revisar si es que en realidad no hay nulos como datos mal inputados, categorias faltantes u otros errores también debe estar presente en el análisis.

**Columnas a corregir**
- signup_time y purchase_time son object --> convertir a datetime
- source, browser, sex son object --> convertir a category (reducir memoria) aunque considerando visualizaciones en el EDA puede que de más problema.


---

## 1.2 Revisión numérica somera

---

### 💾 **Observaciones**

`purchase_value`: 
- **promedio**: 36.94 $
- **std**: 18.32 $
- **min**: 9 $
- **max**: 154.00 $

`age`:

- **promedio**: 33 años
- **std**: 8.62 años
- **min**: 18 años
- **max**: 76 años



`lower_bound_ip_address`:

- **min**: 16777216
- **max**: 3758096128


`upper_bound_ip_address`:

- **min**: 16777471
- **max**: 3758096383

📢 **Conclusión**

El 75 % de los datos esta por debajo de los 49 $ de `purchase_value`. Considerando esto y el valor del maximo es interesante ver cuantos datos están fuera del 75 % y que tan altos son.

  - El std es bastante alto lo que debe ser principalmente por los valores ya nombrados.

La edad promedio de los clientes es de  33 años.
  - La edad mínima es 18 en sintonia con el negocio y la máxima de 76.
  - El std es alto pero no desmezutado como el de la columna anterior


En cuanto IP, aún sin cruzar los dataframes no podemos ver algo concluyente.


`df` y `df_ip` se relacionan entre las ip. Con el ip de `df` hay que encontrar dentro de que rango cae y se le puede asignar un país a esa ip.

---

##  1.3. Unir los dataframes

---

##### **🔓 Detalle**
Uso merge_assoft porque me permite hacer un merge utilizando rangos.
La idea es ordenar ambos dataset por la columna donde quiera comparar los rangos.

Utilizo `ip_address` en la tabla izquierda y `lower_bound_ip_address` en la derecha
para buscar el valor más cercano o igual hacia atrás de cada IP.

Aun así, esto dejará casos donde `ip_address` > `upper_bound_ip_address`.
En esos casos el país se marca como 'Unknown' ya que la IP no pertenece a ese rango.


---

##  **1.4. Duplicados o nulos?**

---

##### **📢Observación**

Existen 634 valores nulos en el dataframe después de aplicar el merge. No existen duplicados. Los nulos vienen principalmente del cruce entre ambos dataframes. Revisaremo esto en mayor profundidad en el EDA.


---

# **2. EDA**

---

    💡 Nota técnica: Aunque lo ideal para optimizar memoria en Pandas es convertir las variables de texto a tipo category, en la fase de EDA se mantendrán como object/string para asegurar la compatibilidad y estabilidad con los gráficos de Seaborn/Matplotlib.



---

## **2.1. Variables Numéricas**

---

## 2.1.1 Target (Variable independiente)

---

### 📢 Detalle

El dataframe tiene un desbalance alto entre la clase 0 y 1. La primera es totalmente prevalente con un 90.6 % de los datos mientras que la segúnda solo representa 9.4 % de los datos.

-   Aplicar oversampling de la clase minoritaria parece una estrategia indispensable en los datos.

---

### **2.1.2 Purchase_value**

---

### 💾 **Observaciones**

Lo primero que salta a la luz es que ambas distribuciones son identicas o casi identicas compartiendo el mismo skewness a la derecha.

Tanto la clase 0 como la clase 1 tienen casi los mismos datos en las métricas centrales.
- El promedio, el std, el min los rangos cuartilicos son casi identicos.


La similitud tan grande en las distribuciones me lleva a pensar que los movimientos fraudulentos siguen la distribución de los datos legales para no levantar sospechas. Serán las distribuciones iguales ?

---

Considerando los gráficos las distribuciones se ven lejos de ser normal pero aplicaremos igualmente un test estadístico para conocer la normalidad o no. Debido al tamaño de muestra utilizamos D'Agostino-Pearson

---

**Observación**
Datos no normales por lo que necesitamos un test no paramétricos apra saber si las distribuciones son iguales o no.

---


Por lo tanto el monto no influye si es fraude o no.

---

Falla en rechazar la hipotesis nula de que las distribuciones son identicas. Por lo que lo más probable es que si lo sean como se ve arriba

---

**CONCLUSIÓN**

Según lo observado tanto en los gráficos como en los diferentes tests estadisticos. El `purchase_value` no tiene evidencia estadisticamente relevante para ser un discriminante fuerte en si existira fraude o no.

---

### **2.1.3 Age**

---

En age para ambas clases igualmente el promedio, std y los rangos intercuartilicos son casi identicos.

---

Lo primero que salta a la vista que la distribución observada entre transaccciones fraudulentas y lefitimas parecen idénticas. Por otro lado los test estadisticos rechazan sus hipotesis nula, sugiriendo diferencias estadisticamente significantes entre estas clases.
Esta aparente contradicción viene dada en parte por el gran tamaño muestral, que detectan diferencias mínimas que en realidad no tienen relevancia. Por lo tanto considerando las metricas centrales se puede observar que `age` no posee una significancia práctica como feature dominante para detectar fraudes.

---

## **2.2. Variables Str**

---

🔔 **Detalle**

Es clara la diferencia en la cuenta entre ambos segmentos que obviamente viene dada por la proporcion desmezurada de los registros legítimos. En ambos casos son los hombres los que están presente en más registros. En general no se ve una diferencia para los movimientos legítimos y fraudulentos. Necesitamos conocer la cuenta por cada sexo y cada clase

---

🔔 **Detalle**

Como se menciona anteriormente la diferencia de cuentas es grande y se puede observar que al parecer son bastante proporcionales en cuanto a cantidad de hombres y mujeres en cada clase. Para confirmar necesitamos conocer los porcentajes.

---

🔔 **Detalle**

Ahora con los porcentajes es claro ver que no hay una diferencia real entre legítimo y/o fraudulento. Esto nos indica que probablemente no es una feature que nos ayude en gran medida a predecir nuestro target


---

### 🧠  **Conclusiones**

Según lo revisado es claro conocer que la feature sex no tiene un poder predictivo grande para una predicción. Lo siguiente se basa en lo siguiente:
- **Proporciones similares:** Las relaciones entre ambas clases es casi la misma.
- **El efecto del N grande:** Chi2 nos indica que no son independientes pero este resultado se encuentra enmascarado por nuestro n de muestra tan alto. Aplicando v de cramer podemos conocer si esta relación es significativa o en realidad está enmascarada por el tamaño de muestra. Considerando el valor obtenido nos queda claro que la dependencia observada por chi2 en realidad estaba influenciada por el numero de muestra y en realidad las variables son tan poco dependiente que en realidad son dependientes.

Por lo tanto la variable `sex` no nos sirve como una variable predictiva fuerte

---

### 🧠  **Conclusiones**

- La significancia estadística es muy pequeña (7.98 x 10^-15) con un chi2 de 64.92. Lo que viene a evidenciar que las diferencias entre canales no son casualidad.
- El salto de 2% en la columna fraude de Direct puede estar causando este efecto en chi2.
- Considerando la v de cramer de 0.0207 sigue indicando que esta significancia estadistica esta distorsionada por el tamaño de n y que es debil pero es el triple de fuerte que la del sexo.


Si bien `source` tampoco es un predictor fuerte para nuestro target, tiene mejor poder predictivo que `sex`

---

### 🧠  **Conclusiones**

- Muy parecido a las variables anteriores y debido al desbalance importante de los datos en el primer grafico se aprecia que la escala es muy diferente pero se puede ver una relación muy similar entre ambas clases.
- En las crosstab se puede apreciar de mejor forma que en general se sigue la misma proporcion de los datos dominando con un 90% los datos legítimos frente aproximadamente a un 10 % los fraudes.
- Cada `browser` sigue una proporción similar tanto en fraude como en un movimiento legítimo.
- La prueba de `chi2` rechaza la hipotesis nula de independencia con un valor de `p_value` bastante bajo indicando que existe mayor probabilidad de una relación dependiente. Aún asi debido a nuestro alto `n` esto puede ser un resultado sesgado. Según la `v de cramer` podemos decir que esta relación es baja y que lo más probable que las variables sean independientes.
- Con todo esto y lo demás podemos decir que `browser` por si sola no es una buena feature para predecir si hay fraude o no.

---

#### 💿 **Fundamento**

Debido a la cantidad baja de observaciones que no tienen país y considerando que  sigue de manera similar los datos de fraude y no_fraude, por lo anterior y simplicidad en el análisis imputar como `Unknown` es lo correcto

---

### 🧠  **Conclusiones**

- Lo primero relevante es que hay 634 datos en los que el país no existe devido a que en el `merge_asoft` no estaba en ningun rango.
- A cada uno de estos valores se le inputo Unknown por simplicidad.
- Los países unknown tienen un rate de fraude de solo el 9.8 %
- Existen un total de 182 países de los cuales tanto en fraude como en legítimo USA es el que más valores tienen.
- Si bien en el primer gráfico de barras se repite la misma frecuencia de países que son los que más fraudes tienen en la tabla de abajo podemos ver el porcentaje de fraude en cada uno de estos y para el top 10 se puede ver que es un porcentaje que ronda al 10 % la cantidad de fraudes.
- Los países con mayor porcentaje de fraude en cambio en general son paises que no tiene tanta frecuencia en el dataset.
- Chi2 dice que hay una relacion significativa de dependencia pero v de cramer dice que es debil esta relación. 


Según lo anterior podemos ver que si bien no es fuerte predictor si podemos encontrar una relación con aquellos paises que el % de fraude es alto y quizas generar una columna que capte esta relación.


---

## **2.3 VARIABLES TEMPORALES**

---

### 🧠  **Conclusiones**

- Solo tenemos datos del año 2015
- Hay compras desde Enero hasta mediados de diciembre
- El ultimo registro fue en Agosto.

---

### **2.3.1 Purchase_time_month**

---

### 🧠  **Conclusiones**

- Lo primero y más notorio es la diferencia abismal entre el primer mes de compras en relación con los demás meses. El primer mes tiene > 76 % de fraudes mientras en los meses restante oscila entre el 6 a 4 %. Esta diferencia es demasiado grande y por lo tanto mirar el dataset a mayor porfundidad y tratar de entender que pasa en este mes es importante.

- Según el z-score podemos confirmar que el primer mes de los datos es el mes donde se concentra la mayor cantidad de fraudes.
- El primer mes si bien no son los meses de más compras tampoco es uno de los menores. La mayor cantidad de compras se centra entre mayo y agosto.
- El `lift` (ratio fraude x mes / el ratio global o mean) para el primer mes confirma que el primer mes es anomalamente el mes con mayor porcentaje de fraudes.


La feature es interesante puesto que muestra que casi todo el fraude del dataset se encuentra en el primer mes. Esto es interesante puesto que esta diferencia tan grande en relación a los otros meses es demasiado alta. Encontrar que está pasando con esta y otras variables para responder que pasa es importante puesto que una diferencia tan grande tambien podria estar ligada a errores en el dataset si no se pueden respaldar de una forma coherente


---

### **2.3.2 signup_time_month**

---

### 🧠  **Conclusiones**

- La cantidad de registros para el primer mes de registro al igual que el primer mes de compra es altísimo (31 %) en comparación a los demás meses (~ 4.6 %).
- Esto sumado a lo visto que las compras del primer son altisimo entrega una evidencia importante que los fraudes estan hechos en su gran mayoría el primer mes entre que se registra y se compra.

Con esto necesitamos encontrar la relación `purchase_time` - `signup_time`.



---

### **2.3.3 diferencia_signup_purchase_dias : Feature Eng**

---

### 🧠  **OBSERVACIONES**

- La mayor parte de las compras fraudulentas se centran a los 1 y 3 segundos después de realizado el registro.
- La otra mayor cantidad se encuentra en > 7 días pero esto representa todos los datos que vimos anteriormente donde en todos los meses oscila entre un 4 y un 5.6 %.
- Chi2 rechaza la hipotesis nula por lo que lo más probable que exista una relación de dependencia entre la variable cat y el fraude lo que se ve ratificado por la v de cramer que en nuestro caso es alta.

La velocidad entre registro y compra es tan rapida que lo más probable es que sea un sistema automatizado puesto que humanamente es dificil ser tan consistente en tantos datos. La v de cramer tan alta nos dice que sino es un sistema automatizado deberiamos dudar de los datos.







---

### 🧠  **OBSERVACIONES**

- Lo primero que se observa es una repeticion en la ip, device_id, source,browser para distintos user_ids.

Esta relación puede estar dando pistas de porque estas compras son tan rápidas.

---

### 🧠  **OBSERVACIONES**

- Algo interesante a primera vista es que hay varios device_id que tiene mas de una ocurrencia.
- Otra cosa es que solo hay 1 ocurrencia en donde no se repite el mismo `device`
- La mayoria de los datos repiten `device` a lo menos 4 veces.
- En datos donde el `tiempo_cat_reducido` es diferente a `ultra_fast` donde ocurre la mayor parte del fraude podemos ver que la gran parte de los usuarios tiene solo una combinacion unica de `device_id`

---

### 🧠  **OBSERVACIONES**

- En datos donde la compra fue muy rápida y hubo fraude se puede ver que la combinación `device_id`, `source`, `browser` e `ip_adress` se repitió más de una vez en diferentes usuario casi el 99 % de las veces, mientras que fue única solo 1 vez.
- En datos más normales donde ya no existe estas compras tan rápidas se observa que en todos los casos esta combinación fue unica para cada cliente.

Por lo tanto en todas estas compras fraudulentas tenemos que la repetición de estas en diferente usuario es una flag grande junto con la velocidad entre registro y compra.

---

### 🧠  **OBSERVACIONES**

- Confirmamos con estos grágicos que para el primer mes entre los 1 a 3 segundos después del registro tanto `ip` y `device` son extremandamente altos.
- Tambien re afirmamos que para todo los demás datos del dataset en general se da un unico `device` e ip

---

### 🧠  **OBSERVACIONES**

- Tanto `ip` como `device` tienen promedios bastante altos lo que principalmente está influenciado por el primer mes como vimos anteriormente. Esta diferencia entre fraude y no_fraude los convierte en buenos predictores para la variable objetivo

---

### **2.3.4 Purchase_time_hour**

---

### 🧠  **OBSERVACIONES**

- Para la distribuciones de compra tanto para `no_fraude` como para `fraude` se observa que en general ambas siguen distribuciones similares con obviamente diferencias en su frecuencias pero en general no se logra apreciar una diferencia marcada.

---

### 🧠  **OBSERVACIONES**

- La tasa de fraude por hora no entrega ningun resultado concluyente ya que se ve que no hay un patron dominante. 
- La distribución por hora de los eventos super rapidos registrados el primer mes tambien no entregan ningun resultado concluyente debido a una distribución que no tiene patrones significantes.

---

## **2.4 Country v/s variables temporales**

---

### 🧠  **OBSERVACIONES**

- Para el primer mes hay paises que tienen más del 80 % de los datos como fraudes. Con 6 países con 100 % de fraude.
- Para los meses siguientes el % de fraude cae drásticamente. Existe turkmenistan donde hay 100 % fraude pero es un solo registro.
- En la comparación entre ambos casos el fraude en el primer mes y en los meses venideros es claro observar que todos los países que anteriormente tenian mas del 80% de fraude una vez pasa el primer caen en forma proporcional y muy pronunciada con mas del 80 %.
- En cuanto a los paises unknown son solo 33 observaciones que tienen 100% de fraude lo que nos indica que en general estos datos no corresponden a VPNs/proxies fraudulento 

Estas observaciones son importantes ya que deja claro que el fraude viene más influenciado por el tiempo que por el país u otra feature como anteriormente fue descartado. Por estas razones tratar de encontrar alguna relación temporal vs otra feature anteriormente ya observada no lo recomendaria puesto que ya ser observó que las relaciones más importantes se dieron con variables temporales.

---

## **2.5 Correlaciones** 

---

### 💾 **Observaciones**

La unica correlación relevante que se observa es la negativa -0.258 entre `time_to_purchase_sec` vs `class`. Negativa porque los fraudes tienen tiempos muy cortes (segundos) y los lefítimos tienen tiempos largos(días). A más tiempo menos fraude. Con spearman probablemente veriamos algo más alto.

Por otro lado las dmeás relaciones son casi 0 lo que confirma los test estadisticos anteriores donde ninguna de estas ayuda a discriminar si existira o no fraude.

---

## **2.6 CONSLUSIONES FINALES**


1. **TARGET DESBALANCEADO**

Más del 90 % de las transacciones son legítimas y solo un ~ 9 % son fraude. Esto es un problema ya que al contruir el modelo diria que todo es legítimo. Es así que hay que escoger metricas diferentes a accuracy como AUC-PR y F1 soble la clase 1 (fraude)

2. **Relación pobre de features originales**

Gran parte de las features originales se demostró que no ayudan en gran medida a poder diferenciar si existe o no fraude.


| Feature | Cramér's V / Correlación | Veredicto |
|---|---|---|
| `purchase_value` | r = 0.001 | Descartada |
| `age` | r = 0.007 | Descartada |
| `sex` | V = 0.008 | Descartada |
| `browser` | V = 0.017 | Descartada |
| `source` | V = 0.021 | Uso marginal |


> Nota: con n=151K casi todo resulta "estadísticamente significativo".
> Lo que importa es el tamaño del efecto, no el p-value.


### 4. El país no es una buena feature (aunque parecía serlo)
Había países con tasas de fraude del 80-100%, pero al cruzarlos con el mes
de compra se vio que eso era completamente explicado por el evento de enero.
En los otros meses, esos mismos países tienen tasas normales (~4-5%).
**El país no tiene efecto propio; era un espejo del problema temporal.**


### 5. Enero 2015 fue un evento anómalo, no una regla
El 52% de todo el fraude del dataset ocurrió en enero, con una tasa del 76%.
El resto del año tuvo tasas de 4-5%.

Sin embargo, **no vamos a usar el mes como feature**. Si lo hiciéramos, el modelo
aprendería "enero = fraude", lo que no es generalizable: el próximo ataque podría
ser en julio. Lo que sí usamos son las causas del pico de enero: las features de
comportamiento (velocidad + reutilización de dispositivos), que aplican en cualquier
momento del año.


### 6. Features finales para el modelo

**Numéricas:**
`purchase_value`, `age`, `time_to_purchase_sec`, `ip_count`, `device_count`,
`users_per_ip`, `users_per_device`

**Binarias (creadas en el EDA):**
`is_ultra_fast` → 1 si la compra ocurrió ≤ 3 segundos del registro

**Categóricas (requieren encoding):**
`source`, `browser`, `sex`

**Descartadas:** fechas crudas, mes, hora, día de semana, país, IPs crudas,
device_id crudo, columnas de merge internas.



### 7. Consideraciones para el modelado

- **Split temporal, no random:** los datos son de 2015 y el fraude está concentrado
  en enero. Un split random filtraría información del futuro al pasado (data leakage).
  Hay que cortar por fecha: entrenar en los primeros meses, evaluar en los últimos.

- **Manejo del desbalance:** empezar con `class_weight='balanced'` antes de recurrir
  a SMOTE u oversampling. Es más limpio y menos propenso a introducir ruido.

- **Tipo de modelo:** dado que los predictores más fuertes tienen relaciones no lineales
  (el threshold de 3 segundos, la explosión de users_per_device), los modelos
  basados en árboles (LightGBM, XGBoost, Random Forest) deberían funcionar muy bien.

- **Métricas:** reportar AUC-ROC, AUC-PR y F1 sobre clase 1. Nunca reportar accuracy sola


---

## **3. Feature engineer**

---

Ya fueron creadas las siguientes fratures en la exploración
- `diferencia_signup_purchase_dias` la que relaciona los dias de diferencia entre que se registran y realizan la compra.
- Features temporales para purchasey signup year, month, days etc.


---

# 4. MODELADO

---

En esta primera etapa se construye un modelo base.

Para ello se aplican tres decisiones principales:

- Se utiliza un **split temporal** para evaluar la capacidad de generalización real del modelo y evitar una validación optimista causada por mezclar períodos distintos del tiempo.

- Las features históricas asociadas a IP y dispositivo se construyen únicamente a partir del conjunto de entrenamiento, evitando **data leakage** entre entrenamiento, validación y test.

- La variable `time_to_purchase_sec` se transforma a `log_time_to_purchase_sec` para reducir su fuerte asimetría y estabilizar su escala.



---

Usé un split temporal para evaluar la capacidad de generalización real del modelo y evitar una validación optimista causada por mezclar el evento anómalo de enero entre entrenamiento y prueba.
Las features históricas (ip_count, device_count, users_per_ip, users_per_device) fueron construidas usando solo información del conjunto de entrenamiento, evitando leakage entre splits.
Se reemplazó la variable cruda time_to_purchase_sec por log_time_to_purchase_sec para reducir la asimetría extrema y estabilizar su escala

---

Bajo validación temporal, el modelo presenta un desempeño cercano al azar. En particular, el evento anómalo de enero concentra una parte importante de la señal observada, pero esa estructura no se mantiene de forma estable en el resto del tiempo.

---

## **4.1 Modelo sin Mes Enero (anomalo)**

---

### ⚡**Observación**

El modelo sin el mes anomalo de enero tiene un claro desbalance entre la clase positiva y negativa. Para los fraudes no logra ser mejor que el azar como predictor. Tanto las metricas principales como el `AUC-ROC` y `AUC-PR` indica que el modelo no logra poder encontrar mayores relaciones que puedan explicar el fraude en el dataset incluso sin enero. Es así como lo visto en el EDA se confirma y en general al parecer se ha exprimido lo más que se puede de los datos.


---

## **4.2 Modelo para detectar bots**

---

### 🎓**Observaciones**

- El recall con 0.98 detecta el 98 % de los bots.
- El AUC-PR es casi perfecto.
- Existe solo un 22% de tasa de error.
- El histograma muestra que los escore en sep-dic no son 0 sino cercano a 0.2 por lo que si bien comparten caracterísitica con los bots no llegan al umbral de serlo.

---

## **4.4 CONCLUSION MODELOS**


#### **Modelo 1 split temporal**

El train tenia casi la mayor parte del fraude en enero con un 11.4% que concentraba el ataque de "bots". El modelo entendio la relación de la transacción ultra rápida + el device reutilizado = fraude. Pero al evaluar el fraude que existia en los otros meses fuese malo o casi nulo. Como el modelo buscaba "bots" y no detecto el `AUC-PR 0.0048` fue bajísimo. Esto no quiere decir que el modelo sea malo, solo quiere decir que aprendió lo que tenia que aprender y no pudo exprimir más el dataset para encontrar otras relaciones en los otros meses.

#### **Modelo 2 sin Enero (mes anomalo)**

Intentar aislar el problema quitando enero pareceria una solución lógica para observar si los patrones de fraudes durante los otros meses tienen alguna relación importante. Que pasó después de entrenar? El `AUC-PR` es claro con un 0.048 nos indica que el modelo es casi identico al azar. Sin enero, ``is_ultra_fast`` es siempre 0, ``device_count`` y ``users_per_device`` son casi siempre 1, ``ip_count`` ídem. El modelo no tiene ninguna señal porque el fraude es inditinguible de una transacción legítima con las features que hay disponibles.

#### **Modelo 3 detector de bots**

El cambio claro fue aquí donde la idea fue que el modleo entendriera el patron del ataque de bots, para eso se incluyó el 80 % de enero en train para que el modelo aprenda las transacciones elgítimas normales como lo que es un bot. El 20 % restante de enero quedó como set de validación o holdout no visto. El resultado de esto tenia que responder dos preguntas. Detecta bots cuando hay un ataque? El holdout de enero con `AUC-PR` 99% con recall 98% responde que lo hace de manera excelente. La segunda pregunta es si genera falsas alaarmas cuando no hay ataque? Las falsas alarmas son de tan solo el 22 %.


Los datos de los modelos tienen sentido según lo observado en el EDA la mayoria de las features no tenian poder preditivo real como `time_to_purchase`, `purchase_value`, `àge`, `sex`, `browser` y en especial `country` el cual demostraba que el alto riesgo venia altamente enmascarado por el mes de enero tirando una señal no genuina de fraude.



---

## **4.5 Recomendaciones y siguientes pasos**

---

1. Implementar reglas en tiempo real. Si hay un usuario que intenta comprar a los pocos segundos de registrarse o que tenga un dispositivo que ya tiene multiples usuarios registrados se debe enviar a un tipo de captchas manuales.

2. Se necesitan nuevas features que aporten valor real a los datos y se pueda entender mejor el fraude cuando es "normal" durante el año y deje de ser ruido blanco. Tipo de tarjeta, validaciones de cvv, direccion facturación y envío, antiguedad del email o metricas de la pagina como clics, segundos en distintas paginas etc.

3. Investigar que paso en Enero en profundidad. Saber si fue algo de la empresa que lanzo algo promocional o si fue mas bien algo aleatoreo.