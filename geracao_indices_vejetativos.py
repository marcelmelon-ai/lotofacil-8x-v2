import Metashape
import os

# === MAPA DE BANDAS ===
band_map = {
    "Blue": 1,
    "Green": 2,
    "Red": 3,
    "RedEdge": 4,
    "NIR": 5
}

# === PROJETO ATUAL ===
doc = Metashape.app.document
chunk = doc.chunk

# === SELECIONAR PASTA DE SAÍDA ===
output_folder = Metashape.app.getExistingDirectory("Selecione a pasta para salvar os índices")

# === FUNÇÃO PARA CRIAR E EXPORTAR ÍNDICE ===
def create_index(name, expression):
    raster_transform = Metashape.RasterTransform()
    raster_transform.expression = expression

    tif_path = os.path.join(output_folder, f"{name}.tif")
    csv_path = os.path.join(output_folder, f"{name}.csv")

    chunk.exportRaster(transform=raster_transform, path=tif_path, image_format=Metashape.ImageFormatTIFF)
    chunk.exportRaster(transform=raster_transform, path=csv_path, format=Metashape.RasterFormatCSV)

    print(f"✅ {name} exportado: .tif e .csv")

# === GERAR ÍNDICES ===
print("🧪 Gerando índices vegetativos...")

create_index("NDVI",     f"(B{band_map['NIR']} - B{band_map['Red']}) / (B{band_map['NIR']} + B{band_map['Red']})")
create_index("GNDVI",    f"(B{band_map['NIR']} - B{band_map['Green']}) / (B{band_map['NIR']} + B{band_map['Green']})")
create_index("NDRE",     f"(B{band_map['NIR']} - B{band_map['RedEdge']}) / (B{band_map['NIR']} + B{band_map['RedEdge']})")
create_index("RENDVI",   f"(B{band_map['NIR']} - B{band_map['Red']}) / (B{band_map['NIR']} + B{band_map['RedEdge']})")
create_index("SAVI",     f"1.5 * (B{band_map['NIR']} - B{band_map['Red']}) / (B{band_map['NIR']} + B{band_map['Red']} + 0.5)")
create_index("MSAVI",    f"(2 * B{band_map['NIR']} + 1 - sqrt((2 * B{band_map['NIR']} + 1)^2 - 8 * (B{band_map['NIR']} - B{band_map['Red']}))) / 2")

# === CLASSIFICAÇÃO DE NDVI ===
print("📊 Classificando NDVI...")

classification_expr = (
    f"(B{band_map['NIR']} - B{band_map['Red']}) / (B{band_map['NIR']} + B{band_map['Red']}) < 0.2 ? 1 : "
    f"(B{band_map['NIR']} - B{band_map['Red']}) / (B{band_map['NIR']} + B{band_map['Red']}) < 0.5 ? 2 : 3"
)

raster_transform = Metashape.RasterTransform()
raster_transform.expression = classification_expr

tif_class = os.path.join(output_folder, "NDVI_Classificado.tif")
csv_class = os.path.join(output_folder, "NDVI_Classificado.csv")

chunk.exportRaster(transform=raster_transform, path=tif_class, image_format=Metashape.ImageFormatTIFF)
chunk.exportRaster(transform=raster_transform, path=csv_class, format=Metashape.RasterFormatCSV)

print("🎯 Classificação NDVI exportada com sucesso: .tif e .csv")

# === SALVAR PROJETO ===
project_path = Metashape.app.getSaveFileName("Salvar projeto como:")
doc.save(project_path)
print("💾 Projeto salvo com sucesso.")