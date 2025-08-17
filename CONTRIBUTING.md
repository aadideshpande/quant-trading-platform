| Branch      | Purpose                               | When to Create                               | When to Merge                                     |
| ----------- | ------------------------------------- | -------------------------------------------- | ------------------------------------------------- |
| `main`      | Production-ready code                 | After QA approved release or hotfix          | Only from `release/*` or `hotfix/*`               |
| `develop`   | Latest dev features for next release  | Always present                               | Only from `feature/*`, `hotfix/*`, or `release/*` |
| `feature/*` | New features or enhancements          | When starting a new user story/epic          | Into `develop` after PR review                    |
| `release/*` | Staging for a production release      | When develop is ready for release            | Into both `main` and `develop`                    |
| `hotfix/*`  | Urgent patch directly from production | When a critical issue is found in production | Into both `main` and `develop`                    |
