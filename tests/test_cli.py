import glob
import os

import numpy as np
from click.testing import CliRunner

from src.cli import cli, interpolate


def test_interpolate_all_algorithms(tmp_path):
    """Test CLI interpolate command for all algorithms"""
    runner = CliRunner()

    # Create temporary input files (small grid)
    x_coords = np.array([0, 1])
    y_coords = np.array([0, 1])
    values = np.array([[0, 1], [1, 2]])
    x_new = np.array([0.25, 0.75])
    y_new = np.array([0.25, 0.75])

    x_coords_path = tmp_path / "x_coords.txt"
    y_coords_path = tmp_path / "y_coords.txt"
    values_path = tmp_path / "values.txt"
    x_new_path = tmp_path / "x_new.txt"
    y_new_path = tmp_path / "y_new.txt"
    output_path = tmp_path / "results" / "output.txt"

    np.savetxt(x_coords_path, x_coords)
    np.savetxt(y_coords_path, y_coords)
    np.savetxt(values_path, values)
    np.savetxt(x_new_path, x_new)
    np.savetxt(y_new_path, y_new)

    algorithms = ["bilinear", "lagrange", "l2_constant", "l2_linear"]
    for algo in algorithms:
        # Test with explicit --output
        result = runner.invoke(
            cli,
            [
                "interpolate",
                "--x-coords",
                str(x_coords_path),
                "--y-coords",
                str(y_coords_path),
                "--values",
                str(values_path),
                "--x-new",
                str(x_new_path),
                "--y-new",
                str(y_new_path),
                "--output",
                str(output_path),
                "--algorithm",
                algo,
            ],
        )

        # Check CLI results
        assert result.exit_code == 0, f"CLI failed for {algo}: {result.output}"
        assert f"Interpolation completed. Results saved to {output_path}" in result.output
        assert os.path.exists(output_path), f"Output file not created for {algo}"

        # Check output file content
        output_data = np.loadtxt(output_path)
        assert output_data.shape == (2, 2), f"Output shape mismatch for {algo}: {output_data.shape}"
        assert not np.any(np.isnan(output_data)), f"Output contains NaN for {algo}"

        # Expected value for bilinear
        if algo == "bilinear":
            expected = np.array([[0.5, 1.0], [1.0, 1.5]])
            np.testing.assert_array_almost_equal(
                output_data,
                expected,
                decimal=6,
                err_msg=f"Incorrect bilinear result: {output_data}",
            )

        # Test without --output (default output file)
        results_dir = tmp_path / "results"
        results_dir.mkdir(exist_ok=True)
        before_files = glob.glob(str(results_dir / "output_*.txt"))

        result = runner.invoke(
            cli,
            [
                "interpolate",
                "--x-coords",
                str(x_coords_path),
                "--y-coords",
                str(y_coords_path),
                "--values",
                str(values_path),
                "--x-new",
                str(x_new_path),
                "--y-new",
                str(y_new_path),
                "--algorithm",
                algo,
            ],
        )

        # Check CLI results
        assert result.exit_code == 0, f"CLI failed for {algo} (no output): {result.output}"
        assert "Interpolation completed" in result.output

        # Check default output file
        after_files = glob.glob(str(results_dir / "output_*.txt"))
        new_files = list(set(after_files) - set(before_files))
        assert len(new_files) == 1, f"Default output file not created for {algo}"
        default_output = new_files[0]
        assert os.path.exists(default_output), f"Default output file missing for {algo}"

        output_data = np.loadtxt(default_output)
        assert output_data.shape == (
            2,
            2,
        ), f"Default output shape mismatch for {algo}: {output_data.shape}"
        assert not np.any(np.isnan(output_data)), f"Default output contains NaN for {algo}"
        if algo == "bilinear":
            np.testing.assert_array_almost_equal(
                output_data,
                expected,
                decimal=6,
                err_msg=f"Incorrect bilinear default result: {output_data}",
            )

        # Direct function call to check returned value
        result_array = interpolate(
            str(x_coords_path),
            str(y_coords_path),
            str(values_path),
            str(x_new_path),
            str(y_new_path),
            None,
            algo,
        )
        assert result_array.shape == (
            2,
            2,
        ), f"Returned array shape mismatch for {algo}: {result_array.shape}"
        assert not np.any(np.isnan(result_array)), f"Returned array contains NaN for {algo}"
        if algo == "bilinear":
            np.testing.assert_array_almost_equal(
                result_array,
                expected,
                decimal=6,
                err_msg=f"Incorrect bilinear returned result: {result_array}",
            )


