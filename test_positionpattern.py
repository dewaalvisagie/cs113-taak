import subprocess

# Helper function to run the script with given arguments
def run_program(pospat_size, qr_size, align_size):
    """Runs the position pattern program and captures the output."""
    result = subprocess.run(
        ["python3", "positionpattern.py", str(pospat_size), str(qr_size), str(align_size)],
        text=True,
        capture_output=True
    )
    return result

# ✅ Positive Test Cases (Valid Inputs)
def test_valid_7_25_13():
    result = run_program(7, 25, 13)
    assert result.returncode == 0  # Program should exit successfully

def test_valid_5_21_9():
    result = run_program(5, 21, 9)
    assert result.returncode == 0

def test_valid_4_10_5():
    result = run_program(4, 10, 5)
    assert result.returncode == 0

def test_valid_6_30_17():
    result = run_program(6, 30, 17)
    assert result.returncode == 0

def test_valid_7_35_21():
    result = run_program(7, 35, 21)
    assert result.returncode == 0

# ❌ Negative Test Cases (Expected Errors)
def test_negative_pospat_size():
    result = run_program(-5, 20, 6)
    assert "ERROR: Invalid position pattern size argument: -5" in result.stdout

def test_negative_qr_size():
    result = run_program(5, -20, 6)
    assert "ERROR: Invalid QR code size argument: -20" in result.stdout

def test_alignment_too_large():
    result = run_program(7, 10, 15)
    assert "ERROR: Invalid alignment pattern size: 15." in result.stdout

def test_pospat_too_large():
    result = run_program(12, 10, 5)
    assert "ERROR: Invalid position pattern size argument: 12" in result.stdout

def test_qr_too_small():
    result = run_program(4, 3, 2)
    assert "ERROR: Invalid position pattern size argument: 4" in result.stdout

def test_invalid_alignment_size():
    result = run_program(7, 25, 6)
    assert "ERROR: Invalid alignment pattern size: 6." in result.stdout

def test_alignment_out_of_bounds():
    result = run_program(5, 25, 50)
    assert "ERROR: Alignment/position pattern out of bounds" in result.stdout