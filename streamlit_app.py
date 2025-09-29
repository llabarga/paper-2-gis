import streamlit as st
import subprocess
from pathlib import Path
import zipfile

st.title("Paper2GIS demo")
st.write("Sube una imagen y conviértela en shapefile")

uploaded = st.file_uploader("Sube una foto", type=["jpg", "png"])

# Coordenadas manuales (en lugar de QR)
ref_x = st.number_input("Coordenada X de referencia", value=0.0, format="%.6f")
ref_y = st.number_input("Coordenada Y de referencia", value=0.0, format="%.6f")

if uploaded:
    st.image(uploaded)
    st.success("Imagen recibida 🚀")

    # Guardar temporalmente la foto
    tgt_path = Path("target.jpg")
    with open(tgt_path, "wb") as f:
        f.write(uploaded.getbuffer())

    # Supongamos que tienes una imagen de referencia "reference.png" ya preparada
    ref_path = Path("reference.png")

    # Definir archivos de salida
    out_shp = Path("output.shp")

    # Ejecutar p2g.py extract desde el paquete
    cmd = [
        "python", "p2g.py", "extract",
        "--reference", str(ref_path),
        "--target", str(tgt_path),
        "-o", str(out_shp),
        "--demo", "True"  # ejemplo, puedes eliminar o cambiar según tus necesidades
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0 and out_shp.exists():
        # Crear zip con todos los archivos del shapefile
        shp_files = [out_shp.with_suffix(ext) for ext in [".shp", ".shx", ".dbf", ".prj"]]
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
