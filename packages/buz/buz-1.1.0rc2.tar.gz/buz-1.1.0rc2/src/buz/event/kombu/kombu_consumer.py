from logging import Logger
from typing import Type, Dict, Set, List, Optional

from kombu import Connection, Queue, Consumer as MessageConsumer, Message
from kombu.mixins import ConsumerMixin
from kombu.transport.pyamqp import Channel

from buz.event import Event, Subscriber
from buz.event.kombu.serializer_enum import SerializerEnum
from buz.event.middleware import ConsumeMiddleware, ConsumeMiddlewareChainResolver
from buz.locator import Locator

QueueToSubscriberFqnMapping = Dict[Queue, Set[str]]


class KombuConsumer(ConsumerMixin):
    def __init__(
        self,
        connection: Connection,
        queues_mapping: QueueToSubscriberFqnMapping,
        serializer: SerializerEnum,
        prefetch_count: int,
        locator: Locator[Event, Subscriber],
        logger: Logger,
        consume_middlewares: Optional[List[ConsumeMiddleware]] = None,
    ):
        self.connection = connection
        self.__queues_mapping = queues_mapping
        self.__serializer = serializer
        self.__prefetch_count = prefetch_count
        self.__locator = locator
        self.__logger = logger
        self.__consume_middleware_chain_resolver = ConsumeMiddlewareChainResolver(consume_middlewares or [])

    def get_consumers(self, Consumer: Type, channel: Channel) -> List[MessageConsumer]:
        return [
            Consumer(
                queues=[queue],
                callbacks=[lambda body, message: self.__on_message_received(body, message, subscriber_fqns)],
                prefetch_count=self.__prefetch_count,
                accept=[self.__serializer],
            )
            for queue, subscriber_fqns in self.__queues_mapping.items()
        ]

    def __on_message_received(self, body: Dict, message: Message, subscriber_fqns: Set[str]) -> None:
        try:
            event_fqn = message.headers["fqn"]
            event_klass = self.__locator.get_message_klass_by_fqn(event_fqn)
            event = event_klass.restore(**body)
            for subscriber_fqn in subscriber_fqns:
                subscriber = self.__locator.get_handler_by_fqn(subscriber_fqn)
                self.__consume_middleware_chain_resolver.resolve(event, subscriber, self.__perform_consume)
            message.ack()
        except Exception as exc:
            self.__on_consume_exception(body, message, exc)

    def __perform_consume(self, event: Event, subscriber: Subscriber) -> None:
        subscriber.consume(event)

    def __on_consume_exception(self, body: Dict, message: Message, exception: Exception) -> None:
        redelivered = message.delivery_info.get("redelivered", True)

        if redelivered is True:
            event_id = body.get("id", "Unknown") if isinstance(body, dict) else "Unknown"
            self.__logger.exception(f"Event {event_id} was not processed successfully: {exception}")
            message.reject()
            return

        message.requeue()
