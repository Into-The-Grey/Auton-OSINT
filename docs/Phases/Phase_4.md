# 📌 **Phase 4: Additional Module Development & Advanced Integration**

## ✅ **Deliverable Overview**

Phase 4 involves expanding Auton-OSINT through four primary tasks:

1. **Dark Web Module (TOR Integration)**
2. **Real Name & Identity Resolution Module**
3. **Web Dashboard & Front-End Integration**
4. **Advanced Automation & Task Scheduling**

---

## 🌑 **Task 1: Dark Web Module Development**

**Module Path:** `modules/darkweb_integration.py`

### Module Structure(Task 1)

```python
def query_torbot(keyword: str) -> dict:
    """
    Query TorBot to crawl .onion links for given keyword.
    Returns standardized JSON results.
    """

def query_darksearch(keyword: str, limit: int = 20) -> dict:
    """
    Query DarkSearch API for .onion sites matching keyword.
    Returns JSON structured results.
    """

def darkweb_lookup(keyword: str) -> dict:
    """
    Aggregate queries from both TorBot and DarkSearch.
    Integrate into correlation engine schema.
    """
```

### Integration Points(Task 1)

- Correlation schema (`correlation_engine.py`) for dark-web sources.
- Input parsing to handle keywords from centralized parser (`input_parser.py`).

### Configuration (`darkweb_config.yaml`)

```yaml
tor_proxy: "socks5h://127.0.0.1:9050"
darksearch_api_key: "your_darksearch_api_key"
query_limit: 20
timeout: 60
```

### Logging(Task 1)

- Log file: `logs/darkweb_module.log`
- Use existing logging format (`logger.debug/info/error`).

### Unit Testing(Task 1)

- Pytest mocks for TorBot and DarkSearch responses.

---

## 👤 **Task 2: Real Name & Identity Resolution Module**

**Module Path:** `modules/realname_resolution.py`

### Module Structure(Task 2)

```python
def socialscan_lookup(real_name: str) -> dict:
    """
    Query SocialScan to resolve real names into associated accounts.
    Returns structured JSON.
    """

def linkedin_public_search(real_name: str) -> dict:
    """
    Scrape public LinkedIn profiles to correlate real names.
    Returns JSON structured results.
    """

def resolve_identity(real_name: str) -> dict:
    """
    Combine multiple lookup sources into unified correlation schema.
    """
```

### Integration Points(Task 2)

- Correlation schema updates for identity resolution data.
- Utilize centralized input parsing (`input_parser.py`).

### Configuration (`realname_resolution_config.yaml`)

```yaml
socialscan_api_key: "your_socialscan_api_key"
linkedin_search_enabled: true
proxies:
  http: null
  https: null
rate_limit: 10  # requests per minute
```

### Logging(Task 2)

- Log file: `logs/realname_module.log`

### Unit Testing(Task 2)

- Pytest mocks SocialScan API and LinkedIn scraping.

---

## 💻 **Task 3: Web Dashboard & Front-End Integration**

**Framework Recommendation:** FastAPI (lightweight, async-friendly)

### Web Structure

```plaintext
web_dashboard/
├── main.py
├── routers/
│   ├── task_submission.py
│   ├── status_monitor.py
│   └── visualizations.py
├── templates/
│   └── index.html
└── static/
    ├── css/
    └── js/
```

### Example API Endpoints

- `POST /submit-task`: Accepts JSON for task initiation.
- `GET /task-status/{task_id}`: Returns task progress.
- `GET /visualization/{task_id}`: Renders PyVis HTML visualization.

### Configuration (`web_dashboard_config.yaml`)

```yaml
host: "0.0.0.0"
port: 8000
authentication:
  enabled: false
  username: "user"
  password: "pass"
```

### Logging(Task 3)

- Log file: `logs/web_dashboard.log`

### Unit Testing(Task 3)

- FastAPI TestClient for endpoint testing.

---

## 📆 **Task 4: Advanced Automation & Task Scheduling**

**Module Path:** `modules/task_scheduler.py`

### Scheduler Module Structure

```python
def schedule_task(input_data: dict, frequency: str) -> bool:
    """
    Schedule OSINT tasks (daily, weekly, monthly).
    Stores scheduling data in SQLite DB.
    """

def edit_scheduled_task(task_id: int, new_data: dict) -> bool:
    """
    Edit existing scheduled task configuration.
    """

def remove_scheduled_task(task_id: int) -> bool:
    """
    Remove scheduled task from scheduler.
    """

def run_scheduled_tasks() -> None:
    """
    Execute scheduled tasks and integrate with existing modules.
    """
```

### Database Schema (SQLite)

```sql
CREATE TABLE scheduled_tasks (
  task_id INTEGER PRIMARY KEY AUTOINCREMENT,
  input_data TEXT NOT NULL,
  frequency TEXT NOT NULL,
  next_run TIMESTAMP NOT NULL
);
```

### Logging(Task 4)

- Log file: `logs/scheduler_module.log`

### Unit Testing(Task 4)

- Pytest mocks SQLite operations and task executions.

---

## 📚 **Documentation Updates & Consistency**

**Updates Required in Documentation:**

- `modules.md` (document new modules clearly)
- `README.md` (project overview and new module highlights)
- `config_reference.md` (describe new YAML configurations)

**Correlation Schema Adjustments:**

- Add fields relevant to dark web and identity resolution modules (`source`, `confidence_score`, etc.)

---

## 🎯 **Checkpoint & Visualization Integration**

- Ensure new modules (`darkweb_integration.py`, `realname_resolution.py`) integrate fully with checkpointing (`data/.corr_state.json`).
- Validate PyVis visualizations (`generate_graph.py`) fully support new module data.

---

## 🔧 **Immediate Next Steps & Testing**

- Conduct smoke-tests for all newly developed modules:
  - Dark Web Integration (`TorBot`, `DarkSearch`)
  - Identity Resolution (`SocialScan`, LinkedIn)
  - Web Dashboard (end-to-end task submission, progress updates, visualization)
  - Task Scheduler (task addition, editing, execution)
  
- Confirm smooth integration with correlation engine and visualization outputs.

---

## 🚩 **Preparation for Phase 5 (Next Steps)**

- **Data Correlation Enhancements:**
  - Implement advanced correlation rules and heuristics.
  - Explore graph-based correlation (NetworkX).

- **Visualization Improvements:**
  - Explore advanced visualization libraries (D3.js integration).
  - Enhance interactivity (filters, grouping).

- **Performance Optimization:**
  - Optimize module runtime and database interactions.

---

## 📋 **CMD-Style Phase 4 Summary**

```plaintext
Auton-OSINT Project Build Plan
├── Phase 4: Additional Module Development
│   ├── Module: Phone Number Lookup (Completed)
│   ├── Module: Social Media Account Discovery (Completed)
│   ├── Module: TOR/Dark Web Integration (Current Task)
│   ├── Module: Real Name & Identity Resolution (Current Task)
│   ├── Web Dashboard & Front-End Integration (Current Task)
│   └── Advanced Automation & Task Scheduling (Current Task)
```

---

This comprehensive documentation provides clear guidance, ensuring seamless integration into the existing Auton-OSINT framework while preparing for future phases.
