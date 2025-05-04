from typing import Annotated

from fastapi import Depends

from src.services.event import AbstractEventPublisherService, get_event_service
from src.infrastructure.storage import AbstractStorageRepository, get_storage_repository 
from src.infrastructure.producer import AbstractProducerBroker, get_producer

eventDep = Annotated[AbstractEventPublisherService, Depends(get_event_service)]
storage_repoDep = Annotated[AbstractStorageRepository, Depends(get_storage_repository)]
producerDep = Annotated[AbstractProducerBroker, Depends(get_producer)]
