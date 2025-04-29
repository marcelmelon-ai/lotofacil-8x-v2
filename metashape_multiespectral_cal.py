import Metashape
import os

# === CONFIGURAÇÕES INICIAIS ===

# Mapeamento das bandas do Mavic 3M com os índices (conforme a ordem que o Metashape usa: B1, B2, etc.)
# Supondo que a ordem das bandas no ortomosaico seja:
# B1 = Green, B2 = Red, B3 = RedEdge, B4 = NIR
# (Blue não é capturado no Mavic 3M)

band_map = {
    "Green": 1,
    "Red": 2,
    "RedEdge": 3,
    "NIR": 4
}

# === INÍCIO DO PROCESSAMENTO ===

# Criar novo projeto
doc = Metashape.app.document
doc.clear()

# Criar novo chunk
chunk = doc.addChunk()

# Selecionar pasta de imagens
image_folder = Metashape.app.getExistingDirectory("Selecione a pasta com as imagens")
image_list = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.tif', '.jpg', '.jpeg', '.png'))]

if not image_list:
    raise Exception("⚠️ Nenhuma imagem encontrada no diretório!")

chunk.addPhotos(image_list)
print(f"📸 {len(chunk.cameras)} imagens carregadas.")

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

def create_index(name, expression):
    raster_transform = Metashape.RasterTransform()
    raster_transform.expression = expression
    index_path = os.path.join(output_folder, f"{name}.tif")
    chunk.exportRaster(transform=raster_transform, path=index_path, image_format=Metashape.ImageFormatTIFF)
    print(f"✅ {name} gerado: {index_path}")

print("🧪 Gerando índices vegetativos...")

# NDVI = (NIR - Red) / (NIR + Red)
# GNDVI = (NIR - Green) / (NIR + Green)
# NDRE = (NIR - RedEdge) / (NIR + RedEdge)
# RENDVI = (NIR - Red) / (NIR + RedEdge)
# SAVI = 1.5 * (NIR - Red) / (NIR + Red + 0.5)
# MSAVI = (2 * NIR + 1 - sqrt((2 * NIR + 1)^2 - 8 * (NIR - Red))) / 2

create_index("NDVI",     f"(B{band_map['NIR']} - B{band_map['Red']}) / (B{band_map['NIR']} + B{band_map['Red']})")
create_index("GNDVI",    f"(B{band_map['NIR']} - B{band_map['Green']}) / (B{band_map['NIR']} + B{band_map['Green']})")
create_index("NDRE",     f"(B{band_map['NIR']} - B{band_map['RedEdge']}) / (B{band_map['NIR']} + B{band_map['RedEdge']})")
create_index("RENDVI",   f"(B{band_map['NIR']} - B{band_map['Red']}) / (B{band_map['NIR']} + B{band_map['RedEdge']})")
create_index("SAVI",     f"1.5 * (B{band_map['NIR']} - B{band_map['Red']}) / (B{band_map['NIR']} + B{band_map['Red']} + 0.5)")
create_index("MSAVI",    f"(2 * B{band_map['NIR']} + 1 - sqrt((2 * B{band_map['NIR']} + 1)^2 - 8 * (B{band_map['NIR']} - B{band_map['Red']}))) / 2")

print("🎯 Todos os índices vegetativos gerados com sucesso!")

# 6. Salvar projeto
project_path = Metashape.app.getSaveFileName("Salvar projeto como:")
doc.save(project_path)

print("💾 Projeto salvo com sucesso!")
