"""
Adapters for integrating existing agent systems with the 3-Layer Framework

This module provides adapter classes that allow existing agent implementations
(A2A, ADK, etc.) to work with the new 3-layer framework while maintaining
backward compatibility.
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
import asyncio
import json
from datetime import datetime

from . import LayerInterface, LayerType, LayerExpectation, DirectionBuffer
from .fact_checking import (
    FactCheckRequest, CriticAnalysis, RevisedResponse,
    FactCheckAuditor, FactCheckCritic, FactCheckReviser
)


@dataclass
class A2AAgentConfig:
    """Configuration for A2A agent integration"""
    auditor_url: str
    critic_url: str  
    reviser_url: str
    model_name: str
    model_provider: str


@dataclass
class ADKAgentConfig:
    """Configuration for ADK agent integration"""
    agent_module_path: str
    model_endpoint: str
    mcp_gateway_endpoint: str


class A2AAdapter:
    """Adapter for integrating A2A agents with the 3-layer framework"""
    
    def __init__(self, config: A2AAgentConfig):
        self.config = config
        self.auditor = A2AAuditorAdapter(config)
        self.critic = A2ACriticAdapter(config)
        self.reviser = A2AReviserAdapter(config)
    
    async def execute_fact_check(self, request: FactCheckRequest) -> RevisedResponse:
        """Execute fact-checking using A2A agents through the framework"""
        # Use the 3-layer orchestrator with A2A adapters
        from . import ThreeLayerOrchestrator
        
        orchestrator = ThreeLayerOrchestrator(
            top_layer=self.auditor,
            middle_layer=self.critic,
            bottom_layer=self.reviser
        )
        
        return await orchestrator.execute_workflow(request)


class A2AAuditorAdapter(FactCheckAuditor):
    """Adapter for A2A Auditor agent"""
    
    def __init__(self, config: A2AAgentConfig):
        super().__init__()
        self.config = config
        self.agent_url = config.auditor_url
    
    async def orchestrate(self, input_data: FactCheckRequest) -> RevisedResponse:
        """Orchestrate using A2A sequential agent"""
        # This would make HTTP calls to the actual A2A auditor service
        # For now, simulate the behavior
        
        # Convert framework request to A2A format
        a2a_request = {
            "question": input_data.question,
            "answer": input_data.answer,
            "context": input_data.context or ""
        }
        
        # Mock HTTP call to A2A auditor
        a2a_response = await self._call_a2a_auditor(a2a_request)
        
        # Convert A2A response back to framework format
        return RevisedResponse(
            original_answer=input_data.answer,
            revised_answer=a2a_response.get("revised_answer", input_data.answer),
            changes_made=a2a_response.get("changes", []),
            revision_reasoning=a2a_response.get("reasoning", ""),
            quality_score=a2a_response.get("quality_score", 0.8)
        )
    
    async def _call_a2a_auditor(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP call to A2A auditor service"""
        # Mock implementation - would use actual HTTP client
        import json
        
        # Simulate A2A auditor response
        await asyncio.sleep(0.1)  # Simulate network delay
        
        return {
            "revised_answer": request["answer"],  # Would be actually revised
            "changes": [],
            "reasoning": "Processed through A2A auditor",
            "quality_score": 0.85
        }


