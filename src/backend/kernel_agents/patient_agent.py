import logging
from typing import List, Optional

from kernel_agents.agent_base import BaseAgent
from kernel_tools.patient_tools import PatientTools
from models.messages_kernel import AgentType
from semantic_kernel.functions import KernelFunction

logger = logging.getLogger(__name__)

class PatientAgent(BaseAgent):
    """Patient Agent for looking up patient records by name with fuzzy matching."""

    def __init__(
        self,
        agent_name: str,
        session_id: str,
        user_id: str,
        memory_store,
        tools: Optional[List[KernelFunction]] = None,
        system_message: Optional[str] = None,
        client=None,
        definition=None,
    ):
        """Initialize the Patient Agent."""

        # Load patient tools if not provided
        if tools is None:
            tools = []
            patient_tools = PatientTools.get_all_kernel_functions()
            for tool_name, tool_func in patient_tools.items():
                tools.append(tool_func)

        # Use default system message if not provided
        if system_message is None:
            system_message = self.default_system_message()

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

    @staticmethod
    def default_system_message() -> str:
        """Return the default system message for the Patient Agent."""
        return """You are a Patient Lookup Agent specialized in retrieving patient medical records by ID.

Your capabilities:
- Retrieve complete FHIR patient history files by patient ID
- Handle patient data lookup requests

Available patients in the system:
- patient-p01: Robert James Henderson (cardiovascular patient)
- patient-p02: Linda Marie Williams (pulmonary patient)
- patient-p03: Alex Jordan Thompson (healthy young adult)

When looking up patients:
1. Use the get_patient_by_id function with the exact patient ID
2. Return the complete patient record if found
3. Provide helpful error messages if the ID is not found

Always be helpful and provide clear information about patient lookup results."""

    @classmethod
    async def create(
        cls,
        agent_name: str = None,
        session_id: str = None,
        user_id: str = None,
        memory_store=None,
        tools: Optional[List[KernelFunction]] = None,
        system_message: Optional[str] = None,
        client=None,
        **kwargs
    ) -> "PatientAgent":
        """Create a Patient Agent instance."""

        if agent_name is None:
            agent_name = AgentType.PATIENT.value

        # Create Azure AI agent definition
        definition = await cls._create_azure_ai_agent_definition(
            agent_name=agent_name,
            instructions=system_message or cls.default_system_message(),
            tools=tools,
            client=client,
        )

        # Create the agent instance
        agent = cls(
            agent_name=agent_name,
            session_id=session_id,
            user_id=user_id,
            memory_store=memory_store,
            tools=tools,
            system_message=system_message,
            client=client,
            definition=definition,
        )

        logger.info(f"Created Patient Agent: {agent_name} for session {session_id}")
        return agent
