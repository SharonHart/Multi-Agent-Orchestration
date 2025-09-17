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
