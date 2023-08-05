from unittest import TestCase

from holour import json_encode, json_decode
from holour.msg import AddTask, MoveOperation, CompleteOperation, Destination, ConfirmNeeded


class TestAddTask(TestCase):

    def test_add_task(self):
        add_task = AddTask('uuid')
        add_task_string = json_encode(add_task)
        expected_string = '{"_type": "add_task", "task_uuid": "uuid"}'

        assert type(add_task_string) == str
        assert add_task_string == expected_string, f"Expected {expected_string}, got: {add_task_string}"

        add_task_decoded = json_decode(add_task_string)
        assert type(add_task_decoded) == AddTask, f"Got: {type(add_task_decoded)}. Expected {AddTask}"
        assert add_task_decoded == add_task, "The decoded object must be equal to the encoded"

    def test_add_task_equals(self):
        at1 = AddTask('uuid')
        at2 = AddTask('uuid')
        at3 = AddTask('uuid2')

        assert at1 == at2
        assert at1 != at3
        assert at1 != "not status"

    def test_add_task_repr(self):
        add_task = AddTask('uuid')
        expected, got = 'uuid', f'{add_task}'

        assert expected in got, f"Expected {expected} in got: {got}"


class TestMoveOperation(TestCase):

    def test_move_operation(self):
        move_operation = MoveOperation('uuid', Destination.Robot)
        move_operation_string = json_encode(move_operation)
        expected_string = '{"_type": "move_operation", "operation_uuid": "uuid", "destination": "Robot"}'

        assert type(move_operation_string) == str
        assert move_operation_string == expected_string, f"Expected {expected_string}, got: {move_operation_string}"

        move_operation_decoded = json_decode(move_operation_string)
        assert type(move_operation_decoded) == MoveOperation, f"Got: {type(move_operation_decoded)}. " \
                                                              f"Expected {MoveOperation}"
        assert move_operation_decoded == move_operation, f"The decoded object: {move_operation_decoded} " \
                                                         f"must be equal to the encoded: {move_operation}"

    def test_move_operation_equals(self):
        mo1 = MoveOperation('uuid', Destination.Human)
        mo2 = MoveOperation('uuid', Destination.Human)
        mo3 = MoveOperation('uuid', Destination.Robot)

        assert mo1 == mo2, f"This: {mo1}, should be equal to this: {mo2}"
        assert mo1 != mo3, f"This: {mo1}, should not be equal to this: {mo3}"
        assert mo1 != "not status"

    def test_move_operation_repr(self):
        move_operation = MoveOperation('uuid', Destination.Robot)
        expected, got = 'Robot', f'{move_operation}'

        assert expected in got, f"Expected {expected} in got: {got}"


class TestCompleteOperation(TestCase):

    def test_complete_operation(self):
        complete_operation = CompleteOperation('uuid')
        complete_operation_string = json_encode(complete_operation)
        expected_string = '{"_type": "complete_operation", "operation_uuid": "uuid"}'

        assert type(complete_operation_string) == str
        assert complete_operation_string == expected_string, f"Expected {expected_string}, got: {complete_operation_string}"

        complete_operation_decoded = json_decode(complete_operation_string)
        assert type(complete_operation_decoded) == CompleteOperation, f"Got: {type(complete_operation_decoded)}. " \
                                                                      f"Expected {CompleteOperation}"
        assert complete_operation_decoded == complete_operation, f"The decoded object: {complete_operation_decoded} " \
                                                         f"must be equal to the encoded: {complete_operation}"

    def test_complete_operation_equals(self):
        co1 = CompleteOperation('uuid')
        co2 = CompleteOperation('uuid')
        co3 = CompleteOperation('uuid2')

        assert co1 == co2
        assert co1 != co3
        assert co1 != "not status"

    def test_complete_operation_repr(self):
        complete_operation = CompleteOperation('uuid')
        expected, got = 'uuid', f'{complete_operation}'

        assert expected in got, f"Expected {expected} in got: {got}"


class TestConfirmNeeded(TestCase):

    def test_confirm_needed(self):
        confirm_needed = ConfirmNeeded('uuid', True)
        confirm_needed_string = json_encode(confirm_needed)
        expected_string = '{"_type": "confirm_needed", "operation_uuid": "uuid", "confirm_needed": true}'

        assert type(confirm_needed_string) == str
        assert confirm_needed_string == expected_string, f"Expected {expected_string}, got: {confirm_needed_string}"

        confirm_needed_decoded = json_decode(confirm_needed_string)
        assert type(confirm_needed_decoded) == ConfirmNeeded, f"Got: {type(confirm_needed_decoded)}. " \
                                                              f"Expected {ConfirmNeeded}"
        assert confirm_needed_decoded == confirm_needed, f"The decoded object: {confirm_needed_decoded} " \
                                                         f"must be equal to the encoded: {confirm_needed}"

    def test_confirm_needed_equals(self):
        co1 = ConfirmNeeded('uuid', True)
        co2 = ConfirmNeeded('uuid',  True)
        co3 = ConfirmNeeded('uuid', False)

        assert co1 == co2
        assert co1 != co3
        assert co1 != "not status"

    def test_confirm_needed_repr(self):
        confirm_needed = ConfirmNeeded('uuid', True)
        expected, got = 'uuid', f'{confirm_needed}'

        assert expected in got, f"Expected {expected} in got: {got}"
