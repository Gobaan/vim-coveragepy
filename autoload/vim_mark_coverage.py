import mark_coverage
import vim

def is_keyword(word):
    return word.split()[0] in ('', 'def', 'class', 'else:')

def mark_buffer(cb):
    if not mark_coverage.handles(cb.name):
        return

    try:
        marker = mark_coverage.get_file_marker(cb.name)
    except TypeError as e:
        print (f'no coverage information found for {cb.name}', e)

        return

    for line_number in range(len(cb)):
        sign = ''

        if not cb[line_number].strip():
            continue

        if marker.line_fails(line_number + 1):
            sign = 'failing'
        elif not marker.line_is_tested(line_number + 1) and not is_keyword(cb[line_number]):
            sign = 'notcovered'

        if sign:
            cmd = f"execute ':sign place {1000 + line_number} line={line_number + 1} name={sign} file={cb.name}'"
            vim.command(cmd)

def show_tests(cb, line_number):

    if not mark_coverage.handles(cb.name):
        return

    try:
        marker = mark_coverage.get_file_marker(cb.name)
    except TypeError as e:
        print (f'no coverage information found for {cb.name}', e)

    def get_output():
        covering_tests = marker.get_tests_covering_line(line_number)
        result = ('Pass' if marker.get_test_is_successful(test) else 'FAIL' for test in covering_tests)
        output = [f'{test} ... {result}' for test, result in zip(covering_tests, result)]
        output = '\n'.join(output)
        output = output.replace("'", "")

        return output

    cmd = f"""execute ':call vimPanel#Render("{get_output()}", "coveragepy")'"""
    vim.command(cmd)

    return


