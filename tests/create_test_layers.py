"""
Create test polygon layers for Layer Grid View CRS reprojection testing.

All layers contain the SAME polygons around Goiania-GO, but each layer
is stored in a DIFFERENT Coordinate Reference System.

Run from the QGIS Python Console:
    exec(open('/home/tharles/projects_lapig/qgis-lgw/tests/create_test_layers.py').read())
"""

import os
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry,
    QgsPointXY, QgsField, QgsCoordinateReferenceSystem,
    QgsCoordinateTransform, QgsVectorFileWriter,
)
from qgis.PyQt.QtCore import QVariant

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
GPKG_PATH = os.path.join(OUTPUT_DIR, 'test_layers.gpkg')

# Reference: Goiania, GO
CENTER_LON = -49.2648
CENTER_LAT = -16.6869

# Same polygons, different CRS
CRS_LIST = [
    (4326,  'WGS 84 (Geographic)'),
    (4674,  'SIRGAS 2000 (Geographic)'),
    (31982, 'SIRGAS 2000 / UTM zone 22S'),
    (31983, 'SIRGAS 2000 / UTM zone 23S'),
    (3857,  'Web Mercator'),
    (5880,  'SIRGAS 2000 / Brazil Polyconic'),
    (32722, 'WGS 84 / UTM zone 22S'),
    (29192, 'SAD69 / UTM zone 22S'),
]

# Polygons defined in WGS84 around Goiania
# Each polygon: list of (lon, lat) corners
POLYGONS = [
    {
        'name': 'Parque Areiao',
        'coords': [
            (-49.270, -16.695), (-49.260, -16.695),
            (-49.260, -16.685), (-49.270, -16.685),
        ],
    },
    {
        'name': 'Setor Bueno',
        'coords': [
            (-49.258, -16.700), (-49.248, -16.700),
            (-49.248, -16.690), (-49.258, -16.690),
        ],
    },
    {
        'name': 'Lago das Rosas',
        'coords': [
            (-49.285, -16.680), (-49.275, -16.680),
            (-49.275, -16.670), (-49.285, -16.670),
        ],
    },
    {
        'name': 'Campinas',
        'coords': [
            (-49.290, -16.690), (-49.278, -16.690),
            (-49.278, -16.682), (-49.290, -16.682),
        ],
    },
    {
        'name': 'Setor Universitario',
        'coords': [
            (-49.265, -16.678), (-49.255, -16.678),
            (-49.255, -16.668), (-49.265, -16.668),
        ],
    },
    {
        'name': 'Jardim Goias',
        'coords': [
            (-49.250, -16.692), (-49.240, -16.692),
            (-49.240, -16.682), (-49.250, -16.682),
        ],
    },
]


def _transform_point(lon, lat, dst_epsg):
    """Transform a WGS84 point to the destination CRS."""
    if dst_epsg == 4326:
        return QgsPointXY(lon, lat)
    src_crs = QgsCoordinateReferenceSystem('EPSG:4326')
    dst_crs = QgsCoordinateReferenceSystem(f'EPSG:{dst_epsg}')
    transform = QgsCoordinateTransform(src_crs, dst_crs, QgsProject.instance())
    return transform.transform(QgsPointXY(lon, lat))


def _create_features(epsg):
    """Create polygon features, transforming WGS84 coords to target CRS."""
    features = []
    for i, poly in enumerate(POLYGONS):
        ring = [_transform_point(lon, lat, epsg) for lon, lat in poly['coords']]
        ring.append(ring[0])  # close ring
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolygonXY([ring]))
        feat.setAttributes([i + 1, poly['name'], f'EPSG:{epsg}'])
        features.append(feat)
    return features


def create_test_layers():
    """Generate all layers and save to GeoPackage."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if os.path.exists(GPKG_PATH):
        os.remove(GPKG_PATH)

    project = QgsProject.instance()
    created = []

    for epsg, description in CRS_LIST:
        name = f'goiania_epsg{epsg}'
        layer = QgsVectorLayer(f'Polygon?crs=EPSG:{epsg}', name, 'memory')
        provider = layer.dataProvider()

        provider.addAttributes([
            QgsField('id', QVariant.Int),
            QgsField('name', QVariant.String, len=50),
            QgsField('crs', QVariant.String, len=30),
        ])
        layer.updateFields()

        features = _create_features(epsg)
        provider.addFeatures(features)
        layer.updateExtents()

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.layerName = name
        options.driverName = 'GPKG'
        if os.path.exists(GPKG_PATH):
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

        error, msg = QgsVectorFileWriter.writeAsVectorFormatV2(
            layer, GPKG_PATH, project.transformContext(), options
        )
        if error != QgsVectorFileWriter.NoError:
            print(f'  ERROR: {name} - {msg}')
            continue

        print(f'  {name:<25} EPSG:{epsg:<6} {len(features)} polygons  ({description})')
        created.append(name)

    print(f'\nLoading {len(created)} layers...')
    for name in created:
        gpkg_layer = QgsVectorLayer(f'{GPKG_PATH}|layername={name}', name, 'ogr')
        if gpkg_layer.isValid():
            project.addMapLayer(gpkg_layer)
        else:
            print(f'  FAILED: {name}')

    print(f'\nDone! All {len(created)} layers show the same area (Goiania) in different CRS.')
    print('Open Layer Grid View to verify reprojection alignment.')


print('Creating test layers (same location, different CRS)...\n')
create_test_layers()
