import json
import os


def load_fixture(fixture):
    test_root_dir = os.path.abspath(os.path.join(__file__, '..'))
    fixture_path = os.path.join(test_root_dir, 'fixtures', fixture)

    with open(fixture_path, 'r') as f_:
        return json.loads(f_.read())
