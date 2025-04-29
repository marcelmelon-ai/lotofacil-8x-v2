import Metashape
import os

def process_multispectral_project(doc_path):
    Metashape.app.settings.log_enable = True

    doc = Metashape.app.document
    doc.open(doc_path)

    crs = Metashape.CoordinateSystem("EPSG::31982")  # SIRGAS 2000 / UTM Zone 22S

    for chunk in doc.chunks:
        print(f"\n▶ Processando chunk: {chunk.label}")
        chunk.crs = crs

        # Agrupar por linha de voo (útil para sensores multiespectrais)
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
            continue

        # Construir nuvem de pontos (Multiespectral → buildPointCloud)
        print("  - Gerando nuvem de pontos esparsa...")
        chunk.buildPointCloud()

        # Gerar ortomosaico
        print("  - Construindo ortomosaico...")
        chunk.buildOrthomosaic(surface_data=Metashape.PointCloudData)

        # Exportar ortomosaico multibanda
        ortho_path = os.path.join(os.path.dirname(doc_path), f"{chunk.label}_ortho.tif")
        chunk.exportOrthomosaic(
            path=ortho_path,
            format=Metashape.RasterFormat.RasterFormatTiles,
            projection=crs,
            image_format=Metashape.ImageFormatTIFF,
            tiff_compression=Metashape.TiffCompressionNone,
            write_kml=False
        )
        print(f"  - Ortomosaico exportado: {ortho_path}")

        # NDVI - usando bandas específicas (Red = banda 1, NIR = banda 4, depende do sensor)
        print("  - Calculando NDVI...")
        ndvi_index = Metashape.CalibrationIndex()
        ndvi_index.expression = "(B4 - B1) / (B4 + B1)"  # Assumindo: B4 = NIR, B1 = Red
        chunk.addRasterTransform(ndvi_index)

        # Exportar NDVI
        ndvi_path = os.path.join(os.path.dirname(doc_path), f"{chunk.label}_ndvi.tif")
        chunk.exportRaster(
            path=ndvi_path,
            source_data=Metashape.RasterTransform,
            format=Metashape.RasterFormat.RasterFormatTiles,
            image_format=Metashape.ImageFormatTIFF,
            projection=crs,
            raster_transform=Metashape.RasterTransformType.RasterTransformIndex
        )
        print(f"  - NDVI exportado: {ndvi_path}")

        print("✅ Chunk finalizado.\n")

    # Salvar projeto final
    doc.save()
    print("🎯 Processamento completo e projeto salvo.")

# Exemplo de uso
process_multispectral_project("C:/SEU_CAMINHO/PROJETO.pmz")
