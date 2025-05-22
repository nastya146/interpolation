import nox

# Настройки по умолчанию
nox.options.sessions = ["lint", "tests", "typecheck", "docs"]
nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True

# Папки для проверки
SOURCE_DIRS = ["src", "demo", "tests"]


@nox.session
def lint(session):
    """Run ruff for linting and formatting."""
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "ruff", "check", *SOURCE_DIRS, external=True)
    session.run("poetry", "run", "ruff", "format", *SOURCE_DIRS, external=True)


@nox.session
def tests(session):
    """Run pytest with coverage."""
    session.run("poetry", "install", external=True)
    session.run(
        "poetry",
        "run",
        "pytest",
        "tests",
        "--cov=src",
        "--cov=demo",
        "--cov-report=html",
        "--cov-report=term",
        external=True,
    )

@nox.session
def typecheck(session):
    """Run mypy for type checking."""
    session.run("poetry", "install", external=True)
    session.run(
        "poetry",
        "run",
        "mypy",
        "src",
        "demo",
        external=True,
    )

@nox.session
def docs(session):
    """Build Sphinx documentation."""
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "sphinx-build", "docs/source", "docs/build/html", external=True)