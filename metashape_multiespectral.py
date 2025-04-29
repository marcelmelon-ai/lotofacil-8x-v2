import Metashape
import os

# === CONFIGURAÇÕES INICIAIS ===
# Configurar os comprimentos de onda
wavelengths = {
    "B": 475,
    "G": 560,
    "R": 668,
    "RE": 717,
    "NIR": 840
}

# === INÍCIO DO PROCESSAMENTO ===
doc = Metashape.app.document
chunk = doc.chunk

# 1. Criar sensores separados para cada banda
sensors = {}
for band, wl in wavelengths.items():
    sensor = chunk.addSensor()
    sensor.label = band
    sensor.type = Metashape.Sensor.Type.Frame
    sensor.wavelengths = [wl]
    sensors[band] = sensor

# 2. Atribuir sensores às câmeras
for camera in chunk.cameras:
    name_upper = camera.label.upper()
    assigned = False
    for band in wavelengths.keys():
        if band in name_upper:
            camera.sensor = sensors[band]
            assigned = True
            break
    if not assigned:
        print(f"⚠️ Atenção: {camera.label} não corresponde a nenhuma banda conhecida.")

print("✅ Sensores configurados e atribuídos.")

# 3. Construir Ortomosaico Multibanda
print("🛠️ Gerando Ortomosaico Multibanda...")
chunk.buildOrthomosaic(surface=Metashape.ElevationData, blending=Metashape.MosaicBlending, refine_seamlines=True)
print("✅ Ortomosaico pronto.")

# 4. Exportar Ortomosaico Multibanda
output_folder = Metashape.app.getExistingDirectory("Selecione onde salvar o ortomosaico")
output_path = os.path.join(output_folder, "ortomosaico_multibanda.tif")
chunk.exportOrthomosaic(path=output_path, image_format=Metashape.ImageFormatTIFF, save_alpha=False)
print(f"✅ Ortomosaico exportado para: {output_path}")

# 5. Criar Índices Vegetativos

# Função para adicionar índice
def create_index(name, expression):
    raster_transform = Metashape.RasterTransform()
    raster_transform.bands = expression
    index_path = os.path.join(output_folder, f"{name}.tif")
    chunk.exportRaster(transform=raster_transform, path=index_path, image_format=Metashape.ImageFormatTIFF)
    print(f"✅ {name} gerado: {index_path}")

print("🧪 Gerando índices vegetativos...")

# Mapas de Bandas
# B1 - BLUE
# B2 - GREEN
# B3 - RED
# B4 - RED_EDGE
# B5 - NIR

# NDVI = (NIR - RED) / (NIR + RED)
create_index("NDVI", "(B5 - B3) / (B5 + B3)")

# GNDVI = (NIR - GREEN) / (NIR + GREEN)
create_index("GNDVI", "(B5 - B2) / (B5 + B2)")

# NDRE = (NIR - RED_EDGE) / (NIR + RED_EDGE)
create_index("NDRE", "(B5 - B4) / (B5 + B4)")

# RENDVI = (NIR - RED) / (NIR + RED_EDGE)
create_index("RENDVI", "(B5 - B3) / (B5 + B4)")

# SAVI = ((NIR - RED) / (NIR + RED + 0.5)) * (1.5)
create_index("SAVI", "1.5 * (B5 - B3) / (B5 + B3 + 0.5)")

# MSAVI = (2 * NIR + 1 - sqrt((2 * NIR + 1)^2 - 8 * (NIR - RED))) / 2
create_index("MSAVI", "(2 * B5 + 1 - sqrt((2 * B5 + 1)^2 - 8 * (B5 - B3))) / 2")

print("🎯 Todos os índices vegetativos gerados com sucesso!")

