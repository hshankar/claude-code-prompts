# /just - Intelligent Justfile Generator

You are tasked with creating a comprehensive justfile for a software project. Analyze the project structure and create appropriate commands based on the technologies and services present.

## Analysis Phase

First, examine the project to understand:
1. **Project type**: Frontend, backend, full-stack, microservices, etc.
2. **Technologies**: Languages, frameworks, build tools, package managers
3. **Services**: Web servers, databases, APIs, background processes
4. **Configuration**: Look for config files, environment setup, ports
5. **Development workflow**: Testing, linting, building, deployment

## Core Principles

When creating the justfile, follow these principles:

### 1. Background Process Management
- Services that don't exit (servers, dev servers) must run in background with `nohup`
- Use `>>` for log appending (never overwrite existing logs)
- Store PIDs in `logs/*.pid` files for process tracking
- Validate service startup with health checks (curl, process checks)
- Exit with code 1 if any service fails to start

### 2. Composite Commands
- Break complex operations into individual commands first
- Create composite commands that call individual ones
- Use `@just command && echo "✓ Success" || (echo "✗ Failed" && exit 1)` pattern
- Show progress messages between steps
- Fail fast - stop execution if any step fails

### 3. Service Management
- For stop commands, follow proper shutdown order (UI → Services → Database)
- Create individual stop commands (`stop-api`, `stop-db`, etc.)
- Main `stop` command calls individual stops in correct order
- Handle cases where services aren't running gracefully

### 4. Logging and Monitoring
- Create `logs/` directory for all log files  
- Provide `logs` command to show recent logs (tail -n 10)
- Provide `logs-follow` command for real-time monitoring
- Include log file paths in success messages

## Standard Commands to Include

### Setup Commands
- `setup` - Full project setup (dependencies, database, config)
- `setup-[component]` - Individual component setup

### Service Commands  
- `start-[service]` - Individual service startup with validation
- `stop-[service]` - Individual service shutdown
- `start-all` - Start all services with progress tracking
- `stop` - Stop all services in proper order
- `restart` - Stop then start all services

### Development Commands
- `dev` - Development mode (typically API + UI)
- `build` - Production build
- `test` - Run test suite
- `test-coverage` - Tests with coverage report
- `lint` - Code linting

### Utility Commands
- `health` - Check if services are responding
- `logs` - Show recent logs from all services
- `logs-follow` - Follow logs in real-time
- `clean` - Clean generated files and caches
- `default` - Show available commands with `@just --list`

## Background Service Template

```just
start-[service]:
    #!/usr/bin/env bash
    echo "Starting [service] on port [port]..."
    mkdir -p logs
    cd [directory]
    nohup [command] >> ../logs/[service].log 2>&1 &
    echo $! > ../logs/[service].pid
    sleep [appropriate-delay]
    if [health-check]; then
        echo "✓ [Service] started successfully (logs: logs/[service].log)"
    else
        echo "✗ [Service] failed to start"
        exit 1
    fi

stop-[service]:
    #!/usr/bin/env bash
    if [ -f logs/[service].pid ]; then
        kill $(cat logs/[service].pid) 2>/dev/null && echo "✓ [Service] stopped" || echo "[Service] not running"
        rm -f logs/[service].pid
    else
        echo "[Service] not running"
    fi
```

## Health Check Examples

- **Web services**: `curl -f http://localhost:[port]/health >/dev/null 2>&1`
- **Process check**: `kill -0 $PID 2>/dev/null`
- **Port check**: `nc -z localhost [port]`
- **File check**: `[ -f [expected-file] ]`

## Example Project Patterns

### Full-Stack Web App
```just
# Frontend (React/Vue/Angular) + Backend API
start-api: [background uvicorn/flask/express with health check]
start-ui: [background npm run dev with health check]  
start-all: [start-api then start-ui with progress]
dev: [same as start-all]
```

### Microservices
```just
# Multiple services + database
start-db: [background database with health check]
start-auth: [background auth service]
start-api: [background main API]
start-ui: [background frontend]
start-all: [start in dependency order]
```

### Python Project  
```just
# Look for requirements.txt, pyproject.toml, poetry.lock
setup: [venv creation, pip/poetry install]
test: [pytest with coverage]
lint: [flake8/black/ruff]
```

## Output Format

Structure the justfile with:
1. Header comment explaining the project
2. `default` recipe showing available commands
3. Setup commands
4. Individual service commands
5. Composite commands  
6. Development utilities
7. Maintenance commands

Use clear section comments and consistent formatting. Include helpful echo statements and emojis for user feedback (✓ ✗ 🚀 🔧 🌐 🛑).

## Project Detection Logic

- **Frontend**: package.json, webpack.config.js, vite.config.ts
- **Backend API**: main.py, app.py, server.js, Cargo.toml
- **Database**: docker-compose.yml with db, requirements.txt with SQLAlchemy
- **Full-stack**: Both frontend and backend indicators
- **Microservices**: Multiple service directories or docker-compose with multiple services

Adapt the justfile to the specific project needs while following these established patterns.