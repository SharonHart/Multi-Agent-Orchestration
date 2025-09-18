import inspect
import json
import os
from typing import Callable, get_type_hints

from semantic_kernel.functions import kernel_function
from models.messages_kernel import AgentType

class PatientTools:
    """Define Patient Agent functions (tools) for patient lookup by ID"""

    agent_name = AgentType.PATIENT.value

    # File mapping - maps patient IDs to JSON files
    FILE_MAPPING = {
        "patient-p01": {"name": "Robert James Henderson", "file": "p01-heart.json"},
        "patient-p02": {"name": "Linda Marie Williams", "file": "p02-lungs.json"},
        "patient-p03": {"name": "Alex Jordan Thompson", "file": "p03-healthy.json"}
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
            file_path = os.path.join(backend_dir, "data", "patients", filename["file"])

            if not os.path.exists(file_path):
                return f"Error: Patient file not found: {file_path}"

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content

        except Exception as e:
            return f"Error loading patient file: {str(e)}"

    @staticmethod
    @kernel_function(
        description="List full patient names"
    )
    async def get_patient_names() -> str:
        """
        Returns a JSON array (string) containing full patient names for all known patients.
        """
        names = [info["name"] for info in PatientTools.FILE_MAPPING.values()]
        return json.dumps(names, ensure_ascii=False)

    @staticmethod
    @kernel_function(
        description="Get patient data by patient name. Valid names: patient full names in FILE_MAPPING"
    )
    async def get_patient_by_name(patient_name: str) -> str:
        """
        Get patient data by patient full name.

        Args:
            patient_name: Full patient name (e.g., 'Robert James Henderson')

        Returns:
            Full FHIR JSON content if patient found, error message if not found
        """
        if not patient_name or not patient_name.strip():
            return "Error: Please provide a patient name."

        query = patient_name.strip().lower()

        # Find the patient id by matching the provided name (case-insensitive)
        matched_id = None
        for pid, info in PatientTools.FILE_MAPPING.items():
            if isinstance(info, dict):
                name = info.get("name", "")
                if isinstance(name, str) and name.strip().lower() == query:
                    matched_id = pid
                    break

        if not matched_id:
            available_names = [v.get("name") for v in PatientTools.FILE_MAPPING.values() if isinstance(v, dict) and v.get("name")]
            available_str = ", ".join(available_names)
            return f"Error: Patient name '{patient_name}' not found. Available names: {available_str}"

        # Load and return the patient file content using the matched id
        patient_content = PatientTools._load_patient_file(matched_id)

        if isinstance(patient_content, str) and patient_content.startswith("Error:"):
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
