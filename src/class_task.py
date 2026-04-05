from datetime import datetime
from dataclasses import dataclass

class empty:
    """Дескриптор для непустых строк"""
    
    def __set_name__(self, owner, name):
        self.private = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private, None)
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.private[1:]} строка")
        if not value.strip():
            raise ValueError(f"{self.private[1:]} пустое")
        setattr(instance, self.private, value)


class reading(empty):
    """Установка 1 раз"""
    def __set__(self, instance, value):
        if hasattr(instance, self.private):
            raise AttributeError(f"{self.private[1:]} нельзя обновить значение")
        super().__set__(instance, value)


class choice:
    """Значение из списка"""
    def __init__(self, allowed_values):
        self.allowed_values = allowed_values
    
    def __set_name__(self, owner, name):
        self.private = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private, None)
    
    def __set__(self, instance, value):
        if value not in self.allowed_values:
            raise ValueError(f"{self.private[1:]} значение из списка {self.allowed_values}, '{value}'")
        setattr(instance, self.private, value)



@dataclass
class bounded:
    """строка длины не больше опр."""
    max_length: int        
    min_length: int = 1     

    def __set_name__(self, owner, name):
        self.private = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private, None)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.private[1:]} должно быть строкой")
        if len(value) < self.min_length:
            raise ValueError(f"{self.private[1:]}: минимум {self.min_length}")
        if len(value) > self.max_length:
            raise ValueError(f"{self.private[1:]}: максимум {self.max_length}")
        setattr(instance, self.private, value)

class Task:
    """Класс задачи"""
    id = reading()
    description = bounded(max_length=200)
    priority = choice(["low", "medium", "high"])
    status = choice(["new", "in_progress", "done"])
    
    def __init__(self, task_id: str, description: str, priority: str = "medium", status: str = "new"):
        self.id = task_id
        self.description = description
        self.priority = priority
        self.status = status
        self._created_at = datetime.now()
    
    @property
    def created_at(self) -> datetime:
        """Создано d"""
        return self._created_at
    
    @property
    def is_ready(self) -> bool:
        return self.status != "done" and self.priority != "low"
    
    def __repr__(self) -> str:
        return (f"Task(id={self.id!r}, description={self.description!r}, "f"priority={self.priority!r}, status={self.status!r}, "f"created_at={self.created_at.isoformat()!r})")
