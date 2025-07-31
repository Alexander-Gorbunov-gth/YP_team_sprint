from src.infrastructure.models.address import mapped_addresses_table
from src.infrastructure.models.event import mapped_events_table
from src.infrastructure.models.reservation import mapped_reservations_table
from src.infrastructure.models.subscription import mapped_subscription_table


def start_mappers():
    mapped_addresses_table()
    mapped_events_table()
    mapped_reservations_table()
    mapped_subscription_table()
