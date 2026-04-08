import sys
import os
import types
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from class_task import Task
from task_queue import TaskQueue, TaskIterator
from filters import filter_by_status, filter_by_priority, filter_ready, filter_by_status_and_priority, take


def make_queue():
    q = TaskQueue()
    q.add_many([
        Task("t-001", "Написать тесты",       priority="high",   status="new"),
        Task("t-002", "Проверить логи",        priority="low",    status="new"),
        Task("t-003", "Исправить баг",         priority="high",   status="in_progress"),
        Task("t-004", "Обновить документацию", priority="medium", status="done"),
        Task("t-005", "Провести код-ревью",    priority="medium", status="new"),
    ])
    return q

def test_queue_empty():
    q = TaskQueue()
    assert len(q) == 0
    assert q.is_empty is True

def test_queue_add():
    q = TaskQueue()
    q.add(Task("x-1", "Задача"))
    assert len(q) == 1

def test_queue_add_wrong_type():
    q = TaskQueue()
    with pytest.raises(TypeError):
        q.add("не задача")

def test_queue_remove():
    q = make_queue()
    q.remove("t-001")
    assert len(q) == 4

def test_queue_remove_missing():
    q = make_queue()
    with pytest.raises(KeyError):
        q.remove("нет-такого")

def test_queue_get():
    q = make_queue()
    assert q.get("t-003").id == "t-003"

def test_iter_returns_task_iterator():
    assert isinstance(iter(make_queue()), TaskIterator)

def test_for_loop():
    ids = [t.id for t in make_queue()]
    assert ids == ["t-001", "t-002", "t-003", "t-004", "t-005"]

def test_repeat_iteration():
    q = make_queue()
    assert list(q) == list(q)

def test_stop_iteration_on_empty():
    with pytest.raises(StopIteration):
        next(iter(TaskQueue()))

def test_list_and_len():
    q = make_queue()
    assert len(list(q)) == len(q) == 5

def test_filter_status_new():
    result = list(filter_by_status(make_queue(), "new"))
    assert len(result) == 3
    assert all(t.status == "new" for t in result)

def test_filter_status_is_generator():
    assert isinstance(filter_by_status(make_queue(), "new"), types.GeneratorType)

def test_filter_status_invalid():
    with pytest.raises(ValueError):
        list(filter_by_status(make_queue(), "invalid"))

def test_filter_priority_high():
    result = list(filter_by_priority(make_queue(), "high"))
    assert len(result) == 2
    assert all(t.priority == "high" for t in result)

def test_filter_priority_is_generator():
    assert isinstance(filter_by_priority(make_queue(), "high"), types.GeneratorType)

def test_filter_ready():
    result = list(filter_ready(make_queue()))
    assert all(t.status != "done" for t in result)
    assert all(t.priority != "low" for t in result)

def test_filter_combined():
    result = list(filter_by_status_and_priority(make_queue(), "new", "high"))
    assert len(result) == 1
    assert result[0].id == "t-001"

def test_take_n():
    assert len(list(take(make_queue(), 2))) == 2

def test_take_more_than_exists():
    assert len(list(take(make_queue(), 100))) == 5

def test_take_zero():
    assert list(take(make_queue(), 0)) == []

def test_take_from_filter():
    result = list(take(filter_by_priority(make_queue(), "high"), 1))
    assert len(result) == 1
    assert result[0].priority == "high"