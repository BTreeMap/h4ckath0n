## 2024-08-05 - Centralize scope collection mutation helpers
**Learning:** The application repeatedly parsed string scopes, manipulated them using python sets and comprehensions inline in command handlers, and reserialized them. This scattered domain knowledge into procedural mutation.
**Action:** Centralize explicit transformations into `add_scopes` and `remove_scopes` functional helpers, which takes `str | Iterable[str]` for correctness and re-exports deterministic behaviour.
