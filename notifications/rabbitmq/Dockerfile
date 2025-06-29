FROM rabbitmq:3.12-management

# Копируем плагин внутрь контейнера
COPY plugins/rabbitmq_delayed_message_exchange-3.12.0.ez /plugins/

# Включаем плагин
RUN rabbitmq-plugins enable --offline rabbitmq_delayed_message_exchange