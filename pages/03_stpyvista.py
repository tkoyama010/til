import pyvista as pv
import streamlit as st
from stpyvista import stpyvista

factor = st.sidebar.number_input('変位倍率', value=1000.0)

displacement = pv.read("displacement.vtk")
plotter = pv.Plotter()
plotter.add_mesh(displacement.warp_by_vector("u", factor=factor), show_edges=True)
plotter.view_isometric()
stpyvista(plotter)
