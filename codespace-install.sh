conda config --add channels conda-forge
conda config --set channel_priority strict
conda update conda
conda install getfem==5.4.2 -y
conda install pyvista==0.38.5 -y
