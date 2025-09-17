"""Summary Validation Agent for validating medical summaries."""

import logging
from typing import Dict, List, Optional

from context.cosmos_memory_kernel import CosmosMemoryContext
from kernel_agents.agent_base import BaseAgent
from kernel_tools.summary_validation_tools import SummaryValidationTools
from models.messages_kernel import AgentType
from semantic_kernel.functions import KernelFunction


class SummaryValidationAgent(BaseAgent):
    """Summary Validation agent implementation using Semantic Kernel.

    This agent specializes in validating medical summaries to ensure they contain
    the three required fields: patient name, age, and recent medical events, based
    on patterns found in the patient data files.
    """

    def __init__(
        self,
        session_id: str,
        user_id: str,
        memory_store: CosmosMemoryContext,
        tools: Optional[List[KernelFunction]] = None,
        system_message: Optional[str] = None,
        agent_name: str = "Summary_Validation_Agent",
        client=None,
        definition=None,
    ) -> None:
        """Initialize the Summary Validation Agent.

        Args:
            session_id: The current session identifier
            user_id: The user identifier
            memory_store: The Cosmos memory context
            tools: List of tools available to this agent (optional)
            system_message: Optional system message for the agent
            agent_name: Optional name for the agent (defaults to "Summary_Validation_Agent")
            client: Optional client instance
            definition: Optional definition instance
        """
        # Load configuration if tools not provided
        if not tools:
            # Get tools directly from SummaryValidationTools class
            tools = SummaryValidationTools.get_all_kernel_functions()

        # Use system message from config if not explicitly provided
        if not system_message:
            system_message = self.default_system_message(agent_name)

        super().__init__(
            agent_name=agent_name,
            session_id=session_id,
            user_id=user_id,
            memory_store=memory_store,
            tools=tools,
            system_message=system_message,
            client=client,
            definition=definition,
        )

    @classmethod
    async def create(
        cls,
        **kwargs: Dict[str, str],
    ) -> None:
        """Asynchronously create the Summary Validation Agent.

        Creates the Azure AI Agent for summary validation operations against patient data.

        Returns:
            Summary Validation Agent instance
        """

        session_id = kwargs.get("session_id")
        user_id = kwargs.get("user_id")
        memory_store = kwargs.get("memory_store")
        tools = kwargs.get("tools", None)
        system_message = kwargs.get("system_message", None)
        agent_name = kwargs.get("agent_name")
        client = kwargs.get("client")

        try:
            logging.info("Initializing Summary Validation Agent from async init azure AI Agent")

            # Create the Azure AI Agent using AppConfig with string instructions
            agent_definition = await cls._create_azure_ai_agent_definition(
                agent_name=agent_name,
                instructions=system_message,  # Pass the formatted string, not an object
                temperature=0.0,
                response_format=None,
            )

            return cls(
                session_id=session_id,
                user_id=user_id,
                memory_store=memory_store,
                tools=tools,
                system_message=system_message,
                agent_name=agent_name,
                client=client,
                definition=agent_definition,
            )

        except Exception as e:
            logging.error(f"Error creating Summary Validation Agent: {e}")
            raise

    @staticmethod
    def default_system_message(agent_name=None) -> str:
        """Get the default system message for the summary validation agent.
        
        Args:
            agent_name: The name of the agent (optional)
            
        Returns:
            The default system message for the agent
        """
        return (
            "You are a Summary Validation Agent specialized in validating medical summaries to ensure "
            "they contain the three essential fields required for patient care coordination. "
            "Your primary responsibility is to validate that medical summaries include:\n\n"
            "**REQUIRED FIELDS:**\n"
            "1. **Patient Name**: Full name of the patient (can be in fields like 'patient_name', 'name', 'full_name', or within 'patient_demographics')\n"
            "2. **Patient Age**: Age in years or birth date (can be in fields like 'age', 'patient_age', 'birth_date', 'date_of_birth', or 'birthDate')\n"
            "3. **Recent Medical Events**: Recent conditions, procedures, or medical activities (can be in fields like 'medical_events', 'recent_medical_events', 'conditions', 'medical_conditions', or 'diagnoses')\n\n"
            "**VALIDATION PROCESS:**\n"
            "- Check for the presence of all three required fields\n"
            "- Identify any missing fields and provide specific recommendations\n"
            "- Validate that the data is meaningful (not empty or null)\n"
            "- Reference patterns from the patient data files in the system for validation\n\n"
            "**RESPONSE FORMAT:**\n"
            "- Clearly indicate which fields are present (✅) or missing (❌)\n"
            "- Provide specific field names that should be used\n"
            "- Give actionable recommendations for fixing missing fields\n"
            "- Maintain a professional, clear, and helpful tone\n\n"
            "Use your validation tools to check summaries thoroughly and provide structured feedback. "
            "If a summary is missing any of the three required fields, mark it as INVALID and explain "
            "exactly what needs to be added."
        )

    @property
    def plugins(self):
        """Get the plugins for the summary validation agent."""
        return SummaryValidationTools.get_all_kernel_functions()

    # Explicitly inherit handle_action_request from the parent class
    async def handle_action_request(self, action_request_json: str) -> str:
        """Handle an action request from another agent or the system.

        This method is inherited from BaseAgent but explicitly included here for clarity.

        Args:
            action_request_json: The action request as a JSON string

        Returns:
            A JSON string containing the action response
        """
        return await super().handle_action_request(action_request_json)