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
    with pytest.raises(ValueError, match="PCode must be 8 characters long"):
        checkfile("0101", "test.txt")

def test_checkfile_pcode_invalid_chars():
    # Test with non-binary characters
    with pytest.raises(ValueError, match="PCode must be a binary string"):
        checkfile("0123abcd", "test.txt")

# Tests for action 0: Inquiry only
def test_checkfile_action0_file_exists(monkeypatch):
    # Mock os.path.exists to return True
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    
    # Action 0 (inquiry only), file exists
    result = checkfile("00000000", "test.txt")
    # Expect bit 6 set (file existed before), bit 7 set (file exists after)
    assert result == "11000000"

def test_checkfile_action0_file_not_exists(monkeypatch):
    # Mock os.path.exists to return False
    monkeypatch.setattr(os.path, "exists", lambda _: False)
    
    # Action 0 (inquiry only), file doesn't exist
    result = checkfile("00000000", "test.txt")
    # Expect both bit 6 and 7 unset (file never existed)
    assert result == "00000000"

# Tests for action 1: Delete if exists
def test_checkfile_action1_file_exists(monkeypatch):
    # Mock file exists before and not after deletion
    exists_calls = [True, False]
    def mock_exists(_):
        return exists_calls.pop(0)
    
    monkeypatch.setattr(os.path, "exists", mock_exists)
    monkeypatch.setattr(os, "remove", lambda _: None)  # Mock successful deletion
    
    # Action 1 (delete), file exists
    result = checkfile("00000001", "test.txt")
    # Expect bit 6 set (file existed before), bit 7 unset (doesn't exist after)
    assert result == "01000001"

def test_checkfile_action1_file_not_exists_silent(monkeypatch, capsys):
    # Mock os.path.exists to return False
    monkeypatch.setattr(os.path, "exists", lambda _: False)
    
    # Action 1 (delete), file doesn't exist, notification level 0 (silent)
    result = checkfile("00000001", "test.txt")
    # Expect both bits 6 and 7 unset (file never existed)
    assert result == "00000001"
    
    # Check nothing was printed
    captured = capsys.readouterr()
    assert captured.out == ""

def test_checkfile_action1_file_not_exists_inform(monkeypatch, capsys):
    # Mock os.path.exists to return False
    monkeypatch.setattr(os.path, "exists", lambda _: False)
    
    # Action 1 (delete), file doesn't exist, notification level 4 (inform)
    result = checkfile("00000101", "test.txt")
    # Check message was printed
    captured = capsys.readouterr()
    assert "does not exist" in captured.out
    assert result == "00000101"

def test_checkfile_action1_file_not_exists_warn(monkeypatch, capsys):
    # Mock os.path.exists to return False
    monkeypatch.setattr(os.path, "exists", lambda _: False)
    
    # Action 1 (delete), file doesn't exist, notification level 8 (warn)
    result = checkfile("00001001", "test.txt")
    # Check warning was printed
    captured = capsys.readouterr()
    assert "Warning:" in captured.out
    assert result == "00001001"

def test_checkfile_action1_file_not_exists_error(monkeypatch):
    # Mock os.path.exists to return False
    monkeypatch.setattr(os.path, "exists", lambda _: False)
    
    # Action 1 (delete), file doesn't exist, notification level 12 (error)
    with pytest.raises(FileNotFoundError):
        checkfile("00001101", "test.txt")

def test_checkfile_action1_deletion_fails(monkeypatch):
    # Mock os.path.exists to return True but os.remove to fail
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    def mock_remove(_):
        raise PermissionError("Permission denied")
    monkeypatch.setattr(os, "remove", mock_remove)
    
    # Action 1 (delete), file exists but deletion fails
    with pytest.raises(RuntimeError, match="Deletion failed"):
        checkfile("00000001", "test.txt")

# Tests for action 2: Create if not present
def test_checkfile_action2_file_not_exists(monkeypatch, tmp_path):
    # Setup
    test_file = tmp_path / "test.txt"
    file_path = str(test_file)
    
    # Mock file doesn't exist initially but exists after creation
    exists_calls = [False, True]
    def mock_exists(_):
        return exists_calls.pop(0) if exists_calls else True
    monkeypatch.setattr(os.path, "exists", mock_exists)
    
    # Mock file creation
    class MockFile:
        def __init__(self, *args, **kwargs):
            pass
        def close(self):
            pass
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
    
    # Action 2 (create if not present), file doesn't exist
    result = checkfile("00000010", file_path)
    # Expect bit 6 unset (file didn't exist) and bit 7 set (file exists after)
    assert result == "10000010"

