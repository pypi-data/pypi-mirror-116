import numpy as np
import argparse
import os
import onnx
import onnx.numpy_helper
from pathlib import Path

parser = argparse.ArgumentParser(description="Generate samples dir")
parser.add_argument('src', type=str, help='Pb data source')
args = parser.parse_args()
sample_dir = "samples"

os.makedirs(sample_dir, exist_ok=True)


def save_npy(npy, name):
    with open(name, 'wb') as f:
        np.save(f, npy)


def save_npydir(npy, dir_name):
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    npy_loaded = np.load(npy)
    for ni, n in enumerate(npy_loaded):
        with open('{}/{}.npy'.format(dir_name, ni), 'wb') as f:
            np.save(f, n)


def save_pb(npy, name):
    sample = np.load(npy)
    tensor = onnx.numpy_helper.from_array(sample)
    with open(name, 'wb') as f:
        onnx.save_tensor(tensor, f)


with open(args.src, 'rb') as f:
    tensor = onnx.TensorProto()
    tensor.ParseFromString(f.read())
    samples = onnx.numpy_helper.to_array(tensor)
samples = np.transpose(samples, (0, 2, 3, 1))
xshape = str(samples.shape).replace(", ", "x").strip("()")
sample_name = "coco_{}".format(xshape)

save_npy(samples, "{}/{}.npy".format(sample_dir, sample_name))
save_npydir("{}/{}.npy".format(sample_dir, sample_name),
            "{}/{}".format(sample_dir, sample_name))
save_pb("{}/{}.npy".format(sample_dir, sample_name),
        "{}/{}.pb".format(sample_dir, sample_name))
