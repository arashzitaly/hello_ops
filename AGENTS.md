# AGENTS.md — hello_ops

## 1) Project overview (what + why)

**hello_ops** is a learning-first repository to build a small Python API and progressively add DevOps practices **in controlled phases**. Each phase introduces one new concept (testing, CI quality gates, external calls, containers, Terraform, Kubernetes, observability) without jumping to production-complete complexity.

**Core principle:** incremental change + understanding “why” behind each choice.  
**Non-goal:** a production-ready platform. Anything “production-grade” must be explicitly requested later.

---

## 2) Repository structure (tree) + phase additions

Target structure over time:

```text
hello_ops/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py               # Phase 3+
│   ├── services/
│   │   ├── __init__.py
│   │   └── weather.py           # Phase 3+
│   └── metrics.py               # Phase 7+
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_weather.py          # Phase 3+
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile                   # Phase 4+
├── .dockerignore                # Phase 4+
├── infra/
│   └── terraform/               # Phase 5+
│       ├── README.md
│       ├── versions.tf
│       ├── providers.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── main.tf              # learning-grade primitives
└── deploy/
    └── k8s/                     # Phase 6+
        ├── README.md
        ├── deployment.yaml
        ├── service.yaml
        ├── hpa.yaml              # Phase 6+ (if used)
        ├── configmap.yaml        # Phase 6+
        ├── secret.yaml           # Phase 6+ (placeholder refs only)
        ├── prometheus/           # Phase 7+ (dev-only)
        │   └── prometheus.yaml
        └── grafana/              # Phase 7+ (dev-only)
            └── dashboard.json
