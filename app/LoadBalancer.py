from typing import ClassVar, List
import random


class LoadBalancerException(Exception):
    pass

class LoadBalancer:
    MAX_INSTANCES : ClassVar[int] = 10

    def __init__(self):
        self._instances : List = []
        self._round_robin_index : int = 0

    def register_instance(self, instance: str) -> None:
        if instance in self._instances:
            raise LoadBalancerException("Instance already registered")
        elif len(self._instances) >= self.MAX_INSTANCES:
            raise LoadBalancerException("More than 10 instances are not allowed")

        self._instances.append(instance)
    
    def get_instance(self) -> str:
        if not self._instances:
            raise LoadBalancerException
        return random.choice(self._instances)

    def get_instance_round_robin(self) -> str:
        if not self._instances:
            raise LoadBalancerException
        instance = self._instances[self._round_robin_index]
        self._round_robin_index = (self._round_robin_index + 1) % len(self._instances)
        return instance
