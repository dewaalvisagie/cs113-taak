import subprocess

def run_command(args):
    """Helper function to run the command and capture the output"""
    result = subprocess.run(args, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def test_invalid_encoding_argument_negative():
    # Test case for encoding argument -1
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "-1", "10", "4", "1"])
    assert "ERROR: Invalid encoding argument: -1" in stdout
    assert returncode != 0  # Non-zero return code indicates error

def test_invalid_encoding_argument_non_integer():
    # Test case for encoding argument 'adss' (non-integer)
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "adss", "10", "4", "1"])
    assert "ERROR: Invalid encoding argument: adss" in stdout
    assert returncode != 0

def test_invalid_encoding_argument_too_large():
    # Test case for encoding argument 33 (too large)
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "33", "10", "4", "1"])
    assert "ERROR: Invalid encoding argument: 33" in stdout
    assert returncode != 0

def test_too_few_arguments():
    # Test case for too few arguments
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py"])
    assert "ERROR: Too few arguments" in stdout
    assert returncode != 0  # Non-zero return code indicates error

def test_too_many_arguments():
    # Test case for too many arguments
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "1", "2", "3", "4", "5"])
    assert "ERROR: Too many arguments" in stdout
    assert returncode != 0

def test_invalid_qr_size_too_large():
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "1", "50", "4", "1"])
    assert "ERROR: Invalid size argument: 50" in stdout or stderr
    assert returncode != 0

def test_valid_input():
    # Test case for too many arguments
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "0", "25", "8", "5"])
    assert returncode == 0
def test_invalid_pospat_size_too_large():
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "1", "10", "20", "1"])
    assert "ERROR: Invalid position pattern size argument: 20" in stdout or stderr
    assert returncode != 0

def test_invalid_pospat_size_too_small():
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "1", "10", "3", "1"])
    assert "ERROR: Invalid position pattern size argument: 3" in stdout or stderr
    assert returncode != 0

def test_invalid_alignmentpat_size_too_small():
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "1", "10", "4", "2"])
    assert "ERROR: Invalid alignment pattern size argument: 2" in stdout or stderr
    assert returncode != 0
def test_alignment_pattern_out_of_bounds():
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "1", "10", "4", "8"])
    assert "ERROR: Invalid alignment pattern size argument: 8" in stdout or stderr
    assert returncode != 0
def test_valid_input():
    stdout, stderr, returncode = run_command(["python3", "SU28906268.py", "1", "10", "4", "1"])
    assert returncode == 0  # Should succeed with a return code of 0
    # We can check the structure of the output if needed by inspecting the printed QR
    assert "1 1 1" in stdout or stderr  # A valid QR pattern part