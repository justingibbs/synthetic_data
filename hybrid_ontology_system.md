"""
Hybrid Ontology System: Combines predefined core ontology with dynamic discovery
"""

import json
from typing import Dict, List, Set, Tuple, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import networkx as nx
from enum import Enum
import re
from datetime import datetime

class OntologyMode(Enum):
    STRICT = "strict"          # Only predefined types allowed
    GUIDED = "guided"          # Predefined + supervised discovery
    DISCOVERY = "discovery"    # Full dynamic discovery
    HYBRID = "hybrid"         # Predefined core + automatic extension

@dataclass
class OntologyEntity:
    """Represents an entity type in the ontology"""
    name: str
    parent_type: Optional[str] = None
    required_attributes: Set[str] = field(default_factory=set)
    optional_attributes: Set[str] = field(default_factory=set)
    constraints: Dict[str, Any] = field(default_factory=dict)
    discovered: bool = False
    confidence: float = 1.0
    example_instances: List[str] = field(default_factory=list)
    discovery_patterns: List[str] = field(default_factory=list)

@dataclass
class OntologyRelationship:
    """Represents a relationship type in the ontology"""
    name: str
    valid_source_types: Set[str] = field(default_factory=set)
    valid_target_types: Set[str] = field(default_factory=set)
    cardinality: str = "many-to-many"  # one-to-one, one-to-many, many-to-many
    attributes: Set[str] = field(default_factory=set)
    discovered: bool = False
    confidence: float = 1.0
    example_instances: List[Tuple[str, str]] = field(default_factory=list)

