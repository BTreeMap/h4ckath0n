cd packages/create-h4ckath0n/templates/fullstack/web/
sed -i 's/>\n                  Password\n                <\/label>/>\n                  Password <span className="text-danger ml-1">*<\/span>\n                <\/label>/' src/pages/Login.tsx
