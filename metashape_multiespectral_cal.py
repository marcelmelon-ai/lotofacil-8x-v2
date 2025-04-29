import Metashape
import os

def process_multispectral_images(image_folder):
    Metashape.app.settings.log_enable = True

    # Verifica se a pasta existe
    if not os.path.exists(image_folder):
        print(f"❌ Caminho não encontrado: {image_folder}")
        return

    # Caminho do projeto
    project_path = os.path.join(image_folder, "projeto_multiespectral.pmz")

    # Iniciar novo documento
    doc = Metashape.app.document
    doc.clear()

    # Criar novo chunk
    chunk = doc.addChunk()
    chunk.label = "Chunk_1"

    # Importar imagens
    image_list = [os.path.join(image_folder, f) for f in os.listdir(image_folder)
                  if f.lower().endswith(('.tif', '.tiff', '.jpg', '.jpeg', '.png'))]
    image_list.sort()

    if not image_list:
        print("❌ Nenhuma imagem encontrada na pasta.")
        return

    chunk.addPhotos(image_list, layout=Metashape.MultiplaneLayout)

    # Definir sistema de referência
    crs = Metashape.CoordinateSystem("EPSG::31982")  # SIRGAS 2000 / UTM Zone 22S
    chunk.crs = crs

    print(f"\n📸 {len(image_list)} imagens importadas.")
    print("▶ Iniciando processamento...")

    # Agrupar câmeras
    try:
        chunk.groupCameras(by=Metashape.Chunk.GroupByFlightLines)
        print("  - Câmeras agrupadas por linha de voo.")
    except:
        print("  - Aviso: não foi possível agrupar por linha de voo.")

    # Alinhamento
    print("  - Alinhando câmeras...")
    chunk.matchPhotos(downscale=1, generic_preselection=True, reference_preselection=True)
    chunk.alignCameras()

    # Verificar alinhamento
    aligned = [c for c in chunk.cameras if c.transform]
    total = len(chunk.cameras)
    reprojection_errors = [c.reprojection_error for c in aligned if c.reprojection_error is not None]
    media_erro = sum(reprojection_errors) / len(reprojection_errors) if reprojection_errors else 0

    print(f"  - Câmeras alinhadas: {len(aligned)}/{total} | Erro médio: {media_erro:.2f} px")

    if len(aligned) / total < 0.8 or media_erro > 1.5:
        print("  ⚠️ Alinhamento fraco ou erro alto. Verifique imagens ou GCPs.")
        return

    # Nuvem de pontos
    print("  - Gerando nuvem de pontos esparsa...")
    chunk.buildPointCloud()

    # Ortomosaico
    print("  - Construindo ortomosaico multiespectral...")
    chunk.buildOrthomosaic(surface_data=Metashape.PointCloudData)

    ortho_path = os.path.join(image_folder, f"{chunk.label}_ortho.tif")
    chunk.exportOrthomosaic(
        path=ortho_path,
        format=Metashape.RasterFormat.RasterFormatTiles,
        projection=crs,
        image_format=Metashape.ImageFormatTIFF,
        tiff_compression=Metashape.TiffCompressionNone,
        write_kml=False
    )
    print(f"  - Ortomosaico exportado: {ortho_path}")

    # NDVI
    print("  - Calculando NDVI...")
    ndvi_index = Metashape.CalibrationIndex()
    ndvi_index.expression = "(B4 - B1) / (B4 + B1)"  # Red = B1, NIR = B4
    chunk.addRasterTransform(ndvi_index)

    ndvi_path = os.path.join(image_folder, f"{chunk.label}_ndvi.tif")
    chunk.exportRaster(
        path=ndvi_path,
        source_data=Metashape.RasterTransform,
        format=Metashape.RasterFormat.RasterFormatTiles,
        image_format=Metashape.ImageFormatTIFF,
        projection=crs,
        raster_transform=Metashape.RasterTransformType.RasterTransformIndex
    )
    print(f"  - NDVI exportado: {ndvi_path}")

    # Salvar projeto
    doc.save(path=project_path)
    print(f"✅ Projeto salvo em: {project_path}")
    print("🎯 Processamento completo.")

# Exemplo de uso — apenas chame a função com o caminho das imagens
process_multispectral_images("D:/fotos_drones_mapa1")
