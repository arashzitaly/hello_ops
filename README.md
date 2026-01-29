# hello_ops

Build a small Python API and learn DevOps step-by-step: testing, CI/CD, containers, Terraform IaC, Kubernetes, autoscaling, and observability.

This repository is intentionally **learning-first**: each phase is small, reviewable, and focuses on understanding *why* each tool/practice exists. No production-complete stack unless explicitly added later.

---

## Project Goal

- Build a minimal FastAPI service incrementally
- Practice real DevOps workflows:
  - testing and quality gates
  - CI pipelines
  - containerization
  - Infrastructure as Code (Terraform)
  - Kubernetes deployment + autoscaling
  - observability (metrics, dashboards, alerts)

---

## Learning Phases (Extended Roadmap)

Each phase includes **what you build** and **what you learn**. Keep PRs small and reviewable.

### Phase 1 — Minimal API + CI

**Build**
- Tiny FastAPI app with one “Hello World” endpoint
- One pytest test
- GitHub Actions CI for format/lint + tests

**Learn**
- Basic Python project structure
- FastAPI fundamentals
- CI basics and quality gates

---

### Phase 2 — API Parameters + Quality Gates

**Build**
- Add a required query parameter (e.g., `name`)
- Tests for valid and missing inputs
- Stable CI job names usable in branch protection rules

**Learn**
- Request handling and validation
- CI checks as merge gates
- Branch protection basics

---

### Phase 3 — Optional Params + External API (Mocked)

**Build**
- Required params: `name`, `surname`
- Optional params: `phone`, `city`
- Weather lookup if `city` is provided (**mocked in tests**)
- Secure config via environment variables

**Learn**
- Required vs optional inputs
- External API calls (timeouts, retries/error handling)
- Secrets/config management and mocking strategy

---

### Phase 4 — Containerization

**Build**
- `Dockerfile` and `.dockerignore`
- Local `docker build` / `docker run` instructions in this README
- (Optional) CI job to build the image

**Learn**
- Packaging an app into a container
- Reproducible builds
- How CI validates container builds

---

### Phase 5 — Terraform IaC (Learning Scope)

**Build**
- `infra/terraform/` with small, **non-production** examples
- Minimal network primitives (VPC/subnets) + container registry (ECR)
- Documentation for variables and how to `plan/apply/destroy` locally

**Learn**
- Terraform layout, modules, and state basics
- Safe provisioning workflow (plan → apply → destroy)
- Reviewing infra changes before applying

---

### Phase 6 — Kubernetes Deployment (Dev-Grade)

**Build**
- `deploy/k8s/` manifests:
  - `Deployment`
  - `Service`
- Config/Secret references (no real secrets committed)
- Basic autoscaling (HPA) if appropriate

**Learn**
- Core Kubernetes objects and service exposure
- Config and secrets patterns
- Scaling basics

---

### Phase 7 — Observability (Metrics + Dashboards)

**Build**
- Add a metrics endpoint (e.g., Prometheus format)
- Prometheus scrape config (**dev-only**)
- Grafana dashboard JSON export
- Simple alert examples (latency / error rate)

**Learn**
- Metrics-driven visibility
- Dashboards for health checks
- Alerting + SLO thinking foundations

---

## How to Use This Roadmap

- Keep each phase small and reviewable (tiny PRs)
- Add at least **one meaningful test** per phase
- Treat CI as a guardrail (format/lint + tests)
- Document the **why** behind each change in the PR and/or README

---

## Repository Status

- Current phase: **TBD**
- CI status: **TBD**
