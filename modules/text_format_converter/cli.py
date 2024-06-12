#!/usr/bin/env python3
#coding: utf-8

# ##############################################################################

# SETTINGS
MODEL = "gpt-4o"
SYSTEM_PROMPT = """
Je veux que tu prennes un texte en entrée ainsi que le format souhaité de la sortie. Ton but est d'analyser silencieusement le texte afin de fournir en réponse une version convertie du texte dans le format souhaité. Répond uniquement avec le texte converti dans le format demandé, en utilisant toujours la forme suivante :
```
[data converted in format]
```
Mon premier texte est : "[insérer texte ici]". Le format de sortie souhaité est : "[insérer format ici]".
"""
CLI_ARG_PARSER_DESCRIPTION = "CLI app to text-generation of OpenAI's API with GPT Models."
CLI_ARG_PARSER_VERSION = "0.1.0"

# ##############################################################################

import os
from openai import OpenAI
from os import getenv
from os import path
import uuid
from textgen import generate
from argparsing import parser_args as argparser

def insert_module_prompt(text_, format_):
    return f"""texte : \"\"\"\n{text_}\n\"\"\"\nformat : \"{format_}\" """

def main():
    global MODEL
    global SYSTEM_PROMPT

    parser, args = argparser(description=CLI_ARG_PARSER_DESCRIPTION,
                             cli_version=CLI_ARG_PARSER_VERSION)


    verbose = args.verbose
    quiet = args.quiet
    input_ = args.input
    output_ = args.output
    temperature = args.temperature
    max_tokens = args.max_tokens
    top_p = args.top_p
    format_ = args.format
    cut_output_block_delimiter = args.cut

    def generate_unique_filename():
        # 6-16 characters long
        # without spaces or special characters
        # without extension

        # generate UUID
        unique_filename = str(uuid.uuid4())
        # remove the dashes
        unique_filename = unique_filename.replace("-", "")
        # get the length of the string
        length = len(unique_filename)
        # if length is greater than 16, slice the string and get the first 16 characters
        if length > 16:
            unique_filename = unique_filename[:16]
        # if length is less than 6, add random characters to the string, until the length is 6
        elif length < 6:
            unique_filename += str(uuid.uuid4())[:6-length]
        return unique_filename


    def run_llm_call(SYSTEM_PROMPT
            ,MODEL = "gpt-4"
            ,USER_PROMPT = "Quel est le format du texte suivant : \"Bonjour, je m'appelle Pierre et j'adore programmer.\""
            ,TEMPERATURE = 0.7
            ,MAX_TOKENS = 64
            ,TOP_P = 1.0):

        result = generate(
            USER_PROMPT,
            SYSTEM_PROMPT,
            MODEL,
            TEMPERATURE,
            MAX_TOKENS,
            TOP_P
        )

        return result

    # with `os` library,
    # check if `input_` exists ans if is a file
    if input_ and os.path.isfile(input_):
        with open(input_, "r") as f:
            input_ = f.read()

    # with `os` library, check if `output_` exists and if is a file
    # if is a file, display a warning message
    # if is a directory, write the output to a file in the directory
    # - unique output filename
    # - 6-16 characters long
    # - without spaces or special characters
    # - without extension
    if output_ and os.path.isfile(output_):
        print("Warning: The output file already exists. The content will be overwritten.")
        output_filepath = output_
    elif output_ and os.path.isdir(output_):
        dirpath_ = output_
        formated_unique_filename = generate_unique_filename()
        output_filepath = f"{dirpath_}/{formated_unique_filename}"
    elif output_ and not os.path.exists(output_):
        output_filepath = output_
    else:
        output_filepath = None
        # no output file , and no output directory specified
        print("Error: No output file or directory specified.")
        exit(1)

    input_ = insert_module_prompt(input_, format_)
    # run the LLM call
    result = run_llm_call(
        SYSTEM_PROMPT,
        MODEL,
        input_,
        temperature,
        max_tokens,
        top_p)

    if cut_output_block_delimiter:
        first_line = result.split("\n")[0]
        last_line = result.split("\n")[-1]
        # check one or more character(s) : '`' in the first line, and check if one or more character(s) : '`' in the last line.
        # Then remove the first line and the last line.
        if first_line.startswith("`") and last_line.endswith("`"):
            result = "\n".join(result.split("\n")[1:-1])


    # if output file is specified, write the result to the file
    if output_filepath:
        with open(output_filepath, "w") as f:
            f.write(result)
    if ( not quiet ):
        if ( verbose > 0 ):
            print(result)
    exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        # print the error code with ANSI color
        print(f"\033[91m{e}\033[0m")
        exit(1)


