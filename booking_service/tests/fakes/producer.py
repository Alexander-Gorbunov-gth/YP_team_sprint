from src.services.interfaces.producer import IProducer, PublishMessage


class FakeProducer(IProducer):
    def __init__(self) -> None:
        self.publish_message: list[PublishMessage] = []

    async def publish(self, message: PublishMessage) -> None:
        self.publish_message.append(message)
