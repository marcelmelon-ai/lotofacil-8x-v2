import Metashape
import os

# === CONFIGURAÇÕES INICIAIS ===

# Mapeamento de bandas e seus comprimentos de onda
band_wavelengths = {
    "B": 475,    # Blue
    "G": 560,    # Green
    "R": 668,    # Red
    "RE": 717,   # Red Edge
    "NIR": 840   # Near Infrared
}

# === INÍCIO DO PROCESSAMENTO ===

# Criar novo projeto
doc = Metashape.app.document
doc.clear()

# Criar novo chunk
chunk = doc.addChunk()

# Selecionar pasta de imagens
image_folder = Metashape.app.getExistingDirectory("Selecione a pasta com as imagens")

# Carregar imagens
image_list = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.lower().endswith(('.tif', '.jpg', '.jpeg', '.png'))]

if not image_list:
    raise Exception("⚠️ Nenhuma imagem encontrada no diretório!")

chunk.addPhotos(image_list)
print(f"📸 {len(chunk.cameras)} imagens carregadas.")

# === CONFIGURAR SENSORES ===
print("🔧 Configurando sensores...")
sensors = {}
for band, wl in band_wavelengths.items():
    sensor = chunk.addSensor()
    sensor.label = band
    sensor.type = Metashape.Sensor.Type.Frame
    sensor.wavelengths = [wl]   # ✅ CORRETO para Metashape 2.2
    sensors[band] = sensor

# Atribuir sensores às câmeras
for camera in chunk.cameras:
    name_upper = camera.label.upper()
    assigned = False
    for band in band_wavelengths.keys():
        if band in name_upper:
            camera.sensor = sensors[band]
            assigned = True
            break
    if not assigned:
        print(f"⚠️ Atenção: {camera.label} não corresponde a nenhuma banda conhecida.")

print("✅ Sensores configurados e atribuídos.")

# === PROCESSAMENTO AUTOMÁTICO ===

# 1. Alinhar fotos
print("📌 Alinhando fotos...")
chunk.matchPhotos(downscale=1, generic_preselection=True, reference_preselection=True)
chunk.alignCameras()

# 2. Construir Nuvem Densa
print("☁️ Construindo Nuvem Densa...")
chunk.buildDepthMaps(downscale=2, filter_mode=Metashape.MildFiltering)
chunk.buildDenseCloud()

# 3. Construir DEM
print("🗺️ Construindo Modelo Digital de Elevação (DEM)...")
chunk.buildDem(source_data=Metashape.DenseCloudData)

# 4. Construir Ortomosaico
print("🖼️ Construindo Ortomosaico Multibanda...")
chunk.buildOrthomosaic(surface=Metashape.ElevationData, blending=Metashape.MosaicBlending, refine_seamlines=True)

# 5. Exportar Ortomosaico Multibanda
output_folder = Metashape.app.getExistingDirectory("Selecione onde salvar o ortomosaico e índices")
ortho_path = os.path.join(output_folder, "ortomosaico_multibanda.tif")
chunk.exportOrthomosaic(path=ortho_path, image_format=Metashape.ImageFormatTIFF, save_alpha=False)
print(f"✅ Ortomosaico exportado para: {ortho_path}")

# === GERAR ÍNDICES VEGETATIVOS ===

# Função para criar índices
def create_index(name, expression):
    raster_transform = Metashape.RasterTransform()
    raster_transform.expression = expression
    index_path = os.path.join(output_folder, f"{name}.tif")
    chunk.exportRaster(transform=raster_transform, path=index_path, image_format=Metashape.ImageFormatTIFF)
    print(f"✅ {name} gerado: {index_path}")

print("🧪 Gerando índices vegetativos...")

# Notação:
# B1: B (Blue)
# B2: G (Green)
# B3: R (Red)
# B4: RE (Red Edge)
# B5: NIR (Near Infrared)

create_index("NDVI", "(B5 - B3) / (B5 + B3)")
create_index("GNDVI", "(B5 - B2) / (B5 + B2)")
create_index("NDRE", "(B5 - B4) / (B5 + B4)")
create_index("RENDVI", "(B5 - B3) / (B5 + B4)")
create_index("SAVI", "1.5 * (B5 - B3) / (B5 + B3 + 0.5)")
create_index("MSAVI", "(2 * B5 + 1 - sqrt((2 * B5 + 1)^2 - 8 * (B5 - B3))) / 2")

print("🎯 Todos os índices vegetativos gerados com sucesso!")

# 6. Salvar projeto
project_path = Metashape.app.getSaveFileName("Salvar projeto como:")
doc.save(project_path)

print("💾 Projeto salvo com sucesso!")