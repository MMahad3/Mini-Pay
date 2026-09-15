# AI Usage

## Tools used

GitHub Copilot in VS Code was used extensively throughout the assessment. No private repository credentials, API tokens, passwords, or confidential employer/client information were provided to the tool.

## How AI was used

- Generated most of the application implementation, including the FastAPI service, static UI structure, request validation, authentication, idempotency behavior, and error paths.
- Generated the Kubernetes deployment configuration, including namespace, Secret/ConfigMap, PostgreSQL StatefulSet, PVC, Services, probes, resource limits, and rollout configuration.
- Generated much of the Python support utility, SQL queries, test scaffolding, and troubleshooting documentation.
- Reviewed the repository structure against the assessment instructions and identified missing evaluator-facing documents, incident RCAs, and reproducibility details.
- Drafted and refined setup, architecture, coverage, evidence, and final-submission guidance.

## Representative interaction summaries

1. Instructed Copilot to implement a small FastAPI payment API and browser UI with authentication, validation, payment idempotency, health checks, and testable selectors.
2. Instructed Copilot to create Kubernetes deployment configuration for the API and PostgreSQL, then reviewed the generated manifest against the starter defects and operational requirements.
3. Instructed Copilot to create pytest API/unit coverage and Playwright GUI journeys, then ran the tests and corrected behavior or documentation where results differed from expectations.
4. Asked Copilot to inspect the published `INSTRUCTIONS.md`, requirements, and incident prompts and map the actual repository to the scoring areas.
5. Asked Copilot to document the implementation honestly, including limitations, evidence, AI use, and incomplete Rancher/database persistence work.

## Validation and ownership

I provided the requirements and implementation direction, reviewed the generated code, ran the application, validated the Kubernetes behavior, and tested the repository. Generated output was checked against the actual files, commands, test selectors, environment variables, and deployment manifest. The final test run passed all 13 tests, including API, unit, and Playwright GUI coverage.

One material improvement was rejecting an overly broad claim that the demo API used PostgreSQL for CRUD persistence. Review showed that customer/payment state remains in process memory, so the architecture, README, and incident RCA now state that limitation explicitly. I also retained the Rancher Docker privilege constraint rather than presenting it as a completed managed-cluster workflow.

The candidate remains responsible for reviewing, explaining, and modifying every part of the submission during the follow-up discussion.
