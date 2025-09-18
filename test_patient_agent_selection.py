#!/usr/bin/env python3
"""
Test script to verify that the Patient agent is being properly selected by the planner.
"""

import asyncio
import logging
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'backend'))

from kernel_agents.planner_agent import PlannerAgent
from kernel_tools.patient_tools import PatientTools
from kernel_tools.generic_tools import GenericTools
from models.messages_kernel import InputTask, AgentType

async def test_patient_agent_tools():
    """Test that Patient agent tools are properly exposed to planner."""
    
    print("Testing Patient Agent Tools Registration...")
    
    # Create a mock planner agent to test the tools list
    planner = PlannerAgent(
        session_id="test-session",
        user_id="test-user",
        memory_store=None,  # We'll skip memory store for this test
    )
    
    print(f"Available agents: {planner._available_agents}")
    print(f"Agent tools list keys: {list(planner._agent_tools_list.keys())}")
    
    # Test the tools generation
    args = planner._generate_args("Get patient information for patient-p01")
    
    print(f"Objective: Get patient information for patient-p01")
    print(f"Agents string: {args['agents_str']}")
    print(f"Tools list length: {len(args['tools_str'])}")
    
    # Check if Patient agent tools are included
    patient_tools_included = False
    for tools in args['tools_str']:
        if 'get_patient_by_id' in tools:
            patient_tools_included = True
            print("✅ Patient agent tools found in planner tools list!")
            print(f"Patient tools: {tools}")
            break
    
    if not patient_tools_included:
        print("❌ Patient agent tools NOT found in planner tools list!")
        print("Available tools:")
        for i, tools in enumerate(args['tools_str']):
            print(f"  Tool set {i}: {tools[:100]}...")
    
    return patient_tools_included

async def test_patient_tools_directly():
    """Test Patient tools directly."""
    
    print("\nTesting Patient Tools Directly...")
    
    # Test the generate_tools_json_doc method
    try:
        tools_json = PatientTools.generate_tools_json_doc()
        print(f"✅ PatientTools.generate_tools_json_doc() works!")
        print(f"Tools JSON: {tools_json}")
        return True
    except Exception as e:
        print(f"❌ PatientTools.generate_tools_json_doc() failed: {e}")
        return False

async def main():
    """Main test function."""
    
    logging.basicConfig(level=logging.INFO)
    
    print("🧪 Testing Patient Agent Selection Fix")
    print("=" * 50)
    
    # Test 1: Test patient tools directly
    tools_test = await test_patient_tools_directly()
    
    # Test 2: Test planner agent integration
    integration_test = await test_patient_agent_tools()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print(f"Patient Tools Direct Test: {'✅ PASS' if tools_test else '❌ FAIL'}")
    print(f"Planner Integration Test: {'✅ PASS' if integration_test else '❌ FAIL'}")
    
    if tools_test and integration_test:
        print("\n🎉 ALL TESTS PASSED! Patient agent should now be selectable by planner.")
    else:
        print("\n💥 SOME TESTS FAILED! Patient agent may not be properly configured.")

if __name__ == "__main__":
    asyncio.run(main())