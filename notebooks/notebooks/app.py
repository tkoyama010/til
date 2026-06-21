import getfem as gf
import panel as pn
import param
import pyvista as pv
from IPython.display import IFrame

pv.set_plot_theme("document")
pn.extension()


class Veiewer(param.Parameterized):
    plotter = pv.Plotter(notebook=True)
    file_input = pn.widgets.FileInput()

    def handler(self, viewer, src, **kwargs):
        return IFrame(src, "100%", "1000px")

    @param.depends("file_input.value")
    def view(self):
        if self.file_input.value is not None:
            s = self.file_input.value.decode("utf-8")
            m = gf.Mesh("from string", s)
            m.export_to_vtk("mesh.vtk", "ascii")
            mesh = pv.read("mesh.vtk")

            self.plotter.clear()
            self.plotter.add_mesh(mesh)
        iframe = self.plotter.show(
            jupyter_backend="trame",
            jupyter_kwargs=dict(handler=self.handler),
            return_viewer=True,
        )
        return iframe


viewer = Veiewer(name="Viewer")

tabs = pn.Tabs(
    ("Mesh", viewer.file_input),
    ("Model", pn.Spacer(styles=dict(background="red"), width=500, height=1000)),
    ("View", pn.Spacer(styles=dict(background="blue"), width=500, height=1000)),
)

template = pn.template.MaterialTemplate(
    title="panel-getfem",
    sidebar=[tabs],
    main=[pn.panel(viewer.view, width=1500, height=250)],
)

template.servable()
