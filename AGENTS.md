````markdown
# AGENTS.md — DevOps Learning Project (Python API → CI/CD → Containers → IaC → K8s → Observability)

## 1) Project Overview
This repository is a hands-on DevOps learning project where you progressively build a small Python HTTP API and then add delivery and operations capabilities step-by-step: automated tests and linting, pull-request quality gates, containerization, infrastructure as code (Terraform), Kubernetes deployment, autoscaling, and monitoring (Prometheus/Grafana).

The guiding principle is **manual learning first**: you implement core features and key configs yourself. The agent (assistant) can generate scaffolding, examples, checklists, and review guidance, but must not deliver “production-complete” Terraform/Kubernetes stacks unless explicitly requested later.

---

## 2) Repo Structure (and how it evolves)

### Baseline structure (Phase 1+)
Keep it simple and future-proof. Prefer FastAPI for clarity and modern patterns.

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entrypoint
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # endpoints
│   └── core/
│       ├── __init__.py
│       └── config.py           # config loading (env), grows in Phase 3+
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml              # deps + ruff/black/pytest config
├── README.md
├── .gitignore
└── AGENTS.md
````

### Evolving later (outline only; do not add early unless phase allows)

* `infra/terraform/` (introduced later, not Phase 1–2)
* `deploy/k8s/` (introduced later, not Phase 1–2)
* `docker/` or `Dockerfile` (introduced later; Phase 1 forbids it)
* `observability/` (Prometheus/Grafana manifests, later)

---

## 3) Branching Strategy

### Branches

* Work happens **only** on: `feature/phase1`, `feature/phase2`, `feature/phase3`, …
* Integration branch: `develop`
* Release branch: optional later (e.g., `release/x.y.z`)
* Stable branch: `main`

### Flow

1. Create feature branch from `develop` (or from `main` only for initial bootstrap).
2. Implement the phase scope.
3. Open PR **feature/phaseN → develop**.
4. Merge only when required checks pass and health checks are satisfied.
5. Periodically promote `develop → main` via PR (release step).

### Naming rules

* `feature/phase1`, `feature/phase2`, `feature/phase3` (exact)
* For sub-work: `feature/phase2-<topic>` is allowed only if you keep the main phase branch as the final integration branch.

---

## 4) CI/CD Policy

### CI triggers (must)

* Run CI on:

  * pushes to `feature/*`, `develop`, `main`
  * pull requests targeting `develop` or `main`

### Required checks (recommended)

* Lint/format check (ruff + formatting)
* Unit tests (pytest)
* (Later) type checks, security scans, container build, etc.

### GitHub branch protections (Phase 2 requirement)

Enforce on `develop`:

* Require pull request before merging
* Require status checks to pass before merging (select your CI job names)
* Require branches to be up to date before merging (recommended)
* Restrict who can push directly (optional)
* Require conversation resolution (optional)

Do the same on `main` once releases start.

---

## 5) Phase-by-Phase Instructions

> For every phase:
>
> * You implement the core logic and at least one meaningful test.
> * Agent can scaffold files, propose structures, and review your diffs.
> * Agent must not dump full “final production” infra stacks.

---

# Phase 1 — Minimal API + CI + structure (`feature/phase1`)

## Objectives

* Create a minimal HTTP API with one endpoint returning `"Hello World"`.
* Initialize Git repo, push to GitHub.
* Add GitHub Actions CI to run lint + tests.
* Establish a future-proof structure.

## Learning Goals

* Python project structure with `pyproject.toml`
* FastAPI basics: app + route + test
* Basic CI: run formatting/lint + tests on push/PR

## Manual Challenges (what YOU do)

* Write the endpoint and wire routing.
* Write the first pytest test.
* Configure ruff + formatting and ensure CI fails when rules are violated.
* Set the CI workflow triggers correctly.

## Agent Responsibilities (what the agent can generate)

