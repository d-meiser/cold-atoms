import sys
import subprocess
import tempfile
import os.path

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def notebook_run(notebook_file):
    with open(notebook_file) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=100)
        err = 0
        try:
            ep.preprocess(nb, {})
        except:
            err = 1
            raise
        finally:
            base_extension = os.path.splitext(notebook_file)
            outfile_name = base_extension[0] + '_out' + base_extension[-1]
            with open(outfile_name, mode='wt') as fout:
                nbformat.write(nb, fout)
        return err


notebooks = ['./Free particles and ballistic expansion.ipynb']


if __name__ == '__main__':
    num_errors = 0
    for n in notebooks:
        print(n + ' ... ', end="")
        sys.stdout.flush()
        err = notebook_run(n)
        num_errors += err
        if err == 0:
            print('PASS')
        else:
            print('FAIL')
    sys.exit(num_errors)

