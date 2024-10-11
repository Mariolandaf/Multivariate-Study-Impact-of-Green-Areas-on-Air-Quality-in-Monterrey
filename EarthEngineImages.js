// Coordenadas del punto central
var point = ee.Geometry.Point([-100.369527, 25.762929]);

// Crear un círculo de 2.5 km de radio alrededor del punto
var circle = point.buffer(2500);

// Función para obtener imágenes por mes con las bandas necesarias
function getMonthlyImage(month) {
  var startDate = ee.Date.fromYMD(2022, month, 1);
  var endDate = startDate.advance(1, 'month');
  
  var sentinel2 = ee.ImageCollection('COPERNICUS/S2')
    .filterBounds(circle)
    .filterDate(startDate, endDate)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
    .median();
  
  // Mostrar bandas disponibles en la imagen
  print('Band names:', sentinel2.bandNames());
  
  // Seleccionar todas las bandas disponibles
  return sentinel2.clip(circle);
}

// Generar imágenes para cada mes
for (var i = 1; i <= 12; i++) {
  var monthlyImage = getMonthlyImage(i);
  
  // Visualizar la imagen mensual en el mapa
  Map.addLayer(monthlyImage, {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000}, 'Sentinel-2 ' + i + '/2023');
  
  // Exportar la imagen mensual de alta resolución
  Export.image.toDrive({
    image: monthlyImage,
    description: 'Sentinel2_HighRes_CircularArea_' + i + '_2022_Noroeste',
    scale: 10, // Resolución de 10 metros por píxel
    region: circle,
    fileFormat: 'GeoTIFF',
    maxPixels: 1e9
  });
}

// Centrar el mapa en el círculo
Map.centerObject(circle, 12); // Zoom nivel 12
