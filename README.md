# Synthetic Benchmark Data Generator for Convenience Store Chain

A sophisticated Python-based system for generating realistic corporate documents, extracting knowledge graphs, and creating comprehensive benchmarks to evaluate Retrieval-Augmented Generation (RAG) and Knowledge Graph construction systems. This project creates a complete document corpus for a fictional national convenience store chain, with special emphasis on cybersecurity documentation and incidents.

## 🎯 Project Overview

This tool generates synthetic but realistic corporate documents including financial reports, security audits, emails, and operational data, then creates multiple types of benchmarks:
- **Question-Answer pairs** for testing retrieval and comprehension
- **Entity and relationship extraction** ground truth for knowledge graph construction
- **Ontology discovery** patterns for schema learning systems

The methodology is based on [Chroma's Generative Benchmarking research](https://research.trychroma.com/generative-benchmarking) and extends it with knowledge graph capabilities.

### Key Features

- **Diverse Document Generation**: Creates 50-100 documents across multiple categories and formats
- **Cybersecurity Focus**: Includes PCI compliance audits, incident reports, security policies
- **Relationship Tracking**: Documents reference each other realistically
- **Benchmark Creation**: Generates 200-500 Q&A pairs of varying complexity
- **Knowledge Graph Extraction**: Creates ground truth entity and relationship data
- **Hybrid Ontology System**: Combines predefined schema with dynamic discovery
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
│   ├── scenarios.json              # Pre-defined incident scenarios
│   └── kg_schema.json              # Knowledge graph ontology
├── src/
│   ├── generator.py               # Main document generator
│   ├── document_builder.py        # Document construction logic
│   ├── llm_client.py             # LLM interaction wrapper
│   ├── knowledge_graph_extractor.py # KG extraction and management
│   ├── hybrid_ontology_system.py  # Dynamic ontology discovery
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
│   ├── benchmarks/               # Generated Q&A pairs
│   ├── knowledge_graphs/         # Extracted KG data
│   └── ontology/                 # Discovered ontology exports
├── tests/
│   ├── test_generator.py
│   ├── test_validators.py
│   ├── test_benchmarks.py
│   └── test_kg_extraction.py
├── CLAUDE.md                     # Prompts for working with Claude
├── README.md                     # This file
├── documents_templates.json      # Document configuration
├── generator.py                  # Main orchestrator
├── hybrid_ontology_system.md     # Ontology system documentation
├── knowledge_graph_extractor.json # KG schema configuration
├── requirements.txt
└── main.py                       # Entry point
```

## ⚙️ Configuration

### Document Templates Configuration

The `documents_templates.json` file defines your document universe:

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

### Knowledge Graph Schema Configuration

The `knowledge_graph_extractor.json` file defines entity and relationship types:

```json
{
  "knowledge_graph_schema": {
    "entity_types": [
      {
        "type": "Store",
        "attributes": {
          "store_id": "string",
          "region": "string",
          "compliance_status": "enum"
        }
      }
    ],
    "relationship_types": [
      {
        "type": "AFFECTS",
        "source": "SecurityIncident",
        "target": ["Store", "System"],
        "attributes": { ... }
      }
    ]
  }
}
```

### Ontology Configuration

Configure the hybrid ontology system:

```json
{
  "ontology_config": {
    "mode": "hybrid",  // strict, guided, discovery, hybrid
    "discovery_thresholds": {
      "entity_promotion": 3,
      "relationship_promotion": 5,
      "attribute_promotion": 0.3
    },
    "core_ontology": "config/core_ontology.json",
    "discovery_rules": {
      "allow_new_entities": true,
      "allow_new_relationships": true,
      "require_validation": false,
      "confidence_threshold": 0.7
    }
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
# Full pipeline with KG extraction
python main.py run-all --config config/document_templates.json --extract-kg --ontology-mode hybrid

# Generate only specific document types
python main.py generate-documents --types financial,cybersecurity

# Generate documents for specific time period
python main.py generate-documents --start-date 2024-01-01 --end-date 2024-06-30

# Extract knowledge graph from existing documents
python main.py extract-kg --source output/documents/ --ontology-mode discovery

# Create benchmarks with specific difficulty
python main.py generate-benchmarks --difficulty hard --count 100

# Generate KG extraction benchmarks
python main.py generate-kg-benchmarks --source output/knowledge_graphs/

# Validate document consistency
python main.py validate --check temporal,financial,references

# Export relationship graph
python main.py export-relationships --format graphml

# Export discovered ontology
python main.py export-ontology --format owl --output ontology.owl
```

### Python API

```python
from src.generator import DocumentGenerator
from src.benchmark_creator import BenchmarkCreator
from src.knowledge_graph_extractor import KnowledgeGraphExtractor
from src.hybrid_ontology_system import HybridOntologyBuilder, OntologyMode

# Initialize generator with KG extraction
generator = DocumentGenerator(
    config_path="config/document_templates.json",
    api_key="your-anthropic-key"
)

# Initialize ontology builder
ontology = HybridOntologyBuilder(mode=OntologyMode.HYBRID)

# Initialize KG extractor
kg_extractor = KnowledgeGraphExtractor("config/kg_schema.json")

# Generate documents with KG extraction
async def generate_with_kg():
    doc = await generator.generate_document(doc_config)
    
    # Extract KG during generation (ground truth)
    kg_data = kg_extractor.extract_from_generation(
        doc['content'],
        doc['metadata'],
        generator.context
    )
    
    # Discover ontology patterns
    discoveries = ontology.discover_from_document(doc, generator.context)
    
    return doc, kg_data, discoveries

# Create comprehensive benchmarks
benchmark_creator = BenchmarkCreator(generator.document_registry)
qa_benchmarks = benchmark_creator.generate_qa_benchmarks(count=500)
kg_benchmarks = kg_extractor.create_benchmark_dataset()

# Validate consistency
from src.validators import ConsistencyValidator
validator = ConsistencyValidator(generator.document_registry)
report = validator.validate_all()

# Export knowledge graph
kg_export = kg_extractor.export_graph(format='cypher')

# Export discovered ontology
ontology_export = ontology.export_ontology(format='owl')
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

### Question-Answer Benchmarks

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

### Knowledge Graph Benchmarks

1. **Entity Extraction**
   - Named entity recognition across document types
   - Entity attribute extraction
   - Entity type classification

2. **Relationship Extraction**
   - Binary relationship identification
   - Multi-way relationship detection
   - Temporal relationship tracking

3. **Entity Resolution**
   - Cross-document entity matching
   - Coreference resolution
   - Alias detection

4. **Ontology Learning**
   - Entity type discovery
   - Relationship type discovery
   - Hierarchy inference

5. **Graph Construction**
   - Complete KG assembly from document set
   - Temporal graph construction
   - Consistency validation

### Difficulty Levels

- **Easy**: Single document, explicit mentions, predefined types
- **Medium**: 2-3 documents, some inference required, discovered types
- **Hard**: 3+ documents, complex reasoning, temporal analysis, ambiguous references

## 🔧 Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_generator.py
pytest tests/test_kg_extraction.py

# Run with coverage
pytest --cov=src tests/
```

### Adding New Document Types

1. Define template in `documents_templates.json`
2. Create writer in `src/file_writers/`
3. Add validation rules in `src/validators/`
4. Define entity/relationship patterns in `knowledge_graph_extractor.json`
5. Update benchmark categories if needed

### Extending the Knowledge Graph System

```python
# Add custom entity type
ontology.add_entity_type(
    OntologyEntity(
        name='CustomEntity',
        parent_type='Entity',
        required_attributes={'custom_id'},
        optional_attributes={'custom_field'}
    )
)

# Add custom relationship
ontology.add_relationship_type(
    OntologyRelationship(
        name='CUSTOM_REL',
        valid_source_types={'CustomEntity'},
        valid_target_types={'Store'},
        attributes={'custom_attr'}
    )
)
```

### Ontology Modes

- **STRICT**: Only predefined types, no discovery
- **GUIDED**: Discoveries require manual approval
- **DISCOVERY**: Automatic discovery of all patterns
- **HYBRID**: Core types predefined, automatic extension

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
- **KG Extraction**: ~1-2 seconds per document
- **Ontology Discovery**: ~0.5 seconds per document
- **Benchmark Creation**: ~1 second per Q&A pair
- **Memory Usage**: ~2GB for 100 documents with full KG
- **API Costs**: Approximately $0.10-0.20 per document with Claude Opus

### Optimization Tips

- Use batch generation for similar documents
- Cache common context data and ontology
- Implement retry logic for API failures
- Use async generation for parallel processing
- Pre-compute entity resolution for large corpora
- Export KG incrementally for large datasets

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

## Benefits for RAG Testing:

1. **Comprehensive Evaluation**: Test both retrieval and knowledge extraction
2. **Graph-Enhanced Retrieval**: Evaluate systems using KG for retrieval
3. **Multi-hop Reasoning**: Validate traversal of relationship chains
4. **Entity-Centric QA**: Test questions about specific entities
5. **Temporal Queries**: Test understanding of entity evolution
6. **Schema Learning**: Evaluate ontology discovery capabilities

## 📚 Additional Resources

- [CLAUDE.md](CLAUDE.md) - Optimal prompts for working with Claude
- [Chroma's Generative Benchmarking](https://research.trychroma.com/generative-benchmarking)
- [PCI DSS Documentation](https://www.pcisecuritystandards.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Neo4j Graph Database](https://neo4j.com/) - For KG storage
- [OWL Ontology Language](https://www.w3.org/OWL/) - For ontology export

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
