# Academic-Performance-DS

Proyecto de Data Science para analizar el rendimiento académico.

## Estructura

```text
academic-performance/
├── data/
│   ├── raw/          # Datos originales, sin modificaciones
│   └── processed/    # Datos limpios y transformados
├── notebooks/        # Exploracion y analisis reproducible
├── output/           # Graficos, tablas y resultados exportados
├── src/              # Codigo reutilizable del proyecto
├── .gitignore
├── requirements.txt
└── README.md
```

## Reproduccion

1. Crear y activar un entorno virtual:

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

3. Abrir Jupyter Lab:

   ```bash
   jupyter lab
   ```

4. Ejecutar los notebooks en orden. Guardar los datos originales en `data/raw/`, los datos transformados en `data/processed/` y los resultados en `output/`.

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

No se versionan entornos virtuales, caches ni archivos de datos o resultados generados. Los archivos de datos reales deben compartirse por el canal indicado por la catedra si no corresponde almacenarlos en Git.
