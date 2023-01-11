x = imread('../full.tiff');
tic
[y, yy] = otsu(x, 2);
toc