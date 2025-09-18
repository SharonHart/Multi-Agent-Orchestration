# FHIR Summary Agent

## Overview

The FHIR Summary Agent is a specialized agent designed to analyze FHIR (Fast Healthcare Interoperability Resources) patient data and generate concise medical history summaries. This agent can process JSON patient bundles containing conditions, observations, and medical history to provide healthcare professionals with quick, actionable summaries.

## Features

- **Concise Summaries**: Generates 2-4 sentence summaries of patient medical history
- **Major Diagnoses**: Identifies and highlights the most significant medical conditions
- **Lab Test Analysis**: Extracts and summarizes key laboratory findings with clinical significance
- **Medication Inference**: Identifies current treatments and infers likely medications based on conditions
- **Detailed Analysis**: Provides structured, comprehensive analysis of all patient data when needed

## Available Functions

### `generate_patient_summary(patient_id: str)`
Creates a concise 2-4 sentence summary of patient medical history.

**Parameters:**
- `patient_id`: Patient ID (patient-p01, patient-p02, or patient-p03)

**Returns:**
- A concise summary including major diagnoses, key lab tests, and medications

**Example:**
```
Robert James Henderson is a patient with Coronary artery disease, Essential hypertension, Heart failure. 
Key laboratory findings include Troponin I (0.02 ng/mL) - Normal, BNP (385 pg/mL) - High, 
Cholesterol, total (185 mg/dL) - Normal, LDL cholesterol (85 mg/dL) - High. 
The patient is likely on cardiovascular medications and antidiabetic therapy.
```

### `analyze_patient_data(patient_id: str)`
Provides detailed structured analysis of all patient data.

**Parameters:**
- `patient_id`: Patient ID (patient-p01, patient-p02, or patient-p03)

**Returns:**
- Detailed structured information including:
  - Patient demographics
  - Complete list of medical conditions with severity and status
  - All laboratory tests with values, units, and interpretations
  - Reference ranges where available

## Available Patients

- **patient-p01**: Robert James Henderson (68-year-old male with extensive cardiovascular history)
- **patient-p02**: Linda Marie Williams (65-year-old female with complex pulmonary conditions)  
- **patient-p03**: Alex Jordan Thompson (25-year-old healthy male with minimal medical history)

## Integration

The FHIR Summary Agent is fully integrated into the Multi-Agent Orchestration system:

1. **Agent Type**: `AgentType.FHIR_SUMMARY`
2. **Agent Name**: `FHIR_Summary_Agent`
3. **Factory Integration**: Automatically available through `AgentFactory.create_agent()`

## Usage Example

```python
from kernel_agents.agent_factory import AgentFactory
from models.messages_kernel import AgentType

# Create the FHIR Summary Agent
agent = await AgentFactory.create_agent(
    agent_type=AgentType.FHIR_SUMMARY,
    session_id="your_session_id",
    user_id="your_user_id"
)

# The agent will have access to:
# - generate_patient_summary()
# - analyze_patient_data()
```

## Technical Details

### Data Processing
- Parses FHIR R5 JSON bundles
- Extracts Patient, Condition, and Observation resources
- Uses SNOMED CT codes for conditions and LOINC codes for laboratory values
- Handles clinical status, severity, and temporal information

### Summary Algorithm
1. **Patient Identification**: Extracts patient demographics and identifiers
2. **Condition Prioritization**: Focuses on active conditions and those with severe/moderate severity
3. **Lab Test Filtering**: Highlights abnormal results and clinically significant tests
4. **Medication Inference**: Identifies treatments based on condition patterns
5. **Narrative Generation**: Creates coherent, clinically relevant summaries

### Error Handling
- Validates patient IDs against available data
- Handles malformed JSON gracefully
- Provides clear error messages for invalid inputs
- Maintains system stability during parsing errors

## Future Enhancements

- Support for additional FHIR resource types (MedicationStatement, Procedure, etc.)
- Configurable summary length and detail levels
- Integration with clinical decision support systems
- Support for multiple FHIR versions (R4, R5)
- Real-time FHIR server connectivity