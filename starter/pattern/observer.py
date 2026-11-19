from abc import ABC, abstractmethod

class Observer(ABC):
  @abstractmethod
  def update(self, *args, **kwargs):
    """Standard update interface expected by the subject."""
    pass

class ObserverSubject:
  def __init__(self):
    self._observers = []

  def register_observer(self, observer : Observer):
    self._observers.append(observer)

  def notify(self, *args, **kwargs):
    for observer in self._observers:
      observer.update(*args, **kwargs)
