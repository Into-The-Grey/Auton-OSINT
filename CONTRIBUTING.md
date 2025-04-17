# 🤝 Contributing to Auton-OSINT

Thanks for your interest in contributing! This project welcomes contributors of all skill levels.

---

## 📦 Getting Started

1. **Fork** the repository
2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/YOUR_USERNAME/Auton-OSINT.git
   cd Auton-OSINT
   ```

3. **Create a virtual environment** and install dependencies:

   ```bash
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Create a feature branch**:

   ```bash
   git checkout -b feat/your-feature-name
   ```

---

## 🧠 Code Standards

- **Python 3.12+**
- Use `black` for auto-formatting.
- Lint using `flake8`:

  ```bash
  flake8 .
  ```

---

## 🧠 Development Tips

- Run the CLI using:

  ```bash
  python main.py --help
  ```

- Add new modules under `/modules/`
- All module outputs should follow the normalized JSON structure.
- Store module configs in `/config/modules_config/`

---

## 📜 Commits & PRs

- Use clear commit messages:

  ``` bash
  feat(username): added fallback for Sherlock
  fix(email): handle null MX response
  ```

- Pull requests should:
  - Reference related issues
  - Be atomic (one feature/fix per PR)
  - Include CLI or module test cases

---

## 🛡️ Security

See [SECURITY.md](SECURITY.md) for info on reporting vulnerabilities.

---

## 📬 Questions?

Open an issue or reach out via the Discussions tab.

---

Thank you for helping make Auton-OSINT better!