* Suggested folder structure and file skeletons (not full implementation logic).
* Example `ci.yml` with placeholders for job names you can adjust.
* Example `pyproject.toml` tool configuration (you still validate locally).
* Checklist of commands and common pitfalls.

## Step-by-step Checklist

### 1) Create branch

```bash
git checkout -b feature/phase1
```

### 2) Create Python project + deps (manual)

* Create `pyproject.toml` using a tool of your choice (uv/poetry/pip-tools). Keep it simple.
* Dependencies (minimum):

  * `fastapi`
  * `uvicorn[standard]` (for local run)
  * `pytest`
  * `httpx` (or `requests`) for test client if needed
  * `ruff`
  * `black` (or use ruff-format if you prefer)

### 3) Implement the API (manual)

* Endpoint suggestion: `GET /` returns JSON:

  * `{ "message": "Hello World" }` OR plain text `"Hello World"` (choose and stay consistent in tests)

### 4) Add tests (manual)

* At least one test that asserts response code and content.

### 5) Add GitHub Actions CI (manual + agent scaffolding allowed)

**Workflow requirements:**

* Trigger on push + PR for `feature/*`, `develop`, `main`
* Steps:

  * checkout
  * setup python
  * install deps
  * run format/lint checks
  * run tests

**Example CI skeleton (adjust job/step names to match your tools):**

```yaml
name: ci

on:
  push:
    branches:
      - "feature/*"
      - "develop"
      - "main"
  pull_request:
    branches:
      - "develop"
      - "main"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          # Replace with your dependency install command
          pip install -r requirements.txt

      - name: Lint
        run: |
          ruff check .
          black --check .

      - name: Tests
        run: |
          pytest -q
```

> If you use `pyproject.toml` without `requirements.txt`, replace install step accordingly.

### 6) Push and open PR

```bash
git add .
git commit -m "phase1: minimal API + CI"
git push -u origin feature/phase1
```

Open PR: `feature/phase1 → develop` (create `develop` if not present yet).

## Definition of Done

* API responds with `"Hello World"` (as chosen format).
* `pytest` passes locally and in CI.
* CI runs on pushes to `feature/phase1`.
* Repo structure matches the baseline layout.

## Acceptance Criteria

* CI shows green on the PR.
* One endpoint + one test exists.
* Lint/format checks are enforced in CI (fails if formatting is wrong).

---

# Phase 2 — API parameter + multi-branch CI + PR quality gate (`feature/phase2`)

## Objectives

* Extend API: accept a `name` string and respond `"Hello World <name>"`.
* CI runs on every commit to any `feature/*` branch (already required; verify).
* Define and enforce PR merge rules into `develop` using GitHub protections.

## Learning Goals

* Query parameters and validation in FastAPI
* Strengthening CI discipline (required checks)
* Branch protection as a quality gate

## Manual Challenges (what YOU do)

* Implement the endpoint behavior with `name` input.
* Add tests for:

  * missing/empty name behavior (decide: error vs default)
  * normal name case
* Rename/standardize CI job names so branch protection can require them.
* Configure branch protection rules in GitHub UI.

## Agent Responsibilities (what the agent can generate)

* Test case ideas and edge cases.
* Suggested GitHub protection settings and how to map them to workflow job names.
* Health-check strategy for Phase 2 (simple and practical).

## Step-by-step Checklist

### 1) Create branch

```bash
git checkout develop
git pull
git checkout -b feature/phase2
```

### 2) Extend endpoint (manual)

* Example: `GET /hello?name=Arash` → `"Hello World Arash"` (choose your route name)
* Keep response format consistent (JSON vs text).

### 3) Add/extend tests (manual)

* Cover:

  * `name=Alice` → expected response
  * missing name → expected behavior (e.g., 422 validation error if required)

### 4) Ensure CI triggers (verify)

Your `ci.yml` must include:

```yaml
on:
  push:
    branches:
      - "feature/*"
      - "develop"
      - "main"
```

