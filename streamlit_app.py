import streamlit as st
from pathlib import Path
import zipfile
from paper2gis.paper2gis import run_extract  # tu fork con el paquete Paper2GIS

st.title("Paper2GIS demo simplificada")
st.write("Sube una foto y un layout de referencia para extraer el marcado")

# Subida de archivos
reference = st.file_uploader("Sube la imagen de referencia (layout Paper2GIS)", type=["png", "jpg"])
target = st.file_uploader("Sube la foto a procesar", type=["png", "jpg"])

# Coordenadas manuales (opcional)
manual_coords = st.checkbox("Usar coordenadas manuales en vez de QR")
if manual_coords:
    bl_x = st.number_input("Bottom-left X", value=0.0)
    bl_y = st.number_input("Bottom-left Y", value=0.0)
    tr_x = st.number_input("Top-right X", value=1000.0)
    tr_y = st.number_input("Top-right Y", value=1000.0)

if reference and target:
    st.image(target, caption="Foto subida")
    st.image(reference, caption="Referencia subida")

    # Guardar temporalmente
    ref_path = Path("reference.png")
    tgt_path = Path("target.png")
    with open(ref_path, "wb") as f:
        f.write(reference.getbuffer())
    with open(tgt_path, "wb") as f:
        f.write(target.getbuffer())

    # Archivo de salida
    out_shp = Path("output.shp")

    # Llamar a Paper2GIS extract
    if st.button("Procesar imagen"):
        # Puedes ajustar parámetros si quieres, aquí usamos valores por defecto
        run_extract(
            reference=str(ref_path),
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

        # Crear ZIP con shapefile
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