class HybridOntologyBuilder:
    """Builds and manages a hybrid ontology that evolves during document generation"""
    
    def __init__(self, mode: OntologyMode = OntologyMode.HYBRID):
        self.mode = mode
        self.entity_types: Dict[str, OntologyEntity] = {}
        self.relationship_types: Dict[str, OntologyRelationship] = {}
        self.ontology_graph = nx.DiGraph()
        
        # Discovery tracking
        self.candidate_entities: Dict[str, Dict] = defaultdict(lambda: {
            'count': 0, 
            'contexts': [], 
            'attributes': defaultdict(int),
            'patterns': set()
        })
        self.candidate_relationships: Dict[str, Dict] = defaultdict(lambda: {
            'count': 0,
            'source_types': defaultdict(int),
            'target_types': defaultdict(int),
            'contexts': []
        })
        
        # Discovery thresholds
        self.entity_discovery_threshold = 3  # Min occurrences to promote to ontology
        self.relationship_discovery_threshold = 5
        self.attribute_discovery_threshold = 0.3  # Min % of instances having attribute
        
        # Initialize with core ontology
        self._initialize_core_ontology()
    
    def _initialize_core_ontology(self):
        """Initialize with predefined core entity and relationship types"""
        
        # Core entity types with hierarchy
        core_entities = {
            # Top-level abstract types
            'Entity': OntologyEntity(
                name='Entity',
                parent_type=None,
                required_attributes={'id', 'type'},
                optional_attributes={'created_date', 'modified_date'}
            ),
            
            # Organizational entities
            'OrganizationalUnit': OntologyEntity(
                name='OrganizationalUnit',
                parent_type='Entity',
                required_attributes={'name'},
                optional_attributes={'location', 'manager'}
            ),
            'Store': OntologyEntity(
                name='Store',
                parent_type='OrganizationalUnit',
                required_attributes={'store_id', 'region'},
                optional_attributes={'store_type', 'fuel_station', 'atm'},
                constraints={'store_id_pattern': r'ST\d{4}'}
            ),
            
            # Person entities
            'Person': OntologyEntity(
                name='Person',
                parent_type='Entity',
                required_attributes={'name'},
                optional_attributes={'email', 'phone'}
            ),
            'Employee': OntologyEntity(
                name='Employee',
                parent_type='Person',
                required_attributes={'employee_id', 'role'},
                optional_attributes={'department', 'hire_date', 'training_status'},
                constraints={'employee_id_pattern': r'EMP\d+'}
            ),
            'Customer': OntologyEntity(
                name='Customer',
                parent_type='Person',
                optional_attributes={'loyalty_number', 'registration_date'}
            ),
            
            # Event entities
            'Event': OntologyEntity(
                name='Event',
                parent_type='Entity',
                required_attributes={'date', 'description'},
                optional_attributes={'severity', 'status'}
            ),
            'SecurityIncident': OntologyEntity(
                name='SecurityIncident',
                parent_type='Event',
                required_attributes={'incident_id', 'incident_type'},
                optional_attributes={'financial_impact', 'affected_systems'},
                constraints={'incident_id_pattern': r'INC-\d{4}-\d{3}'}
            ),
            'ComplianceAudit': OntologyEntity(
                name='ComplianceAudit',
                parent_type='Event',
                required_attributes={'audit_id', 'audit_type', 'pass_rate'},
                optional_attributes={'findings', 'remediation_required'}
            ),
            
            # Document entities
            'Document': OntologyEntity(
                name='Document',
                parent_type='Entity',
                required_attributes={'document_id', 'document_type', 'created_date'},
                optional_attributes={'author', 'department', 'classification'}
            ),
            
            # System entities
            'System': OntologyEntity(
                name='System',
                parent_type='Entity',
                required_attributes={'system_name', 'system_type'},
                optional_attributes={'version', 'criticality', 'owner'}
            )
        }
        
        # Core relationship types
        core_relationships = {
            'AFFECTS': OntologyRelationship(
                name='AFFECTS',
                valid_source_types={'SecurityIncident', 'Event'},
                valid_target_types={'Store', 'System', 'Employee', 'Entity'},
                attributes={'impact_type', 'severity', 'duration'}
            ),
            'MANAGES': OntologyRelationship(
                name='MANAGES',
                valid_source_types={'Employee'},
                valid_target_types={'Store', 'OrganizationalUnit'},
                cardinality='one-to-many',
                attributes={'start_date', 'end_date'}
            ),
            'REPORTS_TO': OntologyRelationship(
                name='REPORTS_TO',
                valid_source_types={'Employee', 'Person'},
                valid_target_types={'Employee', 'Person'},
                cardinality='many-to-one',
                attributes={'reporting_type'}
            ),
            'DOCUMENTED_IN': OntologyRelationship(
                name='DOCUMENTED_IN',
                valid_source_types={'Entity'},
                valid_target_types={'Document'},
                attributes={'section', 'page', 'mention_type'}
            )
        }
        
        # Add to ontology
        for entity in core_entities.values():
            self.add_entity_type(entity)
        
        for relationship in core_relationships.values():
            self.add_relationship_type(relationship)
    
    def add_entity_type(self, entity: OntologyEntity):
        """Add an entity type to the ontology"""
        self.entity_types[entity.name] = entity
        self.ontology_graph.add_node(entity.name, type='entity', **entity.__dict__)
        
        if entity.parent_type:
            self.ontology_graph.add_edge(entity.parent_type, entity.name, type='subclass_of')
    
    def add_relationship_type(self, relationship: OntologyRelationship):
        """Add a relationship type to the ontology"""
        self.relationship_types[relationship.name] = relationship
        self.ontology_graph.add_node(
            relationship.name, 
            type='relationship',
            **relationship.__dict__
        )
    
    def discover_from_document(self, 
                              document: Dict,
                              generation_context: Dict) -> Dict[str, Any]:
        """
        Discover new ontology elements from generated documents
        """
        discoveries = {
            'new_entity_types': [],
            'new_relationship_types': [],
            'new_attributes': defaultdict(list),
            'pattern_updates': []
        }
        
        if self.mode in [OntologyMode.STRICT]:
            return discoveries  # No discovery in strict mode
        
        # Analyze document for patterns
        content = document.get('content', '')
        doc_type = document.get('type', '')
        
        # Discover potential new entity types
        if self.mode in [OntologyMode.DISCOVERY, OntologyMode.HYBRID]:
            new_entities = self._discover_entity_patterns(content, generation_context)
            discoveries['new_entity_types'] = new_entities
        
        # Discover potential new relationship types
        new_relationships = self._discover_relationship_patterns(content, generation_context)
        discoveries['new_relationship_types'] = new_relationships
        
        # Discover new attributes for existing types
        new_attrs = self._discover_attribute_patterns(content, generation_context)
        discoveries['new_attributes'] = new_attrs
        
        # Update pattern recognition
        pattern_updates = self._update_extraction_patterns(content, generation_context)
        discoveries['pattern_updates'] = pattern_updates
        
        # Promote candidates to ontology if threshold met
        self._promote_discovered_elements()
        
        return discoveries
    
    def _discover_entity_patterns(self, 
                                 content: str,
                                 context: Dict) -> List[OntologyEntity]:
        """Discover potential new entity types from content"""
        discovered = []
        
        # Pattern-based discovery
        patterns = [
            # Capitalized terms that appear multiple times
            (r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b', 'named_entity'),
            # Terms with ID patterns
            (r'(\w+)[-_]ID[-_:]?\s*([A-Z0-9]+)', 'identifier'),
            # Terms described as types
            (r'type(?:s)?\s+of\s+(\w+)', 'type_reference'),
            # New document types mentioned
            (r'(\w+)\s+(?:report|document|form|audit|assessment)', 'document_type')
        ]
        
        for pattern, pattern_type in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                candidate = match.group(1)
                
                # Skip if already in ontology
                if candidate in self.entity_types:
                    continue
                
                # Track candidate
                self.candidate_entities[candidate]['count'] += 1
                self.candidate_entities[candidate]['contexts'].append({
                    'text': content[max(0, match.start()-50):min(len(content), match.end()+50)],
                    'pattern_type': pattern_type,
                    'document': context.get('document_id', 'unknown')
                })
                self.candidate_entities[candidate]['patterns'].add(pattern_type)
        
        # Analyze generation context for structured entities
        if 'entities_generated' in context:
            for entity_data in context['entities_generated']:
                entity_type = entity_data.get('type')
                if entity_type and entity_type not in self.entity_types:
                    # This is a new type used in generation
                    attributes = set(entity_data.keys()) - {'type', 'id'}
                    
                    new_entity = OntologyEntity(
                        name=entity_type,
                        parent_type=self._infer_parent_type(entity_type, entity_data),
                        optional_attributes=attributes,
                        discovered=True,
                        confidence=0.8,
                        example_instances=[entity_data.get('id', '')]
                    )
                    discovered.append(new_entity)
        
        return discovered
    
    def _discover_relationship_patterns(self,
                                       content: str,
                                       context: Dict) -> List[OntologyRelationship]:
        """Discover potential new relationship types"""
        discovered = []
        
        # Verb-based patterns for relationships
        patterns = [
            # Entity VERB Entity patterns
            (r'(\w+)\s+(manages?|oversees?|controls?|owns?)\s+(\w+)', 'management'),
            (r'(\w+)\s+(triggers?|causes?|leads?\s+to|results?\s+in)\s+(\w+)', 'causation'),
            (r'(\w+)\s+(includes?|contains?|comprises?)\s+(\w+)', 'composition'),
            (r'(\w+)\s+(requires?|depends?\s+on|needs?)\s+(\w+)', 'dependency'),
            (r'(\w+)\s+(violates?|breaches?|fails?)\s+(\w+)', 'violation'),
            (r'(\w+)\s+(approves?|authorizes?|signs?\s+off)\s+(\w+)', 'approval')
        ]
        
        for pattern, rel_category in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                source = match.group(1)
                verb = match.group(2).upper().replace(' ', '_')
                target = match.group(3)
                
                # Skip if already exists
                if verb in self.relationship_types:
                    continue
                
                # Track candidate
                self.candidate_relationships[verb]['count'] += 1
                self.candidate_relationships[verb]['source_types'][source] += 1
                self.candidate_relationships[verb]['target_types'][target] += 1
                self.candidate_relationships[verb]['contexts'].append({
                    'text': match.group(0),
                    'category': rel_category,
                    'document': context.get('document_id', 'unknown')
                })
        
        return discovered
    
    def _discover_attribute_patterns(self,
                                    content: str,
                                    context: Dict) -> Dict[str, List[str]]:
        """Discover new attributes for existing entity types"""
        new_attributes = defaultdict(list)
        
        # Look for attribute patterns
        patterns = [
            # "Store's new_attribute"
            (r"(\w+)'s\s+(\w+(?:\s+\w+)?)", 'possessive'),
            # "new_attribute of Store"
            (r"(\w+(?:\s+\w+)?)\s+of\s+(?:the\s+)?(\w+)", 'of_pattern'),
            # "Store has new_attribute"
            (r"(\w+)\s+has\s+(?:a\s+)?(\w+(?:\s+\w+)?)", 'has_pattern')
        ]
        
        for pattern, pattern_type in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                entity_type = match.group(1) if pattern_type != 'of_pattern' else match.group(2)
                attribute = match.group(2) if pattern_type != 'of_pattern' else match.group(1)
                
                # Check if entity type exists
                if entity_type in self.entity_types:
                    existing_attrs = (self.entity_types[entity_type].required_attributes |
                                    self.entity_types[entity_type].optional_attributes)
                    
                    if attribute.lower() not in {a.lower() for a in existing_attrs}:
                        new_attributes[entity_type].append(attribute)
        
        return new_attributes
    
    def _update_extraction_patterns(self,
                                   content: str,
                                   context: Dict) -> List[Dict]:
        """Update extraction patterns based on observed instances"""
        updates = []
        
        # Look for ID patterns
        id_patterns = re.findall(r'\b([A-Z]{2,4}[-_]?\d{2,6})\b', content)
        for pattern in id_patterns:
            # Try to match to entity type
            for entity_type, entity in self.entity_types.items():
                if 'id' in entity.required_attributes or 'id' in entity.optional_attributes:
                    # Check if this could be an ID for this entity type
                    if self._could_be_entity_id(pattern, entity_type, context):
                        if pattern not in entity.discovery_patterns:
                            entity.discovery_patterns.append(pattern)
                            updates.append({
                                'entity_type': entity_type,
                                'new_pattern': pattern,
                                'pattern_type': 'identifier'
                            })
        
        return updates
    
    def _could_be_entity_id(self, pattern: str, entity_type: str, context: Dict) -> bool:
        """Heuristic to determine if a pattern could be an ID for an entity type"""
        # Simple heuristic based on pattern structure and context
        type_prefixes = {
            'Store': ['ST', 'STR', 'LOC'],
            'Employee': ['EMP', 'USR', 'STAFF'],
            'SecurityIncident': ['INC', 'SEC', 'EVT'],
            'ComplianceAudit': ['AUD', 'COMP', 'PCI'],
            'Vendor': ['VND', 'SUPP', 'VENDOR']
        }
        
        prefix = re.match(r'([A-Z]+)', pattern).group(1) if re.match(r'([A-Z]+)', pattern) else ''
        return prefix in type_prefixes.get(entity_type, [])
    
    def _infer_parent_type(self, entity_type: str, entity_data: Dict) -> str:
        """Infer the parent type for a discovered entity"""
        # Simple heuristics
        if 'date' in entity_data or 'time' in entity_data:
            return 'Event'
        elif 'name' in entity_data and 'email' in entity_data:
            return 'Person'
        elif 'document' in entity_type.lower() or 'report' in entity_type.lower():
            return 'Document'
        elif 'system' in entity_type.lower() or 'application' in entity_type.lower():
            return 'System'
        else:
            return 'Entity'
    
    def _promote_discovered_elements(self):
        """Promote frequently seen candidates to the ontology"""
        # Promote entity types
        for candidate, data in self.candidate_entities.items():
            if data['count'] >= self.entity_discovery_threshold:
                # Create new entity type
                new_entity = OntologyEntity(
                    name=candidate,
                    parent_type='Entity',  # Default parent
                    optional_attributes=set(data['attributes'].keys()),
                    discovered=True,
                    confidence=min(1.0, data['count'] / 10),  # Confidence based on frequency
                    discovery_patterns=list(data['patterns'])
                )
                
                if self.mode == OntologyMode.GUIDED:
                    # In guided mode, ask for confirmation
                    print(f"Discovered entity type: {candidate}")
                    print(f"  Occurrences: {data['count']}")
                    print(f"  Patterns: {data['patterns']}")
                    print(f"  Example: {data['contexts'][0]['text'] if data['contexts'] else 'N/A'}")
                    # Would need user confirmation here
                else:
                    # Auto-add in hybrid/discovery mode
                    self.add_entity_type(new_entity)
                    print(f"Auto-added entity type: {candidate}")
        
        # Promote relationship types
        for candidate, data in self.candidate_relationships.items():
            if data['count'] >= self.relationship_discovery_threshold:
                # Determine valid source/target types
                top_sources = set(sorted(data['source_types'].keys(), 
                                        key=lambda x: data['source_types'][x], 
                                        reverse=True)[:3])
                top_targets = set(sorted(data['target_types'].keys(),
                                        key=lambda x: data['target_types'][x],
                                        reverse=True)[:3])
                
                new_relationship = OntologyRelationship(
                    name=candidate,
                    valid_source_types=top_sources,
                    valid_target_types=top_targets,
                    discovered=True,
                    confidence=min(1.0, data['count'] / 10)
                )
                
                if self.mode == OntologyMode.GUIDED:
                    print(f"Discovered relationship: {candidate}")
                    print(f"  Occurrences: {data['count']}")
                    print(f"  Sources: {top_sources}")
                    print(f"  Targets: {top_targets}")
                else:
                    self.add_relationship_type(new_relationship)
                    print(f"Auto-added relationship type: {candidate}")
    
    def export_ontology(self, format: str = 'json') -> Any:
        """Export the complete ontology"""
        if format == 'json':
            return {
                'metadata': {
                    'mode': self.mode.value,
                    'created_at': datetime.now().isoformat(),
                    'statistics': {
                        'total_entity_types': len(self.entity_types),
                        'discovered_entity_types': sum(1 for e in self.entity_types.values() if e.discovered),
                        'total_relationship_types': len(self.relationship_types),
                        'discovered_relationship_types': sum(1 for r in self.relationship_types.values() if r.discovered)
                    }
                },
                'entity_types': {
                    name: {
                        'parent': entity.parent_type,
                        'required_attributes': list(entity.required_attributes),
                        'optional_attributes': list(entity.optional_attributes),
                        'constraints': entity.constraints,
                        'discovered': entity.discovered,
                        'confidence': entity.confidence,
                        'patterns': entity.discovery_patterns
                    }
                    for name, entity in self.entity_types.items()
                },
                'relationship_types': {
                    name: {
                        'valid_sources': list(rel.valid_source_types),
                        'valid_targets': list(rel.valid_target_types),
                        'cardinality': rel.cardinality,
                        'attributes': list(rel.attributes),
                        'discovered': rel.discovered,
                        'confidence': rel.confidence
                    }
                    for name, rel in self.relationship_types.items()
                },
                'hierarchy': self._export_hierarchy()
            }
        elif format == 'owl':
            return self._export_as_owl()
        elif format == 'protege':
            return self._export_for_protege()
    
    def _export_hierarchy(self) -> Dict:
        """Export entity type hierarchy"""
        hierarchy = {}
        
        def build_subtree(node):
            children = [n for n in self.ontology_graph.successors(node) 
                       if self.ontology_graph.nodes[n].get('type') == 'entity']
            if children:
                return {child: build_subtree(child) for child in children}
            return {}
        
        # Find root nodes (no parents)
        roots = [n for n in self.entity_types.keys() 
                if not self.entity_types[n].parent_type]
        
        for root in roots:
            hierarchy[root] = build_subtree(root)
        
        return hierarchy
    
    def _export_as_owl(self) -> str:
        """Export ontology in OWL format"""
        owl = """<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:quickstop="http://example.org/quickstop/ontology#">

    <owl:Ontology rdf:about="http://example.org/quickstop/ontology">
        <rdfs:label>QuickStop Knowledge Graph Ontology</rdfs:label>
    </owl:Ontology>
"""
        
        # Add entity classes
        for name, entity in self.entity_types.items():
            owl += f"""
    <owl:Class rdf:about="http://example.org/quickstop/ontology#{name}">
        <rdfs:label>{name}</rdfs:label>"""
            
            if entity.parent_type:
                owl += f"""
        <rdfs:subClassOf rdf:resource="http://example.org/quickstop/ontology#{entity.parent_type}"/>"""
            
            owl += """
    </owl:Class>
"""
        
        # Add relationship properties
        for name, rel in self.relationship_types.items():
            owl += f"""
    <owl:ObjectProperty rdf:about="http://example.org/quickstop/ontology#{name}">
        <rdfs:label>{name}</rdfs:label>"""
            
            for source in rel.valid_source_types:
                owl += f"""
        <rdfs:domain rdf:resource="http://example.org/quickstop/ontology#{source}"/>"""
            
            for target in rel.valid_target_types:
                owl += f"""
        <rdfs:range rdf:resource="http://example.org/quickstop/ontology#{target}"/>"""
            
            owl += """
    </owl:ObjectProperty>
"""
        
        owl += """
</rdf:RDF>"""
        
        return owl
    
    def validate_extraction(self, 
                           extracted_entities: List[Dict],
                           extracted_relationships: List[Dict]) -> Dict[str, Any]:
        """Validate extracted entities and relationships against ontology"""
        validation_results = {
            'valid_entities': [],
            'invalid_entities': [],
            'valid_relationships': [],
            'invalid_relationships': [],
            'warnings': []
        }
        
        # Validate entities
        for entity in extracted_entities:
            entity_type = entity.get('type')
            if entity_type not in self.entity_types:
                validation_results['invalid_entities'].append({
                    'entity': entity,
                    'reason': f"Unknown entity type: {entity_type}"
                })
            else:
                # Check required attributes
                required = self.entity_types[entity_type].required_attributes
                missing = required - set(entity.get('attributes', {}).keys())
                
                if missing:
                    validation_results['warnings'].append({
                        'entity': entity,
                        'warning': f"Missing required attributes: {missing}"
                    })
                else:
                    validation_results['valid_entities'].append(entity)
        
        # Validate relationships
        for rel in extracted_relationships:
            rel_type = rel.get('type')
            if rel_type not in self.relationship_types:
                validation_results['invalid_relationships'].append({
                    'relationship': rel,
                    'reason': f"Unknown relationship type: {rel_type}"
                })
            else:
                # Check source/target validity
                rel_def = self.relationship_types[rel_type]
                source_type = self._get_entity_type(rel.get('source'), extracted_entities)
                target_type = self._get_entity_type(rel.get('target'), extracted_entities)
                
                if source_type not in rel_def.valid_source_types:
                    validation_results['warnings'].append({
                        'relationship': rel,
                        'warning': f"Source type {source_type} not valid for {rel_type}"
                    })
                elif target_type not in rel_def.valid_target_types:
                    validation_results['warnings'].append({
                        'relationship': rel,
                        'warning': f"Target type {target_type} not valid for {rel_type}"
                    })
                else:
                    validation_results['valid_relationships'].append(rel)
        
        return validation_results
    
    def _get_entity_type(self, entity_id: str, entities: List[Dict]) -> Optional[str]:
        """Get entity type for an entity ID"""
        for entity in entities:
            if entity.get('id') == entity_id:
                return entity.get('type')
        return None
    
    def generate_extraction_rules(self) -> Dict[str, Any]:
        """Generate extraction rules based on the ontology"""
        rules = {
            'entity_extraction_rules': {},
            'relationship_extraction_rules': {},
            'attribute_extraction_rules': {}
        }
        
        # Generate entity extraction rules
        for name, entity in self.entity_types.items():
            rules['entity_extraction_rules'][name] = {
                'patterns': entity.discovery_patterns,
                'required_context': list(entity.required_attributes),
                'optional_context': list(entity.optional_attributes),
                'constraints': entity.constraints,
                'parent_type': entity.parent_type
            }
        
        # Generate relationship extraction rules
        for name, rel in self.relationship_types.items():
            rules['relationship_extraction_rules'][name] = {
                'valid_sources': list(rel.valid_source_types),
                'valid_targets': list(rel.valid_target_types),
                'cardinality': rel.cardinality,
                'attributes': list(rel.attributes)
            }
        
        return rules


# Integration with main document generator
class OntologyAwareDocumentGenerator:
    """Document generator that builds ontology during generation"""
    
    def __init__(self, config_path: str, api_key: str, ontology_mode: OntologyMode = OntologyMode.HYBRID):
        self.config = self._load_config(config_path)
        self.ontology_builder = HybridOntologyBuilder(mode=ontology_mode)
        self.kg_extractor = None  # Will be initialized with discovered ontology
        # ... rest of initialization
    
    async def generate_document_with_ontology_discovery(self, doc_config: Dict) -> Dict:
        """Generate document and discover ontology patterns"""
        
        # Generate document
        document_content = await self._generate_with_llm(doc_config)
        
        # Discover ontology elements from this document
        discoveries = self.ontology_builder.discover_from_document(
            {'content': document_content, 'type': doc_config['type']},
            self.generation_context
        )
        
        # Log discoveries
        if discoveries['new_entity_types']:
            print(f"Discovered {len(discoveries['new_entity_types'])} potential new entity types")
        if discoveries['new_relationship_types']:
            print(f"Discovered {len(discoveries['new_relationship_types'])} potential new relationship types")
        
        # Extract KG using current ontology
        if not self.kg_extractor:
            # Initialize KG extractor with discovered ontology
            self.kg_extractor = self._create_kg_extractor_from_ontology()
        
        kg_data = self.kg_extractor.extract_from_generation(
            document_content,
            doc_config,
            self.generation_context
        )
        
        return {
            'document': document_content,
            'kg_extraction': kg_data,
            'ontology_discoveries': discoveries
        }
    
    def _create_kg_extractor_from_ontology(self):
        """Create KG extractor using discovered ontology"""
        # Convert ontology to KG schema format
        schema = {
            'entity_types': [
                {
                    'type': name,
                    'attributes': entity.__dict__
                }
                for name, entity in self.ontology_builder.entity_types.items()
            ],
            'relationship_types': [
                {
                    'type': name,
                    'source': list(rel.valid_source_types),
                    'target': list(rel.valid_target_types),
                    'attributes': rel.__dict__
                }
                for name, rel in self.ontology_builder.relationship_types.items()
            ]
        }
        
        # Create KG extractor with dynamic schema
        return KnowledgeGraphExtractor(schema)
    
    def export_final_ontology(self):
        """Export the complete discovered ontology"""
        return self.ontology_builder.export_ontology(format='json')
