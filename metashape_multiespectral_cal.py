import Metashape
import os

# === CONFIGURAÇÕES INICIAIS ===

band_wavelengths = {
    "B": 475, "G": 560, "R": 668, "RE": 717, "NIR": 840
}

# === INÍCIO DO PROCESSAMENTO ===

doc = Metashape.app.document
doc.clear()
chunk = doc.addChunk()

# Seleção da pasta com imagens
image_folder = Metashape.app.getExistingDirectory("Selecione a pasta com as imagens")
image_list = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.tif', '.jpg', '.jpeg', '.png'))]
if not image_list:
    raise Exception("Nenhuma imagem encontrada!")

chunk.addPhotos(image_list)
print(f"📸 {len(chunk.cameras)} imagens carregadas.")

# === CONFIGURAR SENSORES AUTOMATICAMENTE ===
print("🔧 Configurando sensores...")

sensors = {}
for cam in chunk.cameras:
    if not cam.sensor.label in sensors:
        cam.sensor.wavelengths = [band_wavelengths.get(cam.label[-2:].upper(), 550)]  # default: 550nm
        sensors[cam.sensor.label] = cam.sensor

print("✅ Sensores configurados.")

# === DEFINIR SISTEMA DE REFERÊNCIA ===
print("🌍 Corrigindo sistema de coordenadas para SIRGAS 2000 / UTM Zone 22S...")
chunk.crs = Metashape.CoordinateSystem("EPSG::31982")

# === ALINHAMENTO ===
print("📌 Alinhando fotos...")
chunk.matchPhotos(downscale=1, generic_preselection=True, reference_preselection=True)
chunk.alignCameras()

# Verificar qualidade do alinhamento
aligned = sum([1 for cam in chunk.cameras if cam.transform])
total = len(chunk.cameras)
if aligned / total < 0.9:
    raise Exception(f"⚠️ Alinhamento ruim: apenas {aligned}/{total} câmeras alinhadas!")
print(f"✅ Alinhamento OK: {aligned}/{total} câmeras.")

# === CONSTRUIR NUVEM DE PONTOS ===
print("☁️ Construindo nuvem de pontos (buildPointCloud)...")
chunk.buildPointCloud()

# === MODELO DE ELEVAÇÃO ===
print("🗺️ Criando Modelo Digital de Elevação (DEM)...")
chunk.buildDem(source_data=Metashape.PointCloudData)

# === ORTOMOSAICO ===
print("🖼️ Criando Ortomosaico Multibanda...")
chunk.buildOrthomosaic(surface=Metashape.ElevationData, blending=Metashape.MosaicBlending, refine_seamlines=True)

# === EXPORTAR ORTOMOSAICO ===
output_folder = Metashape.app.getExistingDirectory("Selecione onde salvar o ortomosaico e índices")
ortho_path = os.path.join(output_folder, "ortomosaico_multibanda.tif")
chunk.exportOrthomosaic(path=ortho_path, image_format=Metashape.ImageFormatTIFF, save_alpha=False)
print(f"✅ Ortomosaico exportado: {ortho_path}")

# === ÍNDICES VEGETATIVOS ===

def create_index(name, expression):
    transform = Metashape.RasterTransform()
    transform.expression = expression
    out_tif = os.path.join(output_folder, f"{name}.tif")
    out_csv = os.path.join(output_folder, f"{name}.csv")
    
    # Exporta GeoTIFF
    chunk.exportRaster(transform=transform, path=out_tif, image_format=Metashape.ImageFormatTIFF)
    
    # Exporta CSV com estatísticas (média, min, max)
    chunk.exportRaster(transform=transform, path=out_csv, format=Metashape.RasterFormatCSV)
    print(f"✅ {name} exportado: .tif e .csv")

print("🧪 Gerando índices vegetativos...")
create_index("NDVI", "(B5 - B3) / (B5 + B3)")
create_index("GNDVI", "(B5 - B2) / (B5 + B2)")
create_index("NDRE", "(B5 - B4) / (B5 + B4)")
create_index("RENDVI", "(B5 - B3) / (B5 + B4)")
create_index("SAVI", "1.5 * (B5 - B3) / (B5 + B3 + 0.5)")
create_index("MSAVI", "(2 * B5 + 1 - sqrt((2 * B5 + 1)^2 - 8 * (B5 - B3))) / 2")

# === SALVAR PROJETO ===
project_path = Metashape.app.getSaveFileName("Salvar projeto como:")
doc.save(project_path)
print("💾 Projeto salvo com sucesso.")