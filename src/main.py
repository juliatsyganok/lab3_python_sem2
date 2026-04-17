from class_task import Task
from task_queue import TaskQueue
from filters import filter_by_status, filter_by_priority, filter_ready, filter_by_status_and_priority, take


def f1() -> TaskQueue:
    """тестовая очередь"""
    queue = TaskQueue()
    queue.add_many([
        Task("1", "тесты", priority="high", status="new"),
        Task("2", "логи", priority="low", status="new"),
        Task("3", "баг", priority="high", status="in_progress"),
        Task("4", "док", priority="medium", status="done"),
        Task("5", "код", priority="medium", status="new"),
        Task("6", "ci cd", priority="high", status="in_progress"),
        Task("7", "задачи", priority="low", status="done"),
    ])
    return queue


def f2(queue: TaskQueue) -> None:
    for task in queue:
        print(f"{task.priority:6} {task.id} {task.description} {task.status}")


def f3(queue: TaskQueue) -> None:
    print("Повторный обход")
    first  = sum(1 for _ in queue)
    second = sum(1 for _ in queue)
    print(f"  Первый обход:  {first}  задач")
    print(f"  Второй обход: {second}  задач")
    assert first == second, "не совпадают"


def f4(queue: TaskQueue) -> None:
    print("Совместимость со встроенными функциями")
    as_list = list(queue)
    print(f"{len(as_list)} элементов")
    print(f"{len(queue)}")


def demo_filters(queue: TaskQueue) -> None:
    print("Ленивые фильтры")
    print("\n  — filter_by_status(queue, 'new'):")
    for task in filter_by_status(queue, "new"):
        print(f"    {task.id}: {task.description}")

    print("\n  — filter_by_priority(queue, 'high'):")
    for task in filter_by_priority(queue, "high"):
        print(f"    {task.id}: {task.description}")

    print("\n  — filter_ready(queue)  [не done И не low]:")
    for task in filter_ready(queue):
        print(f"    {task.id}: {task.description}")

    print("\n  — filter_by_status_and_priority(queue, 'in_progress', 'high'):")
    for task in filter_by_status_and_priority(queue, "in_progress", "high"):
        print(f"    {task.id}: {task.description}")


def f5(queue: TaskQueue) -> None:
    print("Генератор take")
    first_3 = list(take(queue, 3))
    print(f"  take(queue, 3) → {[t.id for t in first_3]}")


def f6(queue: TaskQueue) -> None:
    print("Цепочка фильтров")
    result = list(take(filter_by_priority(filter_by_status(queue, "new"), "high"), 2))
    for task in result:
        print(f"{task.id}: {task.description}")


if __name__ == "__main__":
    queue = f1()
    f1(queue)
    f2(queue)
    f3(queue)
    f4(queue)
    f5(queue)
    f6(queue)