# SIH-V2V

# Testing
## Purpose
This folder contains tests used to verify the correctness of the V2V software.

Testing should focus on the decision pipeline rather than only checking whether functions execute.

## Main Testing Areas
### Message Testing
Verify:
- Valid messages are encoded correctly
- Valid messages are decoded correctly
- Required fields are present
- Invalid messages are rejected
- Unknown message types are handled

### Relevance Testing
Example:
Input:
Vehicle A:
Lane 1
Position 100

Vehicle B:
Lane 1
Position 80

Expected: RELEVANT
Another vehicle: Lane 2
Expected: NOT_RELEVANT

### Safety Testing
Example:
Input:
Relevant emergency event

Expected: CRITICAL
Action: BRAKE

Example: Low-risk event
Expected: WARNING
Action: SLOW_DOWN

## Test Philosophy
Tests should be deterministic.

Given the same vehicle states and message, the system should produce the same result.

## Files
### test_messages.py
Tests communication message creation, encoding and decoding.

### test_relevance.py
Tests the relevance engine.

### test_safety.py
Tests the safety decision engine.

## Before Merge
Every contributor should run the relevant tests before merging code into the main branch.