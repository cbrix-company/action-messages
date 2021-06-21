import argparse
import json
import logging
import sys

from parsers import BanditParser


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


parsers = {
    'bandit': {
        'output_type': 'json',
        'parser': BanditParser,
    }
}


def load_output(file_path, output_type):
    with open(file_path, 'r') as f_:
        if file_path.endswith('.json'):
            return json.loads(f_.read())
        else:
            sys.exit('only json is supported')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Process some integers.')
    arg_parser.add_argument('--input-file', type=str, dest='input_file', help='path to tool output file')
    arg_parser.add_argument('--output-type', type=str, dest='output_type', choices=['slack'])

    arg_parser.add_argument('--repo-name', type=str, dest='repo_name', help='name of repo scanned')
    arg_parser.add_argument('--tool', type=str, dest='tool', help='name of tool', choices=parsers.keys())

    params = arg_parser.parse_args()

    parser_cls = parsers.get(params.tool)
    if not parser_cls:
        sys.exit(f"'{params.tool}' is not a supported parser")

    output = load_output(params.output_file)
    parser = parser_cls(output)

    fn_name = f'render_to_{params.tool}'
    try:
        render_fn = getattr(parser, fn_name)
    except AttributeError:
        sys.exit(f"'{params.tool}' has no '{fn_name}' method")

    message = render_fn()

    # Set Github outputs
    print('::set-output name={0}::{1}'.format('message', message))
    print('::set-output name={0}::{1}'.format('isEmpty', parser.is_empty()))
