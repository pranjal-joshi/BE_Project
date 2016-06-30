
%clear  all;
%clc;

path = 'C:\Users\Pranjal\Desktop\Rohit_images\red.bmp';

img = imread(path);
s = size(img);
d = zeros(s(1),s(2),s(3));
d = img;

for i=1:s(2)
    if(d(:,:,1)>195)
        if(d(:,:,1)<202)
            d(:,:,1) = 0;
        else
            d(:,:,1) = 128;
        end
    end
    
    if(d(:,:,2)>69)
        if(d(:,:,2)<75)
            d(:,:,2) = 0;
        else
            d(:,:,2) = 128;
        end
    end
    
    if(d(:,:,3)>30)
        if(d(:,:,3)<40)
            d(:,:,3) = 0;
        else
            d(:,:,3) = 128;
        end
    end
end

subplot(2,1,1);
imshow(img);
title('input image');
subplot(2,1,2);
imshow(im2bw(d));
title('output image');
