queries = {
    "create_user_events_table": """
        CREATE TABLE IF NOT EXISTS user_events (
            user_id UUID,
            ip_address String,
            user_agent String,
            event_type String,
            timestamp DateTime,
            item_id Nullable(String),
            item_type Nullable(String),
            page_type Nullable(String),
            duration_seconds Nullable(Int32),
            video_id Nullable(String),
            from_quality Nullable(String),
            to_quality Nullable(String),
            current_time_seconds Nullable(Int32),
            total_duration_seconds Nullable(Int32),
            filters Array(Nullable(String)),
            watched_seconds Nullable(Int32)
        )
        ENGINE = MergeTree()
        ORDER BY (user_id, timestamp);
    """
}
