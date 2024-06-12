#coding: utf-8

import argparse

def parser_args(description, cli_version):
    parser = argparse.ArgumentParser(description=f"{description}")

    """
    Arguments :
    -h : help
    -V : version
    ----------------
    -v : verbose level
    -q : quiet mode
    ----------------
    -i : input file (USER_PROMPT)
    -o : output file (ASSISTANT_PROMPT)
    -t : parameter for the temperature
    -m : maximum number of tokens
    -T : top-p sampling
    """

    def usage():
        nonlocal parser
        parser.print_help()
        exit(1)

    # version
    parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {cli_version}')

    # verbose level ( `-v`, `-vv`, `-vvv`)
    parser.add_argument('-v', '--verbose', action='count', default=0, help="Verbose level")

    # quiet mode
    parser.add_argument('-q', '--quiet', action='store_true', help="Quiet mode")

    # input file
    parser.add_argument('-i', '--input', type=str, help="Input file", required=True)

    # output file
    parser.add_argument('-o', '--output', type=str, help="Output file", required=True)

    # temperature
    parser.add_argument('-t', '--temperature', type=float, help="Temperature", default=0.7)

    # maximum number of tokens
    parser.add_argument('-m', '--max_tokens', type=int, help="Maximum number of tokens", default=64)

    # top-p sampling
    parser.add_argument('-T', '--top_p', type=float, help="Top-p sampling", default=1.0)

    # format of the input file
    parser.add_argument('-format', '--format', type=str, help="Format of the input file", default="plain text")

    # cut outputs lines with: '```' and '```' ( first line and last line )
    parser.add_argument('-cut', '--cut', action='store_true', help="Cut outputs lines with: '```' and '```' ( first line and last line )")


    # parse arguments
    def parsing():
        nonlocal parser
        nonlocal usage
        try:
            args = parser.parse_args()
            return args
        # handle exceptions for `parser.parse_args()` method
        except Exception as e:
            print(f"Error : {e}")
            usage()
        except SystemExit:
            exit(1)
        except KeyboardInterrupt:
            exit(1)
        # handle exceptions for all other cases : 'a required argument is missing', 'the type of an argument is incorrect', 'the value of an argument is invalid', 'the number of arguments is incorrect'
        # handle exceptions for 'a required argument is missing'
        except argparse.ArgumentError as e:
            print(f"Error : {e}")
            usage()
        except argparse.ArgumentTypeError as e:
            print(f"Error : {e}")
            usage()
        else:
            # unknown error
            raise Exception("An unknown error occurred")

    args_ = parsing()
    return parser, args_


