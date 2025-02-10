# receipt-processor-challenge



### Installation Guide - development

1. Create virtual environment using poetry
```bash
potrey shell
```
2. Install dependencies
```bash
poetry install
```
4. Copy .env.example to .env
5. Run server
```bash
uvicorn src.main:app --port 8080 --reload
```
