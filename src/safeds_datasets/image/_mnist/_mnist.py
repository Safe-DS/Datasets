import gzip
import os
import struct
import sys
import urllib.request
from array import array
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.error import HTTPError

import torch
from safeds._config import _init_default_device
from safeds.data.image.containers._single_size_image_list import _SingleSizeImageList
from safeds.data.labeled.containers import ImageDataset
from safeds.data.tabular.containers import Column

if TYPE_CHECKING:
    from safeds.data.image.containers import ImageList

_mnist_links: list[str] = ["http://yann.lecun.com/exdb/mnist/", "https://ossci-datasets.s3.amazonaws.com/mnist/"]
_mnist_files: dict[str, str] = {
    "train-images-idx3": "train-images-idx3-ubyte.gz",
    "train-labels-idx1": "train-labels-idx1-ubyte.gz",
    "test-images-idx3": "t10k-images-idx3-ubyte.gz",
    "test-labels-idx1": "t10k-labels-idx1-ubyte.gz",
}
_mnist_labels: dict[int, str] = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9"}
_mnist_folder: str = "mnist"

_fashion_mnist_links: list[str] = ["http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/"]
_fashion_mnist_files: dict[str, str] = _mnist_files
_fashion_mnist_labels: dict[int, str] = {
    0: "T-shirt/top",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle boot",
}
_fashion_mnist_folder: str = "fashion-mnist"

_kuzushiji_mnist_links: list[str] = ["http://codh.rois.ac.jp/kmnist/dataset/kmnist/"]
_kuzushiji_mnist_files: dict[str, str] = _mnist_files
_kuzushiji_mnist_labels: dict[int, str] = {
    0: "\u304a",
    1: "\u304d",
    2: "\u3059",
    3: "\u3064",
    4: "\u306a",
    5: "\u306f",
    6: "\u307e",
    7: "\u3084",
    8: "\u308c",
    9: "\u3092",
}
_kuzushiji_mnist_folder: str = "kmnist"


def load_mnist(path: str | Path, download: bool = True) -> tuple[ImageDataset[Column], ImageDataset[Column]]:
    """
    Load the `MNIST <http://yann.lecun.com/exdb/mnist/>`_ datasets.

    Parameters
    ----------
    path:
        the path were the files are stored or will be downloaded to
    download:
        whether the files should be downloaded to the given path

    Returns
    -------
    train_dataset, test_dataset:
        The train and test datasets.

    Raises
    ------
    FileNotFoundError
        if a file of the dataset cannot be found
    """
    path = Path(path) / _mnist_folder
    path.mkdir(parents=True, exist_ok=True)
    path_files = os.listdir(path)
    missing_files = []
    for file_path in _mnist_files.values():
        if file_path not in path_files:
            missing_files.append(file_path)
    if len(missing_files) > 0:
        if download:
            _download_mnist_like(
                path,
                {name: f_path for name, f_path in _mnist_files.items() if f_path in missing_files},
                _mnist_links,
            )
        else:
            raise FileNotFoundError(f"Could not find files {[str(path / file) for file in missing_files]}")
    return _load_mnist_like(path, _mnist_files, _mnist_labels)


def load_fashion_mnist(path: str | Path, download: bool = True) -> tuple[ImageDataset[Column], ImageDataset[Column]]:
    """
    Load the `Fashion-MNIST <https://github.com/zalandoresearch/fashion-mnist>`_ datasets.

    Parameters
    ----------
    path:
        the path were the files are stored or will be downloaded to
    download:
        whether the files should be downloaded to the given path

    Returns
    -------
    train_dataset, test_dataset:
        The train and test datasets.

    Raises
    ------
    FileNotFoundError
        if a file of the dataset cannot be found
    """
    path = Path(path) / _fashion_mnist_folder
    path.mkdir(parents=True, exist_ok=True)
    path_files = os.listdir(path)
    missing_files = []
    for file_path in _fashion_mnist_files.values():
        if file_path not in path_files:
            missing_files.append(file_path)
    if len(missing_files) > 0:
        if download:
            _download_mnist_like(
                path,
                {name: f_path for name, f_path in _fashion_mnist_files.items() if f_path in missing_files},
                _fashion_mnist_links,
            )
        else:
            raise FileNotFoundError(f"Could not find files {[str(path / file) for file in missing_files]}")
    return _load_mnist_like(path, _fashion_mnist_files, _fashion_mnist_labels)


