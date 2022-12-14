from subprocess import run
from skvideo.measure import msssim
import PIL.Image as im
import numpy as np
import cv2

class MetricsCalculator():
    """ 
    Class for calculating image/video comparison metrics
    such as MSSSIM, VMAF, LPIPS, X-PNSR, and others.
    """

    def __init__(self):
        pass

    def xpsnr(self, videoref: str, videodis: str, output: str) -> float:
        ffmpegpath = ''
        cmdline = ffmpegpath + " -i " + videoref + " -i " + videodis + ' -lavfi xpsnr="stats_file=' + output + '" -f null -'
        print(cmdline)
        #os.system(cmdline)    

    def vmaf(self, videoref: str , videodis: str, output: str) -> float:
        vmafpath = ''
        cmdline = vmafpath + " -r " + videoref + " -d " + videodis + " -o " + output +  " --csv"
        print(cmdline)
        #os.system(cmdline)

    def lpips(self, videoref: str, videodis: str) -> float:
        # TODO: caminhos hardcoded devem passar para constantes (usar singleton)
        cmdline = f"python3.7 ~/VC/tools/PerceptualSimilarity/lpips_2imgs.py \
                        -p0  {videoref} -p1 {videodis}"
        lpips = run([cmdline], shell=True, capture_output=True).stdout\
                    .decode('utf-8').split('\n')[-2].split()[-1]        
        return lpips

    def msssim(self, videoref: str, videodis: str) -> float:
        original_array_luminance = self.__get_image_array(videoref, "y", "cv2")
        decoded_array_luminance = self.__get_image_array(videodis, "y", "cv2")

        ssim_ms = msssim(original_array_luminance, decoded_array_luminance, 'product')[0]
        return ssim_ms

    ################################################
    """         Private methods below           """
    ################################################
    def __get_image_array(path, color_space, package = 'PIL'):
        """Acquires numpy array from an image using either PIL or CV2"""

        if package.lower() == 'pil':
            if color_space.lower() == "rgb":
                imgArray = np.array(im.open(path))
            elif color_space.lower() == "ycbcr":
                imgArray = np.array(im.open(path).convert('YCbCr'))
            else:
                print("That is not a valid color space.")
        elif package.lower() == 'cv2':
            if color_space.lower() == "rgb":
                imgArray = cv2.imread(path, 1)
            elif color_space.lower() == "ycbcr":
                imgArray = cv2.cvtColor(cv2.imread(path, 1), cv2.COLOR_BGR2YCR_CB)
            elif color_space.lower() == "y":
                imgArray = cv2.cvtColor(cv2.imread(path, 1), cv2.COLOR_BGR2YCR_CB)
                return imgArray[:,:,0]
            else:
                print("That is not a valid color space.")
        
        return imgArray