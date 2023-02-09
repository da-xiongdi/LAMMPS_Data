import MDAnalysis as mda
from MDAnalysis.tests.datafiles import PSF, DCD, GRO, XTC

psf = mda.Universe(PSF)
hasattr(psf, 'trajectory')