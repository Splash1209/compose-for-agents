"""
Shared 3-Layer Framework for Multi-Agent Systems

This framework provides standardized interfaces and buffers for implementing
a 3-layer architecture in multi-agent systems, ensuring proper direction
and validation of expectations between layers.

Layers:
- Top Layer (Orchestrator): Coordinates workflow and defines expectations
- Middle Layer (Processor): Executes core logic with validation buffers  
- Bottom Layer (Finalizer): Produces final output with quality assurance

Each layer has defined interfaces for inputs, outputs, and expectations
to ensure proper data flow and validation.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Generic
import json
import logging
from datetime import datetime

# Set up logging for the framework
logger = logging.getLogger(__name__)

# Type variables for generic implementations
InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')
ExpectationType = TypeVar('ExpectationType')


class LayerType(Enum):
    """Enumeration of the three layer types"""
    TOP = "top"
    MIDDLE = "middle" 
    BOTTOM = "bottom"


class ValidationStatus(Enum):
    """Status of validation checks"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


@dataclass
class LayerExpectation:
    """Defines expectations for a layer's behavior and outputs"""
    layer_type: LayerType
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    validation_rules: List[str]
    quality_requirements: Dict[str, Any]
    performance_constraints: Dict[str, Any]
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data against schema"""
        # Implementation would validate against input_schema
        return True
    
    def validate_output(self, data: Any) -> bool:
        """Validate output data against schema"""
        # Implementation would validate against output_schema
        return True


@dataclass
class BufferValidation:
    """Result of buffer validation"""
    status: ValidationStatus
    message: str
    timestamp: datetime
    layer_from: LayerType
    layer_to: LayerType
    data_size: int
    validation_details: Dict[str, Any]


@dataclass
class DirectionBuffer:
    """Buffer for managing data flow between layers with validation"""
    source_layer: LayerType
    target_layer: LayerType
    expectations: LayerExpectation
    data: Any
    metadata: Dict[str, Any]
    validation_results: List[BufferValidation]
    
    def validate(self) -> BufferValidation:
        """Validate the buffer contents"""
        try:
            # Check if data meets expectations
            input_valid = self.expectations.validate_input(self.data)
            
            status = ValidationStatus.PASSED if input_valid else ValidationStatus.FAILED
            message = "Buffer validation passed" if input_valid else "Buffer validation failed"
            
            validation = BufferValidation(
                status=status,
                message=message,
                timestamp=datetime.now(),
                layer_from=self.source_layer,
                layer_to=self.target_layer,
                data_size=len(str(self.data)) if self.data else 0,
                validation_details={"input_valid": input_valid}
            )
            
            self.validation_results.append(validation)
            return validation
            
        except Exception as e:
            validation = BufferValidation(
                status=ValidationStatus.FAILED,
                message=f"Buffer validation error: {str(e)}",
                timestamp=datetime.now(),
                layer_from=self.source_layer,
                layer_to=self.target_layer,
                data_size=0,
                validation_details={"error": str(e)}
            )
            self.validation_results.append(validation)
            return validation


class LayerInterface(ABC, Generic[InputType, OutputType]):
    """Abstract base class for all layer implementations"""
    
    def __init__(self, layer_type: LayerType, expectations: LayerExpectation):
        self.layer_type = layer_type
        self.expectations = expectations
        self.input_buffer: Optional[DirectionBuffer] = None
        self.output_buffer: Optional[DirectionBuffer] = None
        
    @abstractmethod
    async def process(self, input_data: InputType) -> OutputType:
        """Process input data and return output"""
        pass
    
    @abstractmethod
    def validate_requirements(self, requirements: Dict[str, Any]) -> bool:
        """Validate that layer can meet the given requirements"""
        pass
    
    def set_input_buffer(self, buffer: DirectionBuffer) -> None:
        """Set the input buffer for this layer"""
        self.input_buffer = buffer
        
    def create_output_buffer(self, target_layer: LayerType, data: OutputType) -> DirectionBuffer:
        """Create output buffer for the next layer"""
        # Create expectations for the target layer
        target_expectations = LayerExpectation(
            layer_type=target_layer,
            input_schema=self.expectations.output_schema,
            output_schema={},  # Will be defined by target layer
            validation_rules=[],
            quality_requirements={},
            performance_constraints={}
        )
        
        buffer = DirectionBuffer(
            source_layer=self.layer_type,
            target_layer=target_layer,
            expectations=target_expectations,
            data=data,
            metadata={
                "created_at": datetime.now().isoformat(),
                "source_layer_type": self.layer_type.value
            },
            validation_results=[]
        )
        
        self.output_buffer = buffer
        return buffer


class TopLayer(LayerInterface[InputType, OutputType]):
    """Top layer (Orchestrator) - defines workflow and expectations"""
    
    def __init__(self, expectations: LayerExpectation):
        super().__init__(LayerType.TOP, expectations)
        self.workflow_definition: Dict[str, Any] = {}
        self.middle_layer_requirements: Dict[str, Any] = {}
        self.bottom_layer_requirements: Dict[str, Any] = {}
    
    def define_workflow(self, workflow: Dict[str, Any]) -> None:
        """Define the workflow for this orchestration"""
        self.workflow_definition = workflow
        
    def set_middle_layer_requirements(self, requirements: Dict[str, Any]) -> None:
        """Set requirements for the middle layer"""
        self.middle_layer_requirements = requirements
        
    def set_bottom_layer_requirements(self, requirements: Dict[str, Any]) -> None:
        """Set requirements for the bottom layer"""
        self.bottom_layer_requirements = requirements
    
    @abstractmethod
    async def orchestrate(self, input_data: InputType) -> OutputType:
        """Orchestrate the entire workflow"""
        pass


class MiddleLayer(LayerInterface[InputType, OutputType]):
    """Middle layer (Processor) - executes core logic with validation"""
    
    def __init__(self, expectations: LayerExpectation):
        super().__init__(LayerType.MIDDLE, expectations)
        self.processing_config: Dict[str, Any] = {}
        self.quality_gates: List[str] = []
    
    def configure_processing(self, config: Dict[str, Any]) -> None:
        """Configure processing parameters"""
        self.processing_config = config
        
    def add_quality_gate(self, gate_name: str) -> None:
        """Add a quality gate for validation"""
        self.quality_gates.append(gate_name)
    
    @abstractmethod
    async def execute_core_logic(self, input_data: InputType) -> OutputType:
        """Execute the core processing logic"""
        pass
    
    async def process(self, input_data: InputType) -> OutputType:
        """Process with quality gates"""
        # Validate input buffer
        if self.input_buffer:
            validation = self.input_buffer.validate()
            if validation.status == ValidationStatus.FAILED:
                raise ValueError(f"Input validation failed: {validation.message}")
        
        # Execute core logic
        result = await self.execute_core_logic(input_data)
        
        # Apply quality gates
        for gate in self.quality_gates:
            if not self._check_quality_gate(gate, result):
                logger.warning(f"Quality gate '{gate}' failed")
        
        return result
    
    def _check_quality_gate(self, gate_name: str, data: OutputType) -> bool:
        """Check a specific quality gate"""
        # Implementation would check specific quality criteria
        return True


class BottomLayer(LayerInterface[InputType, OutputType]):
    """Bottom layer (Finalizer) - produces final output with quality assurance"""
    
    def __init__(self, expectations: LayerExpectation):
        super().__init__(LayerType.BOTTOM, expectations)
        self.finalization_rules: List[str] = []
        self.output_validators: List[str] = []
    
    def add_finalization_rule(self, rule: str) -> None:
        """Add a rule for finalization"""
        self.finalization_rules.append(rule)
        
    def add_output_validator(self, validator: str) -> None:
        """Add an output validator"""
        self.output_validators.append(validator)
    
    @abstractmethod
    async def finalize_output(self, input_data: InputType) -> OutputType:
        """Finalize and produce the output"""
        pass
    
    async def process(self, input_data: InputType) -> OutputType:
        """Process with finalization and validation"""
        # Validate input buffer
        if self.input_buffer:
            validation = self.input_buffer.validate()
            if validation.status == ValidationStatus.FAILED:
                raise ValueError(f"Input validation failed: {validation.message}")
        
        # Apply finalization rules
        for rule in self.finalization_rules:
            input_data = self._apply_finalization_rule(rule, input_data)
        
        # Finalize output
        result = await self.finalize_output(input_data)
        
        # Validate output
        for validator in self.output_validators:
            if not self._validate_output(validator, result):
                logger.warning(f"Output validator '{validator}' failed")
        
        return result
    
    def _apply_finalization_rule(self, rule: str, data: InputType) -> InputType:
        """Apply a specific finalization rule"""
        # Implementation would apply specific finalization logic
        return data
    
    def _validate_output(self, validator: str, data: OutputType) -> bool:
        """Validate output with a specific validator"""
        # Implementation would validate with specific criteria
        return True


class ThreeLayerOrchestrator:
    """Orchestrator for managing the complete 3-layer workflow"""
    
    def __init__(self, 
                 top_layer: TopLayer,
                 middle_layer: MiddleLayer, 
                 bottom_layer: BottomLayer):
        self.top_layer = top_layer
        self.middle_layer = middle_layer
        self.bottom_layer = bottom_layer
        self.execution_log: List[Dict[str, Any]] = []
    
    async def execute_workflow(self, initial_input: Any) -> Any:
        """Execute the complete 3-layer workflow with buffers"""
        try:
            # Log workflow start
            self._log_execution("workflow_start", {"input_type": type(initial_input).__name__})
            
            # Step 1: Top layer processing
            top_result = await self.top_layer.process(initial_input)
            
            # Create buffer from top to middle
            top_to_middle_buffer = self.top_layer.create_output_buffer(
                LayerType.MIDDLE, top_result
            )
            self.middle_layer.set_input_buffer(top_to_middle_buffer)
            
            # Step 2: Middle layer processing
            middle_result = await self.middle_layer.process(top_result)
            
            # Create buffer from middle to bottom
            middle_to_bottom_buffer = self.middle_layer.create_output_buffer(
                LayerType.BOTTOM, middle_result
            )
            self.bottom_layer.set_input_buffer(middle_to_bottom_buffer)
            
            # Step 3: Bottom layer finalization
            final_result = await self.bottom_layer.process(middle_result)
            
            # Log workflow completion
            self._log_execution("workflow_complete", {"output_type": type(final_result).__name__})
            
            return final_result
            
        except Exception as e:
            self._log_execution("workflow_error", {"error": str(e)})
            raise
    
    def _log_execution(self, event: str, details: Dict[str, Any]) -> None:
        """Log execution events"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details
        }
        self.execution_log.append(log_entry)
        logger.info(f"3-Layer Workflow: {event} - {details}")
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of workflow execution"""
        return {
            "total_steps": len(self.execution_log),
            "execution_log": self.execution_log,
            "buffer_validations": self._collect_buffer_validations()
        }
    
    def _collect_buffer_validations(self) -> List[Dict[str, Any]]:
        """Collect all buffer validation results"""
        validations = []
        
        if self.middle_layer.input_buffer:
            validations.extend([
                {
                    "buffer": "top_to_middle",
                    "validation": v.__dict__
                } for v in self.middle_layer.input_buffer.validation_results
            ])
            
        if self.bottom_layer.input_buffer:
            validations.extend([
                {
                    "buffer": "middle_to_bottom", 
                    "validation": v.__dict__
                } for v in self.bottom_layer.input_buffer.validation_results
            ])
            
        return validations