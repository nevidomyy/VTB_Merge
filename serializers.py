import os
import re
import typing
import datetime
from abc import ABC, abstractmethod


class ABCRegistry(ABC):
    _encoding = str()
    _bank_name = str()
    compile = typing.Pattern

    @property
    def filename(self):
        if hasattr(self, 'filepath'):
            return os.path.basename(self.filepath)

    @property
    def encoding(self):
        return self._encoding

    @property
    def bank_name(self):
        return self._bank_name

    @abstractmethod
    def serialize(self, data: str) -> str:
        """ This method search and return line over template in file"""
        pass


class RegistryFactory:
    registry_objects: list = list()

    def __init__(self, filepath: str):
        self._registry_object = self._registry_init(filepath)

    def _registry_init(self, filepath: str) -> ABCRegistry:
        filename = os.path.basename(filepath)
        for obj in self.registry_objects:
            if obj.compile.search(filename):
                obj = obj()
                obj.filepath = filepath
                return obj

    def merge(self,
              output_file: str,
              filenumber: int,
              filecount: int,
              registry_number: str,
              company_name: str,
              line_count: str,
              summ: str):
        if self._registry_object is None:
            return
        with open(
                self._registry_object.filepath, mode='r',
                encoding=self._registry_object.encoding
        ) as fr, open(output_file, mode='a', encoding='UTF-8') as fw:
            if filenumber == 0:
                date = datetime.datetime.now()
                fw.write('START;' + date.strftime('%d') +
                         date.strftime('%m') + date.strftime('%Y') + ';' +
                         registry_number + ';' + 'CREDIT' + ';'
                         + company_name + '\n')
            for line in fr:
                serialized_line = (self._registry_object.serialize(line))
                if serialized_line is not None:
                    fw.write(serialized_line)
            if filenumber == filecount - 1:
                fw.write('END;' + line_count + ';' + summ + ';' + 'RUR' + '\n')

    def get_info(self) -> dict | None:
        if self._registry_object is None:
            return
        summ = float()
        line_count = int()
        with open(self._registry_object.filepath, mode='r',
                  encoding=self._registry_object.encoding) as f:
            for line in f:
                serialized_line = self._registry_object.serialize(line)
                if serialized_line is not None:
                    summ += (float(serialized_line.split(';')[1].replace(',', '.')))
                    line_count += 1

            return {'summ': round(summ, 2),
                    'line_count': line_count,
                    'bank_name': self._registry_object.bank_name,
                    'filename': self._registry_object.filename
                    }


def registrar(cls):
    RegistryFactory.registry_objects.append(cls)
    return cls


@registrar
class VTB(ABCRegistry):
    _encoding = 'utf-8'
    _bank_name = 'ВТБ'
    compile = re.compile('^Z_\d{10}_\d{8}_\d+.*\.txt$')

    def serialize(self, line: str) -> str:
        if re.search(r'\d{20};\d+,\d{2};\D+;.*;\d;(\d+,\d{2})?;;\d*$', line):
            return line


@registrar
class RNCB(ABCRegistry):
    _encoding = 'cp1251'
    _bank_name = 'РНКБ'
    compile = re.compile('^test_rncb+')

    def serialize(self, line: str) -> str:
        if re.search(r'\d{20};.+', line):
            data = line.split(';')
            account = data[0]
            summ = data[1]
            full_name = data[2]
            snils = data[3]
            flag = data[4]
            rent = data[5]
            flag2 = data[6]
            bik = data[7]

            line = account + ';' + summ + ';' + full_name + ';' + snils + ';' + flag + ';' + rent + ';' + flag2 + ';' + bik
            return line
