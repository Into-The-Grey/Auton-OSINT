# 🏷️ Labeling System – Auton-OSINT

This file outlines the structure, automation, and conventions used for managing **labels** in the Auton-OSINT GitHub repository.

---

## 📄 File Location

All label definitions are maintained in:

```bash
.github/labels.yml
```

These are **automatically synchronized** with GitHub using a workflow.

---

## ⚙️ Sync Automation

We use the [`EndBug/label-sync`](https://github.com/EndBug/label-sync) GitHub Action to automatically apply labels from `labels.yml`.

### Workflow File

```bash
.github/workflows/label-sync.yml
```

It triggers on changes to the label file and also supports manual sync from the Actions tab.

---

## 🔖 Default Labels

| Name          | Color   | Description                          |
|---------------|---------|--------------------------------------|
| `bug`         | d73a4a  | Something isn't working              |
| `auto-generated` | cfd3d7 | Created automatically by CI         |
| `reviewing`   | 0366d6  | Under manual or automated review     |
| `approved`    | 0e8a16  | Review or test passed                |
| `dependencies`| 7057ff  | Dependency updates                   |
| `ci`          | f9d0c4  | Continuous Integration-related changes |
| `docs`        | fef2c0  | Markdown or documentation update    |
| `python`      | c5def5  | Python-related source changes        |

---

## 📌 Notes

- ✅ Labels are case-sensitive.
- 🚫 Do **not** modify labels manually in the GitHub UI.
- 🛠️ Edit `.github/labels.yml` and commit for updates.

---

## 📢 Questions or Suggestions?

Start a thread under the **GitHub Discussions** tab or open an issue with label `question`.
