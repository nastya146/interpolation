import os

import numpy as np
import pytest
from PIL import Image

from demo.example1 import main


@pytest.fixture
def input_data(tmp_path):
    """Create temporary input data files."""
    x_coords = np.array([0, 1])
    y_coords = np.array([0, 1])
    values = np.array([[0, 1], [1, 2]])
    x_new = np.array([0.25, 0.75])
    y_new = np.array([0.25, 0.75])

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    x_coords_path = data_dir / "x_coords.txt"
    y_coords_path = data_dir / "y_coords.txt"
    values_path = data_dir / "values.txt"
    x_new_path = data_dir / "x_new.txt"
    y_new_path = data_dir / "y_new.txt"

    np.savetxt(x_coords_path, x_coords)
    np.savetxt(y_coords_path, y_coords)
    np.savetxt(values_path, values)
    np.savetxt(x_new_path, x_new)
    np.savetxt(y_new_path, y_new)

    return {
        "x_coords": x_coords,
        "y_coords": y_coords,
        "values": values,
        "x_new": x_new,
        "y_new": y_new,
        "data_dir": data_dir,
        "tmp_path": tmp_path,
    }


def test_plot_creation(input_data, monkeypatch):
    """Test that the interpolation comparison plot is created."""
    plots_dir = input_data["tmp_path"] / "plots"
    plots_dir.mkdir()

    # Patch base_dir to use tmp_path
    def mock_abspath(path):
        return str(input_data["tmp_path"])

    with monkeypatch.context() as m:
        m.setattr(os.path, "abspath", mock_abspath)

        # Run the visualization
        main()

    # Check if the plot file exists (match any timestamp)
    plot_files = list(plots_dir.glob("interpolation_comparison_*.png"))
    assert len(plot_files) == 1, f"Expected one plot file, found: {plot_files}"
    plot_file = plot_files[0]

    # Check file is not empty
    assert os.path.getsize(plot_file) > 0, f"Plot file is empty: {plot_file}"

    # Check image dimensions
    with Image.open(plot_file) as img:
        width, height = img.size
        assert width > 0 and height > 0, f"Invalid image dimensions: {width}x{height}"
        # Expected dimensions for figsize=(10, 10) at default DPI (100)
        expected_width = 1000  # 10 inches * 100 DPI
        expected_height = 1000
        assert (
            abs(width - expected_width) < 50
        ), f"Unexpected width: {width} (expected ~{expected_width})"
        assert (
            abs(height - expected_height) < 50
        ), f"Unexpected height: {height} (expected ~{expected_height})"


def test_plot_content(input_data, monkeypatch):
    """Test that the plot contains expected content."""
    plots_dir = input_data["tmp_path"] / "plots"
    plots_dir.mkdir()

    # Patch base_dir
    def mock_abspath(path):
        return str(input_data["tmp_path"])

    with monkeypatch.context() as m:
        m.setattr(os.path, "abspath", mock_abspath)

        # Run the visualization
        main()

    # Check image content
    plot_files = list(plots_dir.glob("interpolation_comparison_*.png"))
    assert len(plot_files) == 1, f"Expected one plot file, found: {plot_files}"
    plot_file = plot_files[0]

    with Image.open(plot_file) as img:
        img_array = np.array(img)
        assert img_array.shape[2] in [3, 4], f"Unexpected image channels: {img_array.shape}"
        assert np.any(img_array != 0), "Image is completely black"
        assert np.any(img_array != 255), "Image is completely white"


def test_plot_failure_invalid_data(input_data, monkeypatch):
    """Test that visualization handles invalid data gracefully."""
    plots_dir = input_data["tmp_path"] / "plots"
    plots_dir.mkdir()

    # Create invalid data (empty values file)
    invalid_values_path = input_data["data_dir"] / "values.txt"
    with open(invalid_values_path, "w") as f:
        f.write("")  # Empty file

    # Patch base_dir
    def mock_abspath(path):
        return str(input_data["tmp_path"])

    with monkeypatch.context() as m:
        m.setattr(os.path, "abspath", mock_abspath)

        # Run the visualization (should handle error gracefully)
        try:
            main()
        except Exception as e:
            pytest.fail(f"Visualization failed with invalid data: {e}")

    # Check if plot file was created despite invalid data
    plot_files = list(plots_dir.glob("interpolation_comparison_*.png"))
    assert len(plot_files) == 1, f"Expected one plot file, found: {plot_files}"
    plot_file = plot_files[0]
    assert os.path.getsize(plot_file) > 0, f"Plot file is empty: {plot_file}"
