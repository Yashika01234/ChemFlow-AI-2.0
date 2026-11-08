# ChemFlow AI 2.0

A demonstrable chemistry intelligence platform with a React dashboard and a modular FastAPI backend.

## What it does

- **Compound intelligence:** parses SMILES, validates structures, returns formula, molecular weight, exact mass, TPSA, logP, H-bond donors/acceptors, rotatable bonds, and functional-group matches.
- **Organic chemistry engine:** functional-group inspection, simple formula-based isomer grouping, reaction classification, and plain-language explanations.
- **Reaction prediction:** applies a deliberately small, explicit set of RDKit reaction templates (ester hydrolysis, alkene hydrogenation, and alcohol oxidation). It does **not** claim general-purpose reaction prediction.
- **Stoichiometry:** balances equations, computes limiting reagent and theoretical product yield from user-supplied quantities.
- **Monte Carlo:** samples uncertain yield assumptions and returns a distribution summary and histogram.
- **Engineering:** FastAPI validation, SQLite persistence, REST endpoints, unit/API tests, sample dataset, Dockerfile, and a React/Vite dashboard.

## Important scientific scope

ChemFlow is an educational decision-support demonstrator, not a laboratory safety system or a validated synthesis-planning tool. Reaction templates cover only a few transformations and may produce multiple candidates. Confirm all chemistry with authoritative references and qualified supervision. Monte Carlo output is only as meaningful as the assumptions and distributions supplied.

## Quick start

### 1. Backend

Python 3.10+ recommended.

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

If RDKit installation via pip is unavailable for your platform, install it with conda:
`conda install -c conda-forge rdkit`

### 2. Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL (normally http://localhost:5173). The frontend expects the API at `http://127.0.0.1:8000`; set `VITE_API_URL` to override it.

### 3. Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest -q
```

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/compounds/analyze` | Parse and analyze a SMILES string |
| POST | `/api/organic/classify` | Classify a reaction from reactant SMILES |
| POST | `/api/reactions/predict` | Apply supported reaction templates |
| POST | `/api/stoichiometry/balance` | Balance a chemical equation |
| POST | `/api/stoichiometry/yield` | Limiting reagent and theoretical yield |
| POST | `/api/simulations/monte-carlo` | Yield uncertainty simulation |
| GET | `/api/history` | Recent saved analyses |

## Example requests

Compound analysis:

```json
{"smiles":"CC(=O)OCC","name":"ethyl acetate"}
```

Reaction prediction:

```json
{"reaction":"hydrogenation","reactants":["C=C"]}
```

Balance:

```json
{"equation":"Fe + O2 -> Fe2O3"}
```

Monte Carlo:

```json
{"mean_yield":0.78,"std_yield":0.06,"trials":5000,"seed":7}
```

## Project layout

```text
chemflow-ai-2/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── services/
│   │   ├── db.py
│   │   └── main.py
│   ├── tests/
│   ├── data/sample_compounds.json
│   ├── requirements.txt
│   └── requirements-dev.txt
└── frontend/
    ├── src/
    ├── package.json
    └── vite.config.js
```

## Next upgrades

1. Add a curated reaction dataset and benchmark prediction precision/recall.
2. Add atom-mapped reaction records and reaction-center visualization.
3. Add user accounts, project workspaces, and exportable experiment reports.
4. Add uncertainty models for conversion, selectivity, and recovery separately.
5. Add PubChem or ChEMBL integration with caching and source attribution.
