"""
Document Generation Orchestrator
Processes JSON configuration to generate synthetic benchmark documents
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random
from dataclasses import dataclass
import anthropic
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class DocumentContext:
    """Maintains context across document generation for consistency"""
    company_name: str
    regions: List[str]
    stores: Dict[str, Any]
    employees: Dict[str, Any]
    incidents: List[Dict[str, Any]]
    generated_documents: List[Dict[str, Any]]
    
class DocumentGenerator:
    def __init__(self, config_path: str, api_key: str):
        """Initialize generator with configuration and API key."""
        self.config = self._load_config(config_path)
        self.client = anthropic.Anthropic(api_key=api_key)
        self.context = self._initialize_context()
        self.document_registry = {}  # Track all generated documents
        
    def _load_config(self, config_path: str) -> Dict:
        """Load JSON configuration file."""
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _initialize_context(self) -> DocumentContext:
        """Create initial context from configuration."""
        metadata = self.config['document_universe']['metadata']
        
        # Generate consistent store and employee data
        stores = self._generate_stores(metadata['total_stores'], metadata['regions'])
        employees = self._generate_employees(stores)
        incidents = self._generate_security_incidents(stores, metadata['date_range'])
        
        return DocumentContext(
            company_name=metadata['company_name'],
            regions=metadata['regions'],
            stores=stores,
            employees=employees,
            incidents=incidents,
            generated_documents=[]
        )
    
    def _generate_stores(self, count: int, regions: List[str]) -> Dict[str, Any]:
        """Generate consistent store metadata."""
        stores = {}
        for i in range(count):
            store_id = f"ST{1000 + i:04d}"
            stores[store_id] = {
                'id': store_id,
                'region': random.choice(regions),
                'manager': self._generate_person_name(),
                'address': self._generate_address(),
                'type': random.choice(['urban', 'highway', 'suburban']),
                'fuel_station': random.choice([True, False]),
                'atm': random.choice([True, False])
            }
        return stores
    
    def _generate_employees(self, stores: Dict) -> Dict[str, Any]:
        """Generate consistent employee data."""
        employees = {}
        roles = ['Store Manager', 'Assistant Manager', 'Cashier', 'Stock Clerk']
        
        for store_id, store in stores.items():
            for i in range(random.randint(8, 15)):
                emp_id = f"EMP{store_id[-4:]}{i:02d}"
                employees[emp_id] = {
                    'id': emp_id,
                    'name': self._generate_person_name(),
                    'store_id': store_id,
                    'role': random.choice(roles),
                    'email': f"{emp_id.lower()}@quickstop.com",
                    'training_status': random.choice(['completed', 'in_progress', 'overdue'])
                }
        return employees
    
    def _generate_security_incidents(self, stores: Dict, date_range: Dict) -> List[Dict]:
        """Pre-generate security incidents for consistency across documents."""
        incidents = [
            {
                'id': 'INC-2024-001',
                'type': 'ransomware',
                'date': '2024-03-15',
                'affected_stores': random.sample(list(stores.keys()), 5),
                'impact': 'critical',
                'ransom_demand': 250000,
                'paid': False,
                'downtime_hours': 72,
                'revenue_loss': 450000
            },
            {
                'id': 'INC-2024-002',
                'type': 'data_breach',
                'date': '2024-06-22',
                'affected_stores': random.sample(list(stores.keys()), 12),
                'impact': 'high',
                'records_affected': 15000,
                'notification_sent': True,
                'remediation_cost': 180000
            },
            {
                'id': 'INC-2024-003',
                'type': 'phishing',
                'date': '2024-09-10',
                'affected_employees': random.sample(list(stores.keys()), 3),
                'impact': 'medium',
                'credentials_compromised': 3,
                'training_mandated': True
            }
        ]
        return incidents
    
    def _generate_person_name(self) -> str:
        """Generate realistic person names."""
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'James', 'Lisa']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_address(self) -> str:
        """Generate realistic addresses."""
        streets = ['Main St', 'Oak Ave', 'Highway 101', 'Interstate 95', 'Market St']
        cities = ['Springfield', 'Riverside', 'Franklin', 'Clinton', 'Madison']
        states = ['CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH']
        return f"{random.randint(100, 9999)} {random.choice(streets)}, {random.choice(cities)}, {random.choice(states)}"
    
    async def generate_document(self, doc_config: Dict) -> Dict[str, Any]:
        """Generate a single document using LLM."""
        prompt = self._build_document_prompt(doc_config)
        
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            document_content = response.content[0].text
            
            # Register document for future reference
            doc_metadata = {
                'id': f"{doc_config['id']}_{len(self.document_registry) + 1:04d}",
                'type': doc_config['id'],
                'category': doc_config['category'],
                'format': doc_config['format'],
                'content': document_content,
                'generated_at': datetime.now().isoformat(),
                'relationships': doc_config['template'].get('relationships', [])
            }
            
            self.document_registry[doc_metadata['id']] = doc_metadata
            logger.info(f"Generated document: {doc_metadata['id']}")
            
            return doc_metadata
            
        except Exception as e:
            logger.error(f"Error generating document {doc_config['id']}: {e}")
            raise
    
    def _build_document_prompt(self, doc_config: Dict) -> str:
        """Build comprehensive prompt for document generation."""
        # Get related documents for consistency
        related_docs = self._get_related_documents(doc_config)
        
        prompt = f"""Generate a realistic {doc_config['id']} document for {self.context.company_name}, a national convenience store chain.

