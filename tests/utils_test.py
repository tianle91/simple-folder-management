from tests.utils import make_files_at_dir
import os 
import tempfile

def test_make_files_at_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        make_files_at_dir(tmp_dir, ['a/b/c.txt', 'd/e/f.txt'])
        assert os.path.exists(os.path.join(tmp_dir, 'a/b/c.txt'))
        assert os.path.exists(os.path.join(tmp_dir, 'd/e/f.txt'))
