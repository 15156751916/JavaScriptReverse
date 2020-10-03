from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os

def crop_img(path):
    img = Image.open(path)
    print(img.size)
    width=img.size[1]/4
    height=(img.size[1]-10)/2
    print(width,height)

    if not os.path.exists('./yzm'):
        os.mkdir('./yzm')

    #标题
    cropped1 = img.crop((120, 0, 212,24 ))  # (left, upper, right, lower)
    cropped1.save('./yzm/0.jpg')

    #上
    cropped2 = img.crop((4, 43, 70,109 ))  # (left, upper, right, lower)
    cropped2.save('./yzm/1.jpg')

    cropped3 = img.crop((76, 43, 142,109 ))  # (left, upper, right, lower)
    cropped3.save('./yzm/2.jpg')

    cropped4 = img.crop((148, 43, 214,109 ))  # (left, upper, right, lower)
    cropped4.save('./yzm/3.jpg')

    cropped5 = img.crop((220, 43, 286,109 ))  # (left, upper, right, lower)
    cropped5.save('./yzm/4.jpg')

    #下
    cropped6 = img.crop((4, 113, 70,179 ))  # (left, upper, right, lower)
    cropped6.save('./yzm/5.jpg')

    cropped7 = img.crop((76, 113, 142,179 ))  # (left, upper, right, lower)
    cropped7.save('./yzm/6.jpg')

    cropped8 = img.crop((148, 113, 214,179 ))  # (left, upper, right, lower)
    cropped8.save('./yzm/7.jpg')

    cropped9 = img.crop((220, 113, 286,179 ))  # (left, upper, right, lower)
    cropped9.save('./yzm/8.jpg')

if __name__ == '__main__':
    img=''
    crop_img()