
CREATE TABLE IF NOT EXISTS benchmark (
    id INT,
    name VARCHAR(255)
)
ENGINE = MergeTree()
ORDER BY id
