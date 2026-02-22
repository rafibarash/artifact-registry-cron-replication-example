# Product Guidelines: Artifact Registry Cron Replicator

## 1. Tone and Voice
*   **Concise and Direct:** Communications (documentation, comments) should be clear, brief, and to the point. Avoid jargon where simpler terms suffice.
*   **Instructive and Supportive:** The tone should be helpful and guide the user through setup and usage, anticipating common questions.
*   **Professional:** Maintain a professional and respectful tone in all external and internal communications.

## 2. Documentation Standards
*   **Clarity over Brevity:** While conciseness is valued, clarity is paramount, especially for setup instructions and API explanations.
*   **Examples:** Provide practical, copy-pasteable examples for configuration, deployment, and usage scenarios.
*   **Consistency:** Maintain consistent terminology, formatting, and structure across all documentation (README, config files, code comments).
*   **Completeness:** All aspects of the tool's functionality, configuration options, and potential issues should be documented.

## 3. User Experience (UX) Principles for Configuration and Deployment
*   **Simplicity:** The process of forking, configuring, and deploying should be as simple and frictionless as possible.
*   **Transparency:** Users should understand what resources are being provisioned and what actions the tool will take.
*   **Safety:** Configuration should minimize the risk of accidental data loss or unintended resource usage. Dry-run capabilities should be highlighted.
*   **Feedback:** Provide clear feedback during setup and execution (e.g., logging output, Cloud Run job status).
*   **Low Cognitive Load:** Minimize the amount of new information users need to absorb to get started. Leverage existing Google Cloud patterns and best practices.

## 4. Code Style and Maintainability
*   **Readability:** Code should be easy to read and understand, with clear naming conventions and logical structure.
*   **Testability:** Code should be written with testing in mind, ensuring a high level of test coverage.
*   **Security:** Follow Google Cloud security best practices, particularly regarding authentication, authorization, and data handling.