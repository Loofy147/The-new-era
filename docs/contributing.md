# Contributing to AI-Model Marketplace OS

Thank you for your interest in contributing to the AI-Model Marketplace OS! This guide provides comprehensive instructions for adding new AI models, improving code, and documenting changes. Please read through before submitting a pull request.

---

## Table of Contents
1. [Getting Started](#getting-started)
2. [Repository Structure](#repository-structure)
3. [Adding a New Model](#adding-a-new-model)
4. [Code Quality & Style](#code-quality--style)
5. [Documentation](#documentation)
6. [Testing](#testing)
7. [Workflow & Pull Requests](#workflow--pull-requests)
8. [Versioning](#versioning)
9. [Support & Communication](#support--communication)

---

## Getting Started

1. **Fork the repository** on GitHub and clone your fork:
   ```bash
   git clone https://github.com/your-org/ai-model-marketplace-os.git
   cd ai-model-marketplace-os
   git remote add upstream https://github.com/your-org/ai-model-marketplace-os.git
   ```
2. **Install dependencies**:
   - Services: Node.js (v16+), Python (3.8+)
   - CLI: `npm install` in `cli/`
   - Dashboard: `npm install` in `dashboard/`
3. **Set up environment**:
   - Copy `.env.example` to `.env` and fill in values (API URLs, Kafka brokers, DB credentials).
4. **Run locally**:
   ```bash
   docker-compose up --build
   ```

---

## Repository Structure

Refer to the top-level directories:

- **services/llm-tools/** — LLM refactoring, training, and evolution modules.
- **services/model-runner/** — Core inference service.
- **services/api-gateway/** — REST/gRPC façade.
- **services/billing-engine/** — Usage capture & billing.
- **cli/** — Command-line tool (`aimos`).
- **dashboard/** — React-based web UI.
- **shared/** — Protobuf definitions, utility code.
- **infra/** — Terraform and Kubernetes manifests.
- **scripts/** — Deployment and management scripts.
- **tests/** — Unit, integration, end-to-end tests.

---

## Adding a New Model

### 1. Model Artifact
- **Upload** your model artifacts to the registry (S3/MinIO) under `/models/<model-name>/<version>/`
- Ensure metadata JSON file exists alongside: `model.json` with fields:
  ```json
  {
    "name": "my-model",
    "version": "1.0.0",
    "framework": "pytorch",
    "type": "LLM",
    "parameters": 123456789
  }
  ```

### 2. Protobuf & API
- **Define** input/output schema in `shared/proto/infer.proto` if custom:
  ```proto
  message MyInput { ... }
  message MyOutput { ... }
  ```
- **Update** service definition if adding custom endpoints, then regenerate stubs:
  ```bash
  protoc -I shared/proto/ --js_out=import_style=commonjs:services/api-gateway/src shared/proto/infer.proto
  ```

### 3. Model Runner
- **Implement** inference logic in `services/model-runner/src/infer.js`:
  ```js
  async function runInference(model, input) {
    const loaded = await loadModel(model);
    return loaded.predict(input);
  }
  ```
- **Handle** resource limits via cgroups or Firecracker config in Dockerfile.

### 4. Billing Metrics
- **Emit** inference events to Kafka in `services/model-runner/src/infer.js`:
  ```js
  producer.send({ topic: 'inference.events', messages: [JSON.stringify({ model, units })] });
  ```
- **Adjust** pricing rules in `services/billing-engine/pricing.rules.json` if new unit types introduced.

### 5. CLI & Dashboard
- **CLI**: Add commands in `cli/src/commands/`:
  ```js
  program.command('add-model')...
  ```
- **Dashboard**: Extend API calls in `dashboard/src/components/ModelList.jsx` and related pages.

---

## Code Quality & Style

- **JavaScript/TypeScript**: ESLint (Airbnb style) and Prettier. Run:
  ```bash
  npm run lint && npm run format:check
  ```
- **Python**: `black`, `flake8`. Run:
  ```bash
  black --check services/llm-tools/training
  flake8 services/llm-tools/training
  ```
- **Commit Messages**: Follow Conventional Commits format:
  - `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, etc.

---

## Documentation

- **Phase Docs**: Update relevant docs in `docs/` (e.g., `integration.md`, `transmutation.md`).
- **API Docs**: Keep `openapi.yaml` and generated HTML in sync.
- **CHANGELOG**: Append new entries under `## [Unreleased]`.
- **Code Comments**: Document exports, complex logic, and public interfaces.

---

## Testing

- **Unit Tests**: Add to `tests/unit/`. Use Jest for JS, Pytest for Python.
- **Integration**: Use `tests/integration/` to spin up Docker Compose and test end-to-end flows.
- **E2E**: Add to `tests/e2e/` for user flows via Puppeteer or Cypress.
- **Coverage**: Aim for ≥80%.

Run all tests:
```bash
npm test && pytest
```

---

## Workflow & Pull Requests

1. **Branching**: Create feature branches off `main`: `feature/<name>`, `fix/<issue>`, etc.
2. **Sync**: Rebase regularly with `git pull --rebase upstream main`.
3. **PR Template**: Fill out PR description with:
   - Summary of changes
   - Related issues
   - Testing steps
   - Screenshots (if UI)
4. **Review**: Assign reviewers; address comments promptly.

---

## Versioning

We follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH

- **MAJOR**: incompatible API changes
- **MINOR**: functionality added in backwards-compatible manner
- **PATCH**: backwards-compatible bug fixes

Before merging a PR, update version in `package.json` and `cli/package.json`, and add CHANGELOG entry.

---

## Support & Communication

- Join discussions on **#ai-marketplace-os** channel in Slack.
- For design/architecture questions, create an issue tagged `discussion`.
- For urgent issues, ping `@maintainers` in GitHub.

Thank you for helping improve the AI-Model Marketplace OS! 🎉
