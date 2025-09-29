import streamlit as st
from pathlib import Path
import zipfile

# Importar funciones directamente desde tu paquete
from paper2gis.paper2gis import run_extract

st.title("Paper2GIS Demo")
st.write("Sube una imagen y conviértela en shapefile")

# Subida de archivo
uploaded = st.file_uploader("Sube una foto", type=["jpg", "png"])

if uploaded:
    st.image(uploaded, caption="Imagen subida")
    st.success("Imagen recibida 🚀")

    # Guardar temporalmente la foto
    tgt_path = Path("target.jpg")
    with open(tgt_path, "wb") as f:
        f.write(uploaded.getbuffer())

    # Definir archivos de salida
    out_shp_base = Path("resultado")
    out_shp = out_shp_base.with_suffix(".shp")

    # Aquí llamamos directamente a run_extract del paquete
    # Se pueden dejar parámetros opcionales con valores por defecto
    try:
        # Necesitas pasar también la referencia; aquí puedes poner un ejemplo
        reference_image = Path("reference.png")  # <- Cambia a tu referencia
        run_extract(
            reference=str(reference_image),
            target=str(tgt_path),
            output=str(out_shp),
            lowe_distance=0.5,
            threshold=100,
            kernel=0,
            homo_matches=12,
            frame=0,
            min_area=1000,
            min_ratio=0.2,
            buffer=10,
            convex_hull=False,
            centroid=False,
            representative_point=False,
            exterior=False,
            interior=False,
            demo=False
        )

        # Crear zip con todos los archivos del shapefile
        shp_files = [out_shp_base.with_suffix(ext) for ext in [".shp", ".shx", ".dbf", ".prj"]]
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

    except Exception as e:
        st.error(f"Error al ejecutar Paper2GIS: {e}")
