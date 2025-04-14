import time
import math
import sys
import pytest
import tkinter
from PIL import ImageColor
import shutil
import os
from turtle_oxford import (TurtleCanvas, turtle_canvas) # Standard imports
from turtle_oxford import (_degs_to_angle_units, _scale_x, _scale_y) # Useful helpers
from turtle_oxford import (checkfile, checkdir, chdir, fopen, fclose, fmove, fcopy, fread, freadline, fremove, frestart, fwrite, fwriteline, finddir, findfirst, findnext, isdir, isfile, mkdir, rmdir, mkfile, eof, eoln) # Functions under testing
TclError = tkinter.TclError  # in case needed

# Use a lambda to check if two floats are close (avoiding floating point errors)
is_close = lambda a, b: abs(a - b) < 1e-6

# Fixture to create a canvas and override mainloop so tests don't block
@pytest.fixture
def tc_setup():
    with turtle_canvas() as tc:
        # Monkey-patch mainloop to a no-op
        if TurtleCanvas._canvas:
            TurtleCanvas._canvas.mainloop = lambda: None
        # Reset state for tests
        TurtleCanvas._history = []
        yield tc

# Fixture to create a temporary file for testing
@pytest.fixture
def temp_file(tmp_path):
    # Create a temporary file with some content
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("line1\nline2\nline3")
    return str(file_path)

# Tests for input validation
def test_checkfile_pcode_length():
    # Test with invalid PCode length
    with pytest.raises(ValueError):
        checkfile("0101", "test.txt")

def test_checkfile_pcode_invalid_chars():
    # Test with non-binary characters
    with pytest.raises(ValueError):
        checkfile("0123abcd", "test.txt")

# Tests for action 0: Inquiry only
@pytest.mark.parametrize("file_exists,expected_result", [
    (True, "11000000"),  # File exists
    (False, "00000000")  # File does not exist
])
def test_checkfile_action0(monkeypatch, file_exists, expected_result):
    # Mock os.path.exists to return the parametrized value
    monkeypatch.setattr(os.path, "exists", lambda _: file_exists)
    
    # Action 0 (inquiry only)
    result = checkfile("00000000", "test.txt")
    # Verify result based on parameter
    assert result == expected_result

# Tests for action 1: Delete if exists
@pytest.mark.parametrize("test_case,setup,expected_result,expected_output,expected_exception", [
    # File exists, successful deletion
    ("exists_success", 
     {"exists_calls": [True, False], "mock_remove": lambda _: None}, 
     "01000001", "", None),
    # File doesn't exist, silent
    ("not_exists_silent", 
     {"exists_calls": [False]}, 
     "00000001", "", None),
    # File doesn't exist, inform
    ("not_exists_inform", 
     {"exists_calls": [False], "pcode": "00000101"}, 
     "00000101", "does not exist", None),
    # File doesn't exist, warn
    ("not_exists_warn", 
     {"exists_calls": [False], "pcode": "00001001"}, 
     "00001001", "Warning:", None),
    # File doesn't exist, error
    ("not_exists_error", 
     {"exists_calls": [False], "pcode": "00001101"}, 
     None, None, FileNotFoundError),
    # File exists, deletion fails
    ("exists_deletion_fails", 
     {"exists_calls": [True], 
      "mock_remove": lambda _: (_ for _ in ()).throw(PermissionError("Permission denied"))}, 
     None, None, RuntimeError),
])
def test_checkfile_action1(monkeypatch, capsys, test_case, setup, expected_result, expected_output, expected_exception):
    # Set up mock for os.path.exists
    if "exists_calls" in setup:
        exists_calls = setup["exists_calls"].copy()
        def mock_exists(_):
            if exists_calls:
                return exists_calls.pop(0)
            return False
        monkeypatch.setattr(os.path, "exists", mock_exists)
    
    # Set up mock for os.remove if provided
    if "mock_remove" in setup:
        monkeypatch.setattr(os, "remove", setup["mock_remove"])
    
    # Get pcode from setup or use default
    pcode = setup.get("pcode", "00000001")
    
    if expected_exception:
        # Test cases that should raise exceptions
        with pytest.raises(expected_exception):
            checkfile(pcode, "test.txt")
    else:
        # Test cases that should succeed
        result = checkfile(pcode, "test.txt")
        assert result == expected_result
        
        # Check output if specified
        if expected_output:
            captured = capsys.readouterr()
            assert expected_output in captured.out

