#  CREDIT: All the of this file is taken from the repository: https://github.com/williamjameshandley/py2nb

import os

import nbformat.v4


def new_cell(nb, cell, markdown=False):
    """ Create a new cell

    Parameters
    ----------
    nb: nbformat.notebooknode.NotebookNode
        Notebook to write to, as produced by nbformat.v4.new_notebook()

    cell: str
        String to write to the cell

    markdown: boolean, optional, (default False)
        Whether to create a markdown cell, or a code cell
    """
    cell = cell.rstrip().lstrip()
    if cell:
        if markdown:
            cell = nbformat.v4.new_markdown_cell(cell)
        else:
            cell = nbformat.v4.new_code_cell(cell)
        nb.cells.append(cell)
    return ''


def convert(folder_path, script_name='script.py'):
    """ Convert the python script to jupyter notebook"""
    if not os.path.isdir(folder_path):
        raise ValueError('folder_path argument must be a valid path for the folder containing the script file.')
    script_path = os.path.join(folder_path, script_name)
    if not os.path.isfile(script_path):
        raise FileNotFoundError()
    with open(script_path) as f:
        markdown_cell = ''
        code_cell = ''
        nb = nbformat.v4.new_notebook()
        for line in f:
            if line[:2] == '#-' or line[:2] == '#|':
                code_cell = new_cell(nb, code_cell)
                if line[:2] == '#|':
                    markdown_cell += line[2:]
                else:
                    markdown_cell = new_cell(nb, markdown_cell, markdown=True)
            else:
                markdown_cell = new_cell(nb, markdown_cell, markdown=True)
                code_cell += line

        markdown_cell = new_cell(nb, markdown_cell, markdown=True)
        code_cell = new_cell(nb, code_cell)

        nbformat.write(nb, os.path.join(folder_path, 'script.ipynb'))
