import rasterio
import numpy as np
import os

# Caminho do ortomosaico multibanda exportado pelo Metashape
input_path = "ortomosaico_multibanda.tif"
output_path = "NDVI.tif"

# Carrega o raster multibanda
with rasterio.open(input_path) as src:
    nir = src.read(5).astype('float32')  # Banda 5: NIR
    red = src.read(3).astype('float32')  # Banda 3: Red
    profile = src.profile

# Calcula NDVI
ndvi = (nir - red) / (nir + red + 1e-5)  # evita divisão por zero

# Atualiza metadados para salvar como imagem de 1 banda
profile.update(dtype=rasterio.float32, count=1)

# Salva o NDVI como novo GeoTIFF
with rasterio.open(output_path, 'w', **profile) as dst:
    dst.write(ndvi, 1)

print(f"✅ NDVI salvo em: {output_path}")
