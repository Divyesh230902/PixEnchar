import os
from PIL import Image

class PixEnchar:
    def __init__(self, input_path=f'{os.getcwd()}/input', output_path=f'{os.getcwd()}/output'):
        self.img_path = input_path+'/'
        self.out_path = output_path+'/'
        Image.MAX_IMAGE_PIXELS = None
        self.result = self.out_path + 'result/'
        self.DPI = (900,900)
        print('Input path:', self.img_path)
        print('Output path:', self.out_path)
        if not os.path.exists(self.result):
            os.makedirs(self.result)
        
    def read_imgs(self):
        self.img_ls = os.listdir(self.img_path)
        self.out_ls = os.listdir(self.out_path)

    def remove_processed(self):
        for i in self.out_ls:
            if i in self.img_ls:
                self.img_ls.remove(i)

    def process(self):
        for i in range(len(self.img_ls)):
            if ' ' in self.img_ls[i]:
                os.rename(self.img_path + self.img_ls[i], self.img_path + self.img_ls[i].replace(' ', '_'))
                self.img_ls[i] = self.img_ls[i].replace(' ', '_')

    def pixenchar(self):
        PixEnchar.read_imgs(self)
        PixEnchar.remove_processed(self)
        PixEnchar.process(self)
        for img in self.img_ls:
            print('Processing', img+'...')
            if os.name == 'nt':
                os.system(f'realesrgan-ncnn-vulkan.exe -i {self.img_path}{img} -o {self.out_path}{img} -n realesrgan-x4plus -s 4 -f png')
            elif os.name == 'posix':
                os.system('chmod u+x realesrgan-ncnn-vulkan')
                os.system(f'./realesrgan-ncnn-vulkan -i {self.img_path}{img} -o {self.out_path}{img} -n realesrgan-x4plus -s 4 -f png')
            print('Done!\nYou can check the result in', self.out_path+img+'.')

    def change_dpi(self):
        for image in self.out_ls:
            if image == 'result':
                self.out_ls.remove(image)
                continue
            image = Image.open(f'{self.out_path}{image}')
            img_name = image.filename.split('/')[-1]
            if os.path.exists(self.result):
                out_img = os.path.join(self.result, f'{img_name}_rtl.png')
                image.save(out_img, dpi=self.DPI)
                print(f'Image {img_name} saved to {out_img}')
            else:
                os.mkdir(self.result)
                out_img = os.path.join(self.result, f'{img_name}_rtl.png')
                image.save(out_img, dpi=self.DPI)
                print(f'Image {img_name} saved to {out_img}')


if __name__ == '__main__':
    input_path = input('Please input the path of the image folder: ')
    output_path = input('Please input the path of the output folder: ')
    pe = PixEnchar()
    if input_path == '' or output_path == '':
        for i in range(2):
            pe.pixenchar()
            pe.change_dpi()
    else:
        for i in range(2):
            pe.pixenchar()
            pe.change_dpi()
