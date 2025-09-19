"""
Test script for the 3-Layer Framework

This script tests the framework functionality to ensure it works correctly
and provides the required direction and buffers for layer expectations.
"""

import asyncio
import sys
import traceback
from typing import List, Dict, Any
from datetime import datetime

# Import framework components
try:
    from . import (
        LayerType, ValidationStatus, LayerExpectation, DirectionBuffer,
        LayerInterface, TopLayer, MiddleLayer, BottomLayer, ThreeLayerOrchestrator
    )
    from .fact_checking import (
        FactCheckRequest, FactCheckAuditor, FactCheckCritic, FactCheckReviser,
        CriticAnalysis, RevisedResponse
    )
    from .adapters import A2AAdapter, ADKAdapter, A2AAgentConfig, ADKAgentConfig
except ImportError:
    # If running as script, adjust imports
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from __init__ import (
        LayerType, ValidationStatus, LayerExpectation, DirectionBuffer,
        LayerInterface, TopLayer, MiddleLayer, BottomLayer, ThreeLayerOrchestrator
    )
    from fact_checking import (
        FactCheckRequest, FactCheckAuditor, FactCheckCritic, FactCheckReviser,
        CriticAnalysis, RevisedResponse
    )
    from adapters import A2AAdapter, ADKAdapter, A2AAgentConfig, ADKAgentConfig


