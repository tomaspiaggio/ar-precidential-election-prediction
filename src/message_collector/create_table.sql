CREATE TABLE IF NOT EXISTS messages
(
    name            String,
    type            String,
    remarks         String,
    id              String,
    message         String,
    messageEx       Array(String),
    timestamp       Int64,
    datetime        String,
    elapsedTime     String,
    amountValue     Float32,
    amountString    String,
    currency        String,
    bgColor         Int32,
    author          Nested
    (
        name            String,
        channelId       String,
        channelUrl      String,
        imageUrl        String,
        badgeUrl        String,
        isVerified      UInt8,
        isChatOwner     UInt8,
        isChatSponsor   UInt8,
        isChatModerator UInt8
    )
) ENGINE = MergeTree()
ORDER BY (timestamp);
