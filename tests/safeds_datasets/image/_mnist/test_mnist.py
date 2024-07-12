import os
import tempfile
from pathlib import Path

import pytest
import torch
from safeds.data.labeled.containers import ImageDataset
from safeds_datasets.image import _mnist, load_fashion_mnist, load_kmnist, load_mnist


class TestMNIST:

    def test_should_download_and_return_mnist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname:
            train, test = load_mnist(tmpdirname, download=True)
            files = os.listdir(Path(tmpdirname) / _mnist._mnist._mnist_folder)
            for mnist_file in _mnist._mnist._mnist_files.values():
                assert mnist_file in files
            assert isinstance(train, ImageDataset)
            assert isinstance(test, ImageDataset)
            assert len(train) == 60_000
            assert len(test) == 10_000
            assert (
                train.get_input()._as_single_size_image_list()._tensor.dtype
                == test.get_input()._as_single_size_image_list()._tensor.dtype
                == torch.uint8
            )
            train_output = train.get_output()
            test_output = test.get_output()
            assert (
                set(train_output.get_distinct_values())
                == set(test_output.get_distinct_values())
                == set(_mnist._mnist._mnist_labels.values())
            )

    def test_should_raise_if_file_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname, pytest.raises(FileNotFoundError):
            load_mnist(tmpdirname, download=False)


class TestFashionMNIST:

    def test_should_download_and_return_mnist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname:
            train, test = load_fashion_mnist(tmpdirname, download=True)
            files = os.listdir(Path(tmpdirname) / _mnist._mnist._fashion_mnist_folder)
            for mnist_file in _mnist._mnist._fashion_mnist_files.values():
                assert mnist_file in files
            assert isinstance(train, ImageDataset)
            assert isinstance(test, ImageDataset)
            assert len(train) == 60_000
            assert len(test) == 10_000
            assert (
                train.get_input()._as_single_size_image_list()._tensor.dtype
                == test.get_input()._as_single_size_image_list()._tensor.dtype
                == torch.uint8
            )
            train_output = train.get_output()
            test_output = test.get_output()
            assert (
                set(train_output.get_distinct_values())
                == set(test_output.get_distinct_values())
                == set(_mnist._mnist._fashion_mnist_labels.values())
            )

    def test_should_raise_if_file_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname, pytest.raises(FileNotFoundError):
            load_fashion_mnist(tmpdirname, download=False)


class TestKMNIST:

    def test_should_download_and_return_mnist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname:
            train, test = load_kmnist(tmpdirname, download=True)
            files = os.listdir(Path(tmpdirname) / _mnist._mnist._kuzushiji_mnist_folder)
            for mnist_file in _mnist._mnist._kuzushiji_mnist_files.values():
                assert mnist_file in files
            assert isinstance(train, ImageDataset)
            assert isinstance(test, ImageDataset)
            assert len(train) == 60_000
            assert len(test) == 10_000
            assert (
                train.get_input()._as_single_size_image_list()._tensor.dtype
                == test.get_input()._as_single_size_image_list()._tensor.dtype
                == torch.uint8
            )
            train_output = train.get_output()
            test_output = test.get_output()
            assert (
                set(train_output.get_distinct_values())
                == set(test_output.get_distinct_values())
                == set(_mnist._mnist._kuzushiji_mnist_labels.values())
            )

    def test_should_raise_if_file_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname, pytest.raises(FileNotFoundError):
            load_kmnist(tmpdirname, download=False)
