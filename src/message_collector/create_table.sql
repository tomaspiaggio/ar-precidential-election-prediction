CREATE TABLE IF NOT EXISTS messages
(
    id                String,
    type              String,
    message           String,
    timestamp         Int64,
    datetime          String,
    elapsedTime       String,
    amountValue       Float32,
    amountString      String,
    currency          String,
    author_name       String,
    author_channelId  String,
    author_channelUrl String,
    video_id          String,
    stream_name       String
) ENGINE = MergeTree()
ORDER BY (timestamp);
