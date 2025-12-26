# Purple-Team After Action Report
**Generated:** 2025-11-09T18:03:06.572566

**Log Source:** `safety_governor_log.jsonl`

## Summary
- Total actions: 3
- Allowed: 0
- Denied: 3

## Allowed Operations
## Denied Operations
- `2025-11-09T17:59:30.609011` > `ping 10.0.0.5` (Target out of allowed range.)
- `2025-11-09T17:59:30.610015` > `rm -rf /tmp` (Unsafe keyword detected: rm )
- `2025-11-09T17:59:30.612634` > `curl spam.com` (Unsafe keyword detected: curl )