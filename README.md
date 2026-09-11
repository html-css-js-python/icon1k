# ICON1K
A simple image tool for VidiaG Force RT-X12864

[DOWNLOAD](/download.md)

## Running from source

Clone the repository:
```cmd
git clone https://github.com/html-css-js-python/icon1k.git
cd icon1k
```

Run the application:
```
python app.py 128 64
```

## Getting Started with ICON1K

First, install ICON1K from [this site](/download.md).  

Once ICON1K is installed, test it by opening the help:
```cmd
icon1k --help
```
If that works, you can now use the application.

## Usage

To open ICON1K, you must specify image size:
```cmd
icon1k <width> <height>
```
The image size must meet the following conditions:
- Image size cannot be smaller than 8x8.
- Image size cannot be larger than 128x64.
- Height of image must be divisible by 8.  

You can also use the inverted LCD-style editor:
```cmd
icon1k --invert <width> <height>
```
