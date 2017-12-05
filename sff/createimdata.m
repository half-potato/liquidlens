function imdata = createimdata(folder,focusfile)
buffer = 20;
tmp = struct2cell(dir(strcat(folder,'/*image*.png')));
images = tmp(1,:)';
images = strcat(strcat('./', folder, '/'), images);
imdata.focus = csvread(focusfile);
imdata.focus = imdata.focus(5:36,1)';
imdata.images = images(5:36);
% get image dims
im = imread(images{1});
[h w] = size(im);
imdata.ROI = [buffer, buffer, w-2*buffer, h-2*buffer];
save(strcat(folder, '.mat'), 'imdata');
end