# Synthetic Benchmark Data Generator for Convenience Store Chain

A sophisticated Python-based system for generating realistic corporate documents and benchmark questions to evaluate Retrieval-Augmented Generation (RAG) systems. This project creates a complete document corpus for a fictional national convenience store chain, with special emphasis on cybersecurity documentation and incidents.

## 🎯 Project Overview

This tool generates synthetic but realistic corporate documents including financial reports, security audits, emails, and operational data, then creates benchmark question-answer pairs to test information retrieval and question-answering systems. The methodology is based on [Chroma's Generative Benchmarking research](https://research.trychroma.com/generative-benchmarking).

### Key Features

- **Diverse Document Generation**: Creates 50-100 documents across multiple categories and formats
- **Cybersecurity Focus**: Includes PCI compliance audits, incident reports, security policies
- **Relationship Tracking**: Documents reference each other realistically
- **Benchmark Creation**: Generates 200-500 Q&A pairs of varying complexity
- **Consistency Engine**: Maintains coherent information across all documents
- **Multiple Formats**: Outputs PDF, Excel, CSV, JSON, and email formats

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Document Types](#document-types)
- [Benchmark Categories](#benchmark-categories)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Anthropic API key (for Claude)
- 8GB+ RAM recommended for large document generation

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/synthetic-benchmark-generator.git
cd synthetic-benchmark-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API key
export ANTHROPIC_API_KEY="your-api-key-here"  # On Windows: set ANTHROPIC_API_KEY=your-api-key-here
```

### Required Dependencies

```txt
anthropic>=0.18.0
pandas>=2.0.0
openpyxl>=3.1.0
reportlab>=4.0.0
python-pptx>=0.6.21
faker>=18.0.0
networkx>=3.0
matplotlib>=3.7.0
tqdm>=4.65.0
```

## ⚡ Quick Start

1. **Configure your document universe**:
```bash
cp config/document_templates.example.json config/document_templates.json
# Edit to customize company details and document types
```

2. **Generate documents**:
```bash
python main.py generate-documents --config config/document_templates.json
```

3. **Create benchmarks**:
```bash
python main.py generate-benchmarks --source output/documents/
```

4. **Validate consistency**:
```bash
python main.py validate --check-all
```

## 📁 Project Structure

```
synthetic-benchmark-generator/
├── config/
│   ├── document_templates.json    # Document type definitions
│   ├── company_profile.json       # Company structure & metadata
│   └── scenarios.json              # Pre-defined incident scenarios
├── src/
│   ├── generator.py               # Main document generator
│   ├── document_builder.py        # Document construction logic
│   ├── llm_client.py             # LLM interaction wrapper
│   ├── file_writers/
│   │   ├── __init__.py
│   │   ├── pdf_writer.py         # PDF generation
│   │   ├── excel_writer.py       # Excel file creation
│   │   ├── email_writer.py       # Email format handler
│   │   └── powerpoint_writer.py  # PPT generation
│   ├── validators/
│   │   ├── consistency.py        # Cross-document validation
│   │   ├── temporal.py           # Timeline validation
│   │   └── financial.py          # Financial data validation
│   └── benchmark_creator.py      # Q&A pair generation
├── templates/
│   ├── prompts/                  # LLM prompt templates
│   └── document_layouts/          # Format templates
├── output/
│   ├── documents/                # Generated documents
│   │   ├── financial/
│   │   ├── cybersecurity/
│   │   ├── operations/
│   │   ├── communications/
│   │   └── initiatives/
│   └── benchmarks/               # Generated Q&A pairs
├── tests/
│   ├── test_generator.py
│   ├── test_validators.py
│   └── test_benchmarks.py
├── CLAUDE.md                     # Prompts for working with Claude
├── README.md                     # This file
├── requirements.txt
└── main.py                       # Entry point
```

## ⚙️ Configuration

### Document Templates Configuration

The `config/document_templates.json` file defines your document universe:

```json
{
  "document_universe": {
    "metadata": {
      "company_name": "QuickStop Chain",
      "total_stores": 850,
      "regions": ["Northeast", "Southeast", "Midwest", "Southwest", "West"]
    },
    "document_types": [
      {
        "id": "pci_compliance_audit",
        "category": "cybersecurity",
        "format": "pdf",
        "frequency": "quarterly",
        "quantity": 8,
        "template": { ... }
      }
    ]
  }
}
```

### Company Profile Configuration

Define your company structure in `config/company_profile.json`:

```json
{
  "company": {
    "name": "QuickStop Chain",
    "headquarters": "Atlanta, GA",
    "stores": [ ... ],
    "employees": [ ... ],
    "executives": [ ... ]
  }
}
```

### Scenario Configuration

Pre-define incidents and events in `config/scenarios.json`:

```json
{
  "security_incidents": [
    {
      "id": "INC-2024-001",
      "type": "ransomware",
      "date": "2024-03-15",
      "impact": "critical"
    }
  ]
}
```

## 💻 Usage

### Command Line Interface

```bash
# Full pipeline
python main.py run-all --config config/document_templates.json

# Generate only specific document types
python main.py generate-documents --types financial,cybersecurity

# Generate documents for specific time period
python main.py generate-documents --start-date 2024-01-01 --end-date 2024-06-30

# Create benchmarks with specific difficulty
python main.py generate-benchmarks --difficulty hard --count 100

# Validate document consistency
python main.py validate --check temporal,financial,references

# Export relationship graph
python main.py export-relationships --format graphml
```

### Python API

```python
from src.generator import DocumentGenerator
from src.benchmark_creator import BenchmarkCreator

# Initialize generator
generator = DocumentGenerator(
    config_path="config/document_templates.json",
    api_key="your-anthropic-key"
)

# Generate documents
await generator.generate_all_documents()

# Create benchmarks
benchmark_creator = BenchmarkCreator(generator.document_registry)
benchmarks = benchmark_creator.generate_benchmarks(count=500)

# Validate consistency
from src.validators import ConsistencyValidator
validator = ConsistencyValidator(generator.document_registry)
report = validator.validate_all()
```

## 📄 Document Types

### Financial Documents
- Quarterly/Annual Financial Reports
- P&L Statements by Store/Region
- Budget Forecasts
- Capital Expenditure Reports
- Security Investment Analysis

### Cybersecurity Documents
- PCI DSS Compliance Audits
- Security Incident Reports
- Penetration Testing Results
- Security Awareness Training Reports
- Incident Response Playbooks
- Vendor Security Assessments
- Security KPI Dashboards

### Operational Documents
- Store Inventory Reports
- Sales Analytics
- Staff Scheduling
- Vendor Orders
- Equipment Maintenance Logs

### Communications
- Internal Emails
- Executive Memos
- Security Alerts
- Policy Updates
- Training Announcements

### Strategic Initiatives
- Digital Transformation Plans
- Security Enhancement Proposals
- Market Expansion Strategies
- Technology Upgrade Roadmaps

## 🎯 Benchmark Categories

### Question Types

1. **Factual Retrieval** (30%)
   - Single-fact lookups
   - Specific data points
   - Policy details

2. **Multi-hop Reasoning** (25%)
   - Cross-document information synthesis
   - Cause-and-effect analysis
   - Temporal relationships

3. **Aggregation** (20%)
   - Summation across documents
   - Statistical analysis
   - Trend identification

4. **Comparison** (15%)
   - Regional comparisons
   - Time period analysis
   - Performance benchmarking

5. **Compliance Verification** (10%)
   - Policy adherence checking
   - Audit finding validation
   - Incident response evaluation

### Difficulty Levels

- **Easy**: Single document, direct fact retrieval
- **Medium**: 2-3 documents, simple reasoning
- **Hard**: 3+ documents, complex reasoning, temporal analysis

## 🔧 Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_generator.py

# Run with coverage
pytest --cov=src tests/
```

### Adding New Document Types

1. Define template in `config/document_templates.json`
2. Create writer in `src/file_writers/`
3. Add validation rules in `src/validators/`
4. Update benchmark categories if needed

### Extending the LLM Client

The project uses a wrapper around the Anthropic client for flexibility:

```python
# src/llm_client.py
class LLMClient:
    def generate_document(self, prompt: str, **kwargs) -> str:
        # Add your LLM provider here
        pass
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run code formatting
black src/
isort src/
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Performance Considerations

- **Document Generation**: ~2-5 seconds per document (depending on complexity)
- **Benchmark Creation**: ~1 second per Q&A pair
- **Memory Usage**: ~2GB for 100 documents
- **API Costs**: Approximately $0.10-0.20 per document with Claude Opus

### Optimization Tips

- Use batch generation for similar documents
- Cache common context data
- Implement retry logic for API failures
- Use async generation for parallel processing

## 🐛 Troubleshooting

### Common Issues

**Issue**: API rate limiting
```bash
# Solution: Implement exponential backoff
python main.py generate-documents --delay 2 --max-retries 5
```

**Issue**: Inconsistent document relationships
```bash
# Solution: Run validation and auto-fix
python main.py validate --auto-fix
```

**Issue**: Memory errors with large corpus
```bash
# Solution: Generate in batches
python main.py generate-documents --batch-size 10
```

## 📚 Additional Resources

- [CLAUDE.md](CLAUDE.md) - Optimal prompts for working with Claude
- [Chroma's Generative Benchmarking](https://research.trychroma.com/generative-benchmarking)
- [PCI DSS Documentation](https://www.pcisecuritystandards.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Anthropic for Claude API
- Chroma for the generative benchmarking methodology
- Contributors and testers

## 📧 Contact

For questions or support:
- Open an issue on GitHub
- Email: your-email@example.com
- Documentation: [Project Wiki](https://github.com/yourusername/synthetic-benchmark-generator/wiki)

---

**Note**: This is a synthetic data generation tool. All company names, incidents, and data mentioned are fictional and for testing purposes only.
