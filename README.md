# Advanced Multi-Language Code Visualizer & Debugger

A comprehensive web-based tool for visualizing, analyzing, and debugging code across multiple programming languages including Python, TypeScript, JavaScript, Java, C++, and C#.

## Features

### 🔍 Code Analysis
- **Abstract Syntax Tree (AST) Parsing** - Parse and visualize ASTs for 6+ languages
- **Symbol Extraction** - Extract classes, functions, interfaces, types, and more
- **Code Metrics** - Calculate complexity, lines of code, function counts, etc.
- **Dependency Analysis** - Visualize module and code dependencies

### 📊 Visualization
- **Tree View** - Hierarchical AST visualization
- **Graph View** - Node-based graph representation
- **Class Diagrams** - UML-like class structure visualization
- **Call Graphs** - Function call relationships
- **Flow Diagrams** - Control flow visualization

### 🐛 Debugging Features
- **Breakpoints** - Set, toggle, and manage breakpoints
- **Watch Expressions** - Monitor variable states
- **Call Stack** - View execution call stack
- **Execution Trace** - Track code execution flow
- **Symbol Table** - Browse all defined symbols

### 💻 Multi-Language Support
- Python
- TypeScript
- JavaScript
- Java (basic)
- C++ (basic)
- C# (basic)

## Project Structure

```
rcm/
├── backend/                 # Flask API server
│   ├── app.py             # Main application
│   ├── requirements.txt    # Python dependencies
│   ├── api/              # API endpoints
│   ├── ast_parsers/      # Language-specific AST parsers
│   ├── visualizers/      # Visualization engines
│   ├── debuggers/        # Debugging utilities
│   └── utils/            # Helper utilities
│
└── frontend/              # React TypeScript UI
    ├── src/
    │   ├── components/   # React components
    │   ├── services/     # API services
    │   ├── store/        # Zustand store
    │   ├── types/        # TypeScript types
    │   └── App.tsx       # Main app component
    ├── package.json
    └── vite.config.ts
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Flask server:**
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   The UI will be available at `http://localhost:5173`

4. **Build for production:**
   ```bash
   npm run build
   ```

## API Endpoints

### Parsing & Analysis
- `POST /api/parse` - Parse code and return AST
- `POST /api/visualize` - Visualize code structure
- `POST /api/metrics` - Get code metrics
- `POST /api/dependencies` - Get code dependencies

### Debugging
- `POST /api/breakpoint/add` - Add breakpoint
- `DELETE /api/breakpoint/remove/<id>` - Remove breakpoint
- `POST /api/breakpoint/toggle/<id>` - Toggle breakpoint
- `GET /api/breakpoints` - Get all breakpoints
- `POST /api/watch/add` - Add watch expression
- `DELETE /api/watch/remove/<name>` - Remove watch
- `GET /api/stack` - Get call stack
- `GET /api/trace` - Get execution trace
- `POST /api/trace/clear` - Clear trace

### Health & Info
- `GET /api/health` - Health check endpoint

## Usage Examples

### Parse Python Code
```bash
curl -X POST http://localhost:5000/api/parse \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def hello():\n    return \"world\""
  }'
```

### Visualize Code
```bash
curl -X POST http://localhost:5000/api/visualize \
  -H "Content-Type: application/json" \
  -d '{
    "language": "typescript",
    "code": "class MyClass { method() {} }",
    "format": "tree"
  }'
```

### Get Code Metrics
```bash
curl -X POST http://localhost:5000/api/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "language": "javascript",
    "code": "const x = 1; function test() { return x; }"
  }'
```

## Configuration

### Environment Variables
Backend: create a `.env` file in the root directory:

```env
FLASK_DEBUG=True
FLASK_PORT=5000
FLASK_ENV=development
ALLOWED_LANGUAGES=python,typescript,javascript,java,cpp,csharp
MAX_FILE_SIZE=52428800
```

Frontend (Vite): create `frontend/.env`:

```env
VITE_API_URL=/api
```

## Language Parsers

### Python Parser
- Uses Python's built-in `ast` module
- Supports async functions, decorators, type hints
- Extracts classes, functions, variables, imports

### TypeScript/JavaScript Parser
- Regex-based pattern matching
- Supports ES6+ features
- Detects classes, interfaces, types, enums
- Handles both `.ts` and `.js` files

### Java Parser (Basic)
- Pattern matching for class/method definitions
- Supports generics and annotations
- Extracts methods and properties

### C++ Parser (Basic)
- Regex-based pattern detection
- Finds class, struct, and function definitions
- Supports templates and namespaces

### C# Parser (Basic)
- Detects classes, methods, properties
- Supports async methods and attributes
- Handles namespaces and interfaces

## Performance Considerations

- **AST Parsing**: Optimized for files up to 100KB
- **Large Files**: Consider splitting very large files for analysis
- **Memory**: Uses streaming for visualization generation
- **Complexity Calculation**: O(n) traversal of AST nodes

## Troubleshooting

### Port Already in Use
```bash
# Change port in .env or use different port
FLASK_PORT=5001
```

### Module Not Found (Python)
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt --upgrade
```

### CORS Issues
The CORS is configured in the Flask app. Ensure the frontend API base (`VITE_API_URL`) points at the backend.

### Parse Errors
- Verify syntax of input code
- Check language selection matches code language
- Review error message in API response

## Development

### Adding New Language Support

1. Create parser in `backend/ast_parsers/` following `base_parser.py` interface
2. Register in API endpoints
3. Add language to frontend language selector
4. Update documentation

### Extending Visualizations

1. Create new visualizer class in `backend/visualizers/`
2. Add endpoint in `backend/api/routes.py`
3. Add UI component in `frontend/src/components/`

## Performance Optimization

- Implement code caching
- Add incremental parsing
- Use Web Workers for large file processing
- Implement virtual scrolling for large ASTs

## Future Enhancements

- [ ] Real-time code analysis
- [ ] Collaborative debugging
- [ ] Code search and navigation
- [ ] Performance profiling
- [ ] Code refactoring suggestions
- [ ] Plugin system for custom languages
- [ ] Export analysis reports
- [ ] Version control integration

## License

MIT License

## Support

For issues, questions, or suggestions, please open an issue in the project repository.

## Contributors

- Development Team
