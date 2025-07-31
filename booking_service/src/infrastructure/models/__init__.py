from src.infrastructure.models.subscription import mapped_subscription_table
from src.infrastructure.models.address import mapped_address_table


def start_mappers():
    mapped_subscription_table()
    mapped_address_table()