import rasterio
import os
import json
from rasterio.mask import mask
from typing import List
from osgeo import gdal


class RasterImageTransformer:

    def __init__(self, raster: str, geometry: str = None) -> None:

        #raster and geometry are the filenames for raster and the geometry respectively
        self.raster = self.load_raster_file(filename=raster)
        if geometry is None:
            self.geos = self.set_geometry()
        else:
            data = self.load_geojson(filename=geometry)
            self.geos = [data['features'][0]['geometry']]
            self.type = data['type']
            self.name = data['name']
            self.coordinates = data['features'][0]['geometry']['coordinates'][0][0]

            print(f'{geometry} contains the following information')
            print(f"type: {self.type}")
            print(f"name: {self.name}")
            print(f"coordinates: {self.coordinates}")

    def load_raster_file(self, filename: str):
        if isinstance(filename, str):
            try:
                print(f'Loading {filename} at {self._get_raster_path()}')
                return rasterio.open(f'{self._get_raster_path()}/{filename}')
            except FileNotFoundError:
                print(f'Unable to find {self._get_raster_path()}/{filename}')
        else:
            print('filename is not a string')

    def load_geojson(self, filename: str):
        if isinstance(filename, str):
            try:
                print(f'Loading {filename} at {self._get_geoson_path()}')
                data = open(f'{self._get_geoson_path()}/{filename}', 'r').read()
                return json.loads(data)
            except FileNotFoundError:
                print(f'Unable to find {self._get_geoson_path()}{filename}')
        else:
            print('filename is not a string')

    def transform(self):
        print('Running Raster Transformation')
        out_image, out_transform = mask(self.raster, self.geos, crop=True)
        output_data = self.raster.meta.copy()
        output_data.update(
            {
                'driver': 'GTiff',
                'height': out_image.shape[1],
                'width': out_image.shape[2],
                'transform': out_transform
            }
        )
        output_path = self._get_raster_path()
        with rasterio.open(f'{output_path}/masked_raster.tif', 'w', **output_data) as dest:
            dest.write(out_image)
            print(f"Raster image successfully transformed and saved in {output_path}/masked_raster.tif")
        return None

    @classmethod
    def set_geometry(cls) -> List[dict]:
        coodinates: List[List[List[List[int, int]]]] = list(list(list()))
        while True:
            x = input('Please insert your x coordinate: ')
            y = input('Please insert your y coordinate: ')
            coodinates.append([x,y])
            print('Would you like to add more coordinates?')
            prompt = input('Y/N?')
            if prompt == 'Y':
                continue
            else:
                break

        geometry: dict = {
            'type': 'MultiPolygon',
            'coodinates': coodinates
        }
        return [geometry]

    def tif_file_format_converter(self,
                                  filename: str,
                                  options: list = None,
                                  formatted_extension: str = 'JPEG') -> str:

        options_string = []
        if options is None:
            options_list = [
                '-ot Float32',
                f'-of {formatted_extension}',
                '-b 1',
                '-b 2',
                '-b 3',
                '-scale',
                '-expand rgb',
                '-outsize 10000 10000'
            ]
            options_string = " ".join(options_list)
        else:
            options_string = options

        if formatted_extension == 'JPEG':
            extension = 'jpg'
        else:
            extension = formatted_extension.lower()

        raster_path = self._get_raster_path()
        source_path = f'{raster_path}/{filename}'
        destination = f"{raster_path}/{(filename.split('.')[0])}.{extension}]"

        gdal.Translate(
            destName=destination,
            srcDS=source_path,
            options=options_string,
        )
        print(f'{filename} has been converted to {(filename.split(".")[0])}.{extension} and saved in {destination}')
        return f'raster/{(filename.split(".")[0])}.{extension}'

    def _get_geoson_path(self) -> str:
        return os.path.join(os.getcwd(), f'geojson')

    def _get_raster_path(self) -> str:
        return os.path.join(os.getcwd(), f'raster')