class A2ACriticAdapter(FactCheckCritic):
    """Adapter for A2A Critic agent"""
    
    def __init__(self, config: A2AAgentConfig):
        super().__init__()
        self.config = config
        self.agent_url = config.critic_url
    
    async def execute_core_logic(self, input_data: FactCheckRequest) -> CriticAnalysis:
        """Execute using A2A critic agent"""
        # Convert framework request to A2A format
        a2a_request = {
            "question": input_data.question,
            "answer": input_data.answer,
            "task": "fact_check"
        }
        
        # Mock HTTP call to A2A critic
        a2a_response = await self._call_a2a_critic(a2a_request)
        
        # Convert A2A response to framework format
        return self._convert_a2a_critic_response(a2a_response)
    
    async def _call_a2a_critic(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP call to A2A critic service"""
        # Mock implementation
        await asyncio.sleep(0.2)  # Simulate processing time
        
        return {
            "claims": [
                {
                    "text": "Sample claim from A2A",
                    "verdict": "accurate", 
                    "confidence": 0.9,
                    "sources": ["https://example.com/source1"]
                }
            ],
            "overall_verdict": "mostly_accurate",
            "confidence": 0.85
        }
    
    def _convert_a2a_critic_response(self, response: Dict[str, Any]) -> CriticAnalysis:
        """Convert A2A critic response to framework format"""
        from .fact_checking import Claim, ClaimVerification, Evidence
        
        # Convert claims
        claims = []
        verifications = []
        
        for claim_data in response.get("claims", []):
            claim = Claim(
                text=claim_data["text"],
                context="",
                claim_type="factual",
                source_sentence=claim_data["text"],
                importance=0.8
            )
            claims.append(claim)
            
            # Create evidence from sources
            evidence = [
                Evidence(
                    source_url=url,
                    excerpt="Evidence excerpt from A2A",
                    relevance_score=0.8,
                    credibility_score=0.8,
                    timestamp=datetime.now()
                ) for url in claim_data.get("sources", [])
            ]
            
            verification = ClaimVerification(
                claim=claim,
                verdict=claim_data.get("verdict", "unknown"),
                confidence=claim_data.get("confidence", 0.5),
                evidence=evidence,
                justification=f"A2A verification: {claim_data.get('verdict')}"
            )
            verifications.append(verification)
        
        return CriticAnalysis(
            claims=claims,
            verifications=verifications,
            overall_assessment=response.get("overall_verdict", "unknown"),
            confidence_score=response.get("confidence", 0.5),
            sources_consulted=[url for claim in response.get("claims", []) 
                              for url in claim.get("sources", [])]
        )


class A2AReviserAdapter(FactCheckReviser):
    """Adapter for A2A Reviser agent"""
    
    def __init__(self, config: A2AAgentConfig):
        super().__init__()
        self.config = config
        self.agent_url = config.reviser_url
    
    async def finalize_output(self, input_data: CriticAnalysis) -> RevisedResponse:
        """Finalize using A2A reviser agent"""
        # Convert framework data to A2A format
        a2a_request = {
            "original_answer": "",  # Would come from original request
            "verification_results": self._convert_to_a2a_format(input_data),
            "task": "revise"
        }
        
        # Mock HTTP call to A2A reviser
        a2a_response = await self._call_a2a_reviser(a2a_request)
        
        # Convert back to framework format
        return RevisedResponse(
            original_answer=a2a_request["original_answer"],
            revised_answer=a2a_response.get("revised_answer", ""),
            changes_made=a2a_response.get("changes", []),
            revision_reasoning=a2a_response.get("reasoning", ""),
            quality_score=a2a_response.get("quality_score", 0.8)
        )
    
    def _convert_to_a2a_format(self, analysis: CriticAnalysis) -> Dict[str, Any]:
        """Convert framework analysis to A2A format"""
        return {
            "claims": [
                {
                    "text": v.claim.text,
                    "verdict": v.verdict,
                    "confidence": v.confidence,
                    "justification": v.justification
                } for v in analysis.verifications
            ],
            "overall_assessment": analysis.overall_assessment,
            "confidence": analysis.confidence_score
        }
    
    async def _call_a2a_reviser(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP call to A2A reviser service"""
        # Mock implementation
        await asyncio.sleep(0.1)
        
        return {
            "revised_answer": request.get("original_answer", ""),
            "changes": ["Fixed inaccurate claim"],
            "reasoning": "Applied A2A revisions based on verification",
            "quality_score": 0.9
        }


class ADKAdapter:
    """Adapter for integrating ADK agents with the 3-layer framework"""
    
    def __init__(self, config: ADKAgentConfig):
        self.config = config
        self.auditor = ADKAuditorAdapter(config)
        self.critic = ADKCriticAdapter(config)
        self.reviser = ADKReviserAdapter(config)
    
    async def execute_fact_check(self, request: FactCheckRequest) -> RevisedResponse:
        """Execute fact-checking using ADK agents through the framework"""
        from . import ThreeLayerOrchestrator
        
        orchestrator = ThreeLayerOrchestrator(
            top_layer=self.auditor,
            middle_layer=self.critic,
            bottom_layer=self.reviser
        )
        
        return await orchestrator.execute_workflow(request)


class ADKAuditorAdapter(FactCheckAuditor):
    """Adapter for ADK Sequential Agent (llm_auditor)"""
    
    def __init__(self, config: ADKAgentConfig):
        super().__init__()
        self.config = config
        self.agent_module = None
    
    async def orchestrate(self, input_data: FactCheckRequest) -> RevisedResponse:
        """Orchestrate using ADK SequentialAgent"""
        # This would import and use the actual ADK agent
        # For now, simulate the behavior
        
        try:
            # Mock ADK agent execution
            result = await self._execute_adk_agent(input_data)
            
            return RevisedResponse(
                original_answer=input_data.answer,
                revised_answer=result.get("response", input_data.answer),
                changes_made=result.get("changes", []),
                revision_reasoning="ADK sequential agent processing",
                quality_score=0.9
            )
            
        except Exception as e:
            # Fallback to framework implementation
            return await super().orchestrate(input_data)
    
    async def _execute_adk_agent(self, input_data: FactCheckRequest) -> Dict[str, Any]:
        """Execute the ADK agent"""
        # Mock implementation - would use actual ADK agent
        await asyncio.sleep(0.5)  # Simulate processing
        
        return {
            "response": input_data.answer,  # Would be processed response
            "changes": [],
            "metadata": {
                "agent_type": "adk_sequential",
                "model_used": self.config.model_endpoint
            }
        }


class ADKCriticAdapter(FactCheckCritic):
    """Adapter for ADK Critic Agent"""
    
    def __init__(self, config: ADKAgentConfig):
        super().__init__()
        self.config = config
    
    async def execute_core_logic(self, input_data: FactCheckRequest) -> CriticAnalysis:
        """Execute using ADK critic agent"""
        # Mock ADK critic execution
        result = await self._execute_adk_critic(input_data)
        
        # Convert to framework format
        return self._convert_adk_critic_result(result)
    
    async def _execute_adk_critic(self, input_data: FactCheckRequest) -> Dict[str, Any]:
        """Execute ADK critic agent"""
        # Mock implementation
        await asyncio.sleep(0.3)
        
        return {
            "analysis": "ADK critic analysis complete",
            "claims_found": 3,
            "accuracy_assessment": "high",
            "sources_checked": ["source1.com", "source2.com"]
        }
    
    def _convert_adk_critic_result(self, result: Dict[str, Any]) -> CriticAnalysis:
        """Convert ADK result to framework format"""
        from .fact_checking import Claim, ClaimVerification, Evidence
        
        # Mock conversion
        claims = [
            Claim(
                text="ADK extracted claim",
                context="",
                claim_type="factual",
                source_sentence="",
                importance=0.8
            )
        ]
        
        evidence = [
            Evidence(
                source_url=url,
                excerpt="ADK evidence",
                relevance_score=0.8,
                credibility_score=0.8,
                timestamp=datetime.now()
            ) for url in result.get("sources_checked", [])
        ]
        
        verifications = [
            ClaimVerification(
                claim=claims[0],
                verdict="accurate",
                confidence=0.9,
                evidence=evidence,
                justification="ADK verification complete"
            )
        ]
        
        return CriticAnalysis(
            claims=claims,
            verifications=verifications,
            overall_assessment=result.get("accuracy_assessment", "unknown"),
            confidence_score=0.85,
            sources_consulted=result.get("sources_checked", [])
        )


class ADKReviserAdapter(FactCheckReviser):
    """Adapter for ADK Reviser Agent"""
    
    def __init__(self, config: ADKAgentConfig):
        super().__init__()
        self.config = config
    
    async def finalize_output(self, input_data: CriticAnalysis) -> RevisedResponse:
        """Finalize using ADK reviser agent"""
        # Mock ADK reviser execution
        result = await self._execute_adk_reviser(input_data)
        
        return RevisedResponse(
            original_answer="",  # Would come from original
            revised_answer=result.get("revised_text", ""),
            changes_made=result.get("revisions", []),
            revision_reasoning="ADK reviser processing",
            quality_score=result.get("quality", 0.85)
        )
    
    async def _execute_adk_reviser(self, input_data: CriticAnalysis) -> Dict[str, Any]:
        """Execute ADK reviser agent"""
        # Mock implementation
        await asyncio.sleep(0.2)
        
        return {
            "revised_text": "ADK revised text",
            "revisions": ["corrected claim 1"],
            "quality": 0.9
        }


class UniversalAgentAdapter:
    """Universal adapter that can work with different agent frameworks"""
    
    def __init__(self, agent_type: str, config: Union[A2AAgentConfig, ADKAgentConfig]):
        self.agent_type = agent_type
        self.config = config
        
        if agent_type.lower() == "a2a":
            self.adapter = A2AAdapter(config)
        elif agent_type.lower() == "adk":
            self.adapter = ADKAdapter(config)
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")
    
    async def execute_fact_check(self, request: FactCheckRequest) -> RevisedResponse:
        """Execute fact-checking using the appropriate adapter"""
        return await self.adapter.execute_fact_check(request)
    
    def get_framework_info(self) -> Dict[str, Any]:
        """Get information about the framework being adapted"""
        return {
            "agent_type": self.agent_type,
            "config": self.config.__dict__,
            "framework_version": "1.0.0",
            "supported_operations": ["fact_check", "claim_verification", "text_revision"]
        }