# Tests for action 2: Create if not present
@pytest.mark.parametrize("test_case,setup,expected_result,expected_output,expected_exception", [
    # File doesn't exist, successful creation
    ("not_exists_success", 
     {"exists_calls": [False, True]}, 
     "10000010", "", None),
    # File exists, silent
    ("exists_silent", 
     {"exists_calls": [True]}, 
     "11000010", "", None),
    # File exists, inform
    ("exists_inform", 
     {"exists_calls": [True], "pcode": "00010010"}, 
     "11010010", "already exists", None),
    # File exists, warn
    ("exists_warn", 
     {"exists_calls": [True], "pcode": "00100010"}, 
     "11100010", "Warning:", None),
    # File exists, error
    ("exists_error", 
     {"exists_calls": [True], "pcode": "00110010"}, 
     None, None, FileExistsError),
    # File doesn't exist, creation fails
    ("not_exists_creation_fails", 
     {"exists_calls": [False], "mock_open_fails": True}, 
     None, None, RuntimeError),
])
def test_checkfile_action2(monkeypatch, capsys, tmp_path, test_case, setup, expected_result, expected_output, expected_exception):
    # Set up the test file path
    test_file = tmp_path / "test.txt"
    file_path = str(test_file)
    
    # Set up mock for os.path.exists
    if "exists_calls" in setup:
        exists_calls = setup["exists_calls"].copy()
        def mock_exists(_):
            if exists_calls:
                return exists_calls.pop(0)
            return exists_calls[-1] if exists_calls else True
        monkeypatch.setattr(os.path, "exists", mock_exists)
    
    # Set up mock for open
    class MockFile:
        def __init__(self, *args, **kwargs):
            pass
        def close(self):
            pass
    
    if setup.get("mock_open_fails", False):
        def mock_open(*args, **kwargs):
            raise PermissionError("Permission denied")
        monkeypatch.setattr("builtins.open", mock_open)
    else:
        monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
    
    # Get pcode from setup or use default
    pcode = setup.get("pcode", "00000010")
    
    if expected_exception:
        # Test cases that should raise exceptions
        with pytest.raises(expected_exception):
            checkfile(pcode, file_path)
    else:
        # Test cases that should succeed
        result = checkfile(pcode, file_path)
        assert result == expected_result
        
        # Check output if specified
        if expected_output:
            captured = capsys.readouterr()
            assert expected_output in captured.out

