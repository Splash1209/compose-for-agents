"""
Examples and demonstrations of the 3-Layer Framework

This module provides practical examples of how to use the 3-layer framework
with different agent systems and scenarios.
"""

import asyncio
import json
from typing import Dict, Any
from datetime import datetime

from .fact_checking import FactCheckRequest, FactCheckAuditor, FactCheckCritic, FactCheckReviser
from .adapters import A2AAdapter, ADKAdapter, A2AAgentConfig, ADKAgentConfig, UniversalAgentAdapter
from . import ThreeLayerOrchestrator


async def example_basic_framework():
    """Example using the basic 3-layer framework"""
    print("=== Basic 3-Layer Framework Example ===")
    
    # Create layer instances
    auditor = FactCheckAuditor()
    critic = FactCheckCritic()
    reviser = FactCheckReviser()
    
    # Create orchestrator
    orchestrator = ThreeLayerOrchestrator(
        top_layer=auditor,
        middle_layer=critic,
        bottom_layer=reviser
    )
    
    # Create a fact-check request
    request = FactCheckRequest(
        question="Is the universe infinite?",
        answer="The universe is infinite and has no boundaries. Scientists have proven this through extensive research.",
        context="Cosmology discussion",
        metadata={"source": "example", "timestamp": datetime.now().isoformat()}
    )
    
    print(f"Input Question: {request.question}")
    print(f"Input Answer: {request.answer}")
    print()
    
    # Execute the workflow
    result = await orchestrator.execute_workflow(request)
    
    print(f"Original Answer: {result.original_answer}")
    print(f"Revised Answer: {result.revised_answer}")
    print(f"Changes Made: {result.changes_made}")
    print(f"Revision Reasoning: {result.revision_reasoning}")
    print(f"Quality Score: {result.quality_score}")
    print()
    
    # Get execution summary
    summary = orchestrator.get_execution_summary()
    print("Execution Summary:")
    print(json.dumps(summary, indent=2, default=str))
    print()


async def example_a2a_adapter():
    """Example using A2A adapter with the framework"""
    print("=== A2A Adapter Example ===")
    
    # Configure A2A adapter
    config = A2AAgentConfig(
        auditor_url="http://localhost:8080",
        critic_url="http://localhost:8001",
        reviser_url="http://localhost:8002",
        model_name="o3",
        model_provider="openai"
    )
    
    # Create adapter
    adapter = A2AAdapter(config)
    
    # Create request
    request = FactCheckRequest(
        question="What is the capital of France?",
        answer="The capital of France is Paris, which has been the capital since 1800.",
        context="Geography question"
    )
    
    print(f"Input Question: {request.question}")
    print(f"Input Answer: {request.answer}")
    print()
    
    # Execute through adapter
    result = await adapter.execute_fact_check(request)
    
    print(f"A2A Result:")
    print(f"  Original: {result.original_answer}")
    print(f"  Revised: {result.revised_answer}")
    print(f"  Changes: {result.changes_made}")
    print(f"  Quality: {result.quality_score}")
    print()


async def example_adk_adapter():
    """Example using ADK adapter with the framework"""
    print("=== ADK Adapter Example ===")
    
    # Configure ADK adapter
    config = ADKAgentConfig(
        agent_module_path="agents.agent",
        model_endpoint="http://localhost:8080",
        mcp_gateway_endpoint="http://localhost:8811/sse"
    )
    
    # Create adapter
    adapter = ADKAdapter(config)
    
    # Create request
    request = FactCheckRequest(
        question="How many planets are in our solar system?",
        answer="There are 9 planets in our solar system, including Pluto.",
        context="Astronomy question"
    )
    
    print(f"Input Question: {request.question}")
    print(f"Input Answer: {request.answer}")
    print()
    
    # Execute through adapter
    result = await adapter.execute_fact_check(request)
    
    print(f"ADK Result:")
    print(f"  Original: {result.original_answer}")
    print(f"  Revised: {result.revised_answer}")
    print(f"  Changes: {result.changes_made}")
    print(f"  Quality: {result.quality_score}")
    print()


