import os
import shutil
import unittest

import numpy as np
from comp_sys import CompLabeledSys
from comp_sys import CompSys
from context import dpdata


class TestDeepmdLoadRaw(unittest.TestCase, CompLabeledSys):
    def setUp(self):
        self.system_1 = dpdata.LabeledSystem("poscars/OUTCAR.h2o.md",
                                             fmt="vasp/outcar")
        self.system_2 = dpdata.LabeledSystem("poscars/deepmd.h2o.md",
                                             fmt="deepmd/raw",
                                             type_map=["O", "H"])
        self.places = 6
        self.e_places = 6
        self.f_places = 6
        self.v_places = 6


class TestDeepmdDumpRaw(unittest.TestCase, CompLabeledSys):
    def setUp(self):
        self.system_1 = dpdata.LabeledSystem("poscars/OUTCAR.h2o.md",
                                             fmt="vasp/outcar")
        self.system_1.to_deepmd_raw("tmp.deepmd")
        self.system_2 = dpdata.LabeledSystem("tmp.deepmd", type_map=["O", "H"])
        self.places = 6
        self.e_places = 6
        self.f_places = 6
        self.v_places = 6

    def tearDown(self):
        if os.path.exists("tmp.deepmd"):
            shutil.rmtree("tmp.deepmd")


class TestDeepmdRawNoLabels(unittest.TestCase, CompSys):
    def setUp(self):
        self.system_1 = dpdata.System("poscars/POSCAR.h2o.md",
                                      fmt="vasp/poscar")
        self.system_1.to_deepmd_raw("tmp.deepmd")
        self.system_2 = dpdata.System("tmp.deepmd",
                                      fmt="deepmd/raw",
                                      type_map=["O", "H"])
        self.places = 6
        self.e_places = 6
        self.f_places = 6
        self.v_places = 6

    def tearDown(self):
        if os.path.exists("tmp.deepmd"):
            shutil.rmtree("tmp.deepmd")


class TestDeepmdCompNoLabels(unittest.TestCase, CompSys):
    def setUp(self):
        self.dir_name = "tmp.deepmd.nol"
        natoms = 3
        atom_names = ["O", "H"]
        atom_numbs = [1, 2]
        atom_types = np.array([0, 1, 1], dtype=np.int32)
        nframes = 11
        os.makedirs(self.dir_name, exist_ok=True)
        np.savetxt(os.path.join(self.dir_name, "type.raw"),
                   atom_types,
                   fmt="%d")

        coords = np.random.random([nframes, natoms, 3])
        cells = np.random.random([nframes, 3, 3])
        np.savetxt(
            os.path.join(self.dir_name, "", "coord.raw"),
            np.reshape(coords, [nframes, -1]),
        )
        np.savetxt(os.path.join(self.dir_name, "", "box.raw"),
                   np.reshape(cells, [nframes, -1]))

        data = {
            "atom_names": atom_names,
            "atom_types": atom_types,
            "atom_numbs": atom_numbs,
            "coords": coords,
            "cells": cells,
            "orig": np.zeros(3),
        }

        self.system_1 = dpdata.System(self.dir_name,
                                      fmt="deepmd/raw",
                                      type_map=["O", "H"])
        self.system_2 = dpdata.System()
        self.system_2.data = data

        self.places = 6
        self.e_places = 6
        self.f_places = 6
        self.v_places = 6

    def tearDown(self):
        if os.path.exists(self.dir_name):
            shutil.rmtree(self.dir_name)


if __name__ == "__main__":
    unittest.main()