# Tests for action 3: Create or recreate
@pytest.mark.parametrize("test_case,setup,expected_result,expected_output,expected_exception", [
    # File doesn't exist, successful creation
    ("not_exists_success", 
     {"exists_calls": [False, True]}, 
     "10000011", "", None),
    # File exists, silent recreate
    ("exists_silent", 
     {"exists_calls": [True, True]}, 
     "11000011", "", None),
    # File exists, inform recreate
    ("exists_inform", 
     {"exists_calls": [True, True], "pcode": "00010011"}, 
     "11010011", "will be recreated", None),
    # File exists, warn recreate
    ("exists_warn", 
     {"exists_calls": [True, True], "pcode": "00100011"}, 
     "11100011", "Warning:", None),
    # File exists, error
    ("exists_error", 
     {"exists_calls": [True], "pcode": "00110011"}, 
     None, None, FileExistsError),
    # File exists, deletion fails
    ("exists_deletion_fails", 
     {"exists_calls": [True], "mock_remove_fails": True}, 
     None, None, RuntimeError),
    # File doesn't exist, creation fails
    ("not_exists_creation_fails", 
     {"exists_calls": [False], "mock_open_fails": True}, 
     None, None, RuntimeError),
])
def test_checkfile_action3(monkeypatch, capsys, test_case, setup, expected_result, expected_output, expected_exception):
    # Set up mock for os.path.exists
    if "exists_calls" in setup:
        exists_calls = setup["exists_calls"].copy()
        def mock_exists(_):
            if exists_calls:
                return exists_calls.pop(0)
            return exists_calls[-1] if exists_calls else True
        monkeypatch.setattr(os.path, "exists", mock_exists)
    
    # Set up mock for file operations
    class MockFile:
        def __init__(self, *args, **kwargs):
            pass
        def close(self):
            pass
    
    # Set up mock for os.remove
    if setup.get("mock_remove_fails", False):
        def mock_remove(_):
            raise PermissionError("Permission denied")
        monkeypatch.setattr(os, "remove", mock_remove)
    else:
        monkeypatch.setattr(os, "remove", lambda _: None)
    
    # Set up mock for open
    if setup.get("mock_open_fails", False):
        def mock_open(*args, **kwargs):
            raise PermissionError("Permission denied")
        monkeypatch.setattr("builtins.open", mock_open)
    else:
        monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
    
    # Get pcode from setup or use default
    pcode = setup.get("pcode", "00000011")
    
    if expected_exception:
        # Test cases that should raise exceptions
        with pytest.raises(expected_exception):
            checkfile(pcode, "test.txt")
    else:
        # Test cases that should succeed
        result = checkfile(pcode, "test.txt")
        assert result == expected_result
        
        # Check output if specified
        if expected_output:
            captured = capsys.readouterr()
            assert expected_output in captured.out

# Tests for checkdir input validation
@pytest.mark.parametrize("pcode,expected_error,expected_message", [
    ("0101", ValueError, "PCode must be 8 characters long"),
    ("0123abcd", ValueError, "PCode must be a binary string"),
])
def test_checkdir_pcode_validation(pcode, expected_error, expected_message):
    # Test with invalid PCode inputs
    with pytest.raises(expected_error, match=expected_message):
        checkdir(pcode, "test_dir")

# Tests for action 0: Inquiry only
@pytest.mark.parametrize("dir_exists,expected_result", [
    (True, "11000000"),  # Directory exists
    (False, "00000000")  # Directory does not exist
])
def test_checkdir_action0(monkeypatch, dir_exists, expected_result):
    # Mock os.path.isdir to return the parametrized value
    monkeypatch.setattr(os.path, "isdir", lambda _: dir_exists)
    
    # Action 0 (inquiry only)
    result = checkdir("00000000", "test_dir")
    # Verify result based on parameter
    assert result == expected_result

# Tests for action 1: Delete if exists
@pytest.mark.parametrize("test_case,setup,expected_result,expected_output,expected_exception", [
    # Directory exists, successful deletion
    ("exists_success", 
     {"exists_calls": [True, False], "mock_rmtree": lambda _: None}, 
     "01000001", "", None),
    # Directory doesn't exist, silent
    ("not_exists_silent", 
     {"exists_calls": [False]}, 
     "00000001", "", None),
    # Directory doesn't exist, inform
    ("not_exists_inform", 
     {"exists_calls": [False], "pcode": "00000101"}, 
     "00000101", "does not exist", None),
    # Directory doesn't exist, warn
    ("not_exists_warn", 
     {"exists_calls": [False], "pcode": "00001001"}, 
     "00001001", "Warning:", None),
    # Directory doesn't exist, error
    ("not_exists_error", 
     {"exists_calls": [False], "pcode": "00001101"}, 
     None, None, FileNotFoundError),
    # Directory exists, deletion fails
    ("exists_deletion_fails", 
     {"exists_calls": [True], 
      "mock_rmtree": lambda _: (_ for _ in ()).throw(PermissionError("Permission denied"))}, 
     None, None, RuntimeError),
])
def test_checkdir_action1(monkeypatch, capsys, test_case, setup, expected_result, expected_output, expected_exception):
    # Set up mock for os.path.isdir
    if "exists_calls" in setup:
        exists_calls = setup["exists_calls"].copy()
        def mock_exists(_):
            if exists_calls:
                return exists_calls.pop(0)
            return False
        monkeypatch.setattr(os.path, "isdir", mock_exists)
    
    # Set up mock for shutil.rmtree if provided
    if "mock_rmtree" in setup:
        monkeypatch.setattr(shutil, "rmtree", setup["mock_rmtree"])
    
    # Get pcode from setup or use default
    pcode = setup.get("pcode", "00000001")
    
    if expected_exception:
        # Test cases that should raise exceptions
        with pytest.raises(expected_exception):
            checkdir(pcode, "test_dir")
    else:
        # Test cases that should succeed
        result = checkdir(pcode, "test_dir")
        assert result == expected_result
        
        # Check output if specified
        if expected_output:
            captured = capsys.readouterr()
            assert expected_output in captured.out

