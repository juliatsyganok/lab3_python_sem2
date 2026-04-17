from class_task import Task
from task_queue import TaskQueue
from filters import filt_status, filt_priority, filt_ready, filt_all, take

def f0() -> TaskQueue:
    queue = TaskQueue()
    queue.add_many([
        Task("1", "тесты", prior="high", status="new"),
        Task("2", "логи", prior="low", status="new"),
        Task("3", "баг", prior="high", status="in_progress"),
        Task("4", "док", prior="medium", status="done"),
        Task("5", "код", prior="medium", status="new"),
        Task("6", "ci cd", prior="high", status="in_progress"),
        Task("7", "задачи", prior="low", status="done"),
    ])
    return queue

def f1(queue: TaskQueue) -> None:
    for task in queue:
        print(f"{task.prior:6} {task.id} {task.descr} {task.status}")

def f3(queue: TaskQueue) -> None:
    print("обход 2")
    first = sum(1 for _ in queue)
    second = sum(1 for _ in queue)
    print(f"1: {first} задач")
    print(f"2: {second} задач")
    assert first == second, "не совпадают"

def f4(queue: TaskQueue) -> None:
    as_list = list(queue)
    print(f"{len(as_list)}")
    print(f"{len(queue)}")

def demo_filters(queue: TaskQueue) -> None:
    print("status new:")
    for task in filt_status(queue, "new"):
        print(f"{task.id} {task.descr}")

    print("priority high:")
    for task in filt_priority(queue, "high"):
        print(f"{task.id} {task.descr}")

    print("ready:")
    for task in filt_ready(queue):
        print(f"{task.id} {task.descr}")

    print("all:")
    for task in filt_all(queue, "in_progress", "high"):
        print(f"{task.id} {task.descr}")

def f5(queue: TaskQueue) -> None:
    print("Генератор")
    first_3 = list(take(queue, 3))
    print(f"{[t.id for t in first_3]}")

def f6(queue: TaskQueue) -> None:
    print("фильтры")
    result = list(take(filt_priority(filt_status(queue, "new"), "high"), 2))
    for task in result:
        print(f"{task.id}: {task.descr}")

if __name__ == "__main__":
    queue = f0()
    f1(queue)
    f3(queue)
    f4(queue)
    demo_filters(queue) 
    f5(queue)
    f6(queue)