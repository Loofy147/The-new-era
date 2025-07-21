```
ai-model-marketplace-os/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── cd.yml
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── docs/
│   ├── architecture.md
│   ├── discovery.md
│   ├── integration.md
│   ├── reflection.md
│   ├── design_architecture.md
│   └── transmutation.md
├── infra/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── k8s/
│       ├── base/
│       │   ├── namespace.yaml
│       │   ├── ingress.yaml
│       ├── overlays/
│       │   ├── dev/
│       │   │   └── kustomization.yaml
│       │   ├── staging/
│       │   │   └── kustomization.yaml
│       │   └── prod/
│           └── kustomization.yaml
├── services/
│   ├── api-gateway/
│   │   ├── src/
│   │   │   ├── controllers/
│   │   │   ├── middleware/
│   │   │   └── index.js
│   │   ├── Dockerfile
│   │   └── openapi.yaml
│   ├── model-runner/
│   │   ├── src/
│   │   │   ├── infer.js
│   │   │   └── utils/
│   │   ├── Dockerfile
│   │   └── configs/
│   ├── billing-engine/
│   │   ├── src/
│   │   │   ├── consumer.js
│   │   │   └── billing.js
│   │   ├── Dockerfile
│   │   └── pricing.rules.json
│   └── event-bus/
│       ├── src/
│       │   └── index.js
│       └── Dockerfile
├── cli/
│   ├── src/
│   │   ├── commands/
│   │   │   ├── run.js
│   │   │   ├── list.js
│   │   │   └── info.js
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── dashboard/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   ├── package.json
│   └── tailwind.config.js
├── shared/
│   ├── proto/
│   │   ├── infer.proto
│   │   └── billing.proto
│   └── utils/
│       └── logger.js
├── scripts/
│   ├── deploy.sh
│   └── manage-models.sh
├── tests/
│   ├── integration/
│   ├── unit/
│   └── e2e/
├── .env.example
├── docker-compose.yml
└── README.md
```

