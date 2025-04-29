import Metashape
import os
import math

# === CONFIGURAÇÕES ===
band_map = {
    "Blue": 1,
    "Green": 2,
    "Red": 3,
    "RedEdge": 4,
    "NIR": 5
}

# === INÍCIO ===
doc = Metashape.app.document
doc.clear()
chunk = doc.addChunk()

# === INPUT ===
image_folder = Metashape.app.getExistingDirectory("📂 Selecione a pasta com as imagens")
image_list = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.tif', '.jpg', '.jpeg', '.png'))]
if not image_list:
    raise Exception("❌ Nenhuma imagem encontrada na pasta!")

chunk.addPhotos(image_list)
print(f"📸 {len(chunk.cameras)} imagens carregadas.")

# === SENSOR ===
print("🔧 Configurando sensores...")
band_wavelengths = {
    "B": 475, "G": 560, "R": 668, "RE": 717, "NIR": 840
}
sensors = {}
for cam in chunk.cameras:
    if not cam.sensor.label in sensors:
        cam.sensor.wavelengths = [band_wavelengths.get(cam.label[-2:].upper(), 550)]
        sensors[cam.sensor.label] = cam.sensor
print("✅ Sensores configurados.")

# === SISTEMA DE COORDENADAS ===
print("🌍 Sistema de coordenadas: SIRGAS 2000 / UTM Zone 22S")
chunk.crs = Metashape.CoordinateSystem("EPSG::31982")

# === ALINHAMENTO ===
print("📌 Alinhando imagens...")
chunk.matchPhotos(downscale=1, generic_preselection=True, reference_preselection=True)
chunk.alignCameras()

aligned = sum([1 for cam in chunk.cameras if cam.transform])
total = len(chunk.cameras)
if aligned / total < 0.9:
    raise Exception(f"⚠️ Alinhamento ruim: apenas {aligned}/{total} câmeras alinhadas.")
print(f"✅ Alinhamento OK: {aligned}/{total} câmeras.")

# === NUVEM DE PONTOS ===
print("☁️ Gerando nuvem de pontos...")
chunk.buildPointCloud()

# === DEM ===
print("🗺️ Criando Modelo Digital de Elevação (DEM)...")
chunk.buildDem(source_data=Metashape.PointCloudData)

# === ORTOMOSAICO MULTIBANDA ===
print("🖼️ Gerando ortomosaico...")
chunk.buildOrthomosaic(surface=Metashape.ElevationData, blending=Metashape.MosaicBlending, refine_seamlines=True)

# === SAÍDA ===
output_folder = Metashape.app.getExistingDirectory("💾 Selecione a pasta de saída")
ortho_path = os.path.join(output_folder, "ortomosaico_multibanda.tif")
chunk.exportOrthomosaic(path=ortho_path, image_format=Metashape.ImageFormatTIFF, save_alpha=False)
print(f"✅ Ortomosaico exportado: {ortho_path}")

# === FUNÇÃO DE EXPORTAÇÃO DE ÍNDICES ===
def export_index(name, formula):
    tif_path = os.path.join(output_folder, f"{name}.tif")
    csv_path = os.path.join(output_folder, f"{name}.csv")

    chunk.raster_calculator(formula=formula, bands=chunk.orthomosaic, result_name=name)
    chunk.exportRaster(path=tif_path, raster=chunk.raster_layers[name], image_format=Metashape.ImageFormatTIFF)
    chunk.exportRaster(path=csv_path, raster=chunk.raster_layers[name], format=Metashape.RasterFormatCSV)
    print(f"✅ {name} exportado.")

# === ÍNDICES VEGETATIVOS ===
print("🧪 Gerando índices vegetativos...")

export_index("NDVI",   f"(b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['Red']})")
export_index("GNDVI",  f"(b{band_map['NIR']} - b{band_map['Green']}) / (b{band_map['NIR']} + b{band_map['Green']})")
export_index("NDRE",   f"(b{band_map['NIR']} - b{band_map['RedEdge']}) / (b{band_map['NIR']} + b{band_map['RedEdge']})")
export_index("RENDVI", f"(b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['RedEdge']})")
export_index("SAVI",   f"1.5 * (b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['Red']} + 0.5)")
export_index("MSAVI",  f"(2 * b{band_map['NIR']} + 1 - sqrt((2 * b{band_map['NIR']} + 1)^2 - 8 * (b{band_map['NIR']} - b{band_map['Red']}))) / 2")

# === CLASSIFICAÇÃO DE NDVI ===
print("📊 Classificando NDVI em níveis de degradação...")

class_formula = (
    f"(b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['Red']}) < 0.2 ? 1 : "
    f"(b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['Red']}) < 0.4 ? 2 : "
    f"(b{band_map['NIR']} - b{band_map['Red']}) / (b{band_map['NIR']} + b{band_map['Red']}) < 0.6 ? 3 : 4"
)

export_index("NDVI_Classificado", class_formula)

# === SALVAR PROJETO ===
project_path = Metashape.app.getSaveFileName("💾 Salvar projeto como:")
doc.save(project_path)
print("🎉 Projeto completo e salvo com sucesso!")
