import os
import json
import csv
from pathlib import Path
from Codec import Codec

class svt_codec(Codec):

    def __init__(self):
        super().__init__('svt')
        
        self.__passes = self._options_encoder["--passes"]
        self.__rc = self._options_encoder["--rc"]

        svt_path = '~/VC/codec-research/code/codecs/JSON_files/paths.JSON'
        p = Path('~').expanduser()
        svt_path = svt_path.replace('~', str(p))

        with open(svt_path) as json_file:
            data = json.load(json_file)
            self.__decoder = data['svt']['decoder']
            self.__outtime = data['svt']['outtime']

    def get_outtime(self):
        return self.__outtime

    def encode(self):
        print("\nENCODING  SVT...\n")
                
        bitstream_path = self.get_bitstream()
        p = Path('~').expanduser()
        bitstream_path = bitstream_path.replace("~",str(p))
        if not(os.path.exists(bitstream_path)):
            os.mkdir(bitstream_path)
        
        options_encoder = ""
        for flag, val in self.get_options_encoder().items():
            options_encoder += f"{flag} {val} "

        # TODO: fix part 4 to be up to standard with the others        
        part1 = f"{self.get_encoder()} --enable-stat-report 1 --stat-file {self.get_txts()}/{self.get_videoname()}.txt "
        part2 = f"--crf {self.get_qp()} {options_encoder} -i {self.get_videopath()} "
        part3 = f"--output {self.get_bitstream()}/svt_{self.get_videoname()}_{self.get_qp()} 2>"
        part4 = f"{self.get_outtime()}/{self.get_videoname()}_time.txt" # TODO: fix this
        cmdline = part1+part2+part3+part4

        print(cmdline)    #@fix
        os.system(cmdline)    #@fix

    def decode(self):     
        print("\nDECODING SVT...\n")

        decoded_path = self.get_decoded()
        p1 = Path('~').expanduser()
        decoded_path = decoded_path.replace('~', str(p1))

        bitstream_path = self.get_bitstream()
        p2 = Path('~').expanduser()
        bitstream_path = bitstream_path.replace('~', str(p2))
        if not os.path.exists(bitstream_path):
            print("Bitstream path does not exist.")

        part1 = f"{self.get_decoder()} {self.get_options_decoder()} -i {self.get_bitstream()}/svt_{self.get_videoname()}_{self.get_qp()} "
        part2 = f"-o {decoded_path}/svt_{self.get_videoname()}_{self.get_qp()}"
        cmdline = part1+part2

        print(cmdline)
        os.system(cmdline)  

    def parse(self):
        outgen = f"{self.get_txts()}/{self.get_videoname()}.txt"
        outtime = f"{self.get_outtime()}/{self.get_videoname()}_time.txt"

        p = Path('~').expanduser()
        outgen=outgen.replace("~",str(p))
        outtime=outtime.replace("~",str(p))
        
        bitrate, psnr, timems = self._parse_svt_output(outgen,outtime)
        return bitrate, psnr, timems/1000

    def add_to_csv(self):
        outputcsvpath = self.get_csvs()
        p = Path('~').expanduser()
        outputcsvpath = outputcsvpath.replace("~",str(p))
        if not(os.path.exists(outputcsvpath)):
            os.mkdir(outputcsvpath)
        outputcsv = outputcsvpath + '/' + self.get_videoname() +'_'+ self.get_qp() + ".csv"
        bitrate,psnr,timems = self.parse()
        outputcsv = outputcsv.replace("~",str(p))
        with open(outputcsv, 'w', newline='') as metrics_file:
            metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics_writer.writerow(['encoder','video','resolution','fps','number of frames','qp','bitrate', 'psnr', 'timems','optional settings'])
            metrics_writer.writerow(["SVT-AV1",self.get_videoname(),self.get_resolution(),self.get_fps(),self.get_framesnumber(),self.get_qp(),bitrate,psnr,timems,self.get_options_encoder()])
            metrics_file.close()

    def _parse_svt_output(self,pt1,pt2):

        BR_STRING = 'Total Frames	Average QP  	Y-PSNR   	U-PSNR   	V-PSNR		| 	Y-PSNR   	U-PSNR   	V-PSNR   	|	Y-SSIM   	U-SSIM   	V-SSIM   	|	Bitrate\n'
        with open(pt1, 'r') as output_text:
            out_string = output_text.readlines()
            results_index = (out_string.index(BR_STRING) + 1)
            bitrate_string = out_string[results_index].split()[20]
            psnr_string = out_string[results_index].split()[2]
        with open(pt2, 'rt') as outtime_text:
            outtime_string = outtime_text.readlines()
        for strtime in outtime_string:
            if not strtime.startswith("Total Encoding Time"):
                continue
            timems_string = strtime.split()[3]
        return float(bitrate_string)*1024, float(psnr_string) , float(timems_string)

    def set_threads(self, threads: int):
        self.__threads = str(threads)
        self._options_encoder["--lp"] = str(threads)

    def get_threads(self) -> str: # TODO: arrumar isso dps
        return self.__threads

