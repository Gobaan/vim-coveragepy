import pytest
import functions

@pytest.fixture
def dummy():
    yield functions.Dummy()

def test_passes_functions():
    assert functions.sum(10, 10) == 20
    assert functions.product(10, 10) == 100
    assert functions.all_branches_pass(1) == 20
    assert functions.all_branches_pass(2) == 15
    assert functions.all_branches_pass(0) == 10
    assert functions.two_branch_fails(True) == 20
    assert functions.for_loop_passes(2) == 1
    assert functions.for_loop_skipped_passes(0) == 0

def test_passes_classes(dummy):
    assert dummy.sum(10, 10) == 20
    assert dummy.product(10, 10) == 100
    assert dummy.all_branches_pass(1) == 20
    assert dummy.all_branches_pass(2) == 15
    assert dummy.all_branches_pass(0) == 10
    assert dummy.two_branch_fails(1) == 20
    assert dummy.for_loop_passes(2) == 1
    assert dummy.for_loop_skipped_passes(0) == 0

def test_passes_class_repeat(dummy):
    test_passes_classes(dummy)

def test_function_fails():
    functions.fails()

def test_function_branch_fails_on_two():
    functions.two_branch_fails(2)

def test_class_branch_fails_on_two(dummy):
    dummy.two_branch_fails(2)

def test_function_branch_fails():
    functions.two_branch_fails(0)

def test_class_branch_fails(dummy):
    dummy.two_branch_fails(0)

def test_class_fails(dummy):
    dummy.fails()

def test_function_for_loop_fails():
    assert functions.for_loop_fails(1) == 2

def test_function_for_loop_skipped_fails():
    assert functions.for_loop_skipped_fails(0) == 2

def test_class_for_loop_fails(dummy):
    assert dummy.for_loop_fails(1) == 2

def test_class_for_loop_skipped_fails(dummy):
    assert dummy.for_loop_skipped_fails(0) == 2
