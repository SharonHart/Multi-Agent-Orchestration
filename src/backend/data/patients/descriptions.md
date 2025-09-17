# Synthetict Patients

## High-level overview

Patient 1 - Robert James Henderson (heart)
Patient 2 - Linda Marie Williams (lungs)
Patient 3 - Alex Jordan Thompson (healphy)

## Patient 1 - Heart
Robert James Henderson, a 68-year-old male with extensive cardiovascular history and comorbidities.
A typical complex cardiovascular patient with realistic disease progression, appropriate comorbidities, and clinically meaningful laboratory abnormalities that would guide ongoing medical management.

### **Patient Demographics & Contact Information**
- Complete personal details including identifiers (MRN, SSN)
- Contact information and emergency contact (spouse)
- Address and communication preferences

### **Medical Conditions (8 conditions with timeline)**
- **Coronary Artery Disease** (2019) - Multi-vessel disease, severe
- **Essential Hypertension** (2009) - Long-standing, moderate severity
- **Heart Failure with Reduced EF** (2023) - NYHA Class II, moderate
- **Myocardial Infarction** (2021) - Anterior STEMI, resolved after PCI
- **Atrial Fibrillation** (2023) - Paroxysmal, on anticoagulation
- **Type 2 Diabetes Mellitus** (2014) - Moderate, contributing factor
- **Hyperlipidemia** (2019) - Mixed, on statin therapy
- **Chronic Kidney Disease Stage 3A** (2023) - Secondary to diabetes/HTN

### **Laboratory Results (15 comprehensive blood tests)**
- **Cardiac Markers**: Normal troponin, elevated BNP (385 pg/mL) consistent with heart failure
- **Lipid Panel**: Total cholesterol normal, LDL slightly elevated (85 mg/dL), low HDL (38 mg/dL), high triglycerides (210 mg/dL)
- **Diabetes Monitoring**: Elevated fasting glucose (142 mg/dL), HbA1c slightly above goal (7.2%)
- **Renal Function**: Elevated creatinine (1.4 mg/dL), reduced eGFR (52 mL/min/1.73m²)
- **Hematology**: Mild anemia (Hgb 11.8 g/dL) related to CKD
- **Anticoagulation**: Therapeutic INR (2.3) for atrial fibrillation
- **Electrolytes**: Normal sodium and potassium levels

### **Clinical Features**
- **Realistic Timeline**: 15-year progression from hypertension to complex cardiovascular disease
- **Proper FHIR R5 Format**: Bundle with Patient, Organization, Practitioner, Condition, and Observation resources
- **Standard Coding**: SNOMED CT for conditions, LOINC for laboratory values
- **Clinical Coherence**: Logical disease relationships and medication monitoring patterns
- **Evidence-Based Values**: Clinically appropriate abnormal results reflecting actual disease states

## Patient 2 - Lungs

Linda Marie Williams (p02), a 65-year-old female with extensive pulmonary medical history.
A complex pulmonary patient with realistic disease progression, appropriate comorbidities, and clinically meaningful laboratory abnormalities that demonstrate the physiologic consequences of severe lung disease, including hypoxemia, hypercapnia, right heart strain, and compensatory polycythemia.

### **Patient Demographics & Contact Information**
- Complete personal details including identifiers (MRN, SSN)
- Contact information and emergency contact (daughter)
- Address in Denver, CO and communication preferences
- Divorced marital status

### **Pulmonary Conditions (9 conditions with timeline)**
- **Severe COPD** (2015) - FEV1 35% predicted, on triple therapy and supplemental oxygen
- **Long-standing Asthma** (1985) - Since childhood, now ACOS (asthma-COPD overlap)
- **Pulmonary Hypertension** (2020) - Secondary to lung disease, mean PA pressure 35 mmHg
- **Idiopathic Pulmonary Fibrosis** (2022) - Progressive decline, on antifibrotic therapy
- **Severe Obstructive Sleep Apnea** (2018) - AHI 45/hour, excellent CPAP compliance
- **Lung Cancer History** (2017-2018) - Stage IA NSCLC, successfully treated, in remission
- **Recurrent Pneumonia** (2019) - 4 episodes in 2 years, on prophylactic antibiotics
- **Chronic Type II Respiratory Failure** (2023) - Hypercapnia, requires O2 and BiPAP
- **45-pack-year smoking history** - Quit in 2017 with cancer diagnosis

