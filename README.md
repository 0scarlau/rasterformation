## GITHUB LINK
https://github.com/0scarlau/rasterformation

## SETUP (WINDOWS)

As part of this package, it is important to know which python version you are using 
as the library dependencies rely on the version

```
python --version
```

Install the generic python libraries

```
pip install numpy==1.20.3 && pip install flask==2.0.1
```

We are going to be using the libraries GDAL and Rasterio to perform 
our raster image transformation. To install these libraries for windows, you must
download both binaries from https://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio
and https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

Install both binaries using
```
pip install GDAL-<verion>-cp<python_version>-cp<python_version>-win_amd64.whl
pip install rasterio-<version>-cp<python_version>-cp<python_version>-win_amd64.whl
```


## SETUP (LINUX)

1. Create your python virtual environment 
```
python3 -m virtualenv env
```

2. Activate the virtual environment 
```
source /env/bin/activate
```

3. Install the python libraries
```
pip install -r requirements.txt
```

## Running the flask API 
Change your directory to ```<path_to_project>/rasterformation/``` 

Run the flask application

```python raster_transformation_app.py```

You can also run the Flask application using docker containers

```docker build -t raster_transformer .```

```docker run -d -p localhost/raster_transformer_app```

Open to localhost browser http://localhost:5000 or http://127.0.0.1:5000
