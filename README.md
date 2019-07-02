# receipts-stitcher
A service os computing vision which stitches multiple receipts parts into a single image using OpenCV wrote in C++ and Python.

## Building a docker image

```
docker build -t <your_image_name> .
```

## Running a container

```
docker run -it <your_image_name>
```

If you want access bash of your container, you use follow command:

```
docker run -it <your_image_name> bash
``` 

## Running the app

```
python main.py
```

This repo is maitained by rmelo <rdg.melo@gmail.com>
