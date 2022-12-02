import os
import numpy as np
import unittest
from context import dpdata

class TestLmpReadFromTrajsWithRandomTypeId(unittest.TestCase):
    
    def setUp(self): 
        self.system = \
            dpdata.System(os.path.join('lammps', 'traj_with_random_type_id.dump'), fmt = 'lammps/dump', type_map = ["Ta","Nb","W","Mo","V","Al"])
    
    def test_nframes (self) :
        self.system.sort_atom_types()
        atype = self.system['atom_types'].tolist()
        self.assertTrue(atype == [1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5])
        
        coord = self.system['coords'].reshape([2, -1])

        coord0_std = np.array([6.69832  , 3.39136  , 3.34005  , 1.80744  , 5.08708  , 5.01099  ,
                               5.10512  , 5.08007  , 5.01272  , 1.70086  , 1.69544  , 1.66979  ,
                               3.48873  , 0.0697213, 6.67774  , 3.38621  , 0.033338 , 3.34239  ,
                               1.79424  , 1.7281   , 5.01015  , 3.48973  , 3.42896  , 6.67795  ,
                               3.40064  , 3.39148  , 3.34188  , 5.09069  , 1.72876  , 5.00917  ,
                               0.119885 , 6.74841  , 3.33869  , 4.99379  , 1.69262  , 1.67183  ,
                               0.199838 , 3.4185   , 6.67565  , 1.7213   , 5.05235  , 1.66373  ,
                               0.21494  , 6.77616  , 6.67623  , 5.00691  , 5.05     , 1.66532  ])
        self.assertTrue(np.allclose(coord[0, ...], coord0_std))

        coord1_std = np.array([4.85582828e+00, 5.12324490e+00, 1.55763728e+00, 1.82031828e+00,
                               1.61210490e+00, 4.91329728e+00, 5.15568828e+00, 4.91296490e+00,
                               5.02114728e+00, 1.67640828e+00, 1.62756490e+00, 1.61183728e+00,
                               3.41785828e+00, 6.54050490e+00, 3.42793728e+00, 3.39324828e+00,
                               3.47558490e+00, 6.50564728e+00, 3.43286828e+00, 3.44029490e+00,
                               3.37871728e+00, 6.60497828e+00, 3.46782490e+00, 3.42949728e+00,
                               1.82021828e+00, 5.08114490e+00, 4.93158728e+00, 5.20431828e+00,
                               1.80972490e+00, 5.00061728e+00, 6.56278828e+00, 6.62718490e+00,
                               3.35101728e+00, 4.97045828e+00, 1.80536490e+00, 1.73358728e+00,
                               6.61765828e+00, 3.43486490e+00, 6.48447728e+00, 1.57899828e+00,
                               4.89261490e+00, 1.63632728e+00, 6.59585828e+00, 1.40657901e-01,
                               6.51767728e+00, 3.30914005e+00, 7.86399766e-02, 6.66581642e-04])
        self.assertTrue(np.allclose(coord[1, ...], coord1_std))

if __name__ == '__main__':
    unittest.main()

