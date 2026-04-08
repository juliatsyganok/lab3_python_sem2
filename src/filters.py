from typing import Iterator
from class_task import Task

def filter_by_status(tasks, status: str) -> Iterator[Task]:
    """фильтр по статусу задачи"""
    allowed = {"new", "in_progress", "done"}
    if status not in allowed:
        raise ValueError(f"Неверный статус: {status!r}")
    for task in tasks:
        if task.status == status:
            yield task

def filter_by_priority(tasks, priority: str) -> Iterator[Task]:
    """фильтр по приоритету задачи"""
    allowed = {"low", "medium", "high"}
    if priority not in allowed:
        raise ValueError(f"Неверный приоритет: {priority!r}")
    for task in tasks:
        if task.priority == priority:
            yield task


def filter_ready(tasks) -> Iterator[Task]:
    """только задачи, готовые к работе"""
    for task in tasks:
        if task.is_ready:
            yield task

def filter_by_status_and_priority(tasks, status: str, priority: str) -> Iterator[Task]:
    """общий фильтр"""
    return filter_by_priority(filter_by_status(tasks, status), priority)


def take(tasks, n: int) -> Iterator[Task]:
    """генератор"""
    count = 0
    for task in tasks:
        if count >= n:
            return     
        yield task
        count += 1