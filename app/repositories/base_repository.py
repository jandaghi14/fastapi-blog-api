from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass
