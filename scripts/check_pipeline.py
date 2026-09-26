"""Check the actual Hito 4 model cell on synthetic data, without AWS."""
import json
import tempfile
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

root = Path(__file__).resolve().parents[1]
notebook = json.loads((root / 'notebooks/04_entrenamiento_sagemaker_s3.ipynb').read_text())
source = next(''.join(c['source']) for c in notebook['cells']
              if c['cell_type'] == 'code' and 'model = Pipeline(' in ''.join(c['source']))
X_train = pd.DataFrame({'PrecioAnterior': [0, 100, 200, 300],
                        'metros': [30, 50, 70, 90],
                        'habitaciones': [1, 2, np.nan, 3],
                        'baños': [1, 1, 2, 2]})
y_train = pd.Series([100, 200, 300, 400])
scope = {'X_train': X_train, 'y_train': y_train}
exec(compile(source, 'Hito4-model-cell', 'exec'), scope)
model = scope['model']
assert model.named_steps['imputer'].statistics_[2] == 2.0
X_test = pd.DataFrame({'PrecioAnterior': [0, 400], 'metros': [40, 100],
                       'habitaciones': [np.nan, 1000], 'baños': [1, 3]})
pred = model.predict(X_test)
assert np.isfinite(pred).all()
assert model.named_steps['imputer'].statistics_[2] == 2.0
with tempfile.TemporaryDirectory() as temp:
    path = Path(temp) / 'pipeline.joblib'
    joblib.dump(model, path)
    np.testing.assert_allclose(joblib.load(path).predict(X_test), pred)
print('PASS: train-only imputation, missing-value inference and pipeline round-trip')
