import json

latest = {}  # txn_id -> the most recent event for that txn_id

with open("payments.jsonl", encoding="utf-8") as f:
    for line in f:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if not isinstance(event, dict):
            continue

        txn_id = event.get("txn_id")
        if not txn_id:
            continue  # no txn_id, ignore it

        old = latest.get(txn_id)
        if old is None or event["ts"] >= old["ts"]:
            latest[txn_id] = event

total = 0.0
count = 0

for event in latest.values():
    if event["status"] == "success":
        total += float(str(event["amount"]).replace(",", ""))
        count += 1

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
    