DOCUMENT SPECIFICATIONS:
- Type: {doc_config['id']}
- Category: {doc_config['category']}
- Format: {doc_config['format']}

GENERATION INSTRUCTIONS:
{doc_config['generation_instructions']}

REQUIRED SECTIONS:
{json.dumps(doc_config['template'].get('sections', []), indent=2)}

REQUIRED DATA POINTS:
{json.dumps(doc_config['template'].get('data_points', []), indent=2)}

CONTEXT INFORMATION:
- Company: {self.context.company_name}
- Regions: {', '.join(self.context.regions)}
- Sample Stores: {json.dumps(list(self.context.stores.values())[:5], indent=2)}

SECURITY INCIDENTS TO REFERENCE (if relevant):
{json.dumps(self.context.incidents, indent=2)}

RELATED DOCUMENTS TO MAINTAIN CONSISTENCY WITH:
{json.dumps(related_docs, indent=2)}

IMPORTANT GUIDELINES:
1. Use specific store IDs, employee names, and dates from the context
2. Include realistic technical details for cybersecurity documents
3. Ensure financial figures align with the scale of operations
4. Reference other documents/incidents where specified in relationships
5. Use appropriate professional language and formatting
6. Include some inconsistencies or issues that would appear in real documents
7. For security documents, include both successful and problematic findings

