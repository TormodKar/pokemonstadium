# 3-stage build:
# 1. builder: installs deps into a project venv using uv
# 2. dev: includes dev dependency group + source bind mount friendly
# 3. prod: runtime-only deps + minimal final image


# 1. builder

FROM python:3.12-slim AS builder

# System deps (psycopg, build tools, curl for uv install)
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Make uv create the venv in a stable location we can copy between stages 
# (instead of /app/.venv which may get clobbered by bind mounts in dev)
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"


# Copy dependency files first for caching
COPY pyproject.toml uv.lock* ./

# --------- Runtime deps only (for prod) ----
# This installs ONLY [project].dependencies
RUN uv sync --frozen --no-dev || uv sync --no-dev

# Save a copy of the runtime venv so we can reuse it
RUN cp -a /opt/venv /opt/venv-runtime

# ---- Dev deps (runtime + dev group) ----
# Install dev group into the main /opt/venv
RUN uv sync --frozen --group test --group lint || uv sync --group test --group lint


############################
# 2) dev image
############################
FROM python:3.12-slim AS dev

# If you need psycopg build tooling in dev, keep these.
# If you only use psycopg[binary], you can often drop build-essential here.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the dev venv from builder (includes dev group)
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# Copy app code (in docker-compose you'll typically bind-mount anyway)
COPY . .

EXPOSE 8000
# No CMD here so compose can override command easily


############################
# 3) prod image
############################
FROM python:3.12-slim AS prod

WORKDIR /app

# Copy runtime-only venv (no pytest/ruff)
COPY --from=builder /opt/venv-runtime /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# Copy only the application code
COPY . .

EXPOSE 8000

# A sensible default production command (override as you like)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]