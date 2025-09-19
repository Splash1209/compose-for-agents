"""
Fact-Checking Implementation of the 3-Layer Framework

This module provides concrete implementations of the 3-layer framework
specifically designed for fact-checking multi-agent systems like A2A and ADK.

Layers:
- Auditor (Top): Orchestrates fact-checking workflow
- Critic (Middle): Analyzes claims and gathers evidence
- Reviser (Bottom): Finalizes corrected responses
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

from . import (
    TopLayer, MiddleLayer, BottomLayer, LayerExpectation, LayerType,
    DirectionBuffer, ValidationStatus, BufferValidation
)


@dataclass
class FactCheckRequest:
    """Input for fact-checking workflow"""
    question: str
    answer: str
    context: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Claim:
    """Represents a claim to be fact-checked"""
    text: str
    context: str
    claim_type: str  # "factual", "opinion", "logical_argument"
    source_sentence: str
    importance: float  # 0.0 to 1.0


@dataclass
class Evidence:
    """Evidence found for a claim"""
    source_url: str
    excerpt: str
    relevance_score: float
    credibility_score: float
    timestamp: datetime


@dataclass
class ClaimVerification:
    """Result of verifying a claim"""
    claim: Claim
    verdict: str  # "accurate", "inaccurate", "disputed", "unsupported", "not_applicable"
    confidence: float
    evidence: List[Evidence]
    justification: str


@dataclass
class CriticAnalysis:
    """Output from the critic layer"""
    claims: List[Claim]
    verifications: List[ClaimVerification]
    overall_assessment: str
    confidence_score: float
    sources_consulted: List[str]


@dataclass
class RevisedResponse:
    """Final output from the reviser layer"""
    original_answer: str
    revised_answer: str
    changes_made: List[str]
    revision_reasoning: str
    quality_score: float


class FactCheckAuditor(TopLayer[FactCheckRequest, RevisedResponse]):
    """Auditor layer for fact-checking orchestration"""
    
    def __init__(self):
        # Define expectations for fact-checking workflow
        expectations = LayerExpectation(
            layer_type=LayerType.TOP,
            input_schema={
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                    "context": {"type": "string"},
                    "metadata": {"type": "object"}
                },
                "required": ["question", "answer"]
            },
            output_schema={
                "type": "object", 
                "properties": {
                    "original_answer": {"type": "string"},
                    "revised_answer": {"type": "string"},
                    "changes_made": {"type": "array"},
                    "revision_reasoning": {"type": "string"},
                    "quality_score": {"type": "number"}
                }
            },
            validation_rules=[
                "question_must_be_non_empty",
                "answer_must_be_non_empty", 
                "context_should_be_relevant"
            ],
            quality_requirements={
                "accuracy_threshold": 0.8,
                "completeness_threshold": 0.9,
                "response_time_max": 300  # seconds
            },
            performance_constraints={
                "max_claims_per_analysis": 20,
                "max_sources_per_claim": 10
            }
        )
        
        super().__init__(expectations)
        
        # Set workflow definition
        self.define_workflow({
            "steps": [
                {"layer": "critic", "action": "analyze_claims"},
                {"layer": "critic", "action": "verify_claims"},
                {"layer": "reviser", "action": "revise_response"}
            ],
            "quality_gates": ["accuracy_check", "completeness_check"],
            "fallback_strategy": "conservative_revision"
        })
        
        # Define requirements for downstream layers
        self.set_middle_layer_requirements({
            "claim_extraction_method": "comprehensive",
            "evidence_sources": ["web_search", "authoritative_databases"],
            "verification_depth": "thorough",
            "minimum_sources_per_claim": 2,
            "confidence_threshold": 0.7
        })
        
        self.set_bottom_layer_requirements({
            "revision_strategy": "minimal_necessary_changes",
            "preserve_original_style": True,
            "maintain_answer_length": True,
            "require_justification": True,
            "quality_threshold": 0.8
        })
    
    async def orchestrate(self, input_data: FactCheckRequest) -> RevisedResponse:
        """Orchestrate the fact-checking workflow"""
        # This would typically coordinate with actual critic and reviser agents
        # For now, return a mock response
        return RevisedResponse(
            original_answer=input_data.answer,
            revised_answer=input_data.answer,  # Would be actual revised version
            changes_made=[],
            revision_reasoning="Orchestration complete",
            quality_score=0.9
        )
    
    async def process(self, input_data: FactCheckRequest) -> RevisedResponse:
        """Process the fact-checking request"""
        return await self.orchestrate(input_data)
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
        """Validate that auditor can meet the given requirements"""
        required_fields = ["question", "answer"]
        return all(field in requirements for field in required_fields)


class FactCheckCritic(MiddleLayer[FactCheckRequest, CriticAnalysis]):
    """Critic layer for claim analysis and verification"""
    
    def __init__(self):
        # Define expectations for critic analysis
        expectations = LayerExpectation(
            layer_type=LayerType.MIDDLE,
            input_schema={
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                    "context": {"type": "string"}
                }
            },
            output_schema={
                "type": "object",
                "properties": {
                    "claims": {"type": "array"},
                    "verifications": {"type": "array"},
                    "overall_assessment": {"type": "string"},
                    "confidence_score": {"type": "number"},
                    "sources_consulted": {"type": "array"}
                }
            },
            validation_rules=[
                "claims_must_be_extractable",
                "evidence_must_be_credible",
                "sources_must_be_accessible"
            ],
            quality_requirements={
                "claim_extraction_completeness": 0.9,
                "evidence_relevance_threshold": 0.7,
                "source_credibility_minimum": 0.6
            },
            performance_constraints={
                "max_search_queries": 50,
                "max_analysis_time": 180
            }
        )
        
        super().__init__(expectations)
        
        # Configure processing
        self.configure_processing({
            "claim_extraction_model": "advanced_nlp",
            "search_strategy": "comprehensive",
            "evidence_ranking": "relevance_and_credibility",
            "verification_method": "multi_source_validation"
        })
        
        # Add quality gates
        self.add_quality_gate("sufficient_claims_extracted")
        self.add_quality_gate("adequate_evidence_gathered")
        self.add_quality_gate("credible_sources_consulted")
    
    async def execute_core_logic(self, input_data: FactCheckRequest) -> CriticAnalysis:
        """Execute claim analysis and verification logic"""
        # Extract claims from the answer
        claims = await self._extract_claims(input_data.answer, input_data.question)
        
        # Verify each claim
        verifications = []
        for claim in claims:
            verification = await self._verify_claim(claim)
            verifications.append(verification)
        
        # Generate overall assessment
        overall_assessment = self._generate_overall_assessment(verifications)
        confidence_score = self._calculate_confidence_score(verifications)
        
        # Collect sources consulted
        sources_consulted = []
        for verification in verifications:
            sources_consulted.extend([ev.source_url for ev in verification.evidence])
        
        return CriticAnalysis(
            claims=claims,
            verifications=verifications,
            overall_assessment=overall_assessment,
            confidence_score=confidence_score,
            sources_consulted=list(set(sources_consulted))
        )
    
    async def _extract_claims(self, answer: str, question: str) -> List[Claim]:
        """Extract claims from the answer text"""
        # Mock implementation - would use NLP to extract actual claims
        return [
            Claim(
                text="Sample claim from answer",
                context=question,
                claim_type="factual",
                source_sentence=answer[:100] + "...",
                importance=0.8
            )
        ]
    
    async def _verify_claim(self, claim: Claim) -> ClaimVerification:
        """Verify a specific claim using external sources"""
        # Mock implementation - would perform actual web search and verification
        evidence = [
            Evidence(
                source_url="https://example.com/source1",
                excerpt="Supporting evidence excerpt",
                relevance_score=0.9,
                credibility_score=0.8,
                timestamp=datetime.now()
            )
        ]
        
        return ClaimVerification(
            claim=claim,
            verdict="accurate",
            confidence=0.85,
            evidence=evidence,
            justification="Evidence from credible sources supports this claim"
        )
    
    def _generate_overall_assessment(self, verifications: List[ClaimVerification]) -> str:
        """Generate overall assessment based on individual verifications"""
        accurate_count = sum(1 for v in verifications if v.verdict == "accurate")
        total_count = len(verifications)
        
        if total_count == 0:
            return "No claims to verify"
        
        accuracy_rate = accurate_count / total_count
        
        if accuracy_rate >= 0.9:
            return "Highly accurate response"
        elif accuracy_rate >= 0.7:
            return "Mostly accurate response"
        elif accuracy_rate >= 0.5:
            return "Partially accurate response"
        else:
            return "Largely inaccurate response"
    
    def _calculate_confidence_score(self, verifications: List[ClaimVerification]) -> float:
        """Calculate overall confidence score"""
        if not verifications:
            return 0.0
        
        return sum(v.confidence for v in verifications) / len(verifications)
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
        """Validate that critic can meet the given requirements"""
        # Check if we have the necessary tools and capabilities
        required_capabilities = ["claim_extraction", "web_search", "source_verification"]
        return all(cap in self.processing_config for cap in required_capabilities)


class FactCheckReviser(BottomLayer[CriticAnalysis, RevisedResponse]):
    """Reviser layer for finalizing corrected responses"""
    
    def __init__(self):
        # Define expectations for revision
        expectations = LayerExpectation(
            layer_type=LayerType.BOTTOM,
            input_schema={
                "type": "object",
                "properties": {
                    "claims": {"type": "array"},
                    "verifications": {"type": "array"},
                    "overall_assessment": {"type": "string"},
                    "confidence_score": {"type": "number"}
                }
            },
            output_schema={
                "type": "object",
                "properties": {
                    "original_answer": {"type": "string"},
                    "revised_answer": {"type": "string"},
                    "changes_made": {"type": "array"},
                    "revision_reasoning": {"type": "string"},
                    "quality_score": {"type": "number"}
                }
            },
            validation_rules=[
                "revisions_must_be_justified",
                "style_must_be_preserved",
                "accuracy_must_be_improved"
            ],
            quality_requirements={
                "accuracy_improvement_threshold": 0.1,
                "style_preservation_score": 0.8,
                "readability_maintenance": 0.9
            },
            performance_constraints={
                "max_revision_time": 60,
                "max_changes_per_sentence": 3
            }
        )
        
        super().__init__(expectations)
        
        # Add finalization rules
        self.add_finalization_rule("preserve_original_structure")
        self.add_finalization_rule("maintain_answer_length")
        self.add_finalization_rule("improve_accuracy_only")
        
        # Add output validators
        self.add_output_validator("grammar_check")
        self.add_output_validator("fact_consistency_check")
        self.add_output_validator("style_consistency_check")
    
    async def finalize_output(self, input_data: CriticAnalysis) -> RevisedResponse:
        """Finalize the revised response based on critic analysis"""
        # Determine what changes need to be made
        changes_needed = self._analyze_required_changes(input_data.verifications)
        
        # Apply revisions based on verification results
        revised_answer = await self._apply_revisions(
            original_answer="",  # Would come from original request
            verifications=input_data.verifications,
            changes_needed=changes_needed
        )
        
        # Generate revision reasoning
        revision_reasoning = self._generate_revision_reasoning(
            changes_needed, input_data.overall_assessment
        )
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(input_data.confidence_score)
        
        return RevisedResponse(
            original_answer="",  # Would be populated with actual original
            revised_answer=revised_answer,
            changes_made=changes_needed,
            revision_reasoning=revision_reasoning,
            quality_score=quality_score
        )
    
    def _analyze_required_changes(self, verifications: List[ClaimVerification]) -> List[str]:
        """Analyze what changes are needed based on verifications"""
        changes = []
        
        for verification in verifications:
            if verification.verdict == "inaccurate":
                changes.append(f"Correct inaccurate claim: {verification.claim.text}")
            elif verification.verdict == "disputed":
                changes.append(f"Add nuance to disputed claim: {verification.claim.text}")
            elif verification.verdict == "unsupported":
                changes.append(f"Soften unsupported claim: {verification.claim.text}")
        
        return changes
    
    async def _apply_revisions(self, 
                              original_answer: str,
                              verifications: List[ClaimVerification],
                              changes_needed: List[str]) -> str:
        """Apply the necessary revisions to the answer"""
        # Mock implementation - would perform actual text revision
        if not changes_needed:
            return original_answer
        
        # Apply changes while preserving style and structure
        revised_answer = original_answer  # Start with original
        
        for change in changes_needed:
            # Apply specific change - mock implementation
            revised_answer = self._apply_single_revision(revised_answer, change)
        
        return revised_answer
    
    def _apply_single_revision(self, text: str, change: str) -> str:
        """Apply a single revision to the text"""
        # Mock implementation - would perform actual text editing
        return text
    
    def _generate_revision_reasoning(self, changes: List[str], assessment: str) -> str:
        """Generate reasoning for the revisions made"""
        if not changes:
            return f"No revisions needed. {assessment}"
        
        return f"Made {len(changes)} revisions based on fact-checking analysis: {assessment}. " + \
               f"Changes: {', '.join(changes)}"
    
    def _calculate_quality_score(self, confidence_score: float) -> float:
        """Calculate quality score for the revised response"""
        # Base quality score on confidence and other factors
        base_score = confidence_score
        
        # Adjust based on revision quality factors
        # (implementation would consider grammar, style, etc.)
        
        return min(1.0, base_score * 1.1)  # Slight boost for revision process
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
        """Validate that reviser can meet the given requirements"""
        required_capabilities = ["text_editing", "style_preservation", "accuracy_improvement"]
        return True  # Mock implementation