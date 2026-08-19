from intelligence.ttc import calculate_ttc


# ==========================================
# CASE 1 — FAST CLOSING
# ==========================================

result = calculate_ttc(
    receiver_position=80,
    receiver_speed=15,
    sender_position=100,
    sender_speed=10,
)

print("\n==============================")
print("CASE 1 — FAST CLOSING")
print("==============================")

print("Relative Speed :", result.relative_speed)
print("Closing        :", result.closing)
print("TTC            :", result.ttc)

assert result.closing is True
assert result.ttc == 4.0


# ==========================================
# CASE 2 — SAME SPEED
# ==========================================

result = calculate_ttc(
    receiver_position=80,
    receiver_speed=10,
    sender_position=100,
    sender_speed=10,
)

print("\n==============================")
print("CASE 2 — SAME SPEED")
print("==============================")

print("Relative Speed :", result.relative_speed)
print("Closing        :", result.closing)
print("TTC            :", result.ttc)

assert result.closing is False
assert result.ttc is None


# ==========================================
# CASE 3 — RECEIVER SLOWER
# ==========================================

result = calculate_ttc(
    receiver_position=80,
    receiver_speed=8,
    sender_position=100,
    sender_speed=10,
)

print("\n==============================")
print("CASE 3 — RECEIVER SLOWER")
print("==============================")

print("Relative Speed :", result.relative_speed)
print("Closing        :", result.closing)
print("TTC            :", result.ttc)

assert result.closing is False
assert result.ttc is None


# ==========================================
# TEST RESULT
# ==========================================

print("\n==============================")
print("TEST RESULT")
print("==============================")

print("TTC TESTS PASSED!")