# Tests for action 2: Create if not present
@pytest.mark.parametrize("test_case,setup,expected_result,expected_output,expected_exception", [
    # Directory doesn't exist, successful creation
    ("not_exists_success", 
     {"exists_calls": [False, True]}, 
     "10000010", "", None),
    # Directory exists, silent
    ("exists_silent", 
     {"exists_calls": [True]}, 
     "11000010", "", None),
    # Directory exists, inform
    ("exists_inform", 
     {"exists_calls": [True], "pcode": "00010010"}, 
     "11010010", "already exists", None),
    # Directory exists, warn
    ("exists_warn", 
     {"exists_calls": [True], "pcode": "00100010"}, 
     "11100010", "Warning:", None),
    # Directory exists, error
    ("exists_error", 
     {"exists_calls": [True], "pcode": "00110010"}, 
     None, None, FileExistsError),
    # Directory doesn't exist, creation fails
    ("not_exists_creation_fails", 
     {"exists_calls": [False], "mock_makedirs_fails": True}, 
     None, None, RuntimeError),
])
def test_checkdir_action2(monkeypatch, capsys, test_case, setup, expected_result, expected_output, expected_exception):
    # Set up mock for os.path.isdir
    if "exists_calls" in setup:
        exists_calls = setup["exists_calls"].copy()
        def mock_exists(_):
            if exists_calls:
                return exists_calls.pop(0)
            return exists_calls[-1] if exists_calls else True
        monkeypatch.setattr(os.path, "isdir", mock_exists)
    
    # Set up mock for os.makedirs
    if setup.get("mock_makedirs_fails", False):
        def mock_makedirs(_):
            raise PermissionError("Permission denied")
        monkeypatch.setattr(os, "makedirs", mock_makedirs)
    else:
        monkeypatch.setattr(os, "makedirs", lambda _: None)
    
    # Get pcode from setup or use default
    pcode = setup.get("pcode", "00000010")
    
    if expected_exception:
        # Test cases that should raise exceptions
        with pytest.raises(expected_exception):
            checkdir(pcode, "test_dir")
    else:
        # Test cases that should succeed
        result = checkdir(pcode, "test_dir")
        assert result == expected_result
        
        # Check output if specified
        if expected_output:
            captured = capsys.readouterr()
            assert expected_output in captured.out

