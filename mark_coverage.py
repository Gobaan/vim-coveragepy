import logging
import sqlite3
import coverage.numbits
import io
import os

logger = logging.getLogger('coverage')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('coverage-vim.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def compress(arrays):
    if len(arrays) == 0:
        raise TypeError("Numbits array is empty")

    if len(arrays) == 1:
        return arrays[0]

    return coverage.numbits.numbits_union(arrays[0], compress(arrays[1:]))


def matching_key(name, dictionary):
    while name:
        if name in dictionary:
            return name
        name = '.'.join(name.split('.')[1:])

    return None


class PythonFileCover(object):
    def __init__(self, name, test_lines, failing_tests):
        self.name = name
        self.test_lines = test_lines
        self.failing_tests = failing_tests
        logger.debug({ test: coverage.numbits.numbits_to_nums(numbits)
            for test, numbits in self.test_lines.items()})
        self.tested_lines = compress(list(self.test_lines.values()))
        filenames = [matching_key(test, self.test_lines) for test in self.failing_tests]
        filenames = [name for name in filenames if name]
        self.failing_lines = compress([self.test_lines[test] for test in filenames])
        logger.debug(coverage.numbits.numbits_to_nums(self.tested_lines))


    def line_is_tested(self, line_number):
        try:
            return coverage.numbits.num_in_numbits(line_number, self.tested_lines)
        except IndexError:
            return False

    def line_fails(self, line_number):
        try:
            return coverage.numbits.num_in_numbits(line_number, self.failing_lines)
        except IndexError:
            return False

    def get_tests_covering_line(self, line_number):
        return [test for test, value in self.test_lines.items()
            if coverage.numbits.num_in_numbits(value, line_number)]

    def get_test_is_successful(self, name):
        return name not in self.failing_tests

def find_coverage_folder():
    coverage_folder = os.path.join(os.getcwd())

    while not os.path.isfile(os.path.join(coverage_folder, '.coverage')):
        coverage_folder = os.path.abspath(os.path.join(coverage_folder, '..'))

        if coverage_folder == '/':
            raise TypeError('No coverage information found')

    return os.path.join(coverage_folder)

# Given a line
# Give me a list of tests covering that function and which ones pass (if the list is empty mark the line)
## If the line is a non-lambda function (also bug out hard on def inside a string but I DONT CARE)
### Tell me how many tests fail that function
def get_db_context(name):
    # For a given file, get its line bit vector 
    coverage_file = os.path.join(find_coverage_folder(), '.coverage')
    with sqlite3.connect(coverage_file) as conn:
        c = conn.cursor()
        file_query = f"select id from file where path = '{name}';"
        logger.debug(file_query)
        c.execute(file_query)

        file_number = c.fetchone()[0]
        line_query = f"select * from line_bits where file_id = {file_number};"
        logger.debug(line_query)
        c.execute(line_query)

        lines = c.fetchall()
        logger.debug(lines)
        context_ids = tuple(line[1] for line in lines)

        if len(context_ids) == 1:
            context_query = f"select * from context where id == '{context_ids[0]}';"
        else:
            context_query = f"select * from context where id in {context_ids};"

        logger.debug(context_query)
        contexts = c.execute(context_query)
        contexts = c.fetchall()
    logger.debug(contexts)
    id_test = {context[0]: context[1] for context in contexts}
    test_lines = {id_test[line[1]]: line[2] for line in lines}

    return test_lines


def get_failing_tests(pytest_output):
    def format_test_name(name):
        name = name.split()[1]
        name = name.replace('/', '.')
        name = name.replace('.py::', '.')

        return name

    MARKER = '=========================== short test summary info ============================\n'
    try:
        logger.debug(pytest_output)
        failures = pytest_output[pytest_output.index(MARKER) + 1:]
    except IndexError:
        print ("Index Error")

        return [], 0

    failing_tests = [format_test_name(failure) for failure in failures[:-1]]
    number_failures = int(failures[-1].split()[1])

    if len(failing_tests) != number_failures:
        raise Exception("Mismatched length of failures")

    return set(failing_tests)


def handles(name):
    return name.endswith('.py')

def get_file_marker(name):
    test_lines = get_db_context(name)
    pytest_output_file = os.path.join(find_coverage_folder(), 'out.txt')
    with open(pytest_output_file) as fp:
        failing_tests = get_failing_tests(fp.readlines())

    return PythonFileCover(name, test_lines, failing_tests)


if __name__ == '__main__':
    name = '/home/lordofall/menu-translator-django/backend/translator/schema.py'
    marker = get_file_marker(name)
    print (marker.get_tests_covering_line(7))
