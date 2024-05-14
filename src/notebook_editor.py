import nbformat


class NotebookEditor:
    """
    A class to edit and rebuild Jupyter notebooks to ensure they are valid for GitHub.

    Attributes:
        file_path (str): The file path of the notebook to be edited.
        notebook (dict): The loaded notebook object.

    Methods:
        open_notebook(file_path):
            Opens a Jupyter notebook and loads its content.
        save_notebook(file_path=None):
            Saves the current state of the notebook to a file.
        add_cell_code(content=""):
            Adds a new code cell to the notebook.
        add_cell_markdown(content=""):
            Adds a new markdown cell to the notebook.
        rebuild_notebook(new_file_path):
            Rebuilds the notebook, ensuring all cells and outputs are correctly formatted.
    """

    def __init__(self, file_path):
        """
        Initializes the NotebookEditor with the given file path.

        Parameters:
            file_path (str): The file path of the notebook to be edited.
        """
        self.file_path = file_path
        self.notebook = self.open_notebook(file_path)

    def open_notebook(self, file_path):
        """
        Opens a Jupyter notebook and loads its content.

        Parameters:
            file_path (str): The file path of the notebook to be opened.

        Returns:
            dict: The loaded notebook object.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        return notebook

    def save_notebook(self, file_path=None):
        """
        Saves the current state of the notebook to a file.

        Parameters:
            file_path (str): The file path where the notebook will be saved.
                             If None, saves to the original file path.
        """
        if file_path is None:
            file_path = self.file_path
        with open(file_path, 'w', encoding='utf-8') as f:
            nbformat.write(self.notebook, f)

    def add_cell_code(self, content=""):
        """
        Adds a new code cell to the notebook.

        Parameters:
            content (str): The source code to be added to the new code cell.
        """
        new_cell = nbformat.v4.new_code_cell(source=content)
        self.notebook['cells'].append(new_cell)

    def add_cell_markdown(self, content=""):
        """
        Adds a new markdown cell to the notebook.

        Parameters:
            content (str): The markdown content to be added to the new markdown cell.
        """
        new_cell = nbformat.v4.new_markdown_cell(source=content)
        self.notebook['cells'].append(new_cell)

    def rebuild_notebook(self, new_file_path):
        """
        Rebuilds the notebook, ensuring all cells and outputs are correctly formatted.

        Parameters:
            new_file_path (str): The file path where the rebuilt notebook will be saved.
        """
        new_notebook = nbformat.v4.new_notebook()
        new_notebook['metadata'] = self.notebook['metadata']

        for cell in self.notebook['cells']:
            if cell['cell_type'] == 'code':
                new_cell = nbformat.v4.new_code_cell(
                    source=cell.get('source', ''),
                    execution_count=cell.get('execution_count', None),
                    outputs=cell.get('outputs', []),
                    metadata=cell.get('metadata', {})
                )
            elif cell['cell_type'] == 'markdown':
                new_cell = nbformat.v4.new_markdown_cell(
                    source=cell.get('source', ''),
                    metadata=cell.get('metadata', {})
                )
            else:
                continue
            new_notebook['cells'].append(new_cell)

        with open(new_file_path, 'w', encoding='utf-8') as f:
            nbformat.write(new_notebook, f)


if __name__ == "__main__":
    # Example
    original_file_path = "path/to/original_notebook.ipynb"
    new_file_path = "path/to/rebuilt_notebook.ipynb"

    # Initialize notebook editor with original notebook path
    nb_editor = NotebookEditor(file_path=original_file_path)

    # Rebuilds the Notebook in a valid format for Github
    nb_editor.rebuild_notebook(new_file_path=new_file_path)
