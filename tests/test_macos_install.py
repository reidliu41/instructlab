# Standard
import os
import pathlib
import platform
import subprocess

# Third Party
import pytest


@pytest.mark.skipif(
    platform.system() != "Darwin" and platform.machine() != "arm64",
    reason="Test only runs on macOS with Apple Silicon",
)
def test_create_and_validate_virtualenv(
    scripts_path: pathlib.Path, tmp_path: pathlib.Path
):
    dest_dir = "test-install-instructlab"
    env = os.environ.copy()
    env["INSTALL_DIR"] = str(tmp_path / dest_dir)

    # Run the setup script
    setup_script = scripts_path / "setup-ilab-macos.sh"
    result = subprocess.run(
        ["bash", str(setup_script)], capture_output=True, check=True, text=True, env=env
    )

    assert result.returncode == 0

    # Verify that the venv was created
    venv_python = tmp_path / dest_dir / "venv" / "bin" / "python"
    assert venv_python.exists()

    # Verify the Python version in the venv
    python_version_result = subprocess.run(
        [str(venv_python), "--version"], capture_output=True, check=True, text=True
    )
    assert python_version_result.returncode == 0
    assert (
        "3.10" in python_version_result.stdout or "3.11" in python_version_result.stdout
    )

    # Ensure that the required packages are installed
    pip_list_result = subprocess.run(
        [str(tmp_path / dest_dir / "venv" / "bin" / "pip"), "list"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert pip_list_result.returncode == 0
    assert "instructlab" in pip_list_result.stdout

    # Run 'ilab --help' to verify the installation
    ilab_help_result = subprocess.run(
        [str(tmp_path / dest_dir / "venv" / "bin" / "ilab"), "--help"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert ilab_help_result.returncode == 0
    assert "Usage:" in ilab_help_result.stdout
