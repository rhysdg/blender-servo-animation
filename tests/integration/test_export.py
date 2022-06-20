import json
import os
import re
import pytest

@pytest.mark.parametrize(
    "filename, precision, results",
    [
        ("without-precision.json", 0, {
            0: 90,
            11: 78,
            32: 45,
            54: 112,
            65: 135,
            88: 101,
            99: 90,
        }),
        ("with-precision.json", 2, {
            0: 90.0,
            11: 77.7,
            32: 45.0,
            54: 111.67,
            65: 135.0,
            88: 101.08,
            99: 90.0,
        }),
    ],
    ids=['Without precision', 'With precision']
)
def test_json_export(blender, filename, precision, results):
    export_file = blender.tmp(f"tests/tmp/{filename}")

    if os.path.exists(export_file):
        os.remove(export_file)

    assert not os.path.exists(export_file)

    blender.set_file("examples/Simple/example.blend")
    blender.start()
    blender.send_lines([
        "import bpy",
        f"bpy.ops.export_anim.servo_positions_json(filepath='{export_file}', precision={precision})"
    ])
    blender.expect("{'FINISHED'}")
    blender.close()

    assert os.path.exists(export_file), "expected export file to be present"

    with open(export_file, 'r', encoding='utf-8') as file:
        parsed = json.load(file)

    assert parsed["file"] == "example.blend"
    assert parsed["frames"] == 100
    assert len(parsed["positions"]["Bone"]) == 100

    for frame, position in results.items():
        assert parsed["positions"]["Bone"][frame] == position

    os.remove(export_file)


@pytest.mark.parametrize(
    "filename, precision, results",
    [
        ("without-precision.json", 0, {
            0: 90,
            11: 78,
            32: 45,
            54: 112,
            65: 135,
            88: 101,
            99: 90,
        }),
        ("with-precision.json", 2, {
            0: 90.0,
            11: 77.7,
            32: 45.0,
            54: 111.67,
            65: 135.0,
            88: 101.08,
            99: 90.0,
        }),
    ],
    ids=['Without precision', 'With precision']
)
def test_json_arduino(blender, filename, precision, results):
    export_file = blender.tmp(f"tests/tmp/{filename}")

    if os.path.exists(export_file):
        os.remove(export_file)

    assert not os.path.exists(export_file)

    blender.set_file("examples/Simple/example.blend")
    blender.start()
    blender.send_lines([
        "import bpy",
        f"bpy.ops.export_anim.servo_positions_arduino(filepath='{export_file}', precision={precision})"
    ])
    blender.expect("{'FINISHED'}")
    blender.close()

    assert os.path.exists(export_file), "expected export file to be present"

    with open(export_file, 'r', encoding='utf-8') as file:
        content = file.read()

    regex = re.compile(r"\{(.+)\}", re.MULTILINE | re.DOTALL)
    match = regex.search(content)

    assert match is not None

    json_string = match.group(0).replace("{\n ", "[").replace(",\n}", "]").replace("\n", "")
    json_positions = json.loads(json_string)

    assert "Frames: 100" in content
    assert len(json_positions) == 100

    for frame, position in results.items():
        assert json_positions[frame] == position

    os.remove(export_file)
