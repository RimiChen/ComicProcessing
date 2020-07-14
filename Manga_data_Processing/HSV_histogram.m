% get information of COMIC and MANGA 109 data

% color historgram

image_input = imread('west_001.jpg');
hsvImage = rgb2hsv(image_input);
hImage = hsvImage(:, :, 1);
sImage = hsvImage(:, :, 2);
vImage = hsvImage(:, :, 3);
figure;
subplot(2,2,1);
hHist = histogram(hImage);
subplot(2,2,2);
sHist = histogram(sImage);
subplot(2,2,3);
vHist = histogram(vImage);