"""
Example: Integrating 3-Layer Framework with A2A System

This example shows how to enhance the existing A2A fact-checking system
with the new 3-layer framework to provide better direction and buffers.
"""

# This would be the integration approach for the A2A system
integration_example = """
# Original A2A System Enhancement

## Before (Current A2A):
```yaml
# a2a/agents/auditor.yaml
name: LLM Auditor
type: sequential
description: |
  Evaluates LLM-generated answers, verifies actual accuracy using the web,
  and refines the response to ensure alignment with real-world knowledge.
sub_agents:
  - ${CRITIC_AGENT_URL}
  - ${REVISER_AGENT_URL}
```

## After (Enhanced with 3-Layer Framework):
```python
# a2a/enhanced_agents/auditor.py
from shared.layer_framework import ThreeLayerOrchestrator
from shared.layer_framework.adapters import A2AAdapter, A2AAgentConfig
from shared.layer_framework.fact_checking import FactCheckRequest

class EnhancedA2AAuditor:
    def __init__(self):
        # Configure A2A integration
        config = A2AAgentConfig(
            auditor_url="${AUDITOR_AGENT_URL}",
            critic_url="${CRITIC_AGENT_URL}",
            reviser_url="${REVISER_AGENT_URL}",
            model_name="${OPENAI_MODEL_NAME}",
            model_provider="${LLM_AGENT_MODEL_PROVIDER}"
        )
        
        # Create adapter with 3-layer framework
        self.adapter = A2AAdapter(config)
    
    async def process_fact_check(self, question: str, answer: str) -> dict:
        # Convert to framework format
        request = FactCheckRequest(
            question=question,
            answer=answer,
            context="A2A fact-checking"
        )
        
        # Process with enhanced framework
        result = await self.adapter.execute_fact_check(request)
        
        # Return in A2A format
        return {
            "original_answer": result.original_answer,
            "revised_answer": result.revised_answer,
            "changes_made": result.changes_made,
            "quality_score": result.quality_score,
            "framework_metadata": {
                "layer_validations": "passed",
                "quality_gates": "applied",
                "requirements_flow": "validated"
            }
        }
```

## Benefits Added to A2A System:

1. **Clear Layer Expectations**:
   - Auditor defines requirements for Critic and Reviser
   - Each layer validates it can meet requirements
   - Performance and quality constraints enforced

2. **Direction Buffers**:
   - Validated data flow between Auditor → Critic → Reviser
   - Input/output validation at each layer boundary
   - Comprehensive error handling and logging

3. **Quality Assurance**:
   - Quality gates in Critic layer (evidence, sources, coverage)
   - Finalization rules in Reviser layer (structure, accuracy, style)
   - Output validators ensure final quality

4. **Monitoring and Debugging**:
   - Execution logging for workflow steps
   - Buffer validation tracking
   - Performance metrics collection

## Integration Steps:

1. **Install Framework**: Copy shared/layer_framework to A2A project
2. **Update compose.yaml**: Add framework dependencies
3. **Enhance Agents**: Wrap existing agents with framework adapters
4. **Configure Buffers**: Set up validation rules and quality gates
5. **Test Integration**: Verify enhanced functionality works
6. **Deploy**: Replace original agents with enhanced versions

## Backward Compatibility:
- Existing A2A agents continue to work unchanged
- Framework provides additional capabilities on top
- Gradual migration possible (layer by layer)
- All existing APIs and interfaces preserved
"""

print(integration_example)