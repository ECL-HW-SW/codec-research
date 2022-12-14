from Codec import Codec
import os
from pathlib import Path
import csv

class VVcodec(Codec):
    def __init__(self):
        super().__init__("vvcodec")

    def encode(self) -> str:        
        print("\nENCODING VVCODEC...\n")
        
        p = str(Path('~').expanduser())     

        txt_path = self.get_txts()
        txt_path = txt_path.replace('~', p)

        options_encoder = ''
        for key, val in self.get_options_encoder().items():
            options_encoder += f"{key} {val} "

        bitstream_path = self.get_decoded()
        bitstream_path = bitstream_path.replace('~', p)
        if not os.path.exists(bitstream_path):
            os.mkdir(bitstream_path)
        
        part1 = f'{self.get_encoder()} -i {self.get_videopath()} -q {self.get_qp()} {options_encoder} '
        part2 = f'--output {self.get_bitstream()}/vvcodec_{self.get_videoname()}_{self.get_qp()}'
        part3 = f'> {txt_path}/{self.get_videoname()}.txt' # TODO: mudar isso dps
        cmdline  =part1+part2+part3 

        os.system(cmdline)
        print(cmdline) 

    def decode(self):
        print("\nDECODING VVCODEC...\n")

        p = str(Path('~').expanduser())

        decoded_path = self.get_decoded()
        decoded_path = decoded_path.replace('~', p)

        bitstream_path = self.get_bitstream()
        bitstream_path = bitstream_path.replace('~', p)
        if not os.path.exists(bitstream_path):
            print("Bitstream path does not exist.")

        part1 = f'{self.get_decoder()} -b {bitstream_path}/vvcodec_{self.get_videoname()}_{self.get_qp()} {self.get_options_decoder()} '
        part2 = f'-v 0 -f {self.get_framesnumber()} -o {decoded_path}/vvcodec_{self.get_videoname()}_{self.get_qp()}'
        cmdline = part1+part2 

        os.system(cmdline)
        print(cmdline) 

    def parse(self) -> tuple:
        """
        Parses the txt output from the encode() method.

        @return (bitrate, psnr, total time taken to encode)
        """

        p = Path('~').expanduser()
        txtoutput = f"{self.get_txts()}/{self.get_videoname()}.txt" # TODO: mudar isso dps
        txtoutput = txtoutput.replace('~', str(p))

        with open(txtoutput, 'r') as txt:
            text = txt.read().split("\n")
            for line in text:
                if "YUV-PSNR" in line.split():
                    data_line = text[text.index(line)+1].split()
                    break
            txt.close()
            bitrate = data_line[2]
            psnr = data_line[6]
            line_time = text[-2].split()
            total_time = line_time[2]

        return bitrate, psnr, total_time
    
    def add_to_csv(self):
        """
        Adds to csv: 
        encoder name | video name | video resolution | fps | frame count | qp | bitrate | PSNR | time taken to encode | optional settings

        These csvs are stored in /VC/data/vvcodec-output/csv/{videoname}/
        """
        outputcsvpath = self.get_csvs()
        p = Path('~').expanduser()
        outputcsvpath = outputcsvpath.replace('~', str(p))
        if not os.path.exists(outputcsvpath):
            os.mkdir(outputcsvpath)

        outputcsv = outputcsvpath + '/' + self.get_videoname() +'_'+ self.get_qp() + ".csv"
        bitrate, psnr, timems = self.parse()

        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["VVENC",self.get_videoname(),self.get_resolution(),self.get_fps(),
                                        self.get_framesnumber(),self.get_qp(),bitrate,psnr,timems,self.get_options_encoder()])
            metrics_file.close()

    def set_threads(self, threads: int):
        self.__threads = str(threads)
        self._options_encoder["--threads"] = str(threads)
    
    def get_threads(self) -> str:
        return self.__threads