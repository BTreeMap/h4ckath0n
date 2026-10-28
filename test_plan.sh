cd packages/create-h4ckath0n/templates/fullstack/web/

# Add asterisk for required fields in Input and PasswordField components.
sed -i 's/{label && <Label htmlFor={inputId}>{label}<\/Label>}/{label \&\& <Label htmlFor={inputId}>{label}{props.required \&\& <span className="text-danger ml-1">*<\/span>}<\/Label>}/' src/components/Input.tsx
sed -i 's/{label && <Label htmlFor={inputId}>{label}<\/Label>}/{label \&\& <Label htmlFor={inputId}>{label}{props.required \&\& <span className="text-danger ml-1">*<\/span>}<\/Label>}/' src/components/PasswordField.tsx

# In Login.tsx: add required to inputs
sed -i 's/autoCapitalize="none"/autoCapitalize="none"\n              required/' src/pages/Login.tsx
sed -i 's/autoComplete="current-password"/autoComplete="current-password"\n                required/' src/pages/Login.tsx

# In Register.tsx: add required to inputs
sed -i 's/maxLength={DISPLAY_NAME_MAX_LENGTH}/maxLength={DISPLAY_NAME_MAX_LENGTH}\n              required/' src/pages/Register.tsx
sed -i 's/autoCapitalize="none"/autoCapitalize="none"\n              required/' src/pages/Register.tsx
sed -i 's/autoComplete="new-password"/autoComplete="new-password"\n              required/' src/pages/Register.tsx

# Update tests to use regex for label matching instead of exact string
sed -i 's/getByLabelText("Email")/getByLabelText(\/Email\/)/' src/pages/Login.test.tsx
sed -i 's/queryByLabelText("Username")/queryByLabelText(\/Username\/)/' src/pages/Login.test.tsx
sed -i 's/getByLabelText("Secret")/getByLabelText(\/Secret\/)/' src/components/PasswordField.test.tsx

if [ -f src/pages/Register.test.tsx ]; then
  sed -i 's/getByLabelText("Display Name")/getByLabelText(\/Display Name\/)/' src/pages/Register.test.tsx
fi