# Tests for action 3: Create or recreate
@pytest.mark.parametrize("test_case,setup,expected_result,expected_output,expected_exception", [
    # Directory doesn't exist, successful creation
    ("not_exists_success", 
     {"exists_calls": [False, True]}, 
     "10000011", "", None),
    # Directory exists, silent recreate
    ("exists_silent", 
     {"exists_calls": [True, True]}, 
     "11000011", "", None),
    # Directory exists, inform recreate
    ("exists_inform", 
     {"exists_calls": [True, True], "pcode": "00010011"}, 
     "11010011", "will be recreated", None),
    # Directory exists, warn recreate
    ("exists_warn", 
     {"exists_calls": [True, True], "pcode": "00100011"}, 
     "11100011", "Warning:", None),
    # Directory exists, error
    ("exists_error", 
     {"exists_calls": [True], "pcode": "00110011"}, 
     None, None, FileExistsError),
    # Directory exists, deletion fails
    ("exists_deletion_fails", 
     {"exists_calls": [True], "mock_rmtree_fails": True}, 
     None, None, RuntimeError),
    # Directory doesn't exist, creation fails
    ("not_exists_creation_fails", 
     {"exists_calls": [False], "mock_makedirs_fails": True}, 
     None, None, RuntimeError),
])
def test_checkdir_action3(monkeypatch, capsys, test_case, setup, expected_result, expected_output, expected_exception):
    # Set up mock for os.path.isdir
    if "exists_calls" in setup:
        exists_calls = setup["exists_calls"].copy()
        def mock_exists(_):
            if exists_calls:
                return exists_calls.pop(0)
            return exists_calls[-1] if exists_calls else True
        monkeypatch.setattr(os.path, "isdir", mock_exists)
    
    # Set up mock for directory operations
    if setup.get("mock_rmtree_fails", False):
        def mock_rmtree(_):
            raise PermissionError("Permission denied")
        monkeypatch.setattr(shutil, "rmtree", mock_rmtree)
    else:
        monkeypatch.setattr(shutil, "rmtree", lambda _: None)
    
    # Set up mock for os.makedirs
    if setup.get("mock_makedirs_fails", False):
        def mock_makedirs(_):
            raise PermissionError("Permission denied")
        monkeypatch.setattr(os, "makedirs", mock_makedirs)
    else:
        monkeypatch.setattr(os, "makedirs", lambda _: None)
    
    # Get pcode from setup or use default
    pcode = setup.get("pcode", "00000011")
    
    if expected_exception:
        # Test cases that should raise exceptions
        with pytest.raises(expected_exception):
            checkdir(pcode, "test_dir")
    else:
        # Test cases that should succeed
        result = checkdir(pcode, "test_dir")
        assert result == expected_result
        
        # Check output if specified
        if expected_output:
            captured = capsys.readouterr()
            assert expected_output in captured.out

def test_chdir(monkeypatch):
    # Mock os.chdir to increment count
    chdir_calls: int = 0
    def mock_chdir(path):
        nonlocal chdir_calls
        chdir_calls += 1
    monkeypatch.setattr(os, "chdir", mock_chdir)
    
    # Test chdir
    chdir("test_dir")

    # Verify that os.chdir was called with the correct argument
    assert chdir_calls == 1, "chdir should be called once"

def test_fopen_fclose(temp_file):
    # Test mode 1 (read)
    file_handle = fopen(temp_file, 1)
    assert file_handle is not None
    assert file_handle.mode == 'r'
    fclose(file_handle)
    assert file_handle.closed
    
    # Test mode 2 (append)
    file_handle = fopen(temp_file, 2)
    assert file_handle is not None
    assert file_handle.mode == 'a'
    fclose(file_handle)
    assert file_handle.closed
    
    # Test mode 3 (write)
    file_handle = fopen(temp_file, 3)
    assert file_handle is not None
    assert file_handle.mode == 'w'
    fclose(file_handle)
    assert file_handle.closed

def test_fread(temp_file):
    file_handle = fopen(temp_file, 1)
    content = fread(file_handle)
    assert content == "line1\nline2\nline3"
    fclose(file_handle)

def test_freadline(temp_file):
    file_handle = fopen(temp_file, 1)
    line = freadline(file_handle)
    assert line == "line1\n"
    line = freadline(file_handle)
    assert line == "line2\n"
    fclose(file_handle)

def test_frestart(temp_file):
    file_handle = fopen(temp_file, 1)
    # Read one line then restart
    line = freadline(file_handle)
    assert line == "line1\n"
    frestart(file_handle)
    # After restart, should be back at the beginning
    line = freadline(file_handle)
    assert line == "line1\n"
    fclose(file_handle)

def test_fwrite(tmp_path):
    file_path = str(tmp_path / "write_test.txt")
    file_handle = fopen(file_path, 3)  # Write mode
    fwrite(file_handle, "Hello")
    fwrite(file_handle, " World")
    fclose(file_handle)
    
    # Verify the content
    with open(file_path, 'r') as f:
        assert f.read() == "Hello World"

