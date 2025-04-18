# Python Project Analysis System Documentation

## Overview

The Python Project Analysis System is a comprehensive toolset for analyzing Python projects, providing insights into code quality, dependencies, complexity, and testing coverage. This system integrates multiple analysis tools and services to deliver a complete view of Python codebases.

## Core Components

### 1. Dependency Analysis

- **PyDeps Integration**
  - Located in `scripts/analyze_deps.py`
  - Generates dependency graphs and JSON reports
  - Output stored in `analysis_results/pydeps_results.json`
  - Visualizes module relationships and import hierarchies

### 2. Code Quality Analysis

- **Ruff Integration**

  - Enforces code style and quality standards
  - Results stored in `analysis_results/ruff_results.json`
  - Configured via project-level settings

- **Cyclomatic Complexity Analysis**
  - Radon integration for complexity metrics
  - Results in `analysis_results/radon_cc_results.json`
  - Identifies complex code sections requiring refactoring

### 3. Duplicate Code Detection

- **CopyDetect Integration**
  - Generates HTML reports for code duplication
  - Located in `analysis_results/copydetect_report.html`
  - Helps maintain DRY principles

### 4. Service Architecture

#### Chatbot Service

- Primary service for handling analysis requests
- Located in `services/chatbot_service/`
- Key components:
  - Main application logic (`src/main.py`)
  - Unit tests (`tests/test_main.py`)
  - Docker configuration for containerization

#### MCP Service

- Model Context Protocol service
- Located in `services/mcp_service/`
- Features:
  - Health checking system
  - Error handling framework
  - Configuration management
  - Comprehensive test suite

#### Database Mock Services

- Neo4j mock for graph database simulation
- Relational database mock
- Weaviate mock for vector database testing

### 5. Testing Infrastructure

- **Integration Tests**
  - Located in `tests/integration/`
  - Covers:
    - Advanced routing scenarios
    - Complex database interactions
    - Dynamic dependency analysis
    - Error scenarios
    - Performance boundaries
    - Service communication
    - System-level testing

## Usage Examples

### Running Dependency Analysis

```bash
python scripts/analyze_deps.py <project_path>
```

### Executing the Test Suite

```bash
# Run integration tests
cd tests/integration
uv run pytest

# Run service-specific tests
cd services/chatbot_service
uv run pytest
```

### Starting Services

```bash
# Start chatbot service
cd services/chatbot_service
uv run python src/main.py

# Start MCP service
cd services/mcp_service
uv run python main.py
```

## Configuration

### Dependencies

- Managed via `uv` package manager
- Lock files ensure reproducible environments
- Service-specific dependencies in respective pyproject.toml files

### Docker Support

- Containerization supported for all services
- Dockerfile provided for each component
- docker-compose.yml for orchestration

### Kubernetes Support

- Helm charts available in `charts/` directory
- Supports deployment of:
  - Chatbot service
  - MCP service
  - Database mocks

## Best Practices

1. **Code Analysis**

   - Regular dependency analysis to prevent circular imports
   - Complexity monitoring for maintainable code
   - Duplication checks for code quality

2. **Testing**

   - Comprehensive test coverage
   - Integration testing for service interactions
   - Error scenario validation

3. **Development Workflow**
   - Use uv for dependency management
   - Run analysis tools before commits
   - Follow established error handling patterns

## Future Enhancements

1. **Analysis Tools**

   - Additional static analysis integration
   - Dynamic analysis capabilities
   - Custom rule development

2. **Reporting**
   - Enhanced visualization options
   - Trend analysis
   - Metrics dashboards

## AI Analysis Integration

The primary purpose of this system is to generate structured data for AI-powered code analysis. The system produces two key files that are specifically formatted for AI consumption:

### Project Structure Analysis (`project_structure.json`)

This file provides a complete tree representation of the project's file organization:

```json
{
  "": {
    "services": {
      "chatbot_service": {
        "files": [
          "README.md",
          "main.py",
          "pyproject.toml",
          "src.json",
          "uv.lock"
        ],
        "src": {},
        "tests": {}
      }
    }
  }
}
```

AI systems can use this data to:

- Map project architecture and component relationships
- Identify structural patterns and anti-patterns
- Analyze project organization and suggest improvements
- Validate project structure against best practices
- Track structural changes over time

### Dependencies Analysis (`pydeps_results.json`)

This file maps Python module dependencies and imports:

```json
{
  "modules": [
    {
      "name": "services.chatbot_service.src",
      "modules": [
        {
          "file": "main.py",
          "module": "main",
          "imports": [
            "fastapi.FastAPI",
            "fastapi.HTTPException",
            "fastapi.Request",
            "pydantic.BaseModel"
          ]
        }
      ]
    }
  ]
}
```

AI systems can leverage this data to:

- Detect dependency patterns and potential issues
- Analyze module coupling and cohesion
- Identify security vulnerabilities in dependencies
- Suggest architectural improvements
- Monitor dependency health and evolution

### AI Analysis Applications

1. **Architectural Analysis**

- Evaluate service boundaries
- Detect layering violations
- Assess microservice independence
- Identify shared dependencies

2. **Code Quality Assessment**

- Analyze import patterns
- Detect circular dependencies
- Identify unused imports
- Calculate modularity metrics

3. **Security Analysis**

- Track external dependencies
- Identify vulnerable patterns
- Monitor dependency updates
- Assess attack surface

4. **Maintenance Predictions**

- Predict refactoring needs
- Identify technical debt
- Forecast maintenance costs
- Plan modernization efforts

5. **Evolution Tracking**

- Monitor architectural drift
- Track complexity growth
- Assess technical debt accumulation
- Measure architectural conformance

The structured JSON output is specifically designed for machine consumption and analysis, enabling AI systems to perform deep analysis of the codebase's health, structure, and evolution.
