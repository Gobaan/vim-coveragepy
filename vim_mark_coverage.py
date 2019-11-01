import mark_coverage
import vim

def is_keyword(word):
    return word.split()[0] in ('', 'def', 'class', 'else:')

def mark_buffer(cb):
    if not mark_coverage.handles(cb.name):
        return

    try:
        marker = mark_coverage.get_file_marker(cb.name)
    except TypeError:
        print (f'no coverage information found for {cb.name}')

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