def test_fwriteline(tmp_path):
    file_path = str(tmp_path / "writeline_test.txt")
    file_handle = fopen(file_path, 3)  # Write mode
    fwriteline(file_handle, "Hello")
    fwriteline(file_handle, "World")
    fclose(file_handle)
    
    # Verify the content
    with open(file_path, 'r') as f:
        assert f.read() == "Hello\nWorld\n"

def test_fmove(temp_file, tmp_path):
    new_path = str(tmp_path / "moved_file.txt")
    file_handle = fopen(temp_file, 1)
    
    # Move the file
    success = fmove(file_handle, new_path)
    assert success
    
    # Original file should no longer exist
    assert not os.path.exists(temp_file)
    
    # New file should exist with the same content
    assert os.path.exists(new_path)
    with open(new_path, 'r') as f:
        assert f.read() == "line1\nline2\nline3"

def test_fmove_fail(temp_file):
    # Test moving to an invalid location
    file_handle = fopen(temp_file, 1)
    success = fmove(file_handle, "/invalid/path/that/doesnt/exist/file.txt")
    assert not success
    # Original file should still exist
    assert os.path.exists(temp_file)

def test_fcopy(temp_file, tmp_path):
    file_handle = fopen(temp_file, 1)
    
    # Copy the file
    copy_handle = fcopy(file_handle)
    assert copy_handle is not None
    
    # Original file should still exist
    assert os.path.exists(temp_file)
    
    # Copy file should have a .copy extension
    copy_path = temp_file + ".copy"
    assert os.path.exists(copy_path)
    
    # Content should be the same
    original_content = fread(file_handle)
    frestart(file_handle)  # Reset file position
    
    copy_content = fread(copy_handle)
    assert copy_content == original_content
    
    # Clean up
    fclose(file_handle)
    fclose(copy_handle)
    os.remove(copy_path)

def test_fremove(tmp_path):
    # Create a file to remove
    file_path = str(tmp_path / "to_delete.txt")
    file_handle = fopen(file_path, 3)
    fwrite(file_handle, "Delete me")
    fclose(file_handle)
    
    # Verify file exists
    assert os.path.exists(file_path)
    
    # Open and remove the file
    file_handle = fopen(file_path, 1)
    fremove(file_handle)
    
    # Verify file is gone
    assert not os.path.exists(file_path)

def test_complex_file_operations(tmp_path):
    # Test a complex sequence of file operations
    file_path = str(tmp_path / "complex_test.txt")
    
    # Create and write to file
    file_handle = fopen(file_path, 3)
    fwriteline(file_handle, "First line")
    fwriteline(file_handle, "Second line")
    fclose(file_handle)
    
    # Read file
    file_handle = fopen(file_path, 1)
    content = fread(file_handle)
    assert content == "First line\nSecond line\n"
    fclose(file_handle)
    
    # Append to file
    file_handle = fopen(file_path, 2)
    fwriteline(file_handle, "Appended line")
    fclose(file_handle)
    
    # Copy file
    file_handle = fopen(file_path, 1)
    copy_handle = fcopy(file_handle)
    fclose(file_handle)
    fclose(copy_handle)
    
    # Move copy to new location
    copy_path = file_path + ".copy"
    new_path = str(tmp_path / "moved_copy.txt")
    copy_handle = fopen(copy_path, 1)
    success = fmove(copy_handle, new_path)
    assert success
    
    # Verify final state
    assert os.path.exists(file_path)
    assert not os.path.exists(copy_path)
    assert os.path.exists(new_path)
    
    with open(new_path, 'r') as f:
        assert f.read() == "First line\nSecond line\nAppended line\n"

def test_finddir(tmp_path):
    # Create a find handle
    find_handle = []

    # Create a directory structure
    os.mkdir(tmp_path / "dir1")
    os.mkdir(tmp_path / "dir2")
    os.mkdir(tmp_path / "dir3")

    # Create pattern
    pattern = os.path.join(tmp_path, "dir*")
    expected_pattern = os.path.join(tmp_path, "dir1")

    # Find the directory
    result = finddir(pattern, find_handle)
    assert result == expected_pattern

def test_findfirst(tmp_path):
    # Create a find handle
    find_handle = []

    # Create files in tmp_path

    # Go to tmp_path
    os.chdir(tmp_path)

    # Create files
    with open("file1", "w") as f:
        f.write("Hello")
    
    with open("file2", "w") as f:
        f.write("World")
    
    with open("file3", "w") as f:
        f.write("!")

    # Create pattern
    pattern = os.path.join(tmp_path, "file1")
    expected_pattern = os.path.join(tmp_path, "file1")

    # Find the first directory
    result = findfirst(pattern, find_handle)
    assert result == expected_pattern

def test_findnext(tmp_path):
    # Create a find handle
    find_handle = []

    # Create files in tmp_path

    # Go to tmp_path
    os.chdir(tmp_path)

    # Create files
    with open("file1", "w") as f:
        f.write("Hello")
    
    with open("file2", "w") as f:
        f.write("World")
    
    with open("file3", "w") as f:
        f.write("!")

    # Create pattern
    pattern = os.path.join(tmp_path, "file*")
    expected_pattern_1 = os.path.join(tmp_path, "file1")
    expected_pattern_2 = os.path.join(tmp_path, "file2")

    # Find the first two files
    result_1 = findfirst(pattern, find_handle)
    result_2 = findnext(find_handle)

    assert result_1 == expected_pattern_1
    assert result_2 == expected_pattern_2

def test_isdir(tmp_path):
    # Create a directory
    os.mkdir(tmp_path / "test_dir")

    # Check if the directory exists
    dir_path = os.path.join(tmp_path, "test_dir")
    result = isdir(dir_path)
    assert result

def test_isfile(tmp_path):
    # Create a file
    with open(tmp_path / "test_file.txt", "w") as f:
        f.write("Hello World!")

    # Check if the file exists
    file_path = os.path.join(tmp_path, "test_file.txt")
    result = isfile(file_path)
    assert result

def test_mkdir(tmp_path):
    # Create a directory
    os.chdir(tmp_path)
    mkdir("test_dir")

    # Check if the directory exists and is a directory
    assert os.path.exists(tmp_path / "test_dir") and os.path.isdir(tmp_path / "test_dir")

def test_rmdir(tmp_path):
    # Create a directory
    os.mkdir(tmp_path / "test_dir")

    # Remove the directory
    dir_path = os.path.join(tmp_path, "test_dir")
    rmdir(dir_path)

    # Check if the directory exists
    assert not os.path.exists(dir_path)

def test_mkfile(tmp_path):
    # Create a file
    file_path = os.path.join(tmp_path, "test_file.txt")
    mkfile(file_path)

    # Check if the file exists and is a file
    assert os.path.exists(file_path) and os.path.isfile(file_path)

def test_eof(tmp_path):
    # Create a test file with content
    file_path = str(tmp_path / "eof_test.txt")
    with open(file_path, "w") as f:
        f.write("test content")
    
    # Test when not at end of file
    file_handle = fopen(file_path, 1)  # Open in read mode
    assert not eof(file_handle)  # Should not be at EOF initially
    
    # Read all content to reach EOF
    fread(file_handle)
    assert eof(file_handle)  # Should now be at EOF
    
    # Reset to beginning and test again
    frestart(file_handle)
    assert not eof(file_handle)  # After restart, should not be at EOF

def test_eoln(tmp_path):
    # Create a test file with content
    file_path = os.path.join(tmp_path, "eoln_test.txt")
    with open(file_path, "w") as f:
        f.write("line1\n\nline2\n\nline3")
    
    # Test when not at end of line
    file_handle = fopen(file_path, 1)  # Open in read mode
    assert not eoln(file_handle)  # Should not be at EOLN initially
    
    # Read first line to reach EOLN
    print(freadline(file_handle))
    assert eoln(file_handle)  # Should now be at EOLN
    
    # Reset to beginning and test again
    frestart(file_handle)
    assert not eoln(file_handle)  # After restart, should not be at EOLN