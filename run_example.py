import numpy as np
import sys
sys.path.insert(0, './utils/')
import MESH
import FunctionalMap as fMap
import MeshProcess
from scipy.sparse import csr_matrix, spdiags
import time
from scipy import spatial

start = time.time()

DATASET_PATH = 'FAUST_shapes_off/'

s1_name = "tr_reg_000.off"

s2_name = "tr_reg_001.off"

# Load two meshes
t_load = time.time()
S1 = MESH.mesh_load_and_preprocess(DATASET_PATH + s1_name, numEigs=100)
S2 = MESH.mesh_load_and_preprocess(DATASET_PATH + s2_name, numEigs=100)
print("Shapes loaded in : %.2fs " % (time.time()-t_load))

# compute the wave kernel signatures
t_desc = time.time()
desc1 = fMap.wave_kernel_signature(S1.evecs, S1.evals, S1.A, numTimes=100, ifNormalize=True)
desc1 = desc1[:, np.arange(0, 100, 20)]
desc2 = fMap.wave_kernel_signature(S2.evecs, S2.evals, S2.A, numTimes=100, ifNormalize=True)
desc2 = desc2[:, np.arange(0, 100, 20)]
print("Descriptors calculated in : %.2fs " % (time.time()-t_desc))


param = dict()
param['fMap_size'] = [100, 100]
param['weight_descriptor_preservation'] = 1
param['weight_laplacian_commutativity'] = 1
param['weight_descriptor_commutativity'] = 1
param['weight_descriptor_orientation'] = 1


C12 = fMap.compute_functional_map_from_descriptors(S1, S2, desc1, desc2, param)

B1 = S1.evecs[:, 0:param['fMap_size'][0]]
B2 = S2.evecs[:, 0:param['fMap_size'][1]]



T21 = fMap.convert_functional_map_to_pointwise_map(C12, B1, B2)

C12_new = np.linalg.lstsq(B2, B1[T21, :], rcond=None)[0]
T21_new = fMap.convert_functional_map_to_pointwise_map(C12_new, B1, B2)
print(T21_new[0:15])
print("Total runtime : %.2fs" % (time.time()-start))
