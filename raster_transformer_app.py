from flask import Flask, render_template, request
from src.transformer.raster_transformer import RasterImageTransformer
import time
import os

app = Flask(__name__, static_folder='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
@app.route('/home')
def raster_main():
    return render_template('raster.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
     if request.method == 'POST':
        start_time = time.time()

        result = request.form
        raster_image = result['raster image']
        geometry = result['geojson']
        raster = RasterImageTransformer(raster=raster_image, geometry=geometry)
        raster.transform()
        raster_original = raster.tif_file_format_converter(filename=raster_image, formatted_extension='JPEG')
        masked_raster = raster.tif_file_format_converter(filename='masked_raster.tif', formatted_extension='JPEG')
        finish_time = round(time.time() - start_time, 2)
        return render_template("result.html",
                               result=result,
                               geojson=geometry,
                               coordinates=raster.coordinates,
                               time=finish_time,
                               original_image=raster_original,
                               transformed_image=masked_raster
                               )

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run(debug=True)