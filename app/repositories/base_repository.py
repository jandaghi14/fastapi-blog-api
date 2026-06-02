from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    async def create(self, ...):
        pass

    @abstractmethod
    async def get_by_id(self, ...):
        pass

    @abstractmethod
    async def get_all(self, ...):
        pass

    @abstractmethod
    async def update(self, ...):
        pass

    @abstractmethod
    async def delete(self, ...):
        pass
