"""# Import Hook
"""
import os
import sys
import traceback
import typing as tp
from pathlib import Path
from nbconvert import Exporter
from traitlets import Bool, Instance, Type, default
from ..core.exporter import LiteraryExporter
from ..core.project import ProjectOperator
from .finder import inject_loaders
from .loader import NotebookLoader
from .patch import patch

class ProjectImporter(ProjectOperator):
    exporter = Instance(Exporter)
    exporter_class = Type(LiteraryExporter, help='Exporter class').tag(config=True)
    set_except_hook = Bool(True, help='Overwrite `sys.excepthook` to correctly display tracebacks').tag(config=True)
    allow_absolute_local_imports = Bool(True, help='Allow absolute imports of Python scripts / notebooks in the current working directory').tag(config=True)

    @default('exporter')
    def _exporter_default(self):
        return self.exporter_class(parent=self)

    def determine_package_name(self, path: Path) -> str:
        """Determine the corresponding importable name for a package directory given by
    a particular file path. Return `None` if path is not contained within `sys.path`.

    :param path: path to package
    :return:
    """
        for p in sys.path:
            if str(path) == p:
                continue
            try:
                relative_path = path.relative_to(p)
            except ValueError:
                continue
            return '.'.join(relative_path.parts)
        return None

    def install_hook(self):
        """Install notebook import hook

    Don't allow the user to specify a custom search path, because we also need this to
    interoperate with the default Python module importers which use sys.path

    :return:
    """
        cwd = Path.cwd()
        sys.path.append(str(self.packages_path))
        if not self.allow_absolute_local_imports:
            sys.path = [p for p in sys.path if Path(p).resolve() != cwd]
        exporter = self.exporter_class(parent=self)

        def create_notebook_loader(fullname, path):
            return NotebookLoader(fullname, path, exporter=exporter)
        inject_loaders(sys.path_hooks, (create_notebook_loader, ['.ipynb']))
        if self.set_except_hook:
            sys.excepthook = traceback.print_exception

    def update_namespace(self, namespace):
        cwd = Path.cwd()
        namespace.update({'__package__': self.determine_package_name(cwd), 'patch': patch})