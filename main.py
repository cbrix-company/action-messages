import argparse
import json
import logging
import pathlib
import sys

from renderers import BanditMessageRenderer


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


registry = {
    'bandit': BanditMessageRenderer,
}

SUPPORTED_FILE_EXTENSIONS = set({
    '.json',
})


def load_input(file_path):
    suffix = pathlib.Path(file_path).suffix
    if suffix not in SUPPORTED_FILE_EXTENSIONS:
        sys.exit('{0} is not a supported file extension'.format(suffix))

    with open(file_path, 'r') as f_:
        return json.loads(f_.read())


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Process some integers.')
    arg_parser.add_argument('--tool', type=str, help='name of tool', required=True, choices=registry.keys())
    arg_parser.add_argument('--input-file', type=str, dest='input_file', required=True, help='input file')
    arg_parser.add_argument('--output-file', type=str, dest='output_file', required=True, help='output file')
    arg_parser.add_argument('--renderer', type=str, dest='renderer', required=True)

    arg_parser.add_argument('--repository', type=str, required=True)
    arg_parser.add_argument('--ref', type=str, required=True)
    arg_parser.add_argument('--actor', type=str, required=True)
    arg_parser.add_argument('--run-id', type=str, required=True)
    arg_parser.add_argument('--sha', type=str, required=True)

    params = arg_parser.parse_args()

    # find parser class if available
    parser_cls = registry.get(params.tool)
    if not parser_cls:
        sys.exit(f"'{params.tool}' is not a supported parser")

    # check if renderer supported
    fn_name = f'render_to_{params.renderer}'
    renderers = parser_cls.list_renderers()
    if params.renderer not in renderers:
        sys.exit(f"{parser_cls.__name__} has no '{fn_name}' method")

    # default context for renderers
    context = {
        'repository': params.repository,
        'ref': params.ref,
        'actor': params.actor,
        'run-id': params.run_id,
        'sha': params.sha,
    }

    # instantiate parser class
    output_data = load_input(params.input_file)
    parser = parser_cls(output_data, **context)

    # call renderer function
    render_fn = getattr(parser, fn_name)
    message = render_fn()

    with open(params.output_file, 'w') as f:
        f.write(message)

    # Set Github outputs
    print('::set-output name={0}::{1}'.format('output-file', params.output_file))
    print('::set-output name={0}::{1}'.format('isEmpty', parser.is_empty()))
