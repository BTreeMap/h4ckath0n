
## 2024-10-24 - Visual required indicators break exact text matches in tests
 **Learning:** Adding visual `*` indicators dynamically via the `required` prop on standard forms components breaks `getByLabelText` tests in the `vitest` suite, because testing-library queries match the exact textContent.
 **Action:** Update test suites to use regex matching (e.g., `expect(screen.getByText(/Display Name/)).toBeInTheDocument();`) when adding accessible UI decorators like required asterisks.
