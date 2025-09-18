import logging
from typing import List, Optional

from kernel_agents.agent_base import BaseAgent
from kernel_tools.fhir_summary_tools import FHIRSummaryTools
from models.messages_kernel import AgentType
from semantic_kernel.functions import KernelFunction

logger = logging.getLogger(__name__)

class FHIRSummaryAgent(BaseAgent):
    """FHIR Summary Agent for analyzing FHIR patient data and generating concise medical history summaries."""

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
        """Initialize the FHIR Summary Agent."""

        # Load FHIR summary tools if not provided
        if tools is None:
            tools = []
            fhir_tools = FHIRSummaryTools.get_all_kernel_functions()
            for tool_name, tool_func in fhir_tools.items():
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
    def default_system_message(agent_name=None) -> str:
        """Return the default system message for the FHIR Summary Agent."""
        return """You are a FHIR Summary Agent specialized in analyzing FHIR (Fast Healthcare Interoperability Resources) patient data and generating concise medical history summaries.

Your capabilities:
- Analyze FHIR JSON patient data bundles containing conditions, observations, and medical history
- Generate concise 2-4 sentence summaries of patient medical history
- Extract and summarize major diagnoses, key laboratory tests, and medications
- Provide detailed structured analysis of patient data when requested

Available patients in the system:
- patient-p01: Robert James Henderson (68-year-old male with extensive cardiovascular history)
- patient-p02: Linda Marie Williams (65-year-old female with complex pulmonary conditions)
- patient-p03: Alex Jordan Thompson (25-year-old healthy male with minimal medical history)

When generating summaries:
1. Focus on the most significant medical conditions and diagnoses
2. Include key abnormal laboratory results and their clinical significance
3. Mention important medications or treatments when available
4. Keep summaries concise (2-4 sentences) but informative
5. Use clear, professional medical language appropriate for healthcare providers

Available functions:
- generate_patient_summary: Creates a concise 2-4 sentence summary of patient history
- analyze_patient_data: Provides detailed structured analysis of all patient data

Always provide helpful, accurate, and clinically relevant information based on the FHIR data."""

    @classmethod
    async def create(
        cls,
        agent_name: Optional[str] = None,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        memory_store=None,
        tools: Optional[List[KernelFunction]] = None,
        system_message: Optional[str] = None,
        client=None,
        **kwargs
    ) -> "FHIRSummaryAgent":
        """Create a FHIR Summary Agent instance."""

        if agent_name is None:
            agent_name = AgentType.FHIR_SUMMARY.value

        # Create Azure AI agent definition
        definition = await cls._create_azure_ai_agent_definition(
            agent_name=agent_name,
            instructions=system_message or cls.default_system_message(),
            tools=tools,
            client=client,
        )

        # Create the agent instance
        agent = cls(
            agent_name=agent_name or AgentType.FHIR_SUMMARY.value,
            session_id=session_id or "",
            user_id=user_id or "",
            memory_store=memory_store,
            tools=tools,
            system_message=system_message,
            client=client,
            definition=definition,
        )

        logger.info(f"Created FHIR Summary Agent: {agent_name} for session {session_id}")
        return agent