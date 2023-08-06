import unittest
import numpy as np
import shutil
import pathlib
import os
from onnc.bench.get_dataset import get_dataset
TEST_DIR = pathlib.Path("test_get_dataset_tmp")


class TestGetDataset(unittest.TestCase):
    n = np.random.rand(10, 2, 2, 3)

    def setUp(self):
        os.mkdir(TEST_DIR)

    def common_run(self, x):
        dataset = get_dataset(x, k_samples=5)
        self.assertEqual(dataset.sample_size, 5)
        dataset = get_dataset(x, k_samples=20)
        self.assertEqual(dataset.sample_size, 10)
        dataset1 = get_dataset(x, k_samples=10, shuffle=True, seed=1)
        dataset2 = get_dataset(x, k_samples=10, shuffle=True, seed=2)

        self.assertFalse((dataset1.samples == dataset2.samples).all())

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def test_npy(self):
        path = str(TEST_DIR / 'sample.npy')
        np.save(path, self.n)
        dataset = get_dataset(path, k_samples=5)
        self.common_run(path)

    def test_npydir(self):
        sample_dir = TEST_DIR / "sample_dir"
        os.mkdir(sample_dir)
        for i in range(10):
            np.save(sample_dir / (str(i) + ".npy"), self.n[i])
        self.common_run(str(sample_dir))

    def test_npz(self):
        path = str(TEST_DIR / 'sample.npz')
        np.savez(path, self.n)
        self.common_run(path)

    def test_np_ndarray(self):
        self.common_run(self.n)

    def test_np_memmap(self):
        path = str(TEST_DIR / 'sample.npy')
        np.save(path, self.n)
        mmap_obj = np.load(path, mmap_mode='r')
        self.common_run(mmap_obj)

    def test_npzfileobject(self):
        path = str(TEST_DIR / 'sample.npz')
        np.savez(path, self.n)
        npz_file_obj = np.load(path)
        self.common_run(npz_file_obj)

    def test_pb(self):
        import onnx.numpy_helper
        path = str(TEST_DIR / 'sample.pb')
        with open(path, 'wb') as f:
            f.write(onnx.numpy_helper.from_array(self.n).SerializeToString())
        self.common_run(path)


if __name__ == '__main__':
    unittest.main()
