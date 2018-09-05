echo off

set arg1=%1

magick -loop 1 GIF.gif %arg1%.gif
magick GIF.gif[0] %arg1%.png

