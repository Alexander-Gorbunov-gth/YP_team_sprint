from src.infrastructure.models.address import mapped_addresses_table
from src.infrastructure.models.event import mapped_events_table
from src.infrastructure.models.event_feedback import mapped_event_feedbacks_table
from src.infrastructure.models.reservation import mapped_reservations_table
from src.infrastructure.models.subscription import mapped_subscription_table
from src.infrastructure.models.user_feedback import mapped_user_feedbacks_table


def start_mappers():
    mapped_event_feedbacks_table()
    mapped_addresses_table()
    mapped_events_table()
    mapped_reservations_table()
    mapped_subscription_table()
    mapped_user_feedbacks_table()
