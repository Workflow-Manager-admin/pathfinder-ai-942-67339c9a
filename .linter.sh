#!/bin/bash
cd /home/kavia/workspace/code-generation/pathfinder-ai-942-67339c9a/ai_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

