Wait, the `Settings` attributes in `src/h4ckath0n/config.py` do not have descriptions. They are just typed fields. So we cannot generate the "Description" column easily without parsing docstrings or Fields, which don't exist.

Let's look at the "Built-in routes" instead. The routes are registered in the FastAPI app with summary/description in many cases.
Let's see what `test_openapi_desc.py` output earlier:
POST /auth/passkey/register/start - Start passkey registration
POST /auth/passkey/register/finish - Finish passkey registration
...
GET /auth/session - Current session
...

Ah! Generating the endpoints from OpenAPI is a perfect fit. The README currently has:
## Built-in routes

- `GET /` — welcome message confirming the app is reachable.
...
### Session
- `GET /auth/session` — returns the current user session details.

### Background Jobs
...
### Uploads
...
### LLM Chat
...
## Auth model
### Passkeys by default
...

We could replace the manual `check_doc_routes.py` with one that just injects the endpoints directly into `README.md` between some markers like:
<!-- BEGIN GENERATED ROUTES -->
<!-- END GENERATED ROUTES -->

Wait, what if we just add a "Start here" index? Or what if we generate the whole `check_doc_routes.py` to be `generate_doc_routes.py` and have it enforce drift prevention by writing the exact markdown out, and failing in CI if there's a diff?

But wait! What about the environment variables?
If we do "🧭 Replace hand-written endpoint lists with generated tables from OpenAPI", how do we do it?

First, look at README.md from line 52 to 92.
