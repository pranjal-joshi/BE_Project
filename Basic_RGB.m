clear all;
clc;

path = 'C:\Users\Pranjal\Desktop\Rohit_images\MDV-20140729-0229_20160622-10590.png';
img = imread(path);

red=zeros(size(img));
blue=zeros(size(img));
green=zeros(size(img));

figure, imshow(img);
title('Original Image');

for i=1:size(img,1)
    for j=1:size(img,2)
        
        if(img(i,j,1) <= 0)     % Red
            for k=1:3
                red(i,j,k) = img(i,j,k);
            end
        end
        
        if(img(i,j,2) <= 0)     % Green
            for k=1:3
                green(i,j,k) = img(i,j,k);
            end
        end
        
        if(img(i,j,3) <= 0)     % Blue
            for k=1:3
                blue(i,j,k) = img(i,j,k);
            end
        end
        
    end
end

red = uint8(red);
blue = uint8(blue);
green = uint8(green);

figure, imshow(red);
title('Red pixels');

figure, imshow(blue);
title('Blue pixels');

figure, imshow(green);
title('Green pixels');