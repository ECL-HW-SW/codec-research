import cv2
import numpy as np
import os

class Editor():
    def __init__(self):
        pass
    
    def get_frames(self,input,frames_list):
        video = cv2.VideoCapture(input)
        images_list = []
        c = 0
        while True:
            sucess, image = video.read()
            if sucess:
                if c in frames_list:
                    resize = cv2.resize(image,dsize=(1280,960), interpolation=cv2.INTER_CUBIC)
                    images_list.append(resize)
                    if c == frames_list[-1]:
                        break
                c+=1

        video.release()
        cv2.destroyAllWindows()

        return images_list

    def add_border(self,image,border_thickness=5,color=[255,255,255]):
        new_image = cv2.copyMakeBorder(image, border_thickness, border_thickness, border_thickness, border_thickness, cv2.BORDER_CONSTANT, value=color)
        return new_image


    def add_border_and_text(self,image,text):
        black_border = self.add_border(image,3,[0,0,0])
        white_border = self.add_border(black_border,50)
        texted_image =cv2.putText(img=np.copy(white_border), text=text, org=(50,30),fontFace=2, fontScale=1, color=(0,0,0), thickness=1)
        return texted_image

    def concatenate(self,image_a,image_b):
        new_image = np.concatenate((image_a,image_b), axis=1)
        return new_image

    def save(self,image,path,name):
        try:
            os.mkdir(f"images/{path}")
        except FileExistsError:
            pass
        except FileNotFoundError:
            pass
        cv2.imwrite(f'images/{path}/{name}.png',image)

