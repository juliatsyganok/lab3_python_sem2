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
            raise AttributeError(f"{self.private[1:]} нельзя обновить")
        super().__set__(instance, value)


class choice:
    """Значение из списка"""
    def __init__(self, al_val):
        self.al_val = al_val
    
    def __set_name__(self, owner, name):
        self.private = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private, None)
    
    def __set__(self, instance, value):
        if value not in self.al_val:
            raise ValueError(f"{self.private[1:]} знач из списка {self.al_val}, '{value}'")
        setattr(instance, self.private, value)



@dataclass
class bounded:
    """строка длины не больше опр."""
    max_l: int        
    min_l: int = 1     

    def __set_name__(self, owner, name):
        self.private = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private, None)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.private[1:]} не строка")
        if len(value) < self.min_l:
            raise ValueError(f"{self.private[1:]}: минимум {self.min_l}")
        if len(value) > self.max_l:
            raise ValueError(f"{self.private[1:]}: максимум {self.max_l}")
        setattr(instance, self.private, value)

class Task:
    """Класс задачи"""
    id = reading()
    descr = bounded(max_l=200)
    prior = choice(["low", "medium", "high"])
    status = choice(["new", "in_progress", "done"])
    
    def __init__(self, task_id: str, descr: str, prior: str = "medium", status: str = "new"):
        self.id = task_id
        self.descr = descr
        self.prior = prior
        self.status = status
        self._created_at = datetime.now()
    
    @property
    def created_at(self) -> datetime:
        """Создано d"""
        return self._created_at
    
    @property
    def is_ready(self) -> bool:
        return self.status != "done" and self.prior != "low"
    
