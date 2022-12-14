from Codec import Codec
import os
import re
import csv
from pathlib import Path

class EVC(Codec):
    def __init__(self):
        super().__init__('evc')

    def encode(self):
        print("\nENCODING EVC...\n")

        options_encoder = ''
        for key, val in self.get_options_encoder().items():
            options_encoder += f"{key} {val} "
        
        bitstream_path = self.get_bitstream()
        p = Path('~').expanduser()
        bitstream_path = bitstream_path.replace("~", str(p))
        if not(os.path.exists(bitstream_path)):
            os.mkdir(bitstream_path)

        part1 = f'xeve_app -i {self.get_videopath()} -v 3 -q {self.get_qp()} {options_encoder} '
        part2 = f'-o {self.get_bitstream()}/evc_{self.get_videoname()}_{self.get_qp()}'
        part3 = f'> {self.get_txts()}/{self.get_videoname()}.txt'

        print(part1+part2+part3)
        os.system(part1+part2+part3)

    def decode(self):
        print("\nDECODING EVC...\n")

        decoded_path = self.get_decoded()
        p = Path('~').expanduser()
        decoded_path = decoded_path.replace('~', str(p))
        
        part1 = f'xevd_app -i {self.get_bitstream()}/evc_{self.get_videoname()}_{self.get_qp()} '
        part2 = f'-o {decoded_path}/evc_{self.get_videoname()}_{self.get_qp()}.y4m'

        print(part1+part2)
        os.system(part1+part2)


    def parse(self):        
        pattern = re.compile(r"\d+\s+\d{0,4}\s+\([IB]\)\s+\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\s+\d+")
        pattern2 = re.compile(r"\d+\.\d+\skbps")
        parameters_lines = []
        
        txt_path = f'{self.get_txts()}/{self.get_videoname()}.txt'
        p = Path('~').expanduser()
        txt_path = txt_path.replace('~', str(p))

        with open(txt_path) as temp:
            text = temp.read()
            result = pattern.findall(text)
            result2 = pattern2.findall(text)
            for line in range(len(result)):
                original_data = result[line].split()
                original_data2 = result2[line-1].split()
                POC = int(original_data[0])
                Ftype = original_data[2][1]
                QP = original_data[3]
                PSNR_Y = original_data[4]
                PSNR_U = original_data[5]
                PSNR_V = original_data[6]
                Bits = original_data[7]
                Encode_time = original_data[8]
                Bitrate = float(original_data2[0])*1024
                Bitrate = f'{Bitrate:.4f}'
                parsed_data = (POC,Ftype,QP,PSNR_U,PSNR_V,PSNR_Y,Bits,Encode_time,Bitrate)
                parameters_lines.append((parsed_data))
        temp.close()

        new_path = f'{self.get_txts()}/{self.get_videoname()}.txt'
        new_path = new_path.replace('~', str(p))

        with open(new_path) as temp:
            text = temp.readlines()
            name = self.get_videoname()
            # width = text[6].split()[2]
            # height = text[7].split()[2]
            resolution = self.get_resolution()
            fps = text[8].split()[2]
            QP= self.get_qp()
            PSNR_Y_fullvideo = text[-12].split()[3]
            PSNR_U_fullvideo = text[-11].split()[3]
            PSNR_V_fullvideo = text[-10].split()[3]
            psnr = ((4*float(PSNR_Y_fullvideo))+float(PSNR_U_fullvideo)+float(PSNR_V_fullvideo))/6
            psnr= float(f'{psnr:.4f}')
            Brate_fullvideo = float(text[-6].split()[2])*1024
            Brate_fullvideo = f'{Brate_fullvideo:.4f}'
            total_frames = text[-5].split()[4]
            time = text[-4].split()[6]
            geral_parameters = [name,resolution,fps,total_frames,QP,PSNR_Y_fullvideo,PSNR_U_fullvideo,PSNR_V_fullvideo,psnr,Brate_fullvideo]
        return sorted(parameters_lines),geral_parameters, time

    def add_to_csv(self):
        parameters = self.parse()

        info = ['video','resolution','fps','number of frames','qp', 'PSNR-Y','PSNR-U','PSNR-V','psnr','bitrate']
        header=['POC', 'Ftype', 'QP', 'PSNR-Y','PSNR-U','PSNR-V','Bits','EncT(ms)','Bitratekbps']
        
        csv_path = f'{self.get_csvs()}/{self.get_videoname()}_{self.get_qp()}.csv'
        p = Path('~').expanduser()
        csv_path = csv_path.replace('~', str(p))
        
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(info)
            writer.writerow(parameters[1])
            writer.writerow(header)
            for line in parameters[0]:
                writer.writerow(line)
        csvfile.close()

    def set_threads(self, threads: int):
        self.__threads = str(threads)
        self._options_encoder["--threads"] = str(threads)
    
    def get_threads(self) -> str:
        return self.__threads
    
    def gen_config(self):
        pass
    
