import numpy as np
import astroalign

src = [(0, 0), (1, 0), (1, 1), (0, 1)]
sky = [(0,0), (2,0), (2,2), (0,2)]
src = np.array(src)
sky = np.array(sky)
transf = astroalign.estimate_transform('affine', src, sky)
inv_transf = astroalign.estimate_transform('affine', sky, src)

src_points = np.array([(0, 0), (0.5, 0.5)])
sky_points = astroalign.matrix_transform(src_points, transf.params)
print(sky_points)

print(astroalign.matrix_transform(src, transf.params))
print(astroalign.matrix_transform(sky, inv_transf.params))