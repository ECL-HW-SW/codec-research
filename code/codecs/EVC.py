from Codec import Codec
import os
import re
import csv

class EVC(Codec):
    def __init__(self,codec):
        super().__init__(codec)
        
    def encode(self):
        bitstream_path = self.get_bitstream()
        if not(os.path.exists(bitstream_path)):
            os.mkdir(bitstream_path)
        part1 = f'xeve_app -i {self.get_videopath()} -v 3 -q {self.get_qp()} --preset fast '
        part2 = f'-o {self.get_bitstream()}/{self.get_videoname()}{self.get_qp()}.evc'
        part3 = f'> {self.get_txts()}/{self.get_videoname()}.txt'
        print(part1+part2+part3)
        os.system(part1+part2+part3)

    def decode(self,input,output,preset):
        os.system(f'xevd_app -i {self.get_bitstream_path()}/{input} -o {self.get_decoded_path()}/{preset}_{output}')
    
    def parse(self):
        
        pattern = re.compile(r"\d+\s+\d{0,4}\s+\([IB]\)\s+\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\s+\d+")
        pattern2 = re.compile(r"\d+\.\d+\skbps")
        parameters_lines = []

        with open(f'{self.get_txts()}/{self.get_videoname()}.txt') as temp:
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
                Bitrate = original_data2[0]
                parsed_data = (POC,Ftype,QP,PSNR_U,PSNR_V,PSNR_Y,Bits,Encode_time,Bitrate)
                parameters_lines.append((parsed_data))
        temp.close()

        with open(f'{self.get_txts()}/{self.get_videoname()}.txt') as temp:
            text = temp.readlines()
            name = self.get_videoname()
            width = text[6].split()[2]
            height = text[7].split()[2]
            resolution = f'{width}x{height}'
            fps = text[8].split()[2]
            QP= self.get_qp()
            PSNR_Y_fullvideo = text[-12].split()[3]
            PSNR_U_fullvideo = text[-11].split()[3]
            PSNR_V_fullvideo = text[-10].split()[3]
            Brate_fullvideo = text[-6].split()[2]
            total_frames = text[-5].split()[4]
            geral_parameters = [name,resolution,fps,total_frames,QP,PSNR_Y_fullvideo,PSNR_U_fullvideo,PSNR_V_fullvideo,Brate_fullvideo]
        return sorted(parameters_lines),geral_parameters

    def add_to_csv(self,parameters):
        info = ['video','resolution','fps','number of frames','qp', 'PSNR-Y','PSNR-U','PSNR-V','bitrate']
        header=['POC', 'Ftype', 'QP', 'PSNR-Y','PSNR-U','PSNR-V','Bits','EncT(ms)','Bitratekbps']
        with open(f'{self.get_csvs()}/{self.get_videoname()}{self.get_qp()}parameters_frames.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(info)
            writer.writerow(parameters[1])
            writer.writerow(header)
            for line in parameters[0]:
                writer.writerow(line)
        csvfile.close()

    def gen_config(self):
        pass
