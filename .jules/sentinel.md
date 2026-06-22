## 2025-02-28 - Case-Sensitive Email Lookups in Authentication

**Vulnerability:** Email addresses during registration, login, and password reset flows were not being normalized to lowercase before database insertion or lookup.
**Learning:** Due to SQLAlchemy's strict string matching and typical database collation, 'User@Example.com' and 'user@example.com' were treated as distinct identities. This gap could result in duplicate accounts, lockouts for users using different casing to log in, and in some platforms, account impersonation risks.
**Prevention:** Always normalize identity fields (like emails) to a consistent casing (e.g., `.lower()`) at the boundaries of the system before executing validation checks or database queries.