def test_checkfile_action2_file_exists_silent(monkeypatch, capsys):
    # Mock os.path.exists to return True
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    
    # Action 2 (create if not present), file exists, notification level 0 (silent)
    result = checkfile("00000010", "test.txt")
    # Check nothing was printed
    captured = capsys.readouterr()
    assert captured.out == ""
    assert result == "11000010"

def test_checkfile_action2_file_exists_inform(monkeypatch, capsys):
    # Mock os.path.exists to return True
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    
    # Action 2 (create if not present), file exists, notification level 16 (inform)
    result = checkfile("00010010", "test.txt")
    # Check message was printed
    captured = capsys.readouterr()
    assert "already exists" in captured.out
    assert result == "11010010"

def test_checkfile_action2_file_exists_warn(monkeypatch, capsys):
    # Mock os.path.exists to return True
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    
    # Action 2 (create if not present), file exists, notification level 32 (warn)
    result = checkfile("00100010", "test.txt")
    # Check warning was printed
    captured = capsys.readouterr()
    assert "Warning:" in captured.out
    assert result == "11100010"

def test_checkfile_action2_file_exists_error(monkeypatch):
    # Mock os.path.exists to return True
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    
    # Action 2 (create if not present), file exists, notification level 48 (error)
    with pytest.raises(FileExistsError):
        checkfile("00110010", "test.txt")

def test_checkfile_action2_creation_fails(monkeypatch):
    # Mock os.path.exists to return False but file creation to fail
    monkeypatch.setattr(os.path, "exists", lambda _: False)
    def mock_open(*args, **kwargs):
        raise PermissionError("Permission denied")
    monkeypatch.setattr("builtins.open", mock_open)
    
    # Action 2 (create if not present), file doesn't exist but creation fails
    with pytest.raises(RuntimeError, match="Creation failed"):
        checkfile("00000010", "test.txt")

# Tests for action 3: Create or recreate
def test_checkfile_action3_file_not_exists(monkeypatch):
    # Mock file doesn't exist initially but exists after creation
    exists_calls = [False, True]
    def mock_exists(_):
        return exists_calls.pop(0) if exists_calls else True
    monkeypatch.setattr(os.path, "exists", mock_exists)
    
    # Mock file creation
    class MockFile:
        def __init__(self, *args, **kwargs):
            pass
        def close(self):
            pass
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
    
    # Action 3 (create or recreate), file doesn't exist
    result = checkfile("00000011", "test.txt")
    # Expect bit 6 unset (file didn't exist) and bit 7 set (file exists after)
    assert result == "10000011"

def test_checkfile_action3_file_exists_silent(monkeypatch):
    # Setup - file exists before and after recreation
    exists_calls = [True, True]
    def mock_exists(_):
        return exists_calls.pop(0) if exists_calls else True
    monkeypatch.setattr(os.path, "exists", mock_exists)
    
    # Mock file operations
    monkeypatch.setattr(os, "remove", lambda _: None)
    class MockFile:
        def __init__(self, *args, **kwargs):
            pass
        def close(self):
            pass
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
    
    # Action 3 (create or recreate), file exists, notification level 0 (silent)
    result = checkfile("00000011", "test.txt")
    # Expect both bits 6 and 7 set (file existed before and after)
    assert result == "11000011"

def test_checkfile_action3_file_exists_inform(monkeypatch, capsys):
    # Setup - file exists before and after recreation
    exists_calls = [True, True]
    def mock_exists(_):
        return exists_calls.pop(0) if exists_calls else True
    monkeypatch.setattr(os.path, "exists", mock_exists)
    
    # Mock file operations
    monkeypatch.setattr(os, "remove", lambda _: None)
    class MockFile:
        def __init__(self, *args, **kwargs):
            pass
        def close(self):
            pass
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
    
    # Action 3 (create or recreate), file exists, notification level 16 (inform)
    result = checkfile("00010011", "test.txt")
    # Check message was printed
    captured = capsys.readouterr()
    assert "will be recreated" in captured.out
    assert result == "11010011"

