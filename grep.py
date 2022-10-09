import sys
import os
import fnmatch

CASE_INSENSITIVE_FLAG = '-i'
WHOLE_WORD_FLAG = '-w'
ASTERISK_WILDCARD = '*'


def search_in_file(filepath: str, keyword: str, flag: str) -> str:
    """Search for matching lines in a single file"""
    output = ''

    with open(rf'{filepath}', 'r') as fp:
        lines = fp.readlines()
        # Filter each line with flag and wildcard
        for row in lines:
            if flag == CASE_INSENSITIVE_FLAG:
                if fnmatch.fnmatch(row.lower(), ASTERISK_WILDCARD + keyword.lower() + ASTERISK_WILDCARD):
                    output += format_single_output(filepath, lines.index(row) + 1, row)
            elif flag == WHOLE_WORD_FLAG:
                if fnmatch.fnmatch(row, ASTERISK_WILDCARD + keyword + ASTERISK_WILDCARD) and (' ' not in keyword):
                    output += format_single_output(filepath, lines.index(row) + 1, row)
            else:
                if fnmatch.fnmatch(row, ASTERISK_WILDCARD + keyword + ASTERISK_WILDCARD):
                    output += format_single_output(filepath, lines.index(row) + 1, row)

    return output


def traverse_directories(path: str, keyword: str, flag: str) -> str:
    """Traverse all directories and subdirectories, and examine every single file"""
    output = ''

    for (current_path, dirs, files) in os.walk(path, topdown=False):
        # Clean up hidden files and directories
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        # Loop through all files in the current directory
        for file in files:
            temp_output = search_in_file(f'{current_path}/{file}', keyword, flag)
            output += temp_output

    return output


def format_single_output(filepath: str, line_number: int, line_content: str) -> str:
    """Format a single line"""
    filepath_max_length, line_number_max_length, line_content_max_length = 40, 3, 40

    # Trim if max length is exceeded
    filepath = enforce_max_length(filepath, filepath_max_length)
    line_number = enforce_max_length(str(line_number), line_number_max_length)
    line_content = enforce_max_length(line_content.strip(), line_content_max_length)

    # Strip all newline characters to avoid inconsistency in formatting
    line_content = line_content.strip('\n')

    # Apply padding and alignment
    output = f'{filepath:<{filepath_max_length}} line {line_number:<{line_number_max_length}} \
        {line_content:<{line_content_max_length}}'

    # Add newline characters manually
    output += '\n'

    return output


def enforce_max_length(content: str, max_length: int) -> str:
    """Trim the string if characters limit is exceeded"""
    return content[:max_length] if len(content) > max_length else content


def format_final_output(output: str) -> str:
    """Format the whole output string"""
    return output.strip()


def validate_input(path: str, keyword: str, flag: str) -> None:
    """Validate user inputs"""
    args_limit = 4
    wildcard_limit = 4
    invalid_args_error_msg = 'Argumen program tidak benar.'

    try:
        # Validate number of args
        if len(sys.argv) > args_limit:
            raise Exception(invalid_args_error_msg)
        # Validate keyword
        if keyword.count(ASTERISK_WILDCARD) > wildcard_limit:
            raise Exception(invalid_args_error_msg)
        # Validate flag
        if (len(sys.argv) == args_limit) and (flag not in (CASE_INSENSITIVE_FLAG, WHOLE_WORD_FLAG)):
            raise Exception(invalid_args_error_msg)
        # Validate path
        if not os.path.exists(path):
            raise Exception(f'Path {path} tidak ditemukan')
    except Exception as error:
        print(error)
        sys.exit()


def main(path: str, keyword: str, flag: str) -> None:
    """Entry point of the program"""
    validate_input(path, keyword, flag)

    # Check if the path points to a file or a directory
    if os.path.isfile(path):
        output = search_in_file(path, keyword, flag)
    else:
        output = traverse_directories(path, keyword, flag)

    print(format_final_output(output))


# Start the program
main(sys.argv[-1], sys.argv[-2], sys.argv[-3])
