#!/bin/bash
# =============================================================================
# AI Coding Portfolio - Project Creator Script
# Usage: ./scripts/create-project.sh <project-number> <project-name>
# Example: ./scripts/create-project.sh 02 code-reviewer-ai
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}Error: Missing arguments${NC}"
    echo "Usage: $0 <project-number> <project-name>"
    echo "Example: $0 02 code-reviewer-ai"
    exit 1
fi

PROJECT_NUM=$1
PROJECT_NAME=$2
PROJECT_DIR="projects/${PROJECT_NUM}-${PROJECT_NAME}"

# Check if project already exists
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${RED}Error: Project directory already exists: $PROJECT_DIR${NC}"
    exit 1
fi

echo -e "${YELLOW}Creating new project: $PROJECT_DIR${NC}"

# Create directory structure
mkdir -p "$PROJECT_DIR"/{src,tests,docs}

# Copy template files
cp templates/base-python/.env.example "$PROJECT_DIR/.env.example"
cp templates/base-python/requirements.txt "$PROJECT_DIR/requirements.txt"
cp templates/base-python/pyproject.toml "$PROJECT_DIR/pyproject.toml"
cp templates/base-python/Dockerfile "$PROJECT_DIR/Dockerfile"
cp templates/base-python/docker-compose.yml "$PROJECT_DIR/docker-compose.yml"
cp templates/base-python/.pre-commit-config.yaml "$PROJECT_DIR/.pre-commit-config.yaml"

# Copy Python template files
cp templates/base-python/src/__init__.py "$PROJECT_DIR/src/__init__.py"
cp templates/base-python/src/main.py "$PROJECT_DIR/src/main.py"
cp templates/base-python/tests/__init__.py "$PROJECT_DIR/tests/__init__.py"
cp templates/base-python/tests/conftest.py "$PROJECT_DIR/tests/conftest.py"
cp templates/base-python/tests/test_main.py "$PROJECT_DIR/tests/test_main.py"
cp templates/base-python/docs/decisions.md "$PROJECT_DIR/docs/decisions.md"

# Replace placeholders in template files
PROJECT_NAME_CAMEL=$(echo "$PROJECT_NAME" | sed -E 's/(^|-)([a-z])/\U\2/g')

echo -e "${YELLOW}Configuring project files...${NC}"

# Update pyproject.toml (macOS compatible sed)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/{project_name}/$PROJECT_NAME/g" "$PROJECT_DIR/pyproject.toml"
    sed -i '' "s/{project_description}/Project $PROJECT_NUM: $PROJECT_NAME/g" "$PROJECT_DIR/pyproject.toml"
    
    sed -i '' "s/{project_name}/$PROJECT_NAME/g" "$PROJECT_DIR/src/__init__.py"
    sed -i '' "s/{project_description}/Project $PROJECT_NUM: $PROJECT_NAME/g" "$PROJECT_DIR/src/__init__.py"
    
    sed -i '' "s/{project_name}/$PROJECT_NAME/g" "$PROJECT_DIR/src/main.py"
    sed -i '' "s/{project_description}/Project $PROJECT_NUM: $PROJECT_NAME/g" "$PROJECT_DIR/src/main.py"
else
    sed -i "s/{project_name}/$PROJECT_NAME/g" "$PROJECT_DIR/pyproject.toml"
    sed -i "s/{project_description}/Project $PROJECT_NUM: $PROJECT_NAME/g" "$PROJECT_DIR/pyproject.toml"
    
    sed -i "s/{project_name}/$PROJECT_NAME/g" "$PROJECT_DIR/src/__init__.py"
    sed -i "s/{project_description}/Project $PROJECT_NUM: $PROJECT_NAME/g" "$PROJECT_DIR/src/__init__.py"
    
    sed -i "s/{project_name}/$PROJECT_NAME/g" "$PROJECT_DIR/src/main.py"
    sed -i "s/{project_description}/Project $PROJECT_NUM: $PROJECT_NAME/g" "$PROJECT_DIR/src/main.py"
fi

# Create README from template
cat > "$PROJECT_DIR/README.md" << EOL
# ${PROJECT_NUM} - ${PROJECT_NAME_CAMEL}

> Project description here...

## 📋 项目信息

| 属性 | 内容 |
|:---|:---|
| **项目编号** | ${PROJECT_NUM} |
| **类型** | 待填写 |
| **技术栈** | Python, FastAPI |
| **难度** | ⭐⭐⭐ |
| **预计工期** | X 天 |

---

## 🎯 项目目标

- 目标 1
- 目标 2
- 目标 3

---

## 🏗️ 系统架构

\`\`\`
[架构图待添加]
\`\`\`

---

## 🚀 快速开始

### 环境要求

- Python 3.10+

### 本地开发

\`\`\`bash
cd ${PROJECT_DIR}
cp .env.example .env
pip install -r requirements.txt
pytest
python src/main.py
\`\`\`

---

## 📝 迭代记录

### v0.1 (Day 1)
- 初始实现

---

## 🔧 技术决策

见 [docs/decisions.md](./docs/decisions.md)

---

## ⚠️ 隐私声明

本项目所有数据均为 Mock 数据。
EOL

echo -e "${GREEN}✅ Project created successfully!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. cd $PROJECT_DIR"
echo "  2. cp .env.example .env"
echo "  3. Edit .env and README.md"
echo "  4. pip install -r requirements.txt"
echo "  5. pytest"
echo "  6. Start coding!"
echo ""
echo -e "${YELLOW}Good luck! 🚀${NC}"
