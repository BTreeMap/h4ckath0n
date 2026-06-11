#!/bin/bash
cd packages/create-h4ckath0n/templates/fullstack/web

cat << 'INNER_EOF' > modify_test.py
import re

with open('src/components/Layout.test.tsx', 'r') as f:
    content = f.read()

# Make sure we don't accidentally fail screen.queryByRole /Theme: system/
# Although it's unlikely since it queryByRole expects at most 1, but wait!
# If queryByRole finds multiple elements, it will throw an error!
# Wait, let's look at the failure. The failure says "The job has exceeded the maximum execution time of 6h0m0s".
# That's a timeout.
# But "Process completed with exit code 1." for backend job.
INNER_EOF
