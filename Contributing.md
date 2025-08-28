# Contributing

Thanks for your interest. Follow these steps:

1. Fork the repository and create a feature branch.
2. Set up your environment:
   ```bash
   python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
3. Lint and format before committing:
   ```bash
   ruff check .
   ruff format .
   ```
4. Commit with clear messages and open a pull request describing:
   - What changed
   - Why it changed
   - How to test it

## Code style
- Keep functions small and readable.
- Prefer explicit names over comments.
- UI changes should remain accessible and minimal.
