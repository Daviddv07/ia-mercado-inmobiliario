# Resultados y límites de interpretación

Todos los valores siguientes proceden de las salidas guardadas en las entregas originales, revisadas al preparar el portfolio. No se han reejecutado los entrenamientos ni se han descargado los datasets.

## Hito 2 · Alquileres

Partición aleatoria 80/20, `random_state=42`: 7.383 filas de entrenamiento y 1.846 de prueba. La tabla principal del README corresponde a `price` en euros.

Ridge sobre `log1p(price)` obtuvo RMSE 0,243954 y R² 0,820498. La red neuronal posterior también utiliza la variable objetivo en escala logarítmica: RMSE 0,368257 y R² 0,590968. Sus errores no se pueden comparar directamente con los errores en euros de la tabla principal.

En la clasificación de balcón, la clase positiva representa alrededor del 17,9 %:

| Modelo | Accuracy | F1 positivo | ROC AUC |
|---|---:|---:|---:|
| Regresión logística | 0,8310 | 0,2315 | 0,7151 |
| Random Forest | 0,8375 | 0,2308 | 0,7417 |
| Gradient Boosting | 0,8261 | 0,1253 | 0,7047 |
| Red neuronal | 0,7432 | 0,3629 | 0,6933 |

La selección depende de la métrica; la accuracy por sí sola oculta el bajo rendimiento sobre la clase minoritaria.

Limitaciones: no hay evaluación temporal, geográfica o por inmueble independiente, ni una auditoría completa de duplicados. La comparación de varios modelos sobre el mismo test permite una selección exploratoria, pero hace aconsejable una validación separada y un test final nuevo. La conversión a matrices densas en Keras aumenta el uso de memoria. `location` es una variable de cardinalidad alta que requiere revisión.

## Hito 3 · Texto de anuncios de venta

11.826 filas; partición aleatoria 80/20. Se utilizan `titulo` y `tags`, no el cuerpo de `descripcion`.

| Experimento | MAE de test (€) |
|---|---:|
| TF-IDF + Ridge | 441.369,80 |
| Word2Vec + CNN | 776.813,18 |
| BERT en español | 1.034.972,31 |

TF-IDF + Ridge se ajusta con GridSearchCV de tres particiones sobre entrenamiento; MAE de validación cruzada 439.611,59 €. BERT se entrena durante dos épocas. Estos experimentos no son comparables con los alquileres ni acreditan una tasación fiable.

Aspectos pendientes: incorporar un predictor baseline (por ejemplo, mediana), estudiar outliers, evitar que textos nulos se conviertan en la cadena `nan`, revisar duplicados y separar validación y test en las redes. El separador original `_toggle_` y la limpieza que elimina números se conservan para no alterar silenciosamente la lógica del experimento; convendría reevaluarlos. La CNN ajusta vocabulario y Word2Vec antes de extraer su validación interna, por lo que esa validación no es completamente independiente del preprocesamiento.

## Hito 4 · Variables numéricas y AWS

La versión académica de regresión lineal obtuvo:

- MAE: 651.473,21 €.
- RMSE: 1.049.873,62 €.
- R²: 0,293334.

Se ejecutó en un notebook de SageMaker, leyó un CSV de S3 y guardó el modelo mediante boto3. No crea un training job gestionado ni un endpoint.

**La imputación original utilizaba la media del dataset completo antes del split.** En la versión publicada se ha trasladado a un pipeline ajustado solo sobre entrenamiento y se guarda ese pipeline completo. Sus salidas se han limpiado y los resultados de esta versión corregida están pendientes de recalcular. Las cifras anteriores se conservan únicamente como referencia histórica de la entrega.

También debe comprobarse si `PrecioAnterior` estará disponible en el escenario de inferencia deseado; de lo contrario habría que excluirlo y reevaluar.
