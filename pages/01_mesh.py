import getfem as gf
import numpy as np
import pyvista as pv
import streamlit as st
from stpyvista import stpyvista

d = st.sidebar.number_input('直径(mm)', value=100.0)
L = st.sidebar.number_input('高さ(mm)', value=500.0)
T = st.sidebar.number_input('トルク(N mm)', value=1.0e06)


rhos = np.linspace(0.0001, d / 2, 8 + 1)
phis = np.linspace(0.0, 2.0 * np.pi, 16 + 1)
zs = np.linspace(L, 0.0, 25 + 1)
mesh = gf.Mesh("empty", 3)

rho_as = rhos[:-1]
rho_bs = rhos[1:]
phi_as = phis[:-1]
phi_bs = phis[1:]
z_as = zs[:-1]
z_bs = zs[1:]

for z_a, z_b in zip(z_as, z_bs):
    for phi_a, phi_b in zip(phi_as, phi_bs):
        for rho_a, rho_b in zip(rho_as, rho_bs):
            mesh.add_convex(
                gf.GeoTrans("GT_QK(3,1)"),
                [
                    [
                        rho_a * np.cos(phi_a),
                        rho_a * np.cos(phi_b),
                        rho_b * np.cos(phi_a),
                        rho_b * np.cos(phi_b),
                        rho_a * np.cos(phi_a),
                        rho_a * np.cos(phi_b),
                        rho_b * np.cos(phi_a),
                        rho_b * np.cos(phi_b),
                    ],
                    [
                        rho_a * np.sin(phi_a),
                        rho_a * np.sin(phi_b),
                        rho_b * np.sin(phi_a),
                        rho_b * np.sin(phi_b),
                        rho_a * np.sin(phi_a),
                        rho_a * np.sin(phi_b),
                        rho_b * np.sin(phi_a),
                        rho_b * np.sin(phi_b),
                    ],
                    [z_a, z_a, z_a, z_a, z_b, z_b, z_b, z_b],
                ],
            )

mesh.export_to_vtk("mesh.vtk", "ascii")
mesh.save("mesh.msh")

a = [d / 2.0, 0.0, 0.0]
b = [d / 2.0, 0.0, L]
line = pv.Line(a, b)

m = pv.read("mesh.vtk")
plotter = pv.Plotter()
plotter.add_mesh(m, show_edges=True)
plotter.add_mesh(line, color="white", line_width=10)
plotter.add_point_labels(
    [a, b], ["A", "B"], font_size=48, point_color="red", text_color="red"
)
plotter.view_isometric()
stpyvista(plotter)