Generate the complete document content now:"""
        
        return prompt
    
    def _get_related_documents(self, doc_config: Dict) -> List[Dict]:
        """Get previously generated related documents for consistency."""
        related = []
        relationships = doc_config['template'].get('relationships', [])
        
        for relationship in relationships:
            # Parse relationship string (e.g., "references: store_inventory")
            parts = relationship.split(':')
            if len(parts) == 2:
                rel_type, target_doc = parts[0].strip(), parts[1].strip()
                
                # Find matching documents in registry
                for doc_id, doc in self.document_registry.items():
                    if target_doc in doc['type']:
                        related.append({
                            'relationship': rel_type,
                            'document_id': doc_id,
                            'summary': doc['content'][:500] + '...'  # First 500 chars
                        })
                        break
        
        return related[:5]  # Limit to 5 most relevant
    
    async def generate_all_documents(self):
        """Generate all documents defined in configuration."""
        document_types = self.config['document_universe']['document_types']
        total_documents = sum(doc['quantity'] for doc in document_types)
        
        logger.info(f"Starting generation of {total_documents} documents...")
        
        # Group documents by priority
        priority_groups = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        for doc_type in document_types:
            priority = doc_type.get('priority', 'medium')
            for i in range(doc_type['quantity']):
                priority_groups[priority].append(doc_type)
        
        # Generate documents in priority order
        for priority in ['critical', 'high', 'medium', 'low']:
            docs = priority_groups[priority]
            logger.info(f"Generating {len(docs)} {priority} priority documents...")
            
            # Use async generation for efficiency
            tasks = [self.generate_document(doc) for doc in docs]
            results = await asyncio.gather(*tasks)
            
            # Save documents to disk
            for doc_metadata in results:
                self._save_document(doc_metadata)
    
    def _save_document(self, doc_metadata: Dict):
        """Save document to appropriate format and location."""
        output_dir = Path(f"output/documents/{doc_metadata['category']}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        file_name = f"{doc_metadata['id']}.{doc_metadata['format']}"
        file_path = output_dir / file_name
        
        if doc_metadata['format'] == 'text':
            with open(file_path, 'w') as f:
                f.write(doc_metadata['content'])
        elif doc_metadata['format'] == 'json':
            with open(file_path, 'w') as f:
                json.dump(json.loads(doc_metadata['content']), f, indent=2)
        else:
            # For PDF, Excel, PowerPoint - would need specific libraries
            # For now, save as text with appropriate extension
            with open(file_path.with_suffix('.txt'), 'w') as f:
                f.write(doc_metadata['content'])
        
        logger.info(f"Saved: {file_path}")
    
    def generate_benchmarks(self):
        """Generate Q&A pairs from the document corpus."""
        logger.info("Generating benchmark questions...")
        
        benchmark_categories = self.config['document_universe']['benchmark_categories']
        all_benchmarks = []
        
        for category in benchmark_categories:
            logger.info(f"Generating {category['target_count']} {category['category']} questions...")
            
            benchmarks = self._generate_category_benchmarks(category)
            all_benchmarks.extend(benchmarks)
        
        # Save benchmarks
        output_path = Path("output/benchmarks/benchmark_qa.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump({
                'metadata': {
                    'total_questions': len(all_benchmarks),
                    'generation_date': datetime.now().isoformat(),
                    'document_count': len(self.document_registry)
                },
                'questions': all_benchmarks
            }, f, indent=2)
        
        logger.info(f"Generated {len(all_benchmarks)} benchmark questions")
    
    def _generate_category_benchmarks(self, category: Dict) -> List[Dict]:
        """Generate benchmarks for a specific category."""
        benchmarks = []
        
        # Select relevant documents for this category
        relevant_docs = self._select_documents_for_benchmarks(category)
        
        prompt = f"""Generate {category['target_count']} benchmark questions of type '{category['category']}' based on these documents:

CATEGORY DESCRIPTION:
{category['description']}

EXAMPLE QUESTIONS:
{json.dumps(category['examples'], indent=2)}

DOCUMENT SUMMARIES:
{json.dumps(relevant_docs, indent=2)}

Generate questions that:
1. Test specific facts from the documents
2. Require understanding of relationships between documents
3. Have clear, verifiable answers
4. Include the source document IDs in the answer

Format each question as JSON with fields:
- question: The question text
- answer: The correct answer
- source_documents: List of document IDs containing the answer
- difficulty: easy/medium/hard
- category: {category['category']}

Generate the questions now:"""
        
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            temperature=0.5,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response and structure benchmarks
        # (Would need proper JSON parsing here)
        
        return benchmarks
    
    def _select_documents_for_benchmarks(self, category: Dict) -> List[Dict]:
        """Select relevant documents for benchmark generation."""
        # Logic to select appropriate documents based on category
        # For now, return sample of documents
        sample_size = min(10, len(self.document_registry))
        sampled = random.sample(list(self.document_registry.values()), sample_size)
        
        return [{
            'id': doc['id'],
            'type': doc['type'],
            'summary': doc['content'][:300]
        } for doc in sampled]


async def main():
    """Main execution function."""
    # Load configuration
    config_path = "config/document_templates.json"
    api_key = "your-anthropic-api-key"
    
    # Initialize generator
    generator = DocumentGenerator(config_path, api_key)
    
    # Generate all documents
    await generator.generate_all_documents()
    
    # Generate benchmarks from documents
    generator.generate_benchmarks()
    
    logger.info("Generation complete!")


if __name__ == "__main__":
    asyncio.run(main())
