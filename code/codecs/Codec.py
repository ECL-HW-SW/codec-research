from abc import ABC, abstractclassmethod, abstractmethod

class Codec(ABC):
    @abstractmethod
    def __init__(self,bit_stream_path,output_path):
        self.__bit_stream_path = bit_stream_path
        self.__output_path = output_path

    def get_bit_stream_path(self):
        return self.__bit_stream_path

    def set_bit_stream_path(self, bit_stream_path):
        self.__bit_stream_path = bit_stream_path

    def get_output_path(self):
        return self.__output_path

    def set_output_path(self, output_path):
        self.__output_path = output_path

    @abstractmethod
    def encode(self):
        pass

    @abstractmethod
    def decode(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def gen_config(self):
        pass