### **Specialized Laboratory Results (13 pulmonary-specific tests)**
- **Arterial Blood Gas**: Compensated respiratory acidosis (pH 7.35, PCO2 58, PO2 62)
- **Oxygen Saturation**: 89% on 4L supplemental oxygen
- **BNP Elevated**: 425 pg/mL due to right heart strain from pulmonary hypertension
- **Alpha-1 Antitrypsin**: Borderline low (85 mg/dL), contributing to COPD
- **D-dimer Elevated**: 750 ng/mL, chronic thromboembolic risk
- **Eosinophils Elevated**: 8.2%, suggesting allergic asthma component
- **Total IgE Markedly Elevated**: 485 IU/mL, consistent with allergic asthma
- **Vitamin D Deficiency**: 18 ng/mL, common in chronic illness
- **C-Reactive Protein Elevated**: 12.5 mg/L, chronic inflammation
- **Procalcitonin Normal**: 0.08 ng/mL, rules out acute bacterial infection
- **Secondary Polycythemia**: Hemoglobin 16.8 g/dL, Hematocrit 52% (compensation for chronic hypoxemia)

### **Clinical Features**
- **Realistic Timeline**: 40-year progression from childhood asthma to complex pulmonary disease
- **Proper FHIR R5 Format**: Bundle with Patient, Organization, Practitioner, Condition, and Observation resources
- **Standard Coding**: SNOMED CT for conditions, LOINC for laboratory values
- **Clinical Coherence**: Logical disease relationships and physiologic compensations
- **Evidence-Based Values**: Clinically appropriate abnormal results reflecting actual pulmonary pathophysiology
- **Specialty-Specific**: Pulmonary function markers, gas exchange abnormalities, and inflammatory markers

## Patient 3 - Healthy

Alex Jordan Thompson (p03), a 25-year-old healthy male with minimal medical history.
A baseline healthy young adult patient with excellent laboratory values, normal vital signs, and minimal medical history.

## **Patient Demographics & Contact Information**
- Complete personal details including identifiers (MRN, SSN)
- Contact information and emergency contact (mother)
- Address in Austin, TX (university area) and communication preferences
- Single marital status, appropriate for young adult

## **Minimal Medical History (1 resolved condition)**
- **Simple Toe Fracture** (2022) - Right great toe fracture from recreational soccer, fully healed
- No cardiovascular or pulmonary conditions
- No chronic diseases or ongoing medical issues
- Clean medical history appropriate for healthy young adult

## **Comprehensive Normal Laboratory Results (8 test panels)**
- **Complete Blood Count**: All values normal (Hemoglobin 15.2 g/dL, Hematocrit 44.8%, WBC 7.2k, Platelets 285k)
- **Basic Metabolic Panel**: Normal glucose (88 mg/dL), creatinine (1.0 mg/dL), electrolytes
- **Lipid Panel**: Excellent profile (Total cholesterol 165, LDL 95, HDL 52, Triglycerides 98)
- **Vitamin D**: Adequate level (42 ng/mL), consistent with active lifestyle
- **Thyroid Function**: Normal TSH (2.1 mIU/L)
- **Blood Pressure**: Optimal (118/76 mmHg)
- **BMI**: Healthy weight (22.8 kg/m²)

## **Clinical Features**
- **Age-Appropriate Health**: All values within optimal ranges for a 25-year-old
- **Proper FHIR R5 Format**: Bundle with Patient, Organization, Practitioner, Condition, and Observation resources
- **Standard Coding**: SNOMED CT for conditions, LOINC for laboratory values
- **Realistic Scenario**: Represents typical healthy young adult with routine preventive care
- **Normal Physiology**: All laboratory and vital sign values reflect excellent health status
- **Primary Care Setting**: Austin Family Medicine Clinic for routine wellness care

