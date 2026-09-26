# Cómo consultar y ejecutar el proyecto

## Entorno

Las entregas se hicieron en entornos de notebooks (Colab y SageMaker). No se conservó un lockfile de sus dependencias. Los archivos de requisitos enumeran las librerías necesarias; no constituyen una reproducción exacta del entorno original.

Desde la raíz del repositorio, crea un entorno aislado con Python:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m jupyter lab
```

Abre cada notebook dentro de `notebooks/` y ejecuta sus celdas en orden. Las rutas locales son relativas a esa carpeta. Necesitas los datos descritos en [data/README.md](../data/README.md).

## Hitos 1 y 2

Para el Hito 2 instala además:

```bash
python -m pip install tensorflow
```

El Hito 1 realiza exploración; el 2 incluye varios entrenamientos con Random Forest de 300 árboles y redes neuronales. Las transformaciones a arrays densos pueden requerir bastante memoria.

## Hito 3

```bash
python -m pip install -r requirements-nlp.txt
```

El notebook descarga stopwords de NLTK y el modelo público `dccuchile/bert-base-spanish-wwm-cased` de Hugging Face. Necesita conexión; una GPU facilita el entrenamiento de BERT. No se ha vuelto a ejecutar el fine-tuning al preparar esta publicación. La compatibilidad del entorno completo y la repetición de métricas están pendientes.

## Hito 4

```bash
python -m pip install -r requirements-aws.txt
```

Configura estas variables de entorno antes de abrir el notebook, usando tus propios recursos:

| Variable | Función |
|---|---|
| `PROJECT_S3_BUCKET` | Nombre de tu bucket, obligatorio |
| `PROJECT_S3_DATA_KEY` | Clave del CSV; por defecto `raw/Datos.csv` |
| `PROJECT_S3_MODEL_KEY` | Clave de destino; por defecto `model/linear_pipeline.joblib` |
| `PROJECT_UPLOAD_MODEL` | Solo `1` activa la subida del pipeline |

El rol o perfil de AWS debe permitir leer el objeto de datos. Para subir y comprobar el artefacto necesitará también escritura y lectura sobre su clave de destino. Se usa la cadena estándar de credenciales de AWS; no se incluyen claves en el código. La subida puede reemplazar un objeto existente en esa clave, por lo que debes elegir una clave propia.

El Hito 4 puede ejecutarse en un notebook de SageMaker o en un entorno Python con acceso autorizado a S3. No crea infraestructura automáticamente. Si decides usar servicios AWS, comprueba sus costes y detén los recursos cuando termines.

## Validación del repositorio

```bash
python -m pip install nbformat scikit-learn pandas
python scripts/validate_notebooks.py
python scripts/check_pipeline.py
```

La primera comprobación valida formato, sintaxis y ausencia de salidas prohibidas. La segunda usa datos sintéticos para verificar que la imputación del Hito 4 se ajusta solo sobre entrenamiento y que el pipeline serializado conserva sus predicciones. Ninguna vuelve a medir los resultados académicos ni realiza llamadas a AWS.
