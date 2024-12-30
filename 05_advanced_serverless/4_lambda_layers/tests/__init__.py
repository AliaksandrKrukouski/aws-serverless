import sys
from pathlib import Path

SOURCE_FOLDER = 'src'
LAYERS_FOLDER = 'src/lambdas/layers'


class ImportFromSourceContext:
    """Context object to import lambdas and packages. It's necessary because
    root path is not the path to the syndicate project but the path where
    lambdas are accumulated - SOURCE_FOLDER """

    def __init__(self, source_folder=SOURCE_FOLDER, layers_folder=LAYERS_FOLDER):
        self.source_folder = source_folder
        self.layers_folder = layers_folder
        self.assert_source_path_exists()

    @property
    def project_path(self) -> Path:
        project_path = Path(__file__).parent.parent
        print("Project path:", project_path)
        return project_path

    @property
    def source_path(self) -> Path:
        source_path = Path(self.project_path, self.source_folder)
        print("Source path:", source_path)
        return source_path

    @property
    def layers_path(self) -> Path:
        layers_path = Path(self.project_path, self.layers_folder)
        print("Layers path:", layers_path)
        return layers_path

    def assert_source_path_exists(self):
        source_path = self.source_path
        if not source_path.exists():
            print(f'Source path "{source_path}" does not exist.',
                  file=sys.stderr)
            sys.exit(1)

        layers_path = self.layers_path
        if not layers_path.exists():
            print(f'Layers path "{layers_path}" does not exist.',
                  file=sys.stderr)
            sys.exit(1)


    def _add_source_to_path(self):
        source_path = str(self.source_path)
        if source_path not in sys.path:
            print("Adding source to path:", source_path)
            sys.path.append(source_path)
        else:
            print("Source already in path:", source_path)

    def _add_layer_to_path(self):
        layers_path = str(self.layers_path)
        if layers_path not in sys.path:
            print("Adding layers to path:", layers_path)
            sys.path.append(layers_path)
        else:
            print("Layers already in path:", layers_path)

    def _remove_source_from_path(self):
        source_path = str(self.source_path)
        if source_path in sys.path:
            sys.path.remove(source_path)

    def _remove_layers_from_path(self):
        layers_path = str(self.layers_path)
        if layers_path in sys.path:
            sys.path.remove(layers_path)

    def __enter__(self):
        print("Inside __enter__:")
        self._add_source_to_path()
        self._add_layer_to_path()
        print("sys.path:", sys.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Inside __exit__:")
        self._remove_source_from_path()
        self._remove_layers_from_path()

