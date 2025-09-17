import inspect
import json
import os
from typing import Callable

from semantic_kernel.functions import kernel_function
from models.messages_kernel import AgentType

class PatientTools:
    """Define Patient Agent functions (tools) for patient lookup by ID"""

    agent_name = AgentType.PATIENT.value

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
            filename = PatientTools.FILE_MAPPING.get(patient_id)
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
    @kernel_function(
        description="Get patient data by patient ID. Valid IDs: patient-p01, patient-p02, patient-p03"
    )
    async def get_patient_by_id(patient_id: str) -> str:
        """
        Get patient data by patient ID.

        Args:
            patient_id: Patient ID (e.g., patient-p01, patient-p02, patient-p03)

        Returns:
            Full FHIR JSON content if patient found, error message if not found
        """
        if not patient_id or not patient_id.strip():
            return "Error: Please provide a patient ID."

        patient_id = patient_id.strip()

        # Check if patient ID exists
        if patient_id not in PatientTools.FILE_MAPPING:
            available_ids = ", ".join(PatientTools.FILE_MAPPING.keys())
            return f"Error: Patient ID '{patient_id}' not found. Available IDs: {available_ids}"

        # Load and return the patient file content
        patient_content = PatientTools._load_patient_file(patient_id)

        if patient_content.startswith("Error:"):
            return patient_content

        return patient_content

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

                # Process parameters
                for param_name, param in sig.parameters.items():
                    # Skip first parameter 'cls' for class methods
                    if param_name in ["cls", "self"]:
                        continue

                    # Create parameter description
                    args_dict[param_name] = {
                        "description": param_name.replace("_", " "),
                        "title": param_name.replace("_", " ").title(),
                        "type": "string",
                    }

                # Add the tool information to the list
                tool_entry = {
                    "agent": cls.agent_name,
                    "function": name,
                    "description": description,
                    "arguments": json.dumps(args_dict).replace('"', "'"),
                }

                tools_list.append(tool_entry)

        # Return the JSON string representation
        return json.dumps(tools_list, ensure_ascii=False)
