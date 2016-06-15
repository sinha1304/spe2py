#!/usr/bin/env python3
"""
spe2py imports a Princeton Instruments LightField (SPE 3.0) file into a python environment.
"""

import numpy as np
#import tkinter as tk
import untangle
from tkinter import filedialog as fdialog


def get_file():
    fname = fdialog.askopenfilename()
    return fname


def read_header(filename):
    f = open(filename, 'rb')
    header = np.fromfile(f, np.uint8, 4100)
    f.close()
    return header


def read_footer(filename):
    f = open(filename, 'rb')
    f.seek(678)
    footer_pos = np.fromfile(f, np.uint64, 8)[0]
    f.seek(footer_pos)

    xmlFile = open("xmlFile.tmp", 'w')
    xmlText = f.read().decode('utf-8')

    xmlFile.write(xmlText)

    loaded_footer = untangle.parse('xmlFile.tmp')

    return loaded_footer

    # TODO: parse xml with untangle package


class SPE(object):

    def __init__(self, filename, header, footer, data, xcoord, ycoord, regionsOfInterest):
        self.fid = open(filename)
        self.filename = filename
        # self.nfile = len(filename) (when mult files are done in future)
        self.header = header
        # self.footer = parse xml footer
        # self.data = read binary data
        # self.xcoord = assign xcoord from footer
        # self.ycoord = assign ycoord from footer

    def _load_size(self):
        self._xdim = np.int64(self.read_at(42, 1, np.int16)[0])
        self._ydim = np.int64(self.read_at(656, 1, np.int16)[0])

    def read_at(self, pos, size, ntype):
        self._fid.seek(pos)
        return np.fromfile(self._fid, ntype, size)

    def load_img(self):
        img = self.read_at(4100, self._xdim * self._ydim, np.uint16)
        return img.reshape((self._ydim, self._xdim))


def loadspe(filename):
    file = get_file()
    loaded_header = read_header(file)

    loaded_spe = SPE(file, loaded_header)

    return loaded_spe







