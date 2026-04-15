---
description: QA Engineering & Automation Standards
---

## 1. Automation Scope & Strategy
- **No Flaky E2E**: Restrict UI automation (Playwright/JavaScript) strictly to high-priority Happy Paths and daily Smoke Tests.
- **Exploratory First**: Complex edge cases, boundary analyses, and negative UI workflows must be documented in the manual `TEST_PLAN.md` rather than shoehorned into brittle automated scripts.

## 2. UI Locators & Playwright Standards
- **NO Brittle Selectors**: Never use absolute XPaths or deep CSS DOM hierarchies (e.g., `//div[2]/span/ul/li`). If the UI changes slightly, the test will fail.
- **User-Centric Locators**: Always use accessibility-first locators (e.g., `page.getByRole('button', { name: 'Checkout' })`) or explicit test attributes (e.g., `page.getByTestId('cart-total')`).
- **Implicit Waits Only**: Absolutely no hardcoded sleeps (e.g., `page.waitForTimeout(5000)`). Rely entirely on Playwright's auto-waiting web-first assertions (`await expect(locator).toBeVisible()`).

## 3. API Validation (Postman / Python)
- **Strict Assertions**: API tests must explicitly assert the HTTP status code first (e.g., `pm.response.to.have.status(200)`), followed by the exact JSON schema structure. Do not rely on loose string matching in the response body.
- **Trap Validation Errors**: When testing the Python FastAPI backend, always include explicit negative test cases sending missing or invalid JSON payloads to verify the server correctly returns `422 Unprocessable Entity`.

## 4. Database State & Raw SQL
- **Parameterized Queries**: All database validations using raw PostgreSQL or MySQL must use parameterized queries (e.g., `SELECT * FROM orders WHERE user_id = $1`). Never concatenate test variables directly into SQL strings.
- **State Isolation**: Tests must not pollute the database. If an automation script or manual test session creates dummy data (like a test order), execute a teardown SQL script to `DELETE` or rollback those records to maintain a pristine test environment.

## 5. Defect Reporting Standards
- **No Vague Tickets**: Bug reports must strictly contain structured data: Environment (OS, Browser, API version), Steps to Reproduce (numbered list), Expected Result, and Actual Result.
- **Explicit Evidence**: All reported UI defects must mention an attached screenshot/video, and API defects must include the raw JSON request and response payloads.
