# Thumbnail Generator

Simple python scripts that generates thumbnails of any preferred size from a directory containing source photos. 

## Usage

```
Usage: thumbnail_generator.py [FROM] [TO] [PAR] [WIDTH] [HEIGHT] 
> FROM: directory of images to reduce to thumbnails 
> TO: directory to place thumbnails  
> PAR: preserve aspect ratio  
> --- 0 (don't preserve) . 
> --- 1 (preserve based on given width) 
> --- 2 (preserve based on given height) 
> --- 3 (shrink image by factor given in WIDTH argument  
> WIDTH: new width to reduce to (any number if PAR=2; shrink factor if PAR=3)  
> HEIGHT: new height to reduce to (any number if PAR=1,3) 
```