async def example_universal_adapter():
    """Example using the universal adapter"""
    print("=== Universal Adapter Example ===")
    
    # Test with A2A
    a2a_config = A2AAgentConfig(
        auditor_url="http://localhost:8080",
        critic_url="http://localhost:8001", 
        reviser_url="http://localhost:8002",
        model_name="o3",
        model_provider="openai"
    )
    
    a2a_adapter = UniversalAgentAdapter("a2a", a2a_config)
    
    # Test with ADK
    adk_config = ADKAgentConfig(
        agent_module_path="agents.agent",
        model_endpoint="http://localhost:8080",
        mcp_gateway_endpoint="http://localhost:8811/sse"
    )
    
    adk_adapter = UniversalAgentAdapter("adk", adk_config)
    
    # Create request
    request = FactCheckRequest(
        question="Is climate change real?",
        answer="Climate change is a hoax created by politicians to control the economy.",
        context="Environmental discussion"
    )
    
    print(f"Input Question: {request.question}")
    print(f"Input Answer: {request.answer}")
    print()
    
    # Test both adapters
    print("Testing A2A adapter:")
    a2a_result = await a2a_adapter.execute_fact_check(request)
    print(f"  Quality Score: {a2a_result.quality_score}")
    print(f"  Changes: {len(a2a_result.changes_made)}")
    
    print("Testing ADK adapter:")
    adk_result = await adk_adapter.execute_fact_check(request)
    print(f"  Quality Score: {adk_result.quality_score}")
    print(f"  Changes: {len(adk_result.changes_made)}")
    print()


async def example_buffer_validation():
    """Example demonstrating buffer validation between layers"""
    print("=== Buffer Validation Example ===")
    
    from . import DirectionBuffer, LayerExpectation, LayerType, ValidationStatus
    
    # Create expectations
    expectations = LayerExpectation(
        layer_type=LayerType.MIDDLE,
        input_schema={
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "answer": {"type": "string"}
            },
            "required": ["question", "answer"]
        },
        output_schema={},
        validation_rules=["must_have_question", "must_have_answer"],
        quality_requirements={"accuracy": 0.8},
        performance_constraints={"max_time": 60}
    )
    
    # Create a valid buffer
    valid_buffer = DirectionBuffer(
        source_layer=LayerType.TOP,
        target_layer=LayerType.MIDDLE,
        expectations=expectations,
        data={"question": "What is AI?", "answer": "AI is artificial intelligence."},
        metadata={"created_at": datetime.now().isoformat()},
        validation_results=[]
    )
    
    # Validate the buffer
    validation_result = valid_buffer.validate()
    
    print("Valid Buffer Validation:")
    print(f"  Status: {validation_result.status.value}")
    print(f"  Message: {validation_result.message}")
    print(f"  Data Size: {validation_result.data_size}")
    print()
    
    # Create an invalid buffer
    invalid_buffer = DirectionBuffer(
        source_layer=LayerType.TOP,
        target_layer=LayerType.MIDDLE,
        expectations=expectations,
        data={"question": ""},  # Missing required answer field
        metadata={"created_at": datetime.now().isoformat()},
        validation_results=[]
    )
    
    # This would fail validation in a real implementation
    validation_result = invalid_buffer.validate()
    
    print("Buffer with Missing Data:")
    print(f"  Status: {validation_result.status.value}")
    print(f"  Message: {validation_result.message}")
    print()


async def example_layer_expectations():
    """Example showing how layer expectations work"""
    print("=== Layer Expectations Example ===")
    
    # Create auditor with specific expectations
    auditor = FactCheckAuditor()
    
    print("Auditor Layer Expectations:")
    print(f"  Input Schema: {auditor.expectations.input_schema}")
    print(f"  Validation Rules: {auditor.expectations.validation_rules}")
    print(f"  Quality Requirements: {auditor.expectations.quality_requirements}")
    print(f"  Performance Constraints: {auditor.expectations.performance_constraints}")
    print()
    
    print("Middle Layer Requirements (set by Auditor):")
    print(f"  Requirements: {auditor.middle_layer_requirements}")
    print()
    
    print("Bottom Layer Requirements (set by Auditor):")
    print(f"  Requirements: {auditor.bottom_layer_requirements}")
    print()
    
    # Create critic and show it can validate requirements
    critic = FactCheckCritic()
    can_meet_requirements = critic.validate_requirements(auditor.middle_layer_requirements)
    print(f"Critic can meet Auditor requirements: {can_meet_requirements}")
    print()


async def run_all_examples():
    """Run all examples to demonstrate the framework"""
    print("🚀 3-Layer Framework Examples\n")
    
    try:
        await example_basic_framework()
        await example_a2a_adapter()
        await example_adk_adapter()
        await example_universal_adapter()
        await example_buffer_validation()
        await example_layer_expectations()
        
        print("✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run examples
    asyncio.run(run_all_examples())