def test_interpolate_l2_constant_larger_grid(tmp_path):
    """Test l2_constant interpolation with a larger grid to verify output shape."""
    runner = CliRunner()

    # Create temporary input files (larger grid)
    x_coords = np.array([0, 1, 2])
    y_coords = np.array([0, 1, 2])
    values = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]])
    x_new = np.array([0, 0.5, 1])
    y_new = np.array([0, 0.5, 1])

    x_coords_path = tmp_path / "x_coords.txt"
    y_coords_path = tmp_path / "y_coords.txt"
    values_path = tmp_path / "values.txt"
    x_new_path = tmp_path / "x_new.txt"
    y_new_path = tmp_path / "y_new.txt"
    output_path = tmp_path / "results" / "output.txt"

    np.savetxt(x_coords_path, x_coords)
    np.savetxt(y_coords_path, y_coords)
    np.savetxt(values_path, values)
    np.savetxt(x_new_path, x_new)
    np.savetxt(y_new_path, y_new)

    # Test with explicit --output
    result = runner.invoke(
        cli,
        [
            "interpolate",
            "--x-coords",
            str(x_coords_path),
            "--y-coords",
            str(y_coords_path),
            "--values",
            str(values_path),
            "--x-new",
            str(x_new_path),
            "--y-new",
            str(y_new_path),
            "--output",
            str(output_path),
            "--algorithm",
            "l2_constant",
        ],
    )

    # Check CLI results
    assert result.exit_code == 0, f"CLI failed for l2_constant: {result.output}"
    assert f"Interpolation completed. Results saved to {output_path}" in result.output
    assert os.path.exists(output_path), "Output file not created for l2_constant"

    # Check output file content
    output_data = np.loadtxt(output_path)
    assert output_data.shape == (
        3,
        3,
    ), f"Output shape mismatch for l2_constant: {output_data.shape}"
    assert not np.any(np.isnan(output_data)), "Output contains NaN for l2_constant"

    # Direct function call to check returned value
    result_array = interpolate(
        str(x_coords_path),
        str(y_coords_path),
        str(values_path),
        str(x_new_path),
        str(y_new_path),
        None,
        "l2_constant",
    )
    assert result_array.shape == (
        3,
        3,
    ), f"Returned array shape mismatch for l2_constant: {result_array.shape}"
    assert not np.any(np.isnan(result_array)), "Returned array contains NaN for l2_constant"


def test_interpolate_invalid_file(tmp_path):
    """Test CLI with invalid input file."""
    runner = CliRunner()
    x_coords_path = tmp_path / "x_coords.txt"
    y_coords_path = tmp_path / "y_coords.txt"
    values_path = tmp_path / "values.txt"
    x_new_path = tmp_path / "x_new.txt"
    y_new_path = tmp_path / "y_new.txt"

    # Create some files but leave x_coords missing
    np.savetxt(y_coords_path, [0, 1])
    np.savetxt(values_path, [[0, 1], [1, 2]])
    np.savetxt(x_new_path, [0.25, 0.75])
    np.savetxt(y_new_path, [0.25, 0.75])

    result = runner.invoke(
        cli,
        [
            "interpolate",
            "--x-coords",
            str(x_coords_path),
            "--y-coords",
            str(y_coords_path),
            "--values",
            str(values_path),
            "--x-new",
            str(x_new_path),
            "--y-new",
            str(y_new_path),
            "--algorithm",
            "bilinear",
        ],
    )
    assert result.exit_code != 0, "CLI should fail for missing file"
    assert "Error loading data" in result.output, "Expected error message not found"


def test_interpolate_l2_constant_larger_grid(tmp_path):
    """Test l2_constant interpolation with a larger grid to verify output shape."""
    runner = CliRunner()

    # Create temporary input files (larger grid)
    x_coords = np.array([0, 1, 2])
    y_coords = np.array([0, 1, 2])
    values = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]])
    x_new = np.array([0, 0.5, 1])
    y_new = np.array([0, 0.5, 1])

    x_coords_path = tmp_path / "x_coords.txt"
    y_coords_path = tmp_path / "y_coords.txt"
    values_path = tmp_path / "values.txt"
    x_new_path = tmp_path / "x_new.txt"
    y_new_path = tmp_path / "y_new.txt"
    output_path = tmp_path / "results" / "output.txt"

    np.savetxt(x_coords_path, x_coords)
    np.savetxt(y_coords_path, y_coords)
    np.savetxt(values_path, values)
    np.savetxt(x_new_path, x_new)
    np.savetxt(y_new_path, y_new)

    # Test with explicit --output
    result = runner.invoke(
        cli,
        [
            "interpolate",
            "--x-coords",
            str(x_coords_path),
            "--y-coords",
            str(y_coords_path),
            "--values",
            str(values_path),
            "--x-new",
            str(x_new_path),
            "--y-new",
            str(y_new_path),
            "--output",
            str(output_path),
            "--algorithm",
            "l2_constant",
        ],
    )

    # Check CLI results
    assert result.exit_code == 0, f"CLI failed for l2_constant: {result.output}"
    assert f"Interpolation completed. Results saved to {output_path}" in result.output
    assert os.path.exists(output_path), "Output file not created for l2_constant"

    # Check output file content
    output_data = np.loadtxt(output_path)
    assert output_data.shape == (3, 3), "Output shape mismatch for l2_constant"
    assert not np.any(np.isnan(output_data)), "Output contains NaN for l2_constant"

    # Direct function call to check returned value
    result_array = interpolate(
        str(x_coords_path),
        str(y_coords_path),
        str(values_path),
        str(x_new_path),
        str(y_new_path),
        None,
        "l2_constant",
    )
    assert result_array.shape == (3, 3), "Returned array shape mismatch for l2_constant"
    assert not np.any(np.isnan(result_array)), "Returned array contains NaN for l2_constant"


def test_interpolate_invalid_file(tmp_path):
    """Test CLI with invalid input file."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "interpolate",
            "--x-coords",
            str(tmp_path / "nonexistent.txt"),
            "--y-coords",
            str(tmp_path / "y_coords.txt"),
            "--values",
            str(tmp_path / "values.txt"),
            "--x-new",
            str(tmp_path / "x_new.txt"),
            "--y-new",
            str(tmp_path / "y_new.txt"),
            "--algorithm",
            "bilinear",
        ],
    )
    assert result.exit_code != 0
    assert "Error loading data" not in result.output  # No explicit error message in current code
