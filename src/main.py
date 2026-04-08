from class_task import Task
from task_queue import TaskQueue
from filters import filter_by_status, filter_by_priority, filter_ready, filter_by_status_and_priority, take


def make_sample_queue() -> TaskQueue:
    """Создаём тестовую очередь с разными задачами"""
    queue = TaskQueue()
    queue.add_many([
        Task("t-001", "Написать тесты",          priority="high",   status="new"),
        Task("t-002", "Проверить логи",           priority="low",    status="new"),
        Task("t-003", "Исправить баг #42",        priority="high",   status="in_progress"),
        Task("t-004", "Обновить документацию",    priority="medium", status="done"),
        Task("t-005", "Провести код-ревью",       priority="medium", status="new"),
        Task("t-006", "Развернуть на стейдже",    priority="high",   status="in_progress"),
        Task("t-007", "Закрыть старые задачи",    priority="low",    status="done"),
    ])
    return queue


def demo_basic_iteration(queue: TaskQueue) -> None:
    for task in queue:
        print(f"  [{task.priority:6}] {task.id} — {task.description} ({task.status})")


def demo_repeat_iteration(queue: TaskQueue) -> None:
    print("Повторный обход")
    first  = sum(1 for _ in queue)
    second = sum(1 for _ in queue)
    print(f"  Первый обход:  {first}  задач")
    print(f"  Второй обход: {second}  задач")
    assert first == second, "не совпадают"


def demo_builtins(queue: TaskQueue) -> None:
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


def demo_take(queue: TaskQueue) -> None:
    print("Генератор take")
    first_3 = list(take(queue, 3))
    print(f"  take(queue, 3) → {[t.id for t in first_3]}")


def demo_chain(queue: TaskQueue) -> None:
    print("Цепочка фильтров")
    result = list(take(filter_by_priority(filter_by_status(queue, "new"), "high"), 2))
    for task in result:
        print(f"{task.id}: {task.description}")


if __name__ == "__main__":
    queue = make_sample_queue()
    print(f"\nОчередь создана: {queue}\n")

    demo_basic_iteration(queue)
    demo_repeat_iteration(queue)
    demo_builtins(queue)
    demo_filters(queue)
    demo_take(queue)
    demo_chain(queue)