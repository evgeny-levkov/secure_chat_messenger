from abc import ABC, abstractmethod


class BaseObserver(ABC):
    @abstractmethod
    async def on_client_connected(self, client_id: tuple[str, int]) -> None:
        pass

    @abstractmethod
    async def on_message_received(self, client_id: tuple[str, int], message: bytes) -> None:
        pass

    @abstractmethod
    async def on_client_disconnected(self, client_id: tuple[str, int]) -> None:
        pass