# receipt-processor-challenge


### Aussumptions/Notes
- The processing for receipts can be improved in the future to be more scalable by adding
    multiprocessing or on a infastructure scale you can design a pipeline that takes in receipts.


### [Project Structure](#project-structure)


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
### Installation Guide - docker

1. Create virtual environment using poetry
```bash
cd docker
```

3. Copy .env.example to .env and update values

4. Run database
```bash
docker-compose up -d
```

## Testing
```
pytest -v
```
