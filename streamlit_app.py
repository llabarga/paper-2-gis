import streamlit as st
from pathlib import Path
import subprocess
import zipfile

st.title("Paper2GIS demo")
st.write("Sube una imagen y conviértela en shapefile")

# Subida de imágenes
reference = st.file_uploader("Sube la imagen de referencia", type=["jpg", "png"])
target = st.file_uploader("Sube la imagen objetivo", type=["jpg", "png"])

# Nombre del archivo de salida
output_name = st.text_input("Nombre del shapefile de salida", value="resultado.shp")

if reference and target:
    st.image(reference, caption="Referencia")
    st.image(target, caption="Objetivo")
    st.success("Imágenes recibidas 🚀")

    # Guardar temporalmente
    ref_path = Path("reference.jpg")
    tgt_path = Path("target.jpg")
    with open(ref_path, "wb") as f:
        f.write(reference.getbuffer())
    with open(tgt_path, "wb") as f:
        f.write(target.getbuffer())

    # Definir archivo de salida
    out_shp = Path(output_name)

    # Ejecutar Paper2GIS extract
    cmd = [
        "python", "-m", "paper2gis.p2g", "extract",
        "--reference", str(ref_path),
        "--target", str(tgt_path),
        "-o", str(out_shp)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0 and out_shp.exists():
        # Crear zip con todos los archivos del shapefile
        shp_files = [out_shp.with_suffix(ext) for ext in [".shp",".shx",".dbf",".prj"]]
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
