## 2024-05-28 - O(N) Table Scan on User Registration
**Vulnerability:** `await db.execute(select(func.count()).select_from(User))` causes an O(N) full table/index scan on every registration when checking if the first user is an admin.
**Learning:** This is a performance issue that could lead to Denial of Service (DoS) if registration is hit repeatedly on a large table.
**Prevention:** Use an O(1) existence check like `await db.scalar(select(User.id).limit(1))` and check for `None`.

## 2024-05-28 - Timing Attack Vulnerability in User Authentication
**Vulnerability:** The `authenticate_user` function returns early if a user is not found, making it extremely fast (0.001s) compared to when a user exists and their password hash is verified (0.08s+). This allows an attacker to enumerate registered email addresses by measuring the response time.
**Learning:** Returning early before performing the expensive password hashing operation exposes a timing attack vector. The server's response time leaks whether the user exists.
**Prevention:** Perform a dummy hash verification using a static dummy hash even if the user is not found, to ensure the execution time is roughly constant regardless of whether the user exists or not.