Push a commit to a `feature/*` branch and confirm CI runs.

### 5) PR quality gate into `develop` (manual GitHub settings)

In GitHub repository settings:

* Settings → Branches → Add branch protection rule
* Branch name pattern: `develop`
* Enable:

  * Require a pull request before merging
  * Require status checks to pass before merging

    * Select your CI check(s), e.g. `ci / test` (must match exactly)
  * Require branches to be up to date before merging (recommended)
  * (Optional) Require linear history / no force pushes

**Basic health checks pass (Phase 2 practical definition):**

* CI is green on the PR’s latest commit
* Tests include at least:

  * endpoint success
  * required param validation behavior

### 6) Push and PR

```bash
git add .
git commit -m "phase2: name parameter + tests + protection-ready CI"
git push -u origin feature/phase2
```

Open PR: `feature/phase2 → develop`

## Definition of Done

* API supports a `name` input and returns `"Hello World <name>"`.
* CI runs on all `feature/*` pushes and on PRs.
* `develop` branch protection requires CI checks.

## Acceptance Criteria

* PR cannot be merged unless required CI checks pass.
* Tests demonstrate correct behavior for at least 2 scenarios (valid + invalid/missing).
* CI job names are stable and referenced in branch protection.

---

# Phase 3 — Multiple query params + weather lookup (`feature/phase3`)

## Objectives

* Extend API query params:

  * required: `name`, `surname`
  * optional: `phone`, `city`
* If `city` is provided:

  * call a weather API and return **current weather** for that city **at request time**
* Response must include:

  * all provided params
  * if city exists: weather info + timestamp
* Introduce secure secrets approach (local + CI) without hardcoding keys.
* Begin direction-setting for containerization/IaC/K8s (do not fully implement them yet).

## Learning Goals

* Input validation and optional parameters
* External API call patterns + timeouts + error handling
* Config management:

  * local `.env` for development
  * GitHub Secrets for CI
* Testing with mocks (avoid real API calls in CI)

## Manual Challenges (what YOU do)

* Choose a weather API provider and read its docs.
* Implement config loading:

  * local dev uses `.env` (not committed)
  * CI uses GitHub Secrets
* Implement weather client with:

  * timeout
  * graceful failure mode (define what happens if weather API fails)
* Write tests that mock weather calls (no network dependency).

## Agent Responsibilities (what the agent can generate)

* A safe config pattern (env var names + loading strategy).
* A recommended weather call pattern and error-handling checklist.
* pytest mocking examples (you integrate them).
* A “direction-only” outline for Docker/Terraform/K8s additions.

## Secure approach for keys (mandatory)

* Define an environment variable like `WEATHER_API_KEY`.
* Local:

  * `.env` file (gitignored)
  * load into app config at startup
* CI:

  * GitHub Secrets: `WEATHER_API_KEY`
  * Inject into workflow environment for tests (but tests should not require real calls)

**.gitignore must include**

```text
.env
.env.*
```

## Step-by-step Checklist

### 1) Create branch

```bash
git checkout develop
git pull
git checkout -b feature/phase3
```

### 2) Extend endpoint and response (manual)

* Required params: `name`, `surname`
* Optional params: `phone`, `city`
* Response rules:

  * Always include provided fields in response
  * If `city` is present:

    * include `weather` object and `timestamp` (ISO 8601 recommended)

### 3) Weather API integration (manual)

Implementation requirements:

* Use an HTTP client with timeouts (e.g., httpx)
* Validate `city` string (basic sanity)
* Error strategy (choose one):

  * Option A: return response with `weather: null` and an `weather_error` field
  * Option B: return 502/503 with a clear error message
    Pick one and test it.

### 4) Tests (manual)

* Tests must not call real weather APIs.
* Mock the weather client call and assert:

  * when city provided → response includes weather + timestamp
  * when city absent → response does not include weather fields
  * when weather client errors → your chosen error strategy

