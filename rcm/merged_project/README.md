# RCM - Code Visualizer & Diagram Generator

A unified web application that combines code visualization and AI-powered diagram generation.

## Features

### Code Visualizer
- Multi-language Support: Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, Ruby, PHP, SQL
- AST Parsing: Extract functions, classes, variables, imports
- Code Metrics: Lines of code, function count, class count
- Flowchart Generation: Python control flow diagrams

### AI Diagram Generator
- Text-to-Diagram: Natural language to diagrams
- Multiple Types: Flowchart, Sequence, ERD, Class, State, Architecture
- AI-Powered: Uses OpenAI GPT-4o via OpenRouter

## Project Structure

```
merged_project/
├── backend/
│   ├── app.py                 # Flask API
│   ├── parsers/              # Language parsers
│   │   ├── python_parser.py
│   │   ├── javascript_parser.py
│   │   ├── sql_parser.py
│   │   └── generic_parser.py
│   ├── services/             # Business logic
│   │   ├── metrics_service.py
│   │   ├── dependencies_service.py
│   │   ├── diagram_service.py
│   │   └── flowchart_service.py
│   └── utils/
│       └── config.py
│
├── frontend/
│   ├── app.py               # Streamlit UI
│   ├── services/
│   │   └── api_service.py
│   └── utils/
│       ├── helpers.py
│       └── theme.py
│
├── requirements.txt          # Root requirements
├── setup.bat / setup.sh     # Setup scripts
└── run.bat / run.sh         # Run scripts
```

## Quick Start

### Option 1: Windows
```bash
setup.bat
run.bat
```

### Option 2: Linux/Mac
```bash
chmod +x setup.sh && ./setup.sh
chmod +x run.sh && ./run.sh
```

### Option 3: Manual

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Access

- Frontend: http://localhost:8501
- Backend API: http://localhost:5000

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| POST /api/parse | Parse code |
| POST /api/visualize | Generate diagram |
| POST /api/metrics | Get code metrics |
| POST /api/dependencies | Get imports |
| POST /api/flowchart | Generate flowchart |
| POST /api/generate | AI diagram from text |
| GET /api/languages | List languages |
| GET /api/health | Health check |

## License

MIT
