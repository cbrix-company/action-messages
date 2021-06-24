import argparse
import json
import logging
import sys

from renderers import BanditMessageRenderer


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


registry = {
    'bandit': BanditMessageRenderer,
}


def load_input(file_path):
    with open(file_path, 'r') as f_:
        if file_path.endswith('.json'):
            return json.loads(f_.read())
        else:
            sys.exit('only json is supported')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Process some integers.')
    arg_parser.add_argument('--context', type=str, dest='context', required=True)
    arg_parser.add_argument(
        '--tool',
        type=str,
        dest='tool',
        help='name of tool',
        required=True,
        choices=registry.keys()
    )
    arg_parser.add_argument('--input-file', type=str, dest='input_file', required=True, help='input file')
    arg_parser.add_argument('--output-file', type=str, dest='output_file', required=True, help='path to rendered output file')
    arg_parser.add_argument('--renderer', type=str, dest='renderer', required=True)

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

    # load json context
    context = json.loads(params.context)

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
