"""
Integration Example: Using the 3-Layer Framework with A2A and ADK

This example shows how to integrate the new framework with existing agent systems
while maintaining backward compatibility and adding the new direction and buffer capabilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from __init__ import LayerType, LayerExpectation, ThreeLayerOrchestrator
from fact_checking import FactCheckRequest, FactCheckAuditor, FactCheckCritic, FactCheckReviser
import asyncio
import json
from datetime import datetime


async def demonstrate_enhanced_fact_checking():
    """Demonstrate the enhanced fact-checking with direction and buffers"""
    print("🚀 Enhanced 3-Layer Fact-Checking Framework Demo")
    print("=" * 60)
    
    # Create the enhanced fact-checking system
    auditor = FactCheckAuditor()
    critic = FactCheckCritic() 
    reviser = FactCheckReviser()
    
    print("📋 Layer Configuration:")
    print(f"  Top Layer (Auditor): {auditor.layer_type.value}")
    print(f"    - Workflow steps: {len(auditor.workflow_definition.get('steps', []))}")
    print(f"    - Quality gates: {auditor.workflow_definition.get('quality_gates', [])}")
    print(f"    - Middle layer requirements: {list(auditor.middle_layer_requirements.keys())}")
    print(f"    - Bottom layer requirements: {list(auditor.bottom_layer_requirements.keys())}")
    
    print(f"  Middle Layer (Critic): {critic.layer_type.value}")
    print(f"    - Processing config keys: {list(critic.processing_config.keys())}")
    print(f"    - Quality gates: {critic.quality_gates}")
    print(f"    - Performance constraints: {list(critic.expectations.performance_constraints.keys())}")
    
    print(f"  Bottom Layer (Reviser): {reviser.layer_type.value}")
    print(f"    - Finalization rules: {reviser.finalization_rules}")
    print(f"    - Output validators: {reviser.output_validators}")
    print()
    
    # Create orchestrator
    orchestrator = ThreeLayerOrchestrator(
        top_layer=auditor,
        middle_layer=critic,
        bottom_layer=reviser
    )
    
    # Test case 1: Accurate information
    print("📝 Test Case 1: Processing accurate information")
    request1 = FactCheckRequest(
        question="What is the capital of France?",
        answer="The capital of France is Paris, which has been the capital since 987 AD.",
        context="Geography question",
        metadata={"test_case": "accurate_info"}
    )
    
    result1 = await orchestrator.execute_workflow(request1)
    print(f"  Input: {request1.answer}")
    print(f"  Output: {result1.revised_answer}")
    print(f"  Quality Score: {result1.quality_score}")
    print(f"  Changes Made: {len(result1.changes_made)}")
    print()
    
    # Test case 2: Inaccurate information
    print("📝 Test Case 2: Processing inaccurate information")
    request2 = FactCheckRequest(
        question="How many planets are in our solar system?",
        answer="There are 9 planets in our solar system, including Pluto which is the largest.",
        context="Astronomy question",
        metadata={"test_case": "inaccurate_info"}
    )
    
    result2 = await orchestrator.execute_workflow(request2)
    print(f"  Input: {request2.answer}")
    print(f"  Output: {result2.revised_answer}")
    print(f"  Quality Score: {result2.quality_score}")
    print(f"  Changes Made: {len(result2.changes_made)}")
    print()
    
    # Show execution details
    summary = orchestrator.get_execution_summary()
    print("📊 Execution Summary:")
    print(f"  Total Steps: {summary['total_steps']}")
    print(f"  Buffer Validations: {len(summary['buffer_validations'])}")
    
    for i, log_entry in enumerate(summary['execution_log']):
        print(f"  Step {i+1}: {log_entry['event']} - {log_entry['details']}")
    print()
    
    # Show buffer validation details
    if summary['buffer_validations']:
        print("🔍 Buffer Validation Details:")
        for validation in summary['buffer_validations']:
            buffer_name = validation['buffer']
            status = validation['validation']['status']
            message = validation['validation']['message']
            print(f"  {buffer_name}: {status} - {message}")
    print()


async def demonstrate_framework_benefits():
    """Demonstrate the key benefits of the framework"""
    print("🎯 Framework Benefits Demonstration")
    print("=" * 60)
    
    # Benefit 1: Clear Layer Expectations
    print("✅ Benefit 1: Clear Layer Expectations")
    auditor = FactCheckAuditor()
    
    expectations = auditor.expectations
    print(f"  Input Schema Requirements: {list(expectations.input_schema.get('properties', {}).keys())}")
    print(f"  Validation Rules: {expectations.validation_rules}")
    print(f"  Quality Requirements: {expectations.quality_requirements}")
    print(f"  Performance Constraints: {expectations.performance_constraints}")
    print()
    
    # Benefit 2: Direction and Buffers
    print("✅ Benefit 2: Direction and Buffer Management")
    from __init__ import DirectionBuffer
    
    # Create a sample buffer
    buffer = DirectionBuffer(
        source_layer=LayerType.TOP,
        target_layer=LayerType.MIDDLE,
        expectations=expectations,
        data={"question": "Test?", "answer": "Test answer."},
        metadata={"timestamp": datetime.now().isoformat()},
        validation_results=[]
    )
    
    validation = buffer.validate()
    print(f"  Buffer Direction: {buffer.source_layer.value} → {buffer.target_layer.value}")
    print(f"  Validation Status: {validation.status.value}")
    print(f"  Data Size: {validation.data_size} bytes")
    print(f"  Validation Message: {validation.message}")
    print()
    
    # Benefit 3: Quality Assurance
    print("✅ Benefit 3: Quality Assurance at Every Layer")
    critic = FactCheckCritic()
    
    print(f"  Critic Quality Gates: {critic.quality_gates}")
    print(f"  Processing Quality Requirements: {critic.expectations.quality_requirements}")
    
    reviser = FactCheckReviser()
    print(f"  Reviser Finalization Rules: {reviser.finalization_rules}")
    print(f"  Reviser Output Validators: {reviser.output_validators}")
    print()
    
    # Benefit 4: Standardized Architecture
    print("✅ Benefit 4: Standardized Architecture")
    print(f"  All layers implement LayerInterface with consistent methods:")
    print(f"    - process(input_data) -> output_data")
    print(f"    - validate_requirements(requirements) -> bool")
    print(f"    - set_input_buffer(buffer) -> None")
    print(f"    - create_output_buffer(target_layer, data) -> DirectionBuffer")
    print()


async def demonstrate_integration_patterns():
    """Demonstrate how to integrate with existing systems"""
    print("🔗 Integration Patterns")
    print("=" * 60)
    
    # Pattern 1: Wrapping Existing Agents
    print("🏗️  Pattern 1: Wrapping Existing Agents")
    print("   For A2A agents:")
    print("   - AuditorAgent → FactCheckAuditor (Top Layer)")
    print("   - CriticAgent → FactCheckCritic (Middle Layer)")
    print("   - ReviserAgent → FactCheckReviser (Bottom Layer)")
    print()
    
    print("   For ADK agents:")
    print("   - llm_auditor (SequentialAgent) → FactCheckAuditor (Top Layer)")
    print("   - critic_agent → FactCheckCritic (Middle Layer)")
    print("   - reviser_agent → FactCheckReviser (Bottom Layer)")
    print()
    
    # Pattern 2: Adding Framework Benefits
    print("🚀 Pattern 2: Adding Framework Benefits")
    print("   Benefits added to existing systems:")
    print("   ✅ Clear layer expectations and requirements")
    print("   ✅ Direction buffers with validation")
    print("   ✅ Quality gates and performance monitoring")
    print("   ✅ Standardized error handling")
    print("   ✅ Execution logging and debugging")
    print()
    
    # Pattern 3: Maintaining Backward Compatibility
    print("🔄 Pattern 3: Maintaining Backward Compatibility")
    print("   Existing systems continue to work while gaining:")
    print("   - Enhanced validation and quality assurance")
    print("   - Better monitoring and debugging capabilities")
    print("   - Standardized interfaces for future development")
    print("   - Integration with other framework-based systems")
    print()


async def main():
    """Run all demonstrations"""
    try:
        await demonstrate_enhanced_fact_checking()
        await demonstrate_framework_benefits()
        await demonstrate_integration_patterns()
        
        print("🎉 All demonstrations completed successfully!")
        print("\nThe 3-Layer Framework provides:")
        print("  ✅ Clear direction and expectations between layers")
        print("  ✅ Validation buffers for data flow")
        print("  ✅ Quality assurance at every step")
        print("  ✅ Standardized architecture for multi-agent systems")
        print("  ✅ Easy integration with existing agent frameworks")
        
    except Exception as e:
        print(f"❌ Error in demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())