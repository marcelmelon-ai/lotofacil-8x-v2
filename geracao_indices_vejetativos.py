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

# === FUNÇÃO PARA CALCULAR E EXPORTAR ÍNDICE ===
def export_index(name, formula):
    tif_path = os.path.join(output_folder, f"{name}.tif")
    csv_path = os.path.join(output_folder, f"{name}.csv")

    chunk.raster_calculator(formula=formula, bands=chunk.orthomosaic, result_name=name)
    chunk.exportRaster(path=tif_path, raster=chunk.raster_layers[name], image_format=Metashape.ImageFormatTIFF)
    chunk.exportRaster(path=csv_path, raster=chunk.raster_layers[name], format=Metashape.RasterFormatCSV)

    print(f"✅ {name} exportado com sucesso!")

# === GERAR ÍNDICES ===
print("🧪 Gerando índices vegetativos...")

export_index("NDVI",   f"(b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['Red']})")
export_index("GNDVI",  f"(b{band_map['NIR']} - b{band_map['Green']}) / (b{band_map['NIR']} + b{band_map['Green']})")
export_index("NDRE",   f"(b{band_map['NIR']} - b{band_map['RedEdge']}) / (b{band_map['NIR']} + b{band_map['RedEdge']})")
export_index("RENDVI", f"(b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['RedEdge']})")
export_index("SAVI",   f"1.5 * (b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['Red']} + 0.5)")
export_index("MSAVI",  f"(2 * b{band_map['NIR']} + 1 - sqrt((2 * b{band_map['NIR']} + 1)^2 - 8 * (b{band_map['NIR']} - b{band_map['Red']}))) / 2")

# === CLASSIFICAR NDVI EM 3 NÍVEIS ===
print("📊 Classificando NDVI...")

class_formula = (
    f"(b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['Red']}) < 0.2 ? 1 : "
    f"(b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['Red']}) < 0.5 ? 2 : 3"
)

export_index("NDVI_Classificado", class_formula)

# === SALVAR PROJETO ===
project_path = Metashape.app.getSaveFileName("Salvar projeto como:")
doc.save(project_path)
print("💾 Projeto salvo com sucesso.")