def test_checkfile_action3_file_exists_warn(monkeypatch, capsys):
    # Setup - file exists before and after recreation
    exists_calls = [True, True]
    def mock_exists(_):
        return exists_calls.pop(0) if exists_calls else True
    monkeypatch.setattr(os.path, "exists", mock_exists)
    
    # Mock file operations
    monkeypatch.setattr(os, "remove", lambda _: None)
    class MockFile:
        def __init__(self, *args, **kwargs):
            pass
        def close(self):
            pass
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
    
    # Action 3 (create or recreate), file exists, notification level 32 (warn)
    result = checkfile("00100011", "test.txt")
    # Check warning was printed
    captured = capsys.readouterr()
    assert "Warning:" in captured.out
    assert "will be recreated" in captured.out
    assert result == "11100011"

def test_checkfile_action3_file_exists_error(monkeypatch):
    # Mock os.path.exists to return True
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    
    # Action 3 (create or recreate), file exists, notification level 48 (error)
    with pytest.raises(FileExistsError):
        checkfile("00110011", "test.txt")

def test_checkfile_action3_deletion_fails(monkeypatch):
    # Mock file exists but deletion fails
    monkeypatch.setattr(os.path, "exists", lambda _: True)
    def mock_remove(_):
        raise PermissionError("Permission denied")
    monkeypatch.setattr(os, "remove", mock_remove)
    
    # Action 3 (create or recreate), file exists but deletion fails
    with pytest.raises(RuntimeError, match="Deletion failed during recreation"):
        checkfile("00000011", "test.txt")

def test_checkfile_action3_creation_fails(monkeypatch):
    # Mock file doesn't exist and creation fails
    monkeypatch.setattr(os.path, "exists", lambda _: False)
    def mock_open(*args, **kwargs):
        raise PermissionError("Permission denied")
    monkeypatch.setattr("builtins.open", mock_open)
    
    # Action 3 (create or recreate), file doesn't exist but creation fails
    with pytest.raises(RuntimeError, match="Creation failed during recreation"):
        checkfile("00000011", "test.txt")

# Tests for checkdir input validation
def test_checkdir_pcode_length():
    # Test with invalid PCode length
    with pytest.raises(ValueError, match="PCode must be 8 characters long"):
        checkdir("0101", "test_dir")

def test_checkdir_pcode_invalid_chars():
    # Test with non-binary characters
    with pytest.raises(ValueError, match="PCode must be a binary string"):
        checkdir("0123abcd", "test_dir")

# Tests for action 0: Inquiry only
def test_checkdir_action0_dir_exists(monkeypatch):
    # Mock os.path.isdir to return True
    monkeypatch.setattr(os.path, "isdir", lambda _: True)
    
    # Action 0 (inquiry only), directory exists
    result = checkdir("00000000", "test_dir")
    # Expect bit 6 set (directory existed before), bit 7 set (directory exists after)
    assert result == "11000000"

def test_checkdir_action0_dir_not_exists(monkeypatch):
    # Mock os.path.isdir to return False
    monkeypatch.setattr(os.path, "isdir", lambda _: False)
    
    # Action 0 (inquiry only), directory doesn't exist
    result = checkdir("00000000", "test_dir")
    # Expect both bit 6 and 7 unset (directory never existed)
    assert result == "00000000"

# Tests for action 1: Delete if exists
def test_checkdir_action1_dir_exists(monkeypatch):
    # Mock directory exists before and not after deletion
    exists_calls = [True, False]
    def mock_isdir(_):
        return exists_calls.pop(0)
    
    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    monkeypatch.setattr(shutil, "rmtree", lambda _: None)  # Mock successful deletion
    
    # Action 1 (delete), directory exists
    result = checkdir("00000001", "test_dir")
    # Expect bit 6 set (directory existed before), bit 7 unset (doesn't exist after)
    assert result == "01000001"

def test_checkdir_action1_dir_not_exists_silent(monkeypatch, capsys):
    # Mock os.path.isdir to return False
    monkeypatch.setattr(os.path, "isdir", lambda _: False)
    
    # Action 1 (delete), directory doesn't exist, notification level 0 (silent)
    result = checkdir("00000001", "test_dir")
    # Expect both bits 6 and 7 unset (directory never existed)
    assert result == "00000001"
    
    # Check nothing was printed
    captured = capsys.readouterr()
    assert captured.out == ""