### 5) CI secrets handling (manual)

* Add GitHub Secret `WEATHER_API_KEY` (repo settings).
* In workflow, if needed, expose it safely:

```yaml
env:
  WEATHER_API_KEY: ${{ secrets.WEATHER_API_KEY }}
```

But keep tests mock-based so CI does not depend on the secret to pass.

### 6) “Direction only” notes (do not implement fully)

* Add a `docs/` section in README for next steps:

  * containerization plan
  * infra plan
  * k8s plan

### 7) Push and PR

```bash
git add .
git commit -m "phase3: params + weather lookup (mocked) + secure config pattern"
git push -u origin feature/phase3
```

Open PR: `feature/phase3 → develop`

## Definition of Done

* Endpoint supports required + optional params as specified.
* Weather is fetched only when `city` is provided.
* Secrets are not committed; configuration uses env vars.
* Tests mock external calls; CI remains deterministic.

## Acceptance Criteria

* With `city` provided, response includes weather + timestamp.
* With `city` omitted, response excludes weather and still includes other params.
* CI passes without needing live network access or real API calls.
* No secrets appear in git history.

---

## 6) Security & Secrets Guidance

### Rules

* Never commit secrets, tokens, or `.env` files.
* Use environment variables for all sensitive data.
* Use GitHub Secrets for CI/CD and deployment pipelines.
* Rotate keys immediately if leaked.

### Recommended pattern

* App config reads:

  * `WEATHER_API_KEY`
  * (later) `APP_ENV`, `LOG_LEVEL`, etc.
* Local `.env` for convenience
* `.env.example` (optional) with empty placeholders (no real values)

---

## 7) Troubleshooting (quick checks)

### CI not running on feature branches

* Confirm workflow `on.push.branches` includes `"feature/*"`.
* Confirm file path is `.github/workflows/ci.yml` on the branch you pushed.
* Confirm YAML is valid (Actions tab will show parsing errors).

### Branch protection not enforcing required checks

* Check the required check name matches the workflow job name exactly.
* Ensure the PR targets `develop` (protections apply to that branch).
* Ensure “Require status checks” is enabled.

### Tests flaky / external dependency failures

* If tests call a real weather API, fix by mocking.
* Add explicit timeouts to HTTP client.
* Ensure no network calls occur during unit tests.

### FastAPI validation surprises

* Required query params will trigger 422 automatically if missing.
* Decide expected behavior and assert it in tests.

---

## 8) Style Requirements

* Keep naming deterministic:

  * endpoints, file names, job names should remain stable across phases
* Prefer small PRs with clear commit messages:

  * `phaseN: <scope>`
* Keep README updated with:

  * how to run locally
  * how to run tests
  * how CI works
* Avoid “magic” automation:

  * if you add a tool, document it
  * prefer clarity over cleverness

---

## Later Roadmap (outline only; do not fully implement)

### Containerization

* Add `Dockerfile` and `.dockerignore`
* Add local run:

  * `docker build`, `docker run`, and optionally `docker compose`
* Add CI job to build image on PRs (optional later)

### Terraform IaC (AWS direction)

* Create `infra/terraform/` with minimal modules:

  * network basics (VPC/subnets) — only when ready
  * container registry (ECR)
  * compute target (ECS or EKS; choose later)
* Keep secrets in AWS Secrets Manager or Parameter Store

### Kubernetes

* `deploy/k8s/` manifests:

  * Deployment, Service
  * Ingress (if needed)
  * ConfigMaps/Secrets references (never store real secrets)
* Add Kustomize or Helm later (choose one)

### Autoscaling

* Add HPA and load test procedure
* Verify scaling behavior (replicas up/down) and record evidence

### Observability (Prometheus + Grafana)

* Add basic metrics endpoint (Prometheus scrape)
* Add Grafana dashboard JSON (exported)
* Add basic alerts (CPU, errors, latency)

---

```
```