def load_kmnist(path: str | Path, download: bool = True) -> tuple[ImageDataset[Column], ImageDataset[Column]]:
    """
    Load the `Kuzushiji-MNIST <https://github.com/rois-codh/kmnist>`_ datasets.

    Parameters
    ----------
    path:
        the path were the files are stored or will be downloaded to
    download:
        whether the files should be downloaded to the given path

    Returns
    -------
    train_dataset, test_dataset:
        The train and test datasets.

    Raises
    ------
    FileNotFoundError
        if a file of the dataset cannot be found
    """
    path = Path(path) / _kuzushiji_mnist_folder
    path.mkdir(parents=True, exist_ok=True)
    path_files = os.listdir(path)
    missing_files = []
    for file_path in _kuzushiji_mnist_files.values():
        if file_path not in path_files:
            missing_files.append(file_path)
    if len(missing_files) > 0:
        if download:
            _download_mnist_like(
                path,
                {name: f_path for name, f_path in _kuzushiji_mnist_files.items() if f_path in missing_files},
                _kuzushiji_mnist_links,
            )
        else:
            raise FileNotFoundError(f"Could not find files {[str(path / file) for file in missing_files]}")
    return _load_mnist_like(path, _kuzushiji_mnist_files, _kuzushiji_mnist_labels)


def _load_mnist_like(
    path: str | Path,
    files: dict[str, str],
    labels: dict[int, str],
) -> tuple[ImageDataset[Column], ImageDataset[Column]]:
    _init_default_device()

    path = Path(path)
    test_labels: Column | None = None
    train_labels: Column | None = None
    test_image_list: ImageList | None = None
    train_image_list: ImageList | None = None
    for file_name, file_path in files.items():
        if "idx1" in file_name:
            with gzip.open(path / file_path, mode="rb") as label_file:
                magic, size = struct.unpack(">II", label_file.read(8))
                if magic != 2049:
                    raise ValueError(f"Magic number mismatch. Actual {magic} != Expected 2049.")  # pragma: no cover
                if "train" in file_name:
                    train_labels = Column(
                        file_name,
                        [labels[label_index] for label_index in array("B", label_file.read())],
                    )
                else:
                    test_labels = Column(
                        file_name,
                        [labels[label_index] for label_index in array("B", label_file.read())],
                    )
        else:
            with gzip.open(path / file_path, mode="rb") as image_file:
                magic, size, rows, cols = struct.unpack(">IIII", image_file.read(16))
                if magic != 2051:
                    raise ValueError(f"Magic number mismatch. Actual {magic} != Expected 2051.")  # pragma: no cover
                image_data = array("B", image_file.read())
                image_tensor = torch.empty(size, 1, rows, cols, dtype=torch.uint8)
                for i in range(size):
                    image_tensor[i, 0] = torch.frombuffer(
                        image_data[i * rows * cols : (i + 1) * rows * cols],
                        dtype=torch.uint8,
                    ).reshape(rows, cols)
                image_list = _SingleSizeImageList()
                image_list._tensor = image_tensor
                image_list._tensor_positions_to_indices = list(range(size))
                image_list._indices_to_tensor_positions = image_list._calc_new_indices_to_tensor_positions()
                if "train" in file_name:
                    train_image_list = image_list
                else:
                    test_image_list = image_list
    if train_image_list is None or test_image_list is None or train_labels is None or test_labels is None:
        raise ValueError  # pragma: no cover
    return ImageDataset[Column](train_image_list, train_labels, 32, shuffle=True), ImageDataset[Column](
        test_image_list,
        test_labels,
        32,
    )


def _download_mnist_like(path: str | Path, files: dict[str, str], links: list[str]) -> None:
    path = Path(path)
    for file_name, file_path in files.items():
        for link in links:
            try:
                print(f"Trying to download file {file_name} via {link + file_path}")  # noqa: T201
                urllib.request.urlretrieve(link + file_path, path / file_path, reporthook=_report_download_progress)
                print()  # noqa: T201
                break
            except HTTPError as e:
                print(f"An error occurred while downloading: {e}")  # noqa: T201  # pragma: no cover


def _report_download_progress(current_packages: int, package_size: int, file_size: int) -> None:
    percentage = min(((current_packages * package_size) / file_size) * 100, 100)
    sys.stdout.write(f"\rDownloading... {percentage:.1f}%")
    sys.stdout.flush()
