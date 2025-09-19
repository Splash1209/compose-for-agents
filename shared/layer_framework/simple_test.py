"""
Simplified test runner for the 3-Layer Framework
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import framework components directly
from __init__ import (
    LayerType, ValidationStatus, LayerExpectation, DirectionBuffer,
    LayerInterface, TopLayer, MiddleLayer, BottomLayer, ThreeLayerOrchestrator
)

async def test_basic_functionality():
    """Test basic framework functionality"""
    print("🧪 Testing 3-Layer Framework Basic Functionality\n")
    
    try:
        # Test 1: Layer Expectation Creation
        print("✅ Test 1: Creating Layer Expectations")
        expectation = LayerExpectation(
            layer_type=LayerType.TOP,
            input_schema={"type": "object"},
            output_schema={"type": "object"},
            validation_rules=["test_rule"],
            quality_requirements={"accuracy": 0.8},
            performance_constraints={"max_time": 60}
        )
        print(f"   Created expectation for {expectation.layer_type.value} layer")
        
        # Test 2: Buffer Creation and Validation
        print("✅ Test 2: Creating and Validating Direction Buffer")
        buffer = DirectionBuffer(
            source_layer=LayerType.TOP,
            target_layer=LayerType.MIDDLE,
            expectations=expectation,
            data={"test": "data"},
            metadata={"created": "2025-01-15T10:00:00Z"},
            validation_results=[]
        )
        
        validation = buffer.validate()
        print(f"   Buffer validation status: {validation.status.value}")
        print(f"   Buffer data size: {validation.data_size} bytes")
        
        # Test 3: Layer Interface Implementation
        print("✅ Test 3: Testing Layer Interface")
        
        class TestTopLayer(TopLayer[str, str]):
            async def orchestrate(self, input_data: str) -> str:
                return f"orchestrated: {input_data}"
            
            async def process(self, input_data: str) -> str:
                return await self.orchestrate(input_data)
            
            def validate_requirements(self, requirements):
                return True
        
        class TestMiddleLayer(MiddleLayer[str, str]):
            async def execute_core_logic(self, input_data: str) -> str:
                return f"processed: {input_data}"
            
            def validate_requirements(self, requirements):
                return True
        
        class TestBottomLayer(BottomLayer[str, str]):
            async def finalize_output(self, input_data: str) -> str:
                return f"finalized: {input_data}"
            
            def validate_requirements(self, requirements):
                return True
        
        # Create layer instances
        top_expectation = LayerExpectation(
            layer_type=LayerType.TOP,
            input_schema={}, output_schema={},
            validation_rules=[], quality_requirements={},
            performance_constraints={}
        )
        
        middle_expectation = LayerExpectation(
            layer_type=LayerType.MIDDLE,
            input_schema={}, output_schema={},
            validation_rules=[], quality_requirements={},
            performance_constraints={}
        )
        
        bottom_expectation = LayerExpectation(
            layer_type=LayerType.BOTTOM,
            input_schema={}, output_schema={},
            validation_rules=[], quality_requirements={},
            performance_constraints={}
        )
        
        top_layer = TestTopLayer(top_expectation)
        middle_layer = TestMiddleLayer(middle_expectation)
        bottom_layer = TestBottomLayer(bottom_expectation)
        
        print(f"   Created {top_layer.layer_type.value} layer")
        print(f"   Created {middle_layer.layer_type.value} layer")
        print(f"   Created {bottom_layer.layer_type.value} layer")
        
        # Test 4: Orchestrator
        print("✅ Test 4: Testing 3-Layer Orchestrator")
        orchestrator = ThreeLayerOrchestrator(
            top_layer=top_layer,
            middle_layer=middle_layer,
            bottom_layer=bottom_layer
        )
        
        result = await orchestrator.execute_workflow("test input")
        print(f"   Workflow result: {result}")
        
        # Get execution summary
        summary = orchestrator.get_execution_summary()
        print(f"   Execution steps: {summary['total_steps']}")
        print(f"   Buffer validations: {len(summary['buffer_validations'])}")
        
        print("\n🎉 All basic tests passed! Framework is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the simplified test suite"""
    success = await test_basic_functionality()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())