"""Summary Validation Tools for validating medical summaries."""

import inspect
import json
import logging
from typing import Callable, Dict, Any, get_type_hints
from semantic_kernel.functions import kernel_function


class SummaryValidationTools:
    """Tools for validating medical summaries to ensure they contain required fields."""

    @staticmethod
    @kernel_function(
        description="Validate that a medical summary contains all three required fields: patient name, age, and recent medical events."
    )
    async def validate_summary_completeness(summary_data: str) -> str:
        """
        Validate that a medical summary contains the three essential fields.
        
        Args:
            summary_data: JSON string or text containing the medical summary to validate
            
        Returns:
            JSON string with validation results including missing fields and recommendations
        """
        try:
            # Parse summary data if it's JSON
            if summary_data.strip().startswith('{'):
                try:
                    summary_dict = json.loads(summary_data)
                except json.JSONDecodeError:
                    summary_dict = {"raw_text": summary_data}
            else:
                summary_dict = {"raw_text": summary_data}
            
            validation_result = {
                "is_valid": True,
                "missing_fields": [],
                "present_fields": [],
                "recommendations": []
            }
            
            # Check for patient name
            name_fields = ['patient_name', 'name', 'full_name', 'patient_demographics']
            name_found = any(field in summary_dict and summary_dict[field] for field in name_fields)
            
            if not name_found:
                # Also check in raw text for name patterns
                if 'raw_text' in summary_dict:
                    text = summary_dict['raw_text'].lower()
                    name_patterns = ['patient:', 'name:', 'patient name:', 'full name:']
                    name_found = any(pattern in text for pattern in name_patterns)
            
            if name_found:
                validation_result["present_fields"].append("✅ Patient Name")
            else:
                validation_result["is_valid"] = False
                validation_result["missing_fields"].append("❌ Patient Name")
                validation_result["recommendations"].append(
                    "Add patient name in fields like 'patient_name', 'name', or 'full_name'"
                )
            
            # Check for patient age
            age_fields = ['age', 'patient_age', 'birth_date', 'date_of_birth', 'birthDate']
            age_found = any(field in summary_dict and summary_dict[field] for field in age_fields)
            
            if not age_found:
                # Also check in raw text for age patterns
                if 'raw_text' in summary_dict:
                    text = summary_dict['raw_text'].lower()
                    age_patterns = ['age:', 'years old', 'y/o', 'born', 'age ']
                    age_found = any(pattern in text for pattern in age_patterns)
            
            if age_found:
                validation_result["present_fields"].append("✅ Patient Age")
            else:
                validation_result["is_valid"] = False
                validation_result["missing_fields"].append("❌ Patient Age")
                validation_result["recommendations"].append(
                    "Add patient age in fields like 'age', 'patient_age', or 'birth_date'"
                )
            
            # Check for recent medical events
            medical_fields = ['medical_events', 'recent_medical_events', 'conditions', 'medical_conditions', 'diagnoses', 'procedures']
            medical_found = any(field in summary_dict and summary_dict[field] for field in medical_fields)
            
            if not medical_found:
                # Also check in raw text for medical event patterns
                if 'raw_text' in summary_dict:
                    text = summary_dict['raw_text'].lower()
                    medical_patterns = ['diagnosis:', 'condition:', 'procedure:', 'treatment:', 'medical history:', 'recent events:']
                    medical_found = any(pattern in text for pattern in medical_patterns)
            
            if medical_found:
                validation_result["present_fields"].append("✅ Recent Medical Events")
            else:
                validation_result["is_valid"] = False
                validation_result["missing_fields"].append("❌ Recent Medical Events")
                validation_result["recommendations"].append(
                    "Add recent medical events in fields like 'medical_events', 'conditions', or 'diagnoses'"
                )
            
            return json.dumps(validation_result, indent=2)
            
        except Exception as e:
            logging.error(f"Error validating summary: {e}")
            return json.dumps({
                "is_valid": False,
                "error": f"Validation failed: {str(e)}",
                "missing_fields": ["❌ Validation Error"],
                "present_fields": [],
                "recommendations": ["Please check the summary format and try again"]
            })

    @staticmethod
    @kernel_function(
        description="Check if a medical summary follows the expected data patterns found in patient files."
    )
    async def validate_summary_format(summary_data: str) -> str:
        """
        Validate the format and structure of a medical summary.
        
        Args:
            summary_data: JSON string or text containing the medical summary
            
        Returns:
            JSON string with format validation results
        """
        try:
            validation_result = {
                "format_valid": True,
                "format_issues": [],
                "suggestions": []
            }
            
            # Check if it's valid JSON
            if summary_data.strip().startswith('{'):
                try:
                    json.loads(summary_data)
                    validation_result["suggestions"].append("✅ Valid JSON format")
                except json.JSONDecodeError as e:
                    validation_result["format_valid"] = False
                    validation_result["format_issues"].append(f"❌ Invalid JSON: {str(e)}")
                    validation_result["suggestions"].append("Ensure the summary is in valid JSON format")
            
            # Check for empty or minimal content
            if len(summary_data.strip()) < 50:
                validation_result["format_valid"] = False
                validation_result["format_issues"].append("❌ Summary too short")
                validation_result["suggestions"].append("Summary should contain meaningful patient information")
            
            # Check for common medical summary structure
            text_lower = summary_data.lower()
            expected_sections = ['patient', 'age', 'medical', 'condition', 'diagnosis', 'treatment']
            found_sections = [section for section in expected_sections if section in text_lower]
            
            if len(found_sections) < 3:
                validation_result["format_issues"].append("❌ Missing expected medical content sections")
                validation_result["suggestions"].append("Include patient demographics and medical information")
            else:
                validation_result["suggestions"].append(f"✅ Found {len(found_sections)} relevant medical sections")
            
            return json.dumps(validation_result, indent=2)
            
        except Exception as e:
            logging.error(f"Error validating format: {e}")
            return json.dumps({
                "format_valid": False,
                "format_issues": [f"❌ Format validation error: {str(e)}"],
                "suggestions": ["Please check the summary format and try again"]
            })

    @staticmethod
    @kernel_function(
        description="Generate a detailed validation report for a medical summary with specific recommendations."
    )
    async def generate_validation_report(summary_data: str) -> str:
        """
        Generate a comprehensive validation report for a medical summary.
        
        Args:
            summary_data: JSON string or text containing the medical summary
            
        Returns:
            Detailed validation report in JSON format
        """
        try:
            # Get completeness validation
            completeness_result = await SummaryValidationTools.validate_summary_completeness(summary_data)
            completeness_data = json.loads(completeness_result)
            
            # Get format validation
            format_result = await SummaryValidationTools.validate_summary_format(summary_data)
            format_data = json.loads(format_result)
            
            # Generate comprehensive report
            report = {
                "summary_validation_report": {
                    "overall_status": "VALID" if completeness_data["is_valid"] and format_data["format_valid"] else "INVALID",
                    "completeness_check": completeness_data,
                    "format_check": format_data,
                    "required_fields_status": {
                        "patient_name": "✅ Present" if "✅ Patient Name" in completeness_data.get("present_fields", []) else "❌ Missing",
                        "patient_age": "✅ Present" if "✅ Patient Age" in completeness_data.get("present_fields", []) else "❌ Missing",
                        "recent_medical_events": "✅ Present" if "✅ Recent Medical Events" in completeness_data.get("present_fields", []) else "❌ Missing"
                    },
                    "recommendations": completeness_data.get("recommendations", []) + format_data.get("suggestions", [])
                }
            }
            
            return json.dumps(report, indent=2)
            
        except Exception as e:
            logging.error(f"Error generating validation report: {e}")
            return json.dumps({
                "summary_validation_report": {
                    "overall_status": "ERROR",
                    "error": f"Report generation failed: {str(e)}",
                    "recommendations": ["Please check the summary data and try again"]
                }
            })

    @classmethod
    def get_all_kernel_functions(cls) -> Dict[str, Callable]:
        """
        Returns a dictionary of all methods in this class that have the @kernel_function annotation.
        
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