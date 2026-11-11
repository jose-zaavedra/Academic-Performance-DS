# Academic-Performance-DS

Proyecto de Data Science para analizar el rendimiento académico.

## Estructura del proyecto

```text
academic-performance/
├── data/
│   ├── raw/          # Dataset original, sin modificaciones
│   └── processed/    # Datasets limpios y transformados
├── notebooks/        # Notebooks de carga, limpieza y analisis
├── output/
│   ├── fase1/        # Resultados e informe de la Fase 1
│   ├── fase2/        # Resultados e informe de la Fase 2
│   ├── fase3/        # Resultados, informe y presentacion de la Fase 3
│   ├── integrador/   # Informe integrador de las tres fases
│   └── entrega_final/ # ZIP final de entrega
├── docs/             # Guia y enlace del repositorio
├── src/              # Codigo Python reutilizable
├── .gitignore
├── requirements.txt
└── README.md
```

### `data/raw/`

Contiene los archivos de entrada originales. El dataset base es:

```text
Gaming_Academic_Performance_updated.csv
```

Estos archivos no deben editarse manualmente ni reemplazarse por versiones limpiadas. Se pueden almacenar CSV, Excel, PDF u otros formatos de fuente.

### `data/processed/`

Contiene archivos derivados de los datos originales mediante código reproducible. El archivo principal generado por la Fase 1 es:

```text
gaming_academic_clean.csv
```

Aquí se guardan datasets limpios o transformados. No se deben colocar datos originales en esta carpeta.

### `notebooks/`

Contiene los notebooks Jupyter del proyecto. El notebook principal es:

```text
fase1_gaming_rendimiento.ipynb
```

La Fase 2 se encuentra en un notebook independiente:

```text
fase2_gaming_rendimiento.ipynb
```

Ambos notebooks detectan la raíz del repositorio y pueden ejecutarse desde la raíz
o desde una sesión de Jupyter abierta en `notebooks/`. La Fase 1 utiliza el dataset
original `data/raw/Gaming_Academic_Performance_updated.csv` para producir el dataset
limpio; la Fase 2 utiliza `data/processed/gaming_academic_clean.csv` sin volver a
limpiarlo.

La Fase 3 se encuentra en `notebooks/fase3_modelado_rendimiento.ipynb`. Compara
una línea base y tres familias de regresión para predecir `grades` con cinco
predictores definidos a priori. Genera el HTML ejecutado, tablas de resultados y
el modelo ganador en `output/fase3/`. El script `src/infer_fase3.py` permite aplicar el
modelo guardado a un CSV nuevo:

```powershell
.\.venv\Scripts\python.exe src\infer_fase3.py datos_nuevos.csv output\fase3\predicciones.csv
```

La selección de predictores se documenta y compara en
`output/fase3_comparacion_predictores.csv`. Se evalúan, sin usar el conjunto de
prueba, la combinación heredada de Fase 2 con `uso_no_gaming`, la alternativa
inicial de Fase 3 con `social_activity` y una combinación con ambos predictores.
La rama revisada conserva `uso_no_gaming` porque obtuvo el menor RMSE promedio de
validación cruzada; la diferencia fue pequeña y no se interpreta como causalidad.

### `output/`

Los resultados están separados por fase para facilitar la revisión y la entrega:

- `fase1/`: bitácora de limpieza e informe de la Fase 1.
- `fase2/`: HTML, tablas estadísticas e informe de la Fase 2.
- `fase3/`: HTML, modelo, métricas, diagnóstico, informe y presentación de la Fase 3.
- `integrador/`: informe integrador de las tres fases.
- `entrega_final/`: único ZIP vigente con los archivos principales de entrega.

Los archivos guardados aquí son resultados reproducibles o entregables, no datos originales.

### `src/`

Contiene funciones y módulos Python reutilizables. Actualmente incluye la inicialización del paquete; el código de análisis puede trasladarse aquí en fases posteriores.

### Archivos de configuración

- `.gitignore`: excluye entornos virtuales, caches y archivos del sistema. Permite versionar los datos y los entregables definidos para este proyecto.
- `requirements.txt`: lista las dependencias Python.
- `README.md`: documenta la organización y reproducción del proyecto.

## Reproducción

### Compatibilidad

- Python mínimo recomendado: **3.9**.
- Probado de extremo a extremo en Python **3.13** sobre Windows.
- El procedimiento usa herramientas multiplataforma: `venv`, `pip` y Jupyter.
- No se garantiza compatibilidad con Python 3.8 o anteriores porque las versiones actuales de pandas, numpy y matplotlib requieren Python más reciente.

1. Desde la raíz del repositorio, crear y activar un entorno virtual:

   En Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   En macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instalar las dependencias:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Entrar en la carpeta de notebooks. Es necesario hacerlo porque el notebook usa rutas relativas como `../data/raw/`:

   En Windows PowerShell:

   ```powershell
   Set-Location notebooks
   ```

   En macOS/Linux:

   ```bash
   cd notebooks
   ```

