import streamlit as st
import subprocess
from pathlib import Path
import zipfile

st.title("Paper2GIS demo")
st.write("Sube una imagen y conviértela en shapefile")

# Subida de imagen
uploaded = st.file_uploader("Sube una foto", type=["jpg", "png"])
reference = st.file_uploader("Sube la imagen de referencia", type=["jpg", "png"])

if uploaded and reference:
    st.image([reference, uploaded], caption=["Referencia", "Objetivo"])
    st.success("Imágenes recibidas 🚀")

    # Guardar imágenes temporalmente
    ref_path = Path("reference.jpg")
    tgt_path = Path("target.jpg")
    with open(ref_path, "wb") as f:
        f.write(reference.getbuffer())
    with open(tgt_path, "wb") as f:
        f.write(uploaded.getbuffer())

    # Archivo de salida
    out_base = Path("output")
    out_shp = out_base.with_suffix(".shp")

    # Ejecutar Paper2GIS usando p2g.py
    cmd = [
        "python", "p2g.py", "extract",
        "--reference", str(ref_path),
        "--target", str(tgt_path),
        "-o", str(out_shp)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0 and out_shp.exists():
        # Crear ZIP con los archivos del shapefile
        shp_files = [out_base.with_suffix(ext) for ext in [".shp", ".shx", ".dbf", ".prj"]]
        zip_path = Path("shapefile.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for f in shp_files:
                if f.exists():
                    zipf.write(f, arcname=f.name)

        st.success("Shapefile generado correctamente!")
        st.download_button(
            "Descargar shapefile (.zip)",
            zip_path.read_bytes(),
            file_name="resultado_shapefile.zip"
        )
    else:
        st.error("Error al ejecutar Paper2GIS")
        st.text(result.stderr)
else:
    st.info("Por favor, sube tanto la imagen de referencia como la imagen objetivo.")
