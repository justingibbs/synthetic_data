# CLAUDE.md - Working with Claude on the Synthetic Benchmark Generator

This document contains optimized prompts for working with Claude on various aspects of the Synthetic Benchmark Data Generator project. Copy and adapt these prompts based on your specific needs.

## Table of Contents
- [Document Generation Prompts](#document-generation-prompts)
- [Benchmark Question Generation](#benchmark-question-generation)
- [Code Development Assistance](#code-development-assistance)
- [Data Consistency and Validation](#data-consistency-and-validation)
- [Security Scenario Development](#security-scenario-development)

---

## Document Generation Prompts

### Generate a PCI Compliance Audit Report

```
You are generating a PCI DSS compliance audit report for QuickStop Chain, a national convenience store chain with 850 stores.

Context:
- Audit Period: Q3 2024 (July 1 - September 30)
- Stores Audited: 212 stores across Northeast and Southeast regions
- Previous Audit: Q2 2024 showed 87% compliance rate

Please generate a detailed PCI compliance audit report that includes:

1. Executive Summary
   - Overall compliance rate (make it 82%, showing slight decline)
   - Critical findings count
   - Immediate action items

2. Detailed Findings by Store
   - Include specific store IDs (ST1001-ST1212)
   - 15% of stores should have critical failures
   - Common issues: unpatched POS systems, weak password policies, unencrypted card data in logs
   - Include specific technical details (e.g., "Store ST1147 running POS software v3.2.1, missing critical security patch CVE-2024-1234")

3. Regional Analysis
   - Northeast: 78% compliance (down from 85%)
   - Southeast: 86% compliance (up from 84%)

4. Cost Impact
   - Remediation costs: $50-75K per critically failed store
   - Potential fines if not remediated: $25K per store per month

5. Remediation Timeline
   - Critical items: 30 days
   - High priority: 60 days
   - Medium priority: 90 days

Include specific technical violations, reference actual PCI DSS requirements (e.g., Requirement 2.3, 8.3.1), and make the language professional but accessible to non-technical executives.
```

### Generate Ransomware Incident Report

```
Create a detailed ransomware incident report for QuickStop Chain. This is a critical security incident that occurred on March 15, 2024.

Incident Details:
- Attack Vector: Phishing email opened by store manager at ST1455
- Ransomware Variant: LockBit 3.0 variant
- Initial Infection: March 15, 2024, 02:47 AM EST
- Discovery: March 15, 2024, 06:15 AM EST
- Affected Stores: ST1455, ST1456, ST1458, ST1461, ST1467 (all in Midwest region)

Timeline to Include:
- 02:47 AM - Initial infection via email attachment
- 03:15 AM - Lateral movement to shared regional server
- 04:30 AM - Encryption begins on POS systems
- 06:15 AM - Store ST1455 manager reports POS failure
- 06:45 AM - IT Security team alerted
- 07:00 AM - Incident response team activated
- 07:30 AM - Affected stores isolated from network
- 08:00 AM - Ransom note discovered: $250,000 in Bitcoin

Business Impact:
- 5 stores completely offline for 72 hours
- Revenue loss: ~$90,000 per store ($450,000 total)
- Customer transactions: ~8,500 affected customers
- Fuel pumps offline (where applicable)
- Refrigeration monitoring systems offline (potential inventory loss ~$35,000)

Response Actions:
- Network isolation completed
- Law enforcement (FBI) notified
- Cyber insurance carrier notified
- Decision made NOT to pay ransom
- Backup restoration initiated
- PR team prepared customer communications

Include technical indicators of compromise (IoCs), specific file hashes, C2 server IPs (use realistic but fake IPs like 185.236.XXX.XXX), and lessons learned.
```

### Generate Store Manager Security Email Thread

```
Generate a realistic email thread between store managers and IT security team about a suspicious incident. Make it feel authentic with typical email formatting, forwarding, and varying levels of technical understanding.

Thread Participants:
- Mike Johnson (Store Manager ST1234) - mike.johnson@quickstop.com
- Sarah Chen (Regional Manager) - sarah.chen@quickstop.com  
- David Kumar (IT Security) - david.kumar@quickstop.com
- Lisa Martinez (Store Manager ST1236) - lisa.martinez@quickstop.com

Scenario:
Mike noticed someone trying to install something on the external card reader at pump 3. He took a photo with his phone but isn't sure if it's serious.

Email 1 (Mike to Sarah):
- Subject: Strange guy at pump 3 this morning
- Casual tone, not sure if it's important
- Mentions customer seemed nervous when confronted
- Attached blurry phone photo

Email 2 (Sarah forwards to David):
- Adds urgency
- Asks if this could be a skimmer
- CC's Lisa since she's at nearby store

Email 3 (David replies all):
- Confirms it appears to be skimmer installation attempt
- Requests immediate inspection of all pumps
- Provides specific inspection instructions
- Escalates to security incident

Email 4 (Lisa chimes in):
- Reports she found something similar last week but thought it was maintenance
- Worried about customer data

Email 5 (David follows up):
- Incident response protocol activated
- Instructions for preserving evidence
- Mandatory inspection checklist
- Conference call scheduled

Include realistic typos, mobile phone signatures, different email client formatting, and varying levels of concern/understanding.
```

---

## Benchmark Question Generation

### Generate Multi-Hop Reasoning Questions

```
Based on these documents from QuickStop Chain's corpus, generate 25 complex multi-hop reasoning questions that require information from multiple documents to answer correctly.

Document Set Provided:
1. Ransomware Incident Report (March 2024)
2. Q1 2024 Financial Report
3. Q2 2024 Financial Report  
4. PCI Compliance Audit Q2 2024
5. Security Training Completion Report (January-June 2024)
6. Email threads about security incidents

For each question:
1. Require information from at least 2 documents
2. Include temporal reasoning where applicable
3. Provide the complete answer with source citations
4. Rate difficulty (medium/hard)
5. Specify the reasoning type (causal, temporal, aggregation, comparison)

Example Format:
{
  "question": "What was the total financial impact of security incidents in the Midwest region during Q1 2024, including both direct losses and remediation costs?",
  "answer": "$485,000 total ($450,000 revenue loss from ransomware + $35,000 inventory loss)",
  "source_documents": ["ransomware_incident_march2024.pdf", "q1_2024_financial.pdf"],
  "difficulty": "hard",
  "reasoning_type": "aggregation",
  "reasoning_steps": [
    "Identify ransomware incident in Midwest (March 2024)",
    "Find revenue loss figure in incident report",
    "Cross-reference with Q1 financial report",
    "Add remediation costs from financial report"
  ]
}

Focus on questions that would test a RAG system's ability to:
- Connect cause and effect across documents
- Track changes over time
- Aggregate data from multiple sources
- Identify contradictions or inconsistencies
- Understand document relationships
```

### Generate Security Policy Compliance Questions

```
Create 30 questions that test understanding of QuickStop Chain's security policies and whether specific incidents/actions comply with these policies.

Document Context:
- Information Security Policy v2.3
- Acceptable Use Policy
- Incident Response Procedures
- PCI DSS Requirements Documentation
- Third-Party Vendor Security Requirements

Question Types to Include:

1. Policy Violation Identification (10 questions)
Example: "According to the email from March 10, did Store Manager Johnson follow the proper incident reporting procedure when he discovered the potential skimmer?"

2. Compliance Verification (10 questions)
Example: "Which stores in the Q3 audit were non-compliant with the password complexity requirements outlined in Section 4.2 of the Information Security Policy?"

3. Policy Application Scenarios (10 questions)
Example: "A vendor technician needs to access the POS system for maintenance. According to the Third-Party Vendor Security Requirements, what authentication and logging procedures must be followed?"

For each question provide:
- Question text
- Correct answer with policy citation
- Policy section reference
- Difficulty level
- Common wrong answers (distractors)

Make questions specific and reference actual events from the document corpus where possible.
```

---

## Code Development Assistance

### Enhance Document Generator with Relationships

```
I have a Python document generator that creates synthetic documents for a convenience store chain. I need help adding sophisticated relationship tracking between documents.

Current Code Structure:
- DocumentGenerator class with basic generation
- JSON configuration for document types
- Simple document registry

Requirements:
1. Add bidirectional relationship tracking
2. Ensure temporal consistency (documents can't reference future events)
3. Implement dependency resolution (generate prerequisites first)
4. Add relationship validation
5. Create relationship visualization

Specific Relationships to Implement:
- incident_triggers: Security incidents trigger emails, reports, financial impacts
- compliance_cascade: Failed audits trigger remediation plans, training, follow-ups
- financial_incorporation: All costs roll up to financial reports
- email_references: Emails discuss other documents/events

Please provide:
1. Enhanced DocumentRegistry class with relationship graph
2. Relationship validation method
3. Dependency resolver for generation order
4. Method to query related documents
5. Export relationship graph for visualization

The code should maintain backward compatibility with the existing generator.
```

### Create File Format Writers

```
I need help creating specialized file writers for different document formats in my synthetic benchmark generator. Currently everything saves as text files.

Required Format Writers:

1. PDF Writer for:
   - Formal reports (with headers, footers, page numbers)
   - Financial statements (with tables and charts)
   - Audit reports (with executive summary, detailed findings sections)

2. Excel Writer for:
   - Multi-sheet inventory reports
   - Training completion trackers with conditional formatting
   - Financial data with formulas and pivot tables

3. PowerPoint Writer for:
   - Security initiatives (with bullet points, graphics placeholders)
   - Board presentations (with charts from data)

4. Email Writer for:
   - Realistic email format (headers, threading, quotes)
   - HTML and plain text versions
   - Attachment references

Each writer should:
- Accept structured data (JSON/dict)
- Apply appropriate formatting
- Include realistic metadata
- Support templates
- Handle errors gracefully

Provide a base FileWriter class and specific implementations for each format. Use libraries like reportlab for PDF, openpyxl for Excel, and python-pptx for PowerPoint.
```

---

## Data Consistency and Validation

### Create Data Consistency Validator

```
Help me create a comprehensive validation system for my synthetic document corpus to ensure consistency across all generated documents.

Validation Requirements:

1. Temporal Consistency:
   - Events referenced happen in correct order
   - Documents don't reference future events
   - Incident timelines are logical

2. Financial Consistency:
   - Numbers add up across documents
   - Store revenues aggregate correctly to regional
   - Incident costs appear in financial reports

3. Entity Consistency:
   - Store IDs used consistently
   - Employee names/roles remain constant
   - Regional assignments don't change unexpectedly

4. Cross-Reference Validation:
   - Documents mentioned in emails exist
   - Audit findings match remediation plans
   - Training referenced matches completion reports

5. Security Incident Consistency:
   - Incident IDs unique and consistent
   - Impact assessments align across documents
   - Resolution status tracking

Please provide:
1. Validator class structure
2. Specific validation rules for each category
3. Error reporting format
4. Automated fixing suggestions
5. Validation report generator

Include examples of common inconsistencies to catch and how to resolve them.
```

---

## Security Scenario Development

### Generate Realistic Security Incident Scenarios

```
I need help creating 10 highly realistic security incident scenarios for a convenience store chain. These will be used to generate consistent documentation across the synthetic corpus.

For each scenario, provide:

1. Incident Overview:
   - Type (ransomware, data breach, physical breach, insider threat, etc.)
   - Attack vector
   - Threat actor profile (if applicable)

2. Detailed Timeline:
   - Initial compromise
   - Discovery
   - Escalation points
   - Resolution milestones

3. Business Impact:
   - Affected locations/systems
   - Financial losses (direct and indirect)
   - Customer impact
   - Regulatory implications

4. Technical Details:
   - IoCs (Indicators of Compromise)
   - Vulnerabilities exploited
   - Systems affected
   - Data exposed/encrypted

5. Response Actions:
   - Immediate containment
   - Investigation steps
   - Remediation efforts
   - Long-term improvements

6. Document Trail:
   - Which documents would be generated
   - Key facts that should appear consistently
   - Relationships between documents

Make scenarios varied but realistic for a convenience store chain:
- Consider POS systems, fuel pumps, ATMs
- Include supply chain attacks
- Physical security breaches (skimmers)
- Employee-related incidents
- Third-party vendor compromises

Each scenario should be detailed enough to generate 15-20 related documents with consistent information.
```

### Create Phishing Campaign Simulation Data

```
Generate realistic phishing simulation campaign data for QuickStop Chain's security awareness program over 12 months.

Requirements:

1. Monthly Campaign Themes:
   - Month 1: Generic invoice phishing
   - Month 2: Fake IT support requests
   - Month 3: CEO fraud attempt
   - Month 4: Vendor payment update
   - Month 5: Benefits enrollment
   - Month 6: Package delivery notification
   - Continue pattern...

2. For Each Campaign Generate:
   - Email templates (subject lines, sender addresses, body content)
   - Target employee segments
   - Click rates by department/role
   - Credential entry rates
   - Time to report metrics
   - Device/location analysis

3. Progression Over Time:
   - Show improvement in detection rates
   - Identify consistently vulnerable departments
   - Include regression after holidays
   - Correlate with training completion

4. Realistic Metrics:
   - Initial click rates: 25-35%
   - Post-training: 8-15%
   - Credential entry: 3-8% of clicks
   - Report rates: 5-40% depending on training

5. Notable Incidents:
   - At least 2 campaigns where someone senior falls for it
   - One campaign that leads to actual incident
   - One very successful campaign (high report rate)

Format as structured data that can generate multiple document types:
- Executive summaries
- Detailed analyst reports
- Training recommendations
- Department-specific feedback

Include enough detail to answer questions about trends, specific user behavior, and training effectiveness.
```

---

## Usage Tips

1. **Be Specific**: Always provide concrete examples, numbers, and names when asking Claude to generate content
2. **Layer Context**: Build upon previous responses by referencing generated content
3. **Request Formats**: Always specify the output format you need (JSON, narrative, code, etc.)
4. **Validation Loop**: Ask Claude to validate generated content against requirements
5. **Iterative Refinement**: Start with basic generation, then add complexity in follow-up prompts

## Project-Specific Context to Maintain

When working with Claude on this project, always provide:
- Company name: QuickStop Chain
- Store count: 850
- Regions: Northeast, Southeast, Midwest, Southwest, West
- Time period: 2023-2024
- Key incidents: March 2024 ransomware, June 2024 data breach
- Compliance framework: PCI DSS
- Store ID format: ST[0000-9999]
- Employee ID format: EMP[store][00-99]
