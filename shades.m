 
%clear all;
%clc;
 
path = 'C:\Users\Pranjal\Desktop\Rohit_images\a.bmp';
 
img = imread(path);
s = size(img);
d = zeros(s(1),s(2),s(3));
d = img;
g = zeros(s(1),s(2));
 
for i=1:s(2)
    temp = d(:,:,1);
    if(d(:,:,1)>41)
        if(d(:,:,1)<46)
            d(:,:,1) = 0;   
        else
            d(:,:,1) = 128;
       end
    end
    
    if(d(:,:,2)>198)
        if(d(:,:,2)<205)
            d(:,:,2) = 0;
        else
            d(:,:,2) = 128;
        end
    end
    
    if(d(:,:,3)>20)
        if(d(:,:,3)<23)
            d(:,:,3) = 0;
        else
            d(:,:,3) = 128;
        end
    end
end
 
subplot(3,2,1);
imshow(img);
title('input image');
subplot(3,2,2);
imshow(im2bw(d));
title('GREEN ONLY - output image');
 
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
        %if(d(:,:,2)<75)        % thresholding cross instead of range
            d(:,:,2) = 0;
        else
            d(:,:,2) = 128;
        %end
    end
    
    if(d(:,:,3)>30)
        %if(d(:,:,3)<40)
            d(:,:,3) = 0;
        else
            d(:,:,3) = 128;
        %end
    end
end
 
subplot(3,2,3);
imshow(img);
title('input image');
subplot(3,2,4);
imshow(im2bw(d));
title('RED ONLY - output image');
 
d = img;
for i=1:s(2)
    if(d(:,:,1)>195)
        %if(d(:,:,1)<202)
            d(:,:,1) = 0;
        else
            d(:,:,1) = 128;
        %end
    end
    
    if(d(:,:,2)>69)
        %if(d(:,:,2)<75)        % thresholding cross instead of range
            d(:,:,2) = 0;
        else
            d(:,:,2) = 128;
        %end
    end
    
    if(d(:,:,3)>132)
        if(d(:,:,3)<250)
            d(:,:,3) = 0;
        else
            d(:,:,3) = 128;
        end
    end
end
 
subplot(3,2,5);
imshow(img);
title('input image');
subplot(3,2,6);
imshow(im2bw(d));
title('BLUE ONLY - output image');