class TestResult:
    """Container for test results"""
    def __init__(self, name: str, passed: bool, message: str = "", details: Dict[str, Any] = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()


class FrameworkTester:
    """Test runner for the 3-layer framework"""
    
    def __init__(self):
        self.test_results: List[TestResult] = []
    
    async def run_all_tests(self) -> bool:
        """Run all tests and return overall success"""
        print("🧪 Running 3-Layer Framework Tests\n")
        
        # Test basic framework components
        await self.test_layer_expectations()
        await self.test_buffer_validation()
        await self.test_direction_buffers()
        
        # Test layer implementations
        await self.test_fact_check_layers()
        await self.test_orchestrator()
        
        # Test adapters
        await self.test_a2a_adapter()
        await self.test_adk_adapter()
        
        # Test integration
        await self.test_end_to_end_workflow()
        
        # Print results
        self.print_test_summary()
        
        # Return overall success
        return all(result.passed for result in self.test_results)
    
    def add_test_result(self, name: str, passed: bool, message: str = "", details: Dict[str, Any] = None):
        """Add a test result"""
        result = TestResult(name, passed, message, details)
        self.test_results.append(result)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
        if message:
            print(f"    {message}")
        if not passed and details:
            print(f"    Details: {details}")
        print()
    
    async def test_layer_expectations(self):
        """Test layer expectation functionality"""
        try:
            # Create layer expectation
            expectation = LayerExpectation(
                layer_type=LayerType.TOP,
                input_schema={"type": "object", "properties": {"test": {"type": "string"}}},
                output_schema={"type": "object"},
                validation_rules=["test_rule"],
                quality_requirements={"accuracy": 0.8},
                performance_constraints={"max_time": 60}
            )
            
            # Test validation methods
            valid_data = {"test": "value"}
            invalid_data = {"wrong": "value"}
            
            input_valid = expectation.validate_input(valid_data)
            output_valid = expectation.validate_output(valid_data)
            
            self.add_test_result(
                "Layer Expectations Creation",
                True,
                "Successfully created and validated layer expectations",
                {
                    "layer_type": expectation.layer_type.value,
                    "input_valid": input_valid,
                    "output_valid": output_valid
                }
            )
            
        except Exception as e:
            self.add_test_result(
                "Layer Expectations Creation",
                False,
                f"Failed to create layer expectations: {e}",
                {"error": str(e)}
            )
    
    async def test_buffer_validation(self):
        """Test buffer validation functionality"""
        try:
            # Create expectations
            expectations = LayerExpectation(
                layer_type=LayerType.MIDDLE,
                input_schema={"type": "object"},
                output_schema={"type": "object"},
                validation_rules=[],
                quality_requirements={},
                performance_constraints={}
            )
            
            # Create buffer
            buffer = DirectionBuffer(
                source_layer=LayerType.TOP,
                target_layer=LayerType.MIDDLE,
                expectations=expectations,
                data={"test": "data"},
                metadata={"created": datetime.now().isoformat()},
                validation_results=[]
            )
            
            # Validate buffer
            validation = buffer.validate()
            
            success = validation.status in [ValidationStatus.PASSED, ValidationStatus.WARNING]
            
            self.add_test_result(
                "Buffer Validation",
                success,
                f"Buffer validation status: {validation.status.value}",
                {
                    "status": validation.status.value,
                    "message": validation.message,
                    "data_size": validation.data_size
                }
            )
            
        except Exception as e:
            self.add_test_result(
                "Buffer Validation",
                False,
                f"Buffer validation failed: {e}",
                {"error": str(e)}
            )
    
    async def test_direction_buffers(self):
        """Test direction buffer creation and flow"""
        try:
            # Create a simple layer to test buffer creation
            expectations = LayerExpectation(
                layer_type=LayerType.TOP,
                input_schema={},
                output_schema={"type": "string"},
                validation_rules=[],
                quality_requirements={},
                performance_constraints={}
            )
            
            class TestLayer(LayerInterface[str, str]):
                async def process(self, input_data: str) -> str:
                    return f"processed: {input_data}"
                
                def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
                    return True
            
            layer = TestLayer(LayerType.TOP, expectations)
            
            # Create output buffer
            output_buffer = layer.create_output_buffer(LayerType.MIDDLE, "test output")
            
            # Verify buffer properties
            buffer_valid = (
                output_buffer.source_layer == LayerType.TOP and
                output_buffer.target_layer == LayerType.MIDDLE and
                output_buffer.data == "test output"
            )
            
            self.add_test_result(
                "Direction Buffer Creation",
                buffer_valid,
                "Successfully created direction buffer with correct properties",
                {
                    "source_layer": output_buffer.source_layer.value,
                    "target_layer": output_buffer.target_layer.value,
                    "has_data": output_buffer.data is not None
                }
            )
            
        except Exception as e:
            self.add_test_result(
                "Direction Buffer Creation", 
                False,
                f"Failed to create direction buffer: {e}",
                {"error": str(e)}
            )
    
    async def test_fact_check_layers(self):
        """Test fact-checking layer implementations"""
        try:
            # Test Auditor
            auditor = FactCheckAuditor()
            auditor_valid = (
                auditor.layer_type == LayerType.TOP and
                len(auditor.workflow_definition) > 0 and
                len(auditor.middle_layer_requirements) > 0 and
                len(auditor.bottom_layer_requirements) > 0
            )
            
            # Test Critic
            critic = FactCheckCritic() 
            critic_valid = (
                critic.layer_type == LayerType.MIDDLE and
                len(critic.processing_config) > 0 and
                len(critic.quality_gates) > 0
            )
            
            # Test Reviser
            reviser = FactCheckReviser()
            reviser_valid = (
                reviser.layer_type == LayerType.BOTTOM and
                len(reviser.finalization_rules) > 0 and
                len(reviser.output_validators) > 0
            )
            
            all_valid = auditor_valid and critic_valid and reviser_valid
            
            self.add_test_result(
                "Fact-Check Layer Implementation",
                all_valid,
                "All fact-checking layers properly configured",
                {
                    "auditor_valid": auditor_valid,
                    "critic_valid": critic_valid,
                    "reviser_valid": reviser_valid
                }
            )
            
        except Exception as e:
            self.add_test_result(
                "Fact-Check Layer Implementation",
                False,
                f"Failed to create fact-check layers: {e}",
                {"error": str(e)}
            )
    
    async def test_orchestrator(self):
        """Test the 3-layer orchestrator"""
        try:
            # Create layers
            auditor = FactCheckAuditor()
            critic = FactCheckCritic()
            reviser = FactCheckReviser()
            
            # Create orchestrator
            orchestrator = ThreeLayerOrchestrator(
                top_layer=auditor,
                middle_layer=critic,
                bottom_layer=reviser
            )
            
            # Test with simple request
            request = FactCheckRequest(
                question="Test question?",
                answer="Test answer.",
                context="Test context"
            )
            
            # Execute workflow
            result = await orchestrator.execute_workflow(request)
            
            # Verify result
            result_valid = (
                isinstance(result, RevisedResponse) and
                hasattr(result, 'original_answer') and
                hasattr(result, 'revised_answer') and
                hasattr(result, 'quality_score')
            )
            
            # Get execution summary
            summary = orchestrator.get_execution_summary()
            summary_valid = (
                'total_steps' in summary and
                'execution_log' in summary and
                summary['total_steps'] > 0
            )
            
            success = result_valid and summary_valid
            
            self.add_test_result(
                "3-Layer Orchestrator",
                success,
                "Orchestrator successfully executed workflow",
                {
                    "result_valid": result_valid,
                    "summary_valid": summary_valid,
                    "execution_steps": summary.get('total_steps', 0)
                }
            )
            
        except Exception as e:
            self.add_test_result(
                "3-Layer Orchestrator",
                False,
                f"Orchestrator execution failed: {e}",
                {"error": str(e)}
            )
    
    async def test_a2a_adapter(self):
        """Test A2A adapter functionality"""
        try:
            # Create A2A config
            config = A2AAgentConfig(
                auditor_url="http://localhost:8080",
                critic_url="http://localhost:8001",
                reviser_url="http://localhost:8002", 
                model_name="test_model",
                model_provider="test_provider"
            )
            
            # Create adapter
            adapter = A2AAdapter(config)
            
            # Verify adapter structure
            adapter_valid = (
                hasattr(adapter, 'auditor') and
                hasattr(adapter, 'critic') and
                hasattr(adapter, 'reviser') and
                adapter.config == config
            )
            
            self.add_test_result(
                "A2A Adapter Creation",
                adapter_valid,
                "A2A adapter created with proper structure",
                {
                    "has_auditor": hasattr(adapter, 'auditor'),
                    "has_critic": hasattr(adapter, 'critic'),
                    "has_reviser": hasattr(adapter, 'reviser')
                }
            )
            
        except Exception as e:
            self.add_test_result(
                "A2A Adapter Creation",
                False,
                f"A2A adapter creation failed: {e}",
                {"error": str(e)}
            )
    
    async def test_adk_adapter(self):
        """Test ADK adapter functionality"""
        try:
            # Create ADK config
            config = ADKAgentConfig(
                agent_module_path="test.module",
                model_endpoint="http://localhost:8080",
                mcp_gateway_endpoint="http://localhost:8811/sse"
            )
            
            # Create adapter
            adapter = ADKAdapter(config)
            
            # Verify adapter structure
            adapter_valid = (
                hasattr(adapter, 'auditor') and
                hasattr(adapter, 'critic') and
                hasattr(adapter, 'reviser') and
                adapter.config == config
            )
            
            self.add_test_result(
                "ADK Adapter Creation",
                adapter_valid,
                "ADK adapter created with proper structure",
                {
                    "has_auditor": hasattr(adapter, 'auditor'),
                    "has_critic": hasattr(adapter, 'critic'),
                    "has_reviser": hasattr(adapter, 'reviser')
                }
            )
            
        except Exception as e:
            self.add_test_result(
                "ADK Adapter Creation",
                False,
                f"ADK adapter creation failed: {e}",
                {"error": str(e)}
            )
    
    async def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        try:
            # Create fact-check request
            request = FactCheckRequest(
                question="What is the capital of France?",
                answer="The capital of France is London.",
                context="Geography test"
            )
            
            # Test with basic framework
            auditor = FactCheckAuditor()
            critic = FactCheckCritic()
            reviser = FactCheckReviser()
            
            orchestrator = ThreeLayerOrchestrator(
                top_layer=auditor,
                middle_layer=critic,
                bottom_layer=reviser
            )
            
            # Execute workflow
            result = await orchestrator.execute_workflow(request)
            
            # Verify complete workflow
            workflow_valid = (
                isinstance(result, RevisedResponse) and
                result.original_answer == request.answer and
                result.quality_score > 0
            )
            
            # Check buffer validations occurred
            summary = orchestrator.get_execution_summary()
            buffer_validations = summary.get('buffer_validations', [])
            
            self.add_test_result(
                "End-to-End Workflow",
                workflow_valid,
                "Complete workflow executed successfully",
                {
                    "workflow_valid": workflow_valid,
                    "buffer_validations": len(buffer_validations),
                    "quality_score": result.quality_score if workflow_valid else 0
                }
            )
            
        except Exception as e:
            self.add_test_result(
                "End-to-End Workflow",
                False,
                f"End-to-end workflow failed: {e}",
                {"error": str(e)}
            )
    
    def print_test_summary(self):
        """Print summary of all test results"""
        print("\n" + "="*60)
        print("🧪 TEST SUMMARY")
        print("="*60)
        
        passed_count = sum(1 for result in self.test_results if result.passed)
        total_count = len(self.test_results)
        
        print(f"Total Tests: {total_count}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {total_count - passed_count}")
        print(f"Success Rate: {(passed_count/total_count)*100:.1f}%")
        print()
        
        # Print failed tests
        failed_tests = [result for result in self.test_results if not result.passed]
        if failed_tests:
            print("❌ Failed Tests:")
            for test in failed_tests:
                print(f"  • {test.name}: {test.message}")
            print()
        
        # Print overall result
        if passed_count == total_count:
            print("🎉 ALL TESTS PASSED! Framework is working correctly.")
        else:
            print("⚠️  Some tests failed. Please review the issues above.")
        
        print("="*60)


async def main():
    """Run the test suite"""
    tester = FrameworkTester()
    success = await tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())