import rasterio
import numpy as np
import os
import matplotlib.pyplot as plt

# Directorio de imágenes
input_folder = r""
output_folder = os.path.join(input_folder, "Resultados")
os.makedirs(output_folder, exist_ok=True)

# Umbral para NDVI
ndvi_threshold = 0.14

# Procesar cada archivo en la carpeta
for filename in os.listdir(input_folder):
    if filename.endswith(".tif"):
        file_path = os.path.join(input_folder, filename)
        
        with rasterio.open(file_path) as src:
            band_count = src.count
            print(f"{filename} tiene {band_count} bandas.")

            if band_count >= 4:
                red = src.read(4)  # Banda 4: Red
            else:
                print(f"El archivo {filename} no tiene suficientes bandas para calcular NDVI.")
                continue
            
            if band_count >= 8:
                nir = src.read(8)  # Banda 8: Near Infrared (NIR)
            else:
                print(f"El archivo {filename} no tiene suficientes bandas para calcular NDVI.")
                continue

            # Calcular el NDVI
            ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)
            
            # Mascara de áreas verdes
            green_mask = ndvi > ndvi_threshold
            
            # Calcular el porcentaje de áreas verdes
            total_pixels = green_mask.size
            green_pixels = np.sum(green_mask)
            percentage_green_area = (green_pixels / total_pixels) * 100
            
            print(f"Porcentaje de área verde en {filename}: {percentage_green_area:.2f}%")

            # Configurar la figura para NDVI y máscara de áreas verdes
            plt.figure(figsize=(10, 5))

            plt.subplot(1, 2, 1)
            plt.title("NDVI")
            plt.imshow(ndvi, cmap='RdYlGn')
            plt.colorbar()

            plt.subplot(1, 2, 2)
            plt.title("Áreas Verdes")
            plt.imshow(green_mask, cmap='Greens')
            plt.colorbar()

            # Guardar la figura
            output_path = os.path.join(output_folder, f"{filename.split('.')[0]}_NDVI_{percentage_green_area:.2f}%.png")
            plt.savefig(output_path)
            plt.close()  # Cierra la figura después de guardarla

            # Muestra la figura si es necesario
            # plt.show()
