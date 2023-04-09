# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: py:percent,ipynb
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
# ---

# %% [markdown]
# # PyVistaの動作確認
#
# このノートはPyVistaの動作確認を行うために作成したものです。

# %%
import pyvista

pyvista.start_xvfb()
pyvista.set_jupyter_backend("panel")


# %%
mesh = pyvista.Sphere()
plotter = pyvista.Plotter()
plotter.add_mesh(mesh)
plotter.show()
