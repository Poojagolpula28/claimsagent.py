import json


def read_fnol_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def extract_fields(text):
    fields = {}

    for line in text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip().lower()] = value.strip()

    return fields


def find_missing_fields(fields, mandatory_fields):
    missing = []
    for field in mandatory_fields:
        if field not in fields or fields[field] == "":
            missing.append(field)
    return missing


def route_claim(fields, missing_fields):
    reasoning = ""

    if missing_fields:
        return "Manual Review", "Mandatory fields are missing"

    damage = int(fields.get("estimated damage", "0"))

    description = fields.get("description", "").lower()

    if "fraud" in description or "staged" in description or "inconsistent" in description:
        return "Investigation", "Suspicious keywords found in description"

    if damage < 25000:
        return "Fast-track", "Estimated damage is less than 25,000"

    if fields.get("claim type", "").lower() == "injury":
        return "Specialist Queue", "Injury related claim"

    return "Standard Processing", "Does not meet fast-track criteria"


fnol_text = read_fnol_file("sample_fnol.txt")
extracted_fields = extract_fields(fnol_text)

mandatory_fields = [
    "policy number",
    "policyholder name",
    "date",
    "location",
    "description",
    "claim type",
    "estimated damage"
]

missing_fields = find_missing_fields(extracted_fields, mandatory_fields)
route, reason = route_claim(extracted_fields, missing_fields)

output = {
    "extractedFields": extracted_fields,
    "missingFields": missing_fields,
    "recommendedRoute": route,
    "reasoning": reason
}

print(json.dumps(output, indent=2))
