from presidio_analyzer import AnalyzerEngine


# Create the PII analyzer once
analyzer = AnalyzerEngine()


def scan_for_pii(text):
    """Detect personally identifiable information in user input."""

    results = analyzer.analyze(
        text=text,
        language="en",
        entities=[
            "PERSON",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "IBAN_CODE",
            "CREDIT_CARD",
            "IP_ADDRESS",
        ],
    )

    detected_entities = []

    for result in results:
        detected_entities.append(
            {
                "type": result.entity_type,
                "start": result.start,
                "end": result.end,
                "score": round(result.score, 2),
                "value": text[result.start:result.end],
            }
        )

    return detected_entities


def calculate_risk(entities):
    """Assign a simple privacy risk level."""

    if not entities:
        return "LOW"

    high_risk_types = {
        "IBAN_CODE",
        "CREDIT_CARD",
        "IP_ADDRESS",
    }

    medium_risk_types = {
        "PERSON",
        "EMAIL_ADDRESS",
        "PHONE_NUMBER",
    }

    entity_types = {
        entity["type"]
        for entity in entities
    }

    if entity_types.intersection(high_risk_types):
        return "HIGH"

    if entity_types.intersection(medium_risk_types):
        return "MEDIUM"

    return "LOW"


def print_privacy_report(text):
    """Print the privacy scan results."""

    entities = scan_for_pii(text)
    risk = calculate_risk(entities)

    print("\n" + "=" * 60)
    print("PRIVATERAG PRIVACY SCANNER")
    print("=" * 60)

    if entities:
        print("\nDetected PII:\n")

        for entity in entities:
            print(
                f"{entity['type']:<18} "
                f"→ {entity['value']} "
                f"(confidence: {entity['score']})"
            )

    else:
        print("\nNo PII detected.")

    print(f"\nPrivacy Risk Level: {risk}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    user_text = input(
        "\nEnter text to scan for personal information:\n> "
    )

    print_privacy_report(user_text)