def test_checkdir_action1_dir_not_exists_inform(monkeypatch, capsys):
    # Mock os.path.isdir to return False
    monkeypatch.setattr(os.path, "isdir", lambda _: False)
    
    # Action 1 (delete), directory doesn't exist, notification level 4 (inform)
    result = checkdir("00000101", "test_dir")
    # Check message was printed
    captured = capsys.readouterr()
    assert "does not exist" in captured.out
    assert result == "00000101"

def test_checkdir_action1_dir_not_exists_warn(monkeypatch, capsys):
    # Mock os.path.isdir to return False
    monkeypatch.setattr(os.path, "isdir", lambda _: False)
    
    # Action 1 (delete), directory doesn't exist, notification level 8 (warn)
    result = checkdir("00001001", "test_dir")
    # Check warning was printed
    captured = capsys.readouterr()
    assert "Warning:" in captured.out
    assert result == "00001001"

def test_checkdir_action1_dir_not_exists_error(monkeypatch):
    # Mock os.path.isdir to return False
    monkeypatch.setattr(os.path, "isdir", lambda _: False)
    
    # Action 1 (delete), directory doesn't exist, notification level 12 (error)
    with pytest.raises(FileNotFoundError):
        checkdir("00001101", "test_dir")

def test_checkdir_action1_deletion_fails(monkeypatch):
    # Mock os.path.isdir to return True but shutil.rmtree to fail
    monkeypatch.setattr(os.path, "isdir", lambda _: True)
    def mock_rmtree(_):
        raise PermissionError("Permission denied")
    monkeypatch.setattr(shutil, "rmtree", mock_rmtree)
    
    # Action 1 (delete), directory exists but deletion fails
    with pytest.raises(RuntimeError, match="Deletion failed"):
        checkdir("00000001", "test_dir")

# Tests for action 2: Create if not present
def test_checkdir_action2_dir_not_exists(monkeypatch):
    # Setup
    # Mock directory doesn't exist initially but exists after creation
    exists_calls = [False, True]
    def mock_isdir(_):
        return exists_calls.pop(0) if exists_calls else True
    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    
    # Mock directory creation
    monkeypatch.setattr(os, "makedirs", lambda _: None)
    
    # Action 2 (create if not present), directory doesn't exist
    result = checkdir("00000010", "test_dir")
    # Expect bit 6 unset (directory didn't exist) and bit 7 set (directory exists after)
    assert result == "10000010"

def test_checkdir_action2_dir_exists_silent(monkeypatch, capsys):
    # Mock os.path.isdir to return True
    monkeypatch.setattr(os.path, "isdir", lambda _: True)
    
    # Action 2 (create if not present), directory exists, notification level 0 (silent)
    result = checkdir("00000010", "test_dir")
    # Check nothing was printed
    captured = capsys.readouterr()
    assert captured.out == ""
    assert result == "11000010"

def test_checkdir_action2_dir_exists_inform(monkeypatch, capsys):
    # Mock os.path.isdir to return True
    monkeypatch.setattr(os.path, "isdir", lambda _: True)
    
    # Action 2 (create if not present), directory exists, notification level 16 (inform)
    result = checkdir("00010010", "test_dir")
    # Check message was printed
    captured = capsys.readouterr()
    assert "already exists" in captured.out
    assert result == "11010010"

def test_checkdir_action2_dir_exists_warn(monkeypatch, capsys):
    # Mock os.path.isdir to return True
    monkeypatch.setattr(os.path, "isdir", lambda _: True)
    
    # Action 2 (create if not present), directory exists, notification level 32 (warn)
    result = checkdir("00100010", "test_dir")
    # Check warning was printed
    captured = capsys.readouterr()
    assert "Warning:" in captured.out
    assert result == "11100010"

def test_checkdir_action2_dir_exists_error(monkeypatch):
    # Mock os.path.isdir to return True
    monkeypatch.setattr(os.path, "isdir", lambda _: True)
    
    # Action 2 (create if not present), directory exists, notification level 48 (error)
    with pytest.raises(FileExistsError):
        checkdir("00110010", "test_dir")

def test_checkdir_action2_creation_fails(monkeypatch):
    # Mock os.path.isdir to return False but directory creation to fail
    monkeypatch.setattr(os.path, "isdir", lambda _: False)
    def mock_makedirs(_):
        raise PermissionError("Permission denied")
    monkeypatch.setattr(os, "makedirs", mock_makedirs)
    
    # Action 2 (create if not present), directory doesn't exist but creation fails
    with pytest.raises(RuntimeError, match="Creation failed"):
        checkdir("00000010", "test_dir")

# Tests for action 3: Create or recreate
def test_checkdir_action3_dir_not_exists(monkeypatch):
    # Mock directory doesn't exist initially but exists after creation
    exists_calls = [False, True]
    def mock_isdir(_):
        return exists_calls.pop(0) if exists_calls else True
    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    
    # Mock directory creation
    monkeypatch.setattr(os, "makedirs", lambda _: None)
    
    # Action 3 (create or recreate), directory doesn't exist
    result = checkdir("00000011", "test_dir")
    # Expect bit 6 unset (directory didn't exist) and bit 7 set (directory exists after)
    assert result == "10000011"

def test_checkdir_action3_dir_exists_silent(monkeypatch):
    # Setup - directory exists before and after recreation
    exists_calls = [True, True]
    def mock_isdir(_):
        return exists_calls.pop(0) if exists_calls else True
    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    
    # Mock directory operations
    monkeypatch.setattr(shutil, "rmtree", lambda _: None)
    monkeypatch.setattr(os, "makedirs", lambda _: None)
    
    # Action 3 (create or recreate), directory exists, notification level 0 (silent)
    result = checkdir("00000011", "test_dir")
    # Expect both bits 6 and 7 set (directory existed before and after)
    assert result == "11000011"

def test_checkdir_action3_dir_exists_inform(monkeypatch, capsys):
    # Setup - directory exists before and after recreation
    exists_calls = [True, True]
    def mock_isdir(_):
        return exists_calls.pop(0) if exists_calls else True
    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    
    # Mock directory operations
    monkeypatch.setattr(shutil, "rmtree", lambda _: None)
    monkeypatch.setattr(os, "makedirs", lambda _: None)
    
    # Action 3 (create or recreate), directory exists, notification level 16 (inform)
    result = checkdir("00010011", "test_dir")
    # Check message was printed
    captured = capsys.readouterr()
    assert "will be recreated" in captured.out
    assert result == "11010011"

def test_checkdir_action3_dir_exists_warn(monkeypatch, capsys):
    # Setup - directory exists before and after recreation
    exists_calls = [True, True]
    def mock_isdir(_):
        return exists_calls.pop(0) if exists_calls else True
    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    
    # Mock directory operations
    monkeypatch.setattr(shutil, "rmtree", lambda _: None)
    monkeypatch.setattr(os, "makedirs", lambda _: None)
    
    # Action 3 (create or recreate), directory exists, notification level 32 (warn)
    result = checkdir("00100011", "test_dir")
    # Check warning was printed
    captured = capsys.readouterr()
    assert "Warning:" in captured.out
    assert "will be recreated" in captured.out
    assert result == "11100011"

def test_checkdir_action3_dir_exists_error(monkeypatch):
    # Mock os.path.isdir to return True
    monkeypatch.setattr(os.path, "isdir", lambda _: True)
    
    # Action 3 (create or recreate), directory exists, notification level 48 (error)
    with pytest.raises(FileExistsError):
        checkdir("00110011", "test_dir")

def test_checkdir_action3_deletion_fails(monkeypatch):
    # Mock directory exists but deletion fails
    monkeypatch.setattr(os.path, "isdir", lambda _: True)
    def mock_rmtree(_):
        raise PermissionError("Permission denied")
    monkeypatch.setattr(shutil, "rmtree", mock_rmtree)
    
    # Action 3 (create or recreate), directory exists but deletion fails
    with pytest.raises(RuntimeError, match="Deletion failed during recreation"):
        checkdir("00000011", "test_dir")

def test_checkdir_action3_creation_fails(monkeypatch):
    # Mock directory doesn't exist and creation fails
    monkeypatch.setattr(os.path, "isdir", lambda _: False)
    def mock_makedirs(*args, **kwargs):
        raise PermissionError("Permission denied")
    monkeypatch.setattr(os, "makedirs", mock_makedirs)
    
    # Action 3 (create or recreate), directory doesn't exist but creation fails
    with pytest.raises(RuntimeError, match="Creation failed during recreation"):
        checkdir("00000011", "test_dir")

def test_chdir(monkeypatch):
    # Mock os.chdir to return None
    monkeypatch.setattr(os, "chdir", lambda _: None)
    
    # Test chdir
    chdir("test_dir")

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