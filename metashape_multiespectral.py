import Metashape
import os

# Cria um novo projeto
doc = Metashape.app.document
chunk = doc.addChunk()

# Seleciona a pasta com as imagens
image_folder = Metashape.app.getExistingDirectory("Selecione a pasta com as imagens")

# Cria uma lista de imagens
image_list = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.lower().endswith(('tif', 'jpg', 'jpeg', 'png'))]

# Verifica se encontrou imagens
if not image_list:
    raise Exception("⚠️ Nenhuma imagem encontrada no diretório!")

# Adiciona as imagens
chunk.addPhotos(image_list)

# Checa quantas imagens adicionadas
print("📸 {} imagens carregadas.".format(len(chunk.cameras)))

# Alinhamento das fotos
chunk.matchPhotos(accuracy=Metashape.HighAccuracy, generic_preselection=True, reference_preselection=True)
chunk.alignCameras()

# Construir a Nuvem de Pontos Densa
chunk.buildDenseCloud(quality=Metashape.MediumQuality, filtering=Metashape.MildFiltering)

# Construir o Modelo de Superfície (DEM)
chunk.buildDem(source_data=Metashape.DenseCloudData)

# Construir o Ortomosaico
chunk.buildOrthomosaic(surface_data=Metashape.ElevationData, blending_mode=Metashape.MosaicBlending)

# Salvar o projeto
project_path = Metashape.app.getSaveFileName("Salvar projeto como:")
doc.save(project_path)

print("✅ Processamento completo!")

