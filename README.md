# Academic-Performance-DS

Proyecto de Data Science para analizar el rendimiento académico.

## Estructura

```text
academic-performance/
├── data/
│   ├── raw/          # Datos originales, sin modificaciones
│   └── processed/    # Datos limpios y transformados
├── notebooks/        # Notebook unico de exploracion y transformacion
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

4. Ejecutar `notebooks/fase1_gaming_rendimiento.ipynb` desde la carpeta `notebooks/`. El notebook lee el original desde `data/raw/`, escribe el dataset limpio en `data/processed/` y la bitacora en `output/`.

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

No se versionan entornos virtuales, caches ni archivos del sistema. Los archivos de `data/raw/`, `data/processed/` y las salidas CSV se versionan para reproducir la entrega.