4. Abrir Jupyter Lab:

   ```bash
   jupyter lab
   ```

5. Abrir `fase1_gaming_rendimiento.ipynb` y elegir **Restart & Run All**. El notebook lee `../data/raw/Gaming_Academic_Performance_updated.csv`, genera `../data/processed/gaming_academic_clean.csv` y escribe `../output/fase1/bitacora_limpieza.csv`.

El resultado esperado es un dataset limpio de `8000 x 15` y una bitácora de limpieza con `52 x 8`.

### Reproducción de la Fase 2

Abrir `notebooks/fase2_gaming_rendimiento.ipynb` y elegir **Restart & Run All**.
El notebook lee `data/processed/gaming_academic_clean.csv`, ejecuta los contrastes
unificados, diagnósticos de supuestos, corrección BH, análisis de sensibilidad y
bootstrap, y guarda las exportaciones directamente en `output/fase2/`. También puede
ejecutarse automáticamente desde la raíz:

En Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 notebooks\fase2_gaming_rendimiento.ipynb
.\.venv\Scripts\python.exe -m jupyter nbconvert --to html --output-dir output notebooks\fase2_gaming_rendimiento.ipynb
```

En macOS/Linux:

```bash
./.venv/bin/python -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 notebooks/fase2_gaming_rendimiento.ipynb
./.venv/bin/python -m jupyter nbconvert --to html --output-dir output notebooks/fase2_gaming_rendimiento.ipynb
```

La instalación conserva las dependencias existentes y agrega `scipy`, `statsmodels`
y `patsy`, requeridas por los contrastes y modelos de la Fase 2.

### Reproducción de la Fase 3

La Fase 3 utiliza `data/processed/gaming_academic_clean.csv` para predecir la
variable `grades`. El notebook compara `DummyRegressor`, regresión lineal,
Random Forest y KNN mediante validación cruzada de cinco particiones. La semilla
de reproducibilidad es `42`, la división es de 80 % para entrenamiento y 20 %
para prueba, y el conjunto de prueba se mantiene separado durante la selección
y el ajuste.

Para ejecutar el notebook completo desde la raíz del repositorio:

En Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 notebooks\fase3_modelado_rendimiento.ipynb
.\.venv\Scripts\python.exe -m jupyter nbconvert --to html --output-dir output\fase3 notebooks\fase3_modelado_rendimiento.ipynb
```

En macOS/Linux:

```bash
./.venv/bin/python -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 notebooks/fase3_modelado_rendimiento.ipynb
./.venv/bin/python -m jupyter nbconvert --to html --output-dir output/fase3 notebooks/fase3_modelado_rendimiento.ipynb
```

El notebook genera en `output/fase3/` las métricas de prueba, la comparación de
predictores, el diagnóstico de residuos, la importancia de variables, el HTML
ejecutado y el modelo ganador `fase3_modelo_ganador.joblib`. El módulo
`src/fase3_model.py` contiene la lógica reutilizable del entrenamiento.

Para aplicar el modelo a un archivo CSV nuevo, el archivo debe incluir las cinco
columnas predictoras finales: `gaming_hours`, `study_hours`, `sleep_hours`,
`attendance` y `uso_no_gaming`. El comando es:

```powershell
.\.venv\Scripts\python.exe src\infer_fase3.py datos_nuevos.csv output\fase3\predicciones.csv
```

El script conserva las columnas originales y agrega `grades_predicted`. También
se puede indicar otro archivo de modelo con `--model`.

### Ejecución automática sin abrir Jupyter

Desde la raíz del repositorio:

En Windows PowerShell:

```powershell
Set-Location notebooks
..\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=180 fase1_gaming_rendimiento.ipynb
```

En macOS/Linux:

```bash
cd notebooks
../.venv/bin/python -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=180 fase1_gaming_rendimiento.ipynb
```

Al finalizar deben existir o actualizarse `data/processed/gaming_academic_clean.csv` y `output/fase1/bitacora_limpieza.csv`.

## Entregables finales

La guía de la cátedra solicita un informe de Fase 3 de hasta 15 páginas, el
notebook ejecutado con su HTML, el modelo serializado, el script de inferencia,
el informe integrador de hasta 30 páginas y un repositorio ordenado. Estos
materiales se encuentran en `output/fase3/`, `output/integrador/` y
`output/entrega_final/`.

El enlace oficial del repositorio está en `docs/GitHub.txt`.

No se versionan entornos virtuales, caches ni archivos del sistema. Los datos
originales, procesados, resultados y documentos necesarios para reproducir o
entregar el proyecto sí se conservan en sus carpetas correspondientes.
