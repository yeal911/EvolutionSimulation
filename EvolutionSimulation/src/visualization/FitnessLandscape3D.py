from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
import numpy as np

try:
    import pyqtgraph.opengl as gl
    HAS_OPENGL = True
except Exception:
    HAS_OPENGL = False


class FitnessLandscape3D(QWidget):
    """3D fitness landscape: X/Y = gene dims, Z = avg offspring."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        if not HAS_OPENGL:
            self.layout.addWidget(QLabel("PyOpenGL not installed. 3D view unavailable.\nInstall with: pip install PyOpenGL"))
            self.view = None
            return
        self.view = gl.GLViewWidget()
        self.layout.addWidget(self.view)
        self.view.setCameraPosition(distance=200, elevation=30, azimuth=45)
        self.gene_x = 0
        self.gene_y = 1
        self.surface = None
        self.scatter = None

    def set_gene_dims(self, x, y):
        self.gene_x = x
        self.gene_y = y

    def update_landscape(self, threads):
        if not HAS_OPENGL or self.view is None:
            return
        # Collect all dead individuals with known parents (offspring count proxy)
        all_dead = []
        for thread in threads:
            if thread.THREAD_TYPE == "Animal":
                all_dead.extend(thread.dead)
        if len(all_dead) < 10:
            return

        # Grid gene space
        grid = 20
        x_vals = np.linspace(0, 99, grid)
        y_vals = np.linspace(0, 99, grid)
        Z = np.zeros((grid, grid))

        for i, xv in enumerate(x_vals):
            for j, yv in enumerate(y_vals):
                nearby = [ind for ind in all_dead
                          if abs(ind.gene.geneDigits[self.gene_x] - xv) < 5
                          and abs(ind.gene.geneDigits[self.gene_y] - yv) < 5]
                if nearby:
                    Z[j, i] = np.mean([ind.lifespan + ind.fightCapability for ind in nearby])
                else:
                    Z[j, i] = 0

        if self.surface:
            self.view.removeItem(self.surface)

        self.surface = gl.GLSurfacePlotItem(x=x_vals, y=y_vals, z=Z, shader='heightColor',
                                             computeNormals=False, smooth=False)
        self.surface.translate(-50, -50, 0)
        self.view.addItem(self.surface)
