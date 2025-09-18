import inspect
import json
import os
from typing import Callable, Dict, get_type_hints

from semantic_kernel.functions import kernel_function
from models.messages_kernel import AgentType

class FHIRSummaryTools:
    """Define FHIR Summary Agent functions (tools) for analyzing FHIR data and generating patient history summaries"""

    agent_name = AgentType.FHIR_SUMMARY.value

    # File mapping - maps patient IDs to JSON files
    FILE_MAPPING = {
        "patient-p01": "p01-heart.json",
        "patient-p02": "p02-lungs.json",
        "patient-p03": "p03-healthy.json"
    }

    @staticmethod
    def _load_patient_file(patient_id: str) -> str:
        """Load patient file content by ID"""
        try:
            filename = FHIRSummaryTools.FILE_MAPPING.get(patient_id)
            if not filename:
                return f"Error: No file mapping found for patient ID: {patient_id}"

            # Construct file path relative to the backend directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.dirname(current_dir)
            file_path = os.path.join(backend_dir, "data", "patients", filename)

            if not os.path.exists(file_path):
                return f"Error: Patient file not found: {file_path}"

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content

        except Exception as e:
            return f"Error loading patient file: {str(e)}"

    @staticmethod
    def _parse_fhir_data(fhir_content: str) -> Dict:
        """Parse FHIR JSON content and extract relevant information"""
        try:
            fhir_data = json.loads(fhir_content)
            
            # Initialize result structure
            result = {
                "patient_info": {},
                "conditions": [],
                "observations": [],
                "medications": []
            }
            
            # Process FHIR bundle entries
            if "entry" in fhir_data:
                for entry in fhir_data["entry"]:
                    resource = entry.get("resource", {})
                    resource_type = resource.get("resourceType", "")
                    
                    if resource_type == "Patient":
                        # Extract patient demographics
                        result["patient_info"] = {
                            "id": resource.get("id", ""),
                            "name": "",
                            "birth_date": resource.get("birthDate", ""),
                            "gender": resource.get("gender", "")
                        }
                        
                        # Get patient name
                        if "name" in resource and resource["name"]:
                            name_parts = resource["name"][0]
                            given_names = " ".join(name_parts.get("given", []))
                            family_name = name_parts.get("family", "")
                            result["patient_info"]["name"] = f"{given_names} {family_name}".strip()
                    
                    elif resource_type == "Condition":
                        # Extract condition information
                        condition = {
                            "id": resource.get("id", ""),
                            "code": "",
                            "display": "",
                            "severity": "",
                            "onset_date": resource.get("onsetDateTime", ""),
                            "status": ""
                        }
                        
                        # Get condition code and display
                        if "code" in resource and "coding" in resource["code"]:
                            coding = resource["code"]["coding"][0]
                            condition["code"] = coding.get("code", "")
                            condition["display"] = coding.get("display", "")
                        
                        # Get severity
                        if "severity" in resource and "coding" in resource["severity"]:
                            severity_coding = resource["severity"]["coding"][0]
                            condition["severity"] = severity_coding.get("display", "")
                        
                        # Get clinical status
                        if "clinicalStatus" in resource and "coding" in resource["clinicalStatus"]:
                            status_coding = resource["clinicalStatus"]["coding"][0]
                            condition["status"] = status_coding.get("display", "")
                        
                        result["conditions"].append(condition)
                    
                    elif resource_type == "Observation":
                        # Extract observation information (lab tests)
                        observation = {
                            "id": resource.get("id", ""),
                            "code": "",
                            "display": "",
                            "value": "",
                            "unit": "",
                            "reference_range": "",
                            "date": resource.get("effectiveDateTime", ""),
                            "interpretation": ""
                        }
                        
                        # Get observation code and display
                        if "code" in resource and "coding" in resource["code"]:
                            coding = resource["code"]["coding"][0]
                            observation["code"] = coding.get("code", "")
                            observation["display"] = coding.get("display", "")
                        
                        # Get value
                        if "valueQuantity" in resource:
                            value_qty = resource["valueQuantity"]
                            observation["value"] = str(value_qty.get("value", ""))
                            observation["unit"] = value_qty.get("unit", "")
                        elif "valueString" in resource:
                            observation["value"] = resource["valueString"]
                        
                        # Get reference range
                        if "referenceRange" in resource and resource["referenceRange"]:
                            ref_range = resource["referenceRange"][0]
                            if "text" in ref_range:
                                observation["reference_range"] = ref_range["text"]
                        
                        # Get interpretation
                        if "interpretation" in resource and resource["interpretation"]:
                            if "coding" in resource["interpretation"][0]:
                                interp_coding = resource["interpretation"][0]["coding"][0]
                                observation["interpretation"] = interp_coding.get("display", "")
                        
                        result["observations"].append(observation)
            
            return result
            
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON format: {str(e)}"}
        except Exception as e:
            return {"error": f"Error parsing FHIR data: {str(e)}"}

    @staticmethod
    def _generate_summary(parsed_data: Dict) -> str:
        """Generate a 2-4 sentence summary of patient history"""
        try:
            if "error" in parsed_data:
                return f"Error generating summary: {parsed_data['error']}"
            
            patient_info = parsed_data.get("patient_info", {})
            conditions = parsed_data.get("conditions", [])
            observations = parsed_data.get("observations", [])
            
            patient_name = patient_info.get("name", "Patient")
            
            # Extract major diagnoses (active conditions)
            major_diagnoses = []
            for condition in conditions:
                if condition.get("status", "").lower() == "active" or condition.get("severity") in ["Severe", "Moderate"]:
                    diagnosis = condition.get("display", "")
                    if diagnosis:
                        major_diagnoses.append(diagnosis)
            
            # If no major diagnoses, take the first few conditions
            if not major_diagnoses:
                major_diagnoses = [c.get("display", "") for c in conditions[:3] if c.get("display")]
            
            # Extract key lab tests (abnormal or significant ones)
            key_lab_tests = []
            for obs in observations:
                display = obs.get("display", "")
                value = obs.get("value", "")
                unit = obs.get("unit", "")
                interpretation = obs.get("interpretation", "")
                
                # Include tests with abnormal interpretations or specific important tests
                if (interpretation and interpretation.lower() not in ["normal", ""]) or \
                   any(keyword in display.lower() for keyword in ["glucose", "cholesterol", "hemoglobin", "creatinine", "bnp", "troponin"]):
                    test_info = display
                    if value and unit:
                        test_info += f" ({value} {unit})"
                    if interpretation:
                        test_info += f" - {interpretation}"
                    key_lab_tests.append(test_info)
            
            # Extract medications (look for medication-related conditions or observations)
            medications = []
            for condition in conditions:
                condition_text = condition.get("display", "").lower()
                if any(med_keyword in condition_text for med_keyword in ["medication", "therapy", "treatment"]):
                    medications.append(condition.get("display", ""))
            
            # Build summary
            summary_parts = []
            
            # Start with patient and major diagnoses
            if major_diagnoses:
                diagnosis_text = ", ".join(major_diagnoses[:3])  # Limit to top 3
                summary_parts.append(f"{patient_name} is a patient with {diagnosis_text}.")
            else:
                summary_parts.append(f"{patient_name} is a patient with minimal medical history.")
            
            # Add lab test information
            if key_lab_tests:
                lab_text = ", ".join(key_lab_tests[:4])  # Limit to top 4
                summary_parts.append(f"Key laboratory findings include {lab_text}.")
            
            # Add medication information if found
            if medications:
                med_text = ", ".join(medications[:2])  # Limit to top 2
                summary_parts.append(f"Current treatments include {med_text}.")
            elif major_diagnoses:
                # Infer common medications based on conditions
                inferred_meds = []
                diagnosis_text = " ".join(major_diagnoses).lower()
                if "hypertension" in diagnosis_text or "heart" in diagnosis_text:
                    inferred_meds.append("cardiovascular medications")
                if "diabetes" in diagnosis_text:
                    inferred_meds.append("antidiabetic therapy")
                if "copd" in diagnosis_text or "asthma" in diagnosis_text:
                    inferred_meds.append("respiratory medications")
                
                if inferred_meds:
                    summary_parts.append(f"The patient is likely on {' and '.join(inferred_meds)}.")
            
            # Ensure we have 2-4 sentences
            summary = " ".join(summary_parts[:4])  # Limit to max 4 sentences
            
            return summary
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    @staticmethod
    @kernel_function(
        description="Generate a concise 2-4 sentence summary of patient medical history from FHIR data. Includes major diagnoses, key lab tests, and medications. Valid patient IDs: patient-p01, patient-p02, patient-p03"
    )
    async def generate_patient_summary(patient_id: str) -> str:
        """
        Generate a concise summary of patient medical history from FHIR data.

        Args:
            patient_id: Patient ID (e.g., patient-p01, patient-p02, patient-p03)

        Returns:
            2-4 sentence summary including major diagnoses, lab tests, and medications
        """
        if not patient_id or not patient_id.strip():
            return "Error: Please provide a patient ID."

        patient_id = patient_id.strip()

        # Check if patient ID exists
        if patient_id not in FHIRSummaryTools.FILE_MAPPING:
            available_ids = ", ".join(FHIRSummaryTools.FILE_MAPPING.keys())
            return f"Error: Patient ID '{patient_id}' not found. Available IDs: {available_ids}"

        # Load the patient file content
        fhir_content = FHIRSummaryTools._load_patient_file(patient_id)

        if fhir_content.startswith("Error:"):
            return fhir_content

        # Parse FHIR data
        parsed_data = FHIRSummaryTools._parse_fhir_data(fhir_content)
        
        # Generate and return summary
        summary = FHIRSummaryTools._generate_summary(parsed_data)
        
        return summary

    @staticmethod
    @kernel_function(
        description="Get detailed analysis of patient conditions, lab tests, and medications from FHIR data. Returns structured information for the specified patient."
    )
    async def analyze_patient_data(patient_id: str) -> str:
        """
        Analyze patient FHIR data and return detailed structured information.

        Args:
            patient_id: Patient ID (e.g., patient-p01, patient-p02, patient-p03)

        Returns:
            Detailed structured analysis of patient conditions, observations, and medications
        """
        if not patient_id or not patient_id.strip():
            return "Error: Please provide a patient ID."

        patient_id = patient_id.strip()

        # Check if patient ID exists
        if patient_id not in FHIRSummaryTools.FILE_MAPPING:
            available_ids = ", ".join(FHIRSummaryTools.FILE_MAPPING.keys())
            return f"Error: Patient ID '{patient_id}' not found. Available IDs: {available_ids}"

        # Load the patient file content
        fhir_content = FHIRSummaryTools._load_patient_file(patient_id)

        if fhir_content.startswith("Error:"):
            return fhir_content

        # Parse FHIR data
        parsed_data = FHIRSummaryTools._parse_fhir_data(fhir_content)
        
        if "error" in parsed_data:
            return f"Error analyzing patient data: {parsed_data['error']}"
        
        # Format the analysis
        result = []
        
        # Patient information
        patient_info = parsed_data.get("patient_info", {})
        if patient_info:
            result.append(f"**Patient:** {patient_info.get('name', 'Unknown')}")
            result.append(f"**ID:** {patient_info.get('id', 'Unknown')}")
            if patient_info.get('birth_date'):
                result.append(f"**Birth Date:** {patient_info['birth_date']}")
            result.append("")
        
        # Conditions
        conditions = parsed_data.get("conditions", [])
        if conditions:
            result.append("**Medical Conditions:**")
            for condition in conditions:
                line = f"- {condition.get('display', 'Unknown condition')}"
                if condition.get('severity'):
                    line += f" (Severity: {condition['severity']})"
                if condition.get('status'):
                    line += f" - Status: {condition['status']}"
                if condition.get('onset_date'):
                    line += f" - Onset: {condition['onset_date']}"
                result.append(line)
            result.append("")
        
        # Lab tests (observations)
        observations = parsed_data.get("observations", [])
        if observations:
            result.append("**Laboratory Tests:**")
            for obs in observations:
                line = f"- {obs.get('display', 'Unknown test')}"
                if obs.get('value') and obs.get('unit'):
                    line += f": {obs['value']} {obs['unit']}"
                elif obs.get('value'):
                    line += f": {obs['value']}"
                if obs.get('interpretation'):
                    line += f" ({obs['interpretation']})"
                if obs.get('reference_range'):
                    line += f" [Ref: {obs['reference_range']}]"
                result.append(line)
            result.append("")
        
        return "\n".join(result)

    @classmethod
    def get_all_kernel_functions(cls) -> dict[str, Callable]:
        """
        Returns a dictionary of all methods in this class that have the @kernel_function annotation.
        This function itself is not annotated with @kernel_function.

        Returns:
            Dict[str, Callable]: Dictionary with function names as keys and function objects as values
        """
        kernel_functions = {}

        # Get all class methods
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            # Skip this method itself and any private/special methods
            if name.startswith("_") or name == "get_all_kernel_functions":
                continue

            # Check if the method has the kernel_function annotation
            if hasattr(method, "__kernel_function__"):
                kernel_functions[name] = method

        return kernel_functions

    @classmethod
    def generate_tools_json_doc(cls) -> str:
        """
        Generate a JSON document containing information about all methods in the class.

        Returns:
            str: JSON string containing the methods' information
        """

        tools_list = []

        # Get all methods from the class that have the kernel_function annotation
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            # Skip this method itself and any private methods
            if name.startswith("_") or name == "generate_tools_json_doc":
                continue

            # Check if the method has the kernel_function annotation
            if hasattr(method, "__kernel_function__"):
                # Get method description from docstring or kernel_function description
                description = ""
                if hasattr(method, "__doc__") and method.__doc__:
                    description = method.__doc__.strip()

                # Get kernel_function description if available
                if hasattr(method, "__kernel_function__") and getattr(
                    method.__kernel_function__, "description", None
                ):
                    description = method.__kernel_function__.description

                # Get argument information by introspection
                sig = inspect.signature(method)
                args_dict = {}

                # Get type hints if available
                type_hints = get_type_hints(method)

                # Process parameters
                for param_name, param in sig.parameters.items():
                    # Skip first parameter 'cls' for class methods (though we're using staticmethod now)
                    if param_name in ["cls", "self"]:
                        continue

                    # Get parameter type
                    param_type = "string"  # Default type
                    if param_name in type_hints:
                        type_obj = type_hints[param_name]
                        # Convert type to string representation
                        if hasattr(type_obj, "__name__"):
                            param_type = type_obj.__name__
                        else:
                            param_type = str(type_obj)

                    # Get default value if any
                    default_value = None
                    if param.default is not param.empty:
                        default_value = param.default

                    args_dict[param_name] = {
                        "type": param_type,
                        "default": default_value,
                    }

                # Create tool entry
                tool_entry = {
                    "function_name": name,
                    "description": description,
                    "parameters": args_dict,
                }

                tools_list.append(tool_entry)

        # Return the JSON string representation
        return json.dumps(tools_list, ensure_ascii=False)