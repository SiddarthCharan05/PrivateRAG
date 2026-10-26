import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path("audit_logs.db")


def initialize_audit_database():
    """Create the audit log database if it does not exist."""

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                role TEXT NOT NULL,
                privacy_risk TEXT NOT NULL,
                pii_types TEXT,
                source_count INTEGER NOT NULL
            )
            """
        )


def log_interaction(
    role,
    privacy_risk,
    pii_entities,
    documents,
):
    """
    Record privacy-safe metadata about an interaction.

    The user's question and detected PII values
    are deliberately NOT stored.
    """

    initialize_audit_database()

    pii_types = sorted(
        {
            entity["type"]
            for entity in pii_entities
        }
    )

    pii_types_text = ", ".join(pii_types)

    timestamp = datetime.now().isoformat(
        timespec="seconds"
    )

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO audit_logs (
                timestamp,
                role,
                privacy_risk,
                pii_types,
                source_count
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                role,
                privacy_risk,
                pii_types_text,
                len(documents),
            ),
        )


if __name__ == "__main__":
    initialize_audit_database()

    print(
        "PrivateRAG audit database created successfully."
    )