function imdata = createimdata(folder,focusfile)
cd folder
tmp = struct2cell(dir('*image*.png'));
images = tmp(1,:)';
images = strcat('./' + folder + '/', images);
imdata.focus = csvread(focusfile);
imdata.images = images;
save(folder + ".mat", imdata);
end

