# Academic-Performance-DS

Proyecto de Data Science para analizar el rendimiento académico.

## Estructura del proyecto

```text
academic-performance/
├── data/
│   ├── raw/          # Dataset original, sin modificaciones
│   └── processed/    # Datasets limpios y transformados
├── notebooks/        # Notebooks de carga, limpieza y analisis
├── output/           # Informes, graficos, tablas y bitacoras
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

### `output/`

Contiene resultados generados por los notebooks, por ejemplo:

- `bitacora_limpieza.csv`: registro de las decisiones de limpieza.
- `fase2_gaming_rendimiento.html`: exportación HTML del notebook de Fase 2.
- `fase2_tabla_resumen_contrastes.csv`: tabla reproducible de contrastes.
- `fase2_posthoc_C2.csv`: comparaciones post hoc del contraste C2.
- `fase2_intervalos_bootstrap.csv`: intervalos bootstrap y comparación con IC clásicos.
- Gráficos y tablas exportadas.
- Informes de entrega en `.pdf`, `.doc` o `.docx`.

Los archivos guardados aquí son entregables o resultados, no datos originales.

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

5. Abrir `fase1_gaming_rendimiento.ipynb` y elegir **Restart & Run All**. El notebook lee `../data/raw/Gaming_Academic_Performance_updated.csv`, genera `../data/processed/gaming_academic_clean.csv` y escribe `../output/bitacora_limpieza.csv`.

El resultado esperado es un dataset limpio de `8000 x 15` y una bitácora de limpieza con `52 x 8`.

### Reproducción de la Fase 2

Abrir `notebooks/fase2_gaming_rendimiento.ipynb` y elegir **Restart & Run All**.
El notebook lee `data/processed/gaming_academic_clean.csv`, ejecuta los contrastes
unificados, diagnósticos de supuestos, corrección BH, análisis de sensibilidad y
bootstrap, y guarda las exportaciones directamente en `output/`. También puede
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

Al finalizar deben existir o actualizarse `data/processed/gaming_academic_clean.csv` y `output/bitacora_limpieza.csv`.

## Versionado y entrega

El repositorio se comparte con la catedra mediante GitHub:

```bash
git init
git add .
git commit -m "Inicializa estructura del proyecto"
git branch -M main
git remote add origin https://github.com/jose-zaavedra/Academic-Performance-DS.git
git push -u origin main
```

No se versionan entornos virtuales, caches ni archivos del sistema. Los archivos de `data/raw/`, `data/processed/` y las salidas CSV, PDF y Word se versionan para reproducir y entregar el proyecto.
