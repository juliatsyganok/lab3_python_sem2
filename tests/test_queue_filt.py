import sys
import os
import types
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from class_task import Task
from task_queue import TaskQueue, TaskIterator
from filters import filt_status, filt_priority, filt_ready, filt_all, take


def make_queue():
    q = TaskQueue()
    q.add_many([
        Task("1", "Написать тесты", priority="high", status="new"),
        Task("2", "Проверить логи", priority="low", status="new"),
        Task("3", "Исправить баг", priority="high", status="in_progress"),
        Task("4", "Обновить документацию", priority="medium", status="done"),
        Task("5", "Провести код-ревью", priority="medium",status="new"),
    ])
    return q
 
def test_empty():
    q = TaskQueue()
    assert len(q) == 0
    assert q.is_empty is True

def test_add():
    q = TaskQueue()
    q.add(Task("1", "Задача"))
    assert len(q) == 1

def test_type():
    q = TaskQueue()
    with pytest.raises(TypeError):
        q.add("не задача")

def test_remove():
    q = make_queue()
    q.remove("1")
    assert len(q) == 4

def test_missing():
    q = make_queue()
    with pytest.raises(KeyError):
        q.remove("нееееетттттт")

def test_get():
    q = make_queue()
    assert q.get("3").id == "3"

def test_iter():
    assert isinstance(iter(make_queue()), TaskIterator)

def test_loop():
    ids = [t.id for t in make_queue()]
    assert ids == ["1", "2", "3", "4", "5"]

def test_iteration():
    q = make_queue()
    assert list(q) == list(q)

def test_stop():
    with pytest.raises(StopIteration):
        next(iter(TaskQueue()))

def test_list_and_len():
    q = make_queue()
    assert len(list(q)) == len(q) == 5

def test_new():
    result = list(filt_status(make_queue(), "new"))
    assert len(result) == 3
    assert all(t.status == "new" for t in result)

def test_filter():
    assert isinstance(filt_status(make_queue(), "new"), types.GeneratorType)

def test_take_n():
    assert len(list(take(make_queue(), 2))) == 2

def test_exists():
    assert len(list(take(make_queue(), 100))) == 5

def test_zero():
    assert list(take(make_queue(), 0)) == []

