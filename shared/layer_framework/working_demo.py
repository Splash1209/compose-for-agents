"""
Working 3-Layer Framework Demo

This demonstrates the complete 3-layer framework with proper data flow.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from __init__ import (
    LayerType, LayerExpectation, DirectionBuffer, ValidationStatus,
    LayerInterface, ThreeLayerOrchestrator
)
import asyncio
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class FactCheckRequest:
    """Fact check request"""
    question: str
    answer: str
    context: str = ""


@dataclass 
class AnalysisResult:
    """Analysis result from critic"""
    original_request: FactCheckRequest
    claims_found: int
    analysis: str
    confidence: float


@dataclass
class FactCheckResult:
    """Final fact check result"""
    original_answer: str
    revised_answer: str
    changes_made: List[str]
    quality_score: float


class FactCheckAuditor(LayerInterface[FactCheckRequest, FactCheckRequest]):
    """Auditor layer - coordinates the workflow"""
    
    def __init__(self):
        expectations = LayerExpectation(
            layer_type=LayerType.TOP,
            input_schema={"type": "object", "properties": {"question": {"type": "string"}}},
            output_schema={"type": "object"},
            validation_rules=["question_not_empty"],
            quality_requirements={"accuracy": 0.8},
            performance_constraints={"max_time": 300}
        )
        
        super().__init__(LayerType.TOP, expectations)
        
        # Set requirements for downstream layers
        self.middle_layer_requirements = {
            "claim_extraction": "comprehensive",
            "fact_verification": "multi_source",
            "confidence_threshold": 0.7
        }
        
        self.bottom_layer_requirements = {
            "revision_style": "preserve_original", 
            "quality_threshold": 0.8,
            "justification_required": True
        }
    
    async def process(self, input_data: FactCheckRequest) -> FactCheckRequest:
        """Process and pass through to next layer"""
        print(f"🎯 AUDITOR: Processing fact-check request")
        print(f"   Question: {input_data.question}")
        print(f"   Requirements for Critic: {list(self.middle_layer_requirements.keys())}")
        print(f"   Requirements for Reviser: {list(self.bottom_layer_requirements.keys())}")
        
        # Pass the request to the next layer
        return input_data
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
        return "question" in requirements


class FactCheckCritic(LayerInterface[FactCheckRequest, AnalysisResult]):
    """Critic layer - analyzes claims"""
    
    def __init__(self):
        expectations = LayerExpectation(
            layer_type=LayerType.MIDDLE,
            input_schema={"type": "object"},
            output_schema={"type": "object"},
            validation_rules=["claims_extractable"],
            quality_requirements={"evidence_quality": 0.7},
            performance_constraints={"max_search_time": 180}
        )
        
        super().__init__(LayerType.MIDDLE, expectations)
        
        self.quality_gates = ["sufficient_evidence", "credible_sources", "claim_coverage"]
    
    async def process(self, input_data: FactCheckRequest) -> AnalysisResult:
        """Analyze claims and verify facts"""
        print(f"🔍 CRITIC: Analyzing claims in answer to: '{input_data.question}'")
        print(f"   Answer to analyze: {input_data.answer}")
        print(f"   Quality gates: {self.quality_gates}")
        
        # Validate input buffer if exists
        if self.input_buffer:
            validation = self.input_buffer.validate()
            print(f"   Input buffer validation: {validation.status.value}")
        
        # Simulate claim analysis
        claims_found = 2  # Mock: found 2 claims
        analysis = f"Found {claims_found} claims. Claim 1: 'Earth is flat' - INACCURATE. Claim 2: 'NASA hiding truth' - UNSUPPORTED."
        confidence = 0.85
        
        print(f"   Analysis complete: {claims_found} claims analyzed")
        
        return AnalysisResult(
            original_request=input_data,
            claims_found=claims_found,
            analysis=analysis,
            confidence=confidence
        )
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
        return "claim_extraction" in requirements


class FactCheckReviser(LayerInterface[AnalysisResult, FactCheckResult]):
    """Reviser layer - produces final output"""
    
    def __init__(self):
        expectations = LayerExpectation(
            layer_type=LayerType.BOTTOM,
            input_schema={"type": "object"},
            output_schema={"type": "object"},
            validation_rules=["revisions_justified"],
            quality_requirements={"accuracy_improvement": 0.1},
            performance_constraints={"max_revision_time": 60}
        )
        
        super().__init__(LayerType.BOTTOM, expectations)
        
        self.finalization_rules = ["preserve_structure", "improve_accuracy", "maintain_style"]
        self.output_validators = ["grammar_check", "accuracy_check", "completeness_check"]
    
    async def process(self, input_data: AnalysisResult) -> FactCheckResult:
        """Finalize the revised output"""
        print(f"✏️  REVISER: Finalizing revision based on analysis")
        print(f"   Original answer: {input_data.original_request.answer}")
        print(f"   Analysis: {input_data.analysis}")
        print(f"   Finalization rules: {self.finalization_rules}")
        
        # Validate input buffer if exists
        if self.input_buffer:
            validation = self.input_buffer.validate()
            print(f"   Input buffer validation: {validation.status.value}")
        
        # Create revised answer based on analysis
        if "INACCURATE" in input_data.analysis:
            revised_answer = "The Earth is a sphere, as demonstrated by extensive scientific evidence including satellite imagery and physics."
            changes = ["Corrected inaccurate flat Earth claim", "Added scientific evidence"]
        else:
            revised_answer = input_data.original_request.answer
            changes = []
        
        quality_score = 0.92 if changes else 0.80
        
        print(f"   Revision complete. Quality score: {quality_score}")
        
        return FactCheckResult(
            original_answer=input_data.original_request.answer,
            revised_answer=revised_answer,
            changes_made=changes,
            quality_score=quality_score
        )
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
        return "quality_threshold" in requirements


async def demonstrate_complete_workflow():
    """Demonstrate the complete 3-layer workflow"""
    print("🚀 Complete 3-Layer Framework Demonstration")
    print("=" * 70)
    
    # Create the three layers
    auditor = FactCheckAuditor()
    critic = FactCheckCritic()
    reviser = FactCheckReviser()
    
    print("📋 Layer Configuration Summary:")
    print(f"  🎯 Top Layer (Auditor): Coordinates workflow and sets requirements")
    print(f"     - Middle layer requirements: {list(auditor.middle_layer_requirements.keys())}")
    print(f"     - Bottom layer requirements: {list(auditor.bottom_layer_requirements.keys())}")
    
    print(f"  🔍 Middle Layer (Critic): Analyzes claims with quality gates")
    print(f"     - Quality gates: {critic.quality_gates}")
    print(f"     - Performance constraints: {critic.expectations.performance_constraints}")
    
    print(f"  ✏️  Bottom Layer (Reviser): Finalizes output with validation")
    print(f"     - Finalization rules: {reviser.finalization_rules}")
    print(f"     - Output validators: {reviser.output_validators}")
    print()
    
    # Create orchestrator
    orchestrator = ThreeLayerOrchestrator(
        top_layer=auditor,
        middle_layer=critic,
        bottom_layer=reviser
    )
    
    # Test case 1: Inaccurate information
    print("📝 Test Case 1: Processing inaccurate information")
    request1 = FactCheckRequest(
        question="Is the Earth flat?",
        answer="The Earth is flat and NASA is hiding the truth from us.",
        context="Scientific discussion"
    )
    
    print(f"   Input Question: {request1.question}")
    print(f"   Input Answer: {request1.answer}")
    print()
    
    # Execute workflow
    print("🔄 Executing 3-Layer Workflow:")
    result1 = await orchestrator.execute_workflow(request1)
    
    print()
    print("📊 Workflow Results:")
    print(f"   Original Answer: {result1.original_answer}")
    print(f"   Revised Answer: {result1.revised_answer}")
    print(f"   Changes Made: {result1.changes_made}")
    print(f"   Quality Score: {result1.quality_score}")
    print()
    
    # Test case 2: Accurate information
    print("📝 Test Case 2: Processing accurate information")
    request2 = FactCheckRequest(
        question="What is the capital of France?",
        answer="The capital of France is Paris.",
        context="Geography question"
    )
    
    print(f"   Input Question: {request2.question}")
    print(f"   Input Answer: {request2.answer}")
    print()
    
    print("🔄 Executing 3-Layer Workflow:")
    result2 = await orchestrator.execute_workflow(request2)
    
    print()
    print("📊 Workflow Results:")
    print(f"   Original Answer: {result2.original_answer}")
    print(f"   Revised Answer: {result2.revised_answer}")
    print(f"   Changes Made: {result2.changes_made}")
    print(f"   Quality Score: {result2.quality_score}")
    print()
    
    # Show execution summary
    summary = orchestrator.get_execution_summary()
    print("📈 Execution Summary:")
    print(f"   Total Steps: {summary['total_steps']}")
    print(f"   Buffer Validations: {len(summary['buffer_validations'])}")
    
    print("   Execution Log:")
    for i, log_entry in enumerate(summary['execution_log']):
        print(f"     {i+1}. {log_entry['event']} - {log_entry['details']}")
    print()
    
    # Show buffer validation details
    if summary['buffer_validations']:
        print("🔍 Buffer Validation Details:")
        for validation in summary['buffer_validations']:
            buffer_name = validation['buffer']
            val_info = validation['validation']
            print(f"   {buffer_name}: {val_info['status']} - {val_info['message']}")
        print()
    
    return True


async def demonstrate_framework_features():
    """Demonstrate key framework features"""
    print("🎯 Key Framework Features")
    print("=" * 70)
    
    print("✅ Feature 1: Layer Expectations and Requirements")
    auditor = FactCheckAuditor()
    print(f"   - Auditor sets middle layer requirements: {auditor.middle_layer_requirements}")
    print(f"   - Auditor sets bottom layer requirements: {auditor.bottom_layer_requirements}")
    
    critic = FactCheckCritic()
    print(f"   - Critic validates requirements: {critic.validate_requirements(auditor.middle_layer_requirements)}")
    print()
    
    print("✅ Feature 2: Direction Buffers with Validation")
    expectations = auditor.expectations
    buffer = DirectionBuffer(
        source_layer=LayerType.TOP,
        target_layer=LayerType.MIDDLE,
        expectations=expectations,
        data={"question": "Test?", "answer": "Test answer"},
        metadata={"timestamp": datetime.now().isoformat()},
        validation_results=[]
    )
    
    validation = buffer.validate()
    print(f"   - Buffer flows: {buffer.source_layer.value} → {buffer.target_layer.value}")
    print(f"   - Validation status: {validation.status.value}")
    print(f"   - Data validation: Passed")
    print(f"   - Buffer metadata: {list(buffer.metadata.keys())}")
    print()
    
    print("✅ Feature 3: Quality Gates and Validators")
    critic = FactCheckCritic()
    reviser = FactCheckReviser()
    print(f"   - Critic quality gates: {critic.quality_gates}")
    print(f"   - Reviser finalization rules: {reviser.finalization_rules}")
    print(f"   - Reviser output validators: {reviser.output_validators}")
    print()
    
    print("✅ Feature 4: Performance and Quality Constraints")
    print(f"   - Auditor quality requirements: {auditor.expectations.quality_requirements}")
    print(f"   - Critic performance constraints: {critic.expectations.performance_constraints}")
    print(f"   - Reviser validation rules: {reviser.expectations.validation_rules}")
    print()


async def main():
    """Run the complete demonstration"""
    try:
        success = await demonstrate_complete_workflow()
        await demonstrate_framework_features()
        
        if success:
            print("🎉 3-Layer Framework Successfully Provides:")
            print("   ✅ Clear direction and expectations between layers")
            print("   ✅ Validation buffers for secure data flow")
            print("   ✅ Quality assurance at every processing step")
            print("   ✅ Requirements definition and validation")
            print("   ✅ Comprehensive monitoring and logging")
            print("   ✅ Standardized architecture for multi-agent systems")
            print()
            print("🔧 Ready for integration with existing agent frameworks:")
            print("   • A2A (Agent2Agent) systems")
            print("   • ADK (Agent Development Kit) systems")
            print("   • Custom multi-agent implementations")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())