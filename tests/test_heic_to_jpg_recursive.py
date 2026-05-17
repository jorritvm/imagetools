from pathlib import Path

from src.operations import heic_to_jpg


class FakePool:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def map(self, func, iterable):
        for item in iterable:
            func(item)


def test_heic_to_jpg_operation_processes_subfolders_recursively(monkeypatch, tmp_path):
    root_heic = tmp_path / "root.heic"
    nested_dir = tmp_path / "nested" / "child"
    nested_dir.mkdir(parents=True)
    nested_heic = nested_dir / "nested.heic"

    root_heic.write_text("root")
    nested_heic.write_text("nested")

    root_mov = tmp_path / "root.mov"
    nested_mov = nested_dir / "nested.mov"
    root_mov.write_text("root live")
    nested_mov.write_text("nested live")

    messages = []

    monkeypatch.setattr(heic_to_jpg, "check_if_imagemagick_is_installed", lambda callback: True)
    monkeypatch.setattr(heic_to_jpg.mp, "Pool", FakePool)

    def fake_convert(heic_file_path: str) -> None:
        heic_path = Path(heic_file_path)
        heic_path.with_suffix(".jpg").write_text("jpg")

    monkeypatch.setattr(heic_to_jpg, "convert_heic_to_jpg", fake_convert)

    heic_to_jpg.heic_to_jpg_operation(str(tmp_path), lambda msg, progress: messages.append((msg, progress)))

    assert not root_heic.exists()
    assert not nested_heic.exists()
    assert root_heic.with_suffix(".jpg").exists()
    assert nested_heic.with_suffix(".jpg").exists()
    assert not root_mov.exists()
    assert not nested_mov.exists()
    assert messages[-1] == ("Finished!", 100)

