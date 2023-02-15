import core.folder_select as fs

def test_dir_memory():
    dm = fs.DirMemory()
    assert dm.current() == ""

    dm.add("path_a")
    assert dm.current() == "path_a"

    dm.add("path_b")
    assert dm.current() == "path_b"

    dm.backward()
    assert dm.current() == "path_a"

    dm.forward()
    assert dm.current() == "path_b"

    dm.forward()
    assert dm.current() == "path_b"

    dm.backward()
    dm.backward()
    dm.backward()
    dm.backward()
    assert dm.current() == "path_a"
