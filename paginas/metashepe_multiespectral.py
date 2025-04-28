import Metashape

# Cria um novo projeto
doc = Metashape.app.document
chunk = doc.addChunk()

# Define o diretório onde estão as imagens multiespectrais
image_folder = Metashape.app.getExistingDirectory("Selecione a pasta com as imagens")

# Adiciona as imagens
import os
image_list = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('tif', 'jpg', 'jpeg', 'png'))]
chunk.addPhotos(image_list)

# Alinhamento das fotos
chunk.matchPhotos(accuracy=Metashape.HighAccuracy, generic_preselection=True, reference_preselection=True)
chunk.alignCameras()

# Construir a Nuvem de Pontos Densa
chunk.buildDepthMaps(quality=Metashape.MediumQuality, filter=Metashape.MildFiltering)
chunk.buildDenseCloud()

# Gerar o Modelo de Superfície (DEM)
chunk.buildDem(source_data=Metashape.DenseCloudData)

# Gerar o Ortomosaico
chunk.buildOrthomosaic(surface_data=Metashape.ElevationData, blending_mode=Metashape.MosaicBlending)

# Salvar o projeto
project_path = Metashape.app.getSaveFileName("Salvar projeto como:")
doc.save(project_path)

print("✅ Processamento completo!")
