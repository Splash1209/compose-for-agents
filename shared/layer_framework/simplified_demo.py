"""
Simplified Integration Demo

This demo shows the key features of the 3-layer framework without import issues.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from __init__ import (
    LayerType, LayerExpectation, DirectionBuffer, ValidationStatus,
    TopLayer, MiddleLayer, BottomLayer, ThreeLayerOrchestrator
)
import asyncio
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class FactCheckRequest:
    """Simple fact check request"""
    question: str
    answer: str
    context: str = ""


@dataclass 
class FactCheckResult:
    """Simple fact check result"""
    original_answer: str
    revised_answer: str
    changes_made: List[str]
    quality_score: float


class SimpleAuditor(TopLayer[FactCheckRequest, FactCheckResult]):
    """Simple auditor implementation"""
    
    def __init__(self):
        expectations = LayerExpectation(
            layer_type=LayerType.TOP,
            input_schema={
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"}
                },
                "required": ["question", "answer"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "original_answer": {"type": "string"},
                    "revised_answer": {"type": "string"},
                    "quality_score": {"type": "number"}
                }
            },
            validation_rules=["question_not_empty", "answer_not_empty"],
            quality_requirements={"accuracy": 0.8, "completeness": 0.9},
            performance_constraints={"max_time": 300}
        )
        
        super().__init__(expectations)
        
        # Define workflow
        self.define_workflow({
            "steps": ["analyze_claims", "verify_facts", "revise_answer"],
            "quality_gates": ["accuracy_check", "completeness_check"]
        })
        
        # Set layer requirements
        self.set_middle_layer_requirements({
            "claim_extraction": "comprehensive",
            "fact_verification": "multi_source",
            "confidence_threshold": 0.7
        })
        
        self.set_bottom_layer_requirements({
            "revision_style": "preserve_original",
            "quality_threshold": 0.8,
            "justification_required": True
        })
    
    async def orchestrate(self, input_data: FactCheckRequest) -> FactCheckResult:
        """Orchestrate the fact-checking process"""
        print(f"🎯 AUDITOR: Orchestrating fact-check for: '{input_data.question}'")
        print(f"   Requirements for Critic: {list(self.middle_layer_requirements.keys())}")
        print(f"   Requirements for Reviser: {list(self.bottom_layer_requirements.keys())}")
        
        # Mock orchestration result
        return FactCheckResult(
            original_answer=input_data.answer,
            revised_answer=input_data.answer,  # Would be revised by actual workflow
            changes_made=[],
            quality_score=0.9
        )
    
    async def process(self, input_data: FactCheckRequest) -> FactCheckResult:
        """Process the input through orchestration"""
        return await self.orchestrate(input_data)
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
        required_fields = ["question", "answer"]
        return all(field in requirements for field in required_fields)


class SimpleCritic(MiddleLayer[FactCheckRequest, str]):
    """Simple critic implementation"""
    
    def __init__(self):
        expectations = LayerExpectation(
            layer_type=LayerType.MIDDLE,
            input_schema={
                "type": "object",
                "properties": {"question": {"type": "string"}, "answer": {"type": "string"}}
            },
            output_schema={"type": "string"},
            validation_rules=["claims_extractable", "sources_accessible"],
            quality_requirements={"evidence_quality": 0.7, "source_credibility": 0.6},
            performance_constraints={"max_search_time": 180}
        )
        
        super().__init__(expectations)
        
        # Configure processing
        self.configure_processing({
            "claim_extraction": "nlp_based",
            "search_strategy": "multi_source",
            "verification_method": "cross_reference"
        })
        
        # Add quality gates
        self.add_quality_gate("sufficient_evidence")
        self.add_quality_gate("credible_sources")
        self.add_quality_gate("claim_coverage")
    
    async def execute_core_logic(self, input_data: FactCheckRequest) -> str:
        """Execute critic analysis"""
        print(f"🔍 CRITIC: Analyzing claims in answer to: '{input_data.question}'")
        print(f"   Processing config: {list(self.processing_config.keys())}")
        print(f"   Quality gates: {self.quality_gates}")
        
        # Simulate claim analysis
        analysis = f"Analysis of '{input_data.answer}' - Found 2 claims, verified with 3 sources"
        print(f"   Analysis result: {analysis}")
        
        return analysis
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
        return "claim_extraction" in requirements


class SimpleReviser(BottomLayer[str, FactCheckResult]):
    """Simple reviser implementation"""
    
    def __init__(self):
        expectations = LayerExpectation(
            layer_type=LayerType.BOTTOM,
            input_schema={"type": "string"},
            output_schema={
                "type": "object",
                "properties": {
                    "revised_answer": {"type": "string"},
                    "quality_score": {"type": "number"}
                }
            },
            validation_rules=["revisions_justified", "style_preserved"],
            quality_requirements={"accuracy_improvement": 0.1, "readability": 0.9},
            performance_constraints={"max_revision_time": 60}
        )
        
        super().__init__(expectations)
        
        # Add finalization rules
        self.add_finalization_rule("preserve_structure")
        self.add_finalization_rule("improve_accuracy")
        self.add_finalization_rule("maintain_style")
        
        # Add output validators
        self.add_output_validator("grammar_check")
        self.add_output_validator("accuracy_check")
        self.add_output_validator("completeness_check")
    
    async def finalize_output(self, input_data: str) -> FactCheckResult:
        """Finalize the revised output"""
        print(f"✏️  REVISER: Finalizing based on analysis: '{input_data[:50]}...'")
        print(f"   Finalization rules: {self.finalization_rules}")
        print(f"   Output validators: {self.output_validators}")
        
        # Mock finalization
        result = FactCheckResult(
            original_answer="Original answer",
            revised_answer="Revised answer with corrections",
            changes_made=["Fixed inaccurate claim", "Added source reference"],
            quality_score=0.92
        )
        
        print(f"   Final quality score: {result.quality_score}")
        return result
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
        return "quality_threshold" in requirements


async def demonstrate_3_layer_framework():
    """Demonstrate the complete 3-layer framework"""
    print("🚀 3-Layer Framework with Direction and Buffers Demo")
    print("=" * 70)
    
    # Create the three layers
    auditor = SimpleAuditor()
    critic = SimpleCritic()
    reviser = SimpleReviser()
    
    print("📋 Layer Configuration:")
    print(f"  🎯 Top Layer (Auditor): {auditor.layer_type.value}")
    print(f"     - Workflow steps: {auditor.workflow_definition.get('steps', [])}")
    print(f"     - Quality requirements: {auditor.expectations.quality_requirements}")
    
    print(f"  🔍 Middle Layer (Critic): {critic.layer_type.value}")
    print(f"     - Quality gates: {critic.quality_gates}")
    print(f"     - Performance constraints: {critic.expectations.performance_constraints}")
    
    print(f"  ✏️  Bottom Layer (Reviser): {reviser.layer_type.value}")
    print(f"     - Finalization rules: {reviser.finalization_rules}")
    print(f"     - Output validators: {reviser.output_validators}")
    print()
    
    # Create orchestrator
    orchestrator = ThreeLayerOrchestrator(
        top_layer=auditor,
        middle_layer=critic,
        bottom_layer=reviser
    )
    
    # Test the workflow
    print("📝 Testing Workflow with Direction and Buffers:")
    request = FactCheckRequest(
        question="Is the Earth flat?",
        answer="The Earth is flat and NASA is hiding the truth from us.",
        context="Scientific discussion"
    )
    
    print(f"   Input Question: {request.question}")
    print(f"   Input Answer: {request.answer}")
    print()
    
    # Execute workflow
    result = await orchestrator.execute_workflow(request)
    
    print("📊 Workflow Results:")
    print(f"   Original: {result.original_answer}")
    print(f"   Revised: {result.revised_answer}")
    print(f"   Changes: {result.changes_made}")
    print(f"   Quality Score: {result.quality_score}")
    print()
    
    # Show execution summary
    summary = orchestrator.get_execution_summary()
    print("📈 Execution Summary:")
    print(f"   Total Steps: {summary['total_steps']}")
    print(f"   Buffer Validations: {len(summary['buffer_validations'])}")
    
    for i, log_entry in enumerate(summary['execution_log']):
        print(f"   Step {i+1}: {log_entry['event']} - {log_entry['details']}")
    print()
    
    # Show buffer validation details
    if summary['buffer_validations']:
        print("🔍 Buffer Validation Details:")
        for validation in summary['buffer_validations']:
            buffer_name = validation['buffer']
            val_info = validation['validation']
            status = val_info['status']
            message = val_info['message']
            print(f"   {buffer_name}: {status} - {message}")
        print()
    
    return True


async def demonstrate_framework_benefits():
    """Show the key benefits provided by the framework"""
    print("🎯 Framework Benefits")
    print("=" * 70)
    
    print("✅ Benefit 1: Clear Layer Expectations")
    auditor = SimpleAuditor()
    expectations = auditor.expectations
    print(f"   - Input requirements: {list(expectations.input_schema.get('properties', {}).keys())}")
    print(f"   - Validation rules: {expectations.validation_rules}")
    print(f"   - Quality thresholds: {expectations.quality_requirements}")
    print(f"   - Performance limits: {expectations.performance_constraints}")
    print()
    
    print("✅ Benefit 2: Direction Buffers with Validation")
    buffer = DirectionBuffer(
        source_layer=LayerType.TOP,
        target_layer=LayerType.MIDDLE,
        expectations=expectations,
        data={"question": "Test?", "answer": "Test answer"},
        metadata={"timestamp": datetime.now().isoformat()},
        validation_results=[]
    )
    
    validation = buffer.validate()
    print(f"   - Buffer direction: {buffer.source_layer.value} → {buffer.target_layer.value}")
    print(f"   - Validation status: {validation.status.value}")
    print(f"   - Data size: {validation.data_size} bytes")
    print(f"   - Validation time: {validation.timestamp}")
    print()
    
    print("✅ Benefit 3: Quality Assurance at Every Layer")
    critic = SimpleCritic()
    reviser = SimpleReviser()
    print(f"   - Critic quality gates: {critic.quality_gates}")
    print(f"   - Reviser finalization rules: {reviser.finalization_rules}")
    print(f"   - Reviser output validators: {reviser.output_validators}")
    print()
    
    print("✅ Benefit 4: Requirements Flow (Top → Middle → Bottom)")
    print(f"   - Auditor → Critic requirements: {list(auditor.middle_layer_requirements.keys())}")
    print(f"   - Auditor → Reviser requirements: {list(auditor.bottom_layer_requirements.keys())}")
    print(f"   - Requirements validation: {critic.validate_requirements(auditor.middle_layer_requirements)}")
    print()


async def main():
    """Run the complete demonstration"""
    try:
        success1 = await demonstrate_3_layer_framework()
        await demonstrate_framework_benefits()
        
        if success1:
            print("🎉 3-Layer Framework Successfully Demonstrates:")
            print("   ✅ Clear direction and expectations between layers")
            print("   ✅ Validation buffers for secure data flow")
            print("   ✅ Quality assurance at every processing step")
            print("   ✅ Requirements definition and validation")
            print("   ✅ Standardized architecture for multi-agent systems")
            print("   ✅ Comprehensive execution monitoring and logging")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())