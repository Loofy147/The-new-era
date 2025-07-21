"""
Advanced Decision Engine for AI Orchestrator System
Handles intelligent decision making, strategy selection, and adaptive reasoning.
"""

import asyncio
import json
import math
from typing import Dict, List, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict, deque
import random

class DecisionType(Enum):
    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    OPERATIONAL = "operational"
    REACTIVE = "reactive"

class ConfidenceLevel(Enum):
    VERY_HIGH = 0.9
    HIGH = 0.8
    MEDIUM = 0.6
    LOW = 0.4
    VERY_LOW = 0.2

class DecisionPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    DEFERRED = 5

@dataclass
class DecisionContext:
    """Context information for making decisions."""
    decision_id: str
    timestamp: datetime
    decision_type: DecisionType
    priority: DecisionPriority
    context_data: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    objectives: List[str] = field(default_factory=list)
    available_options: List[Dict[str, Any]] = field(default_factory=list)
    historical_data: List[Dict[str, Any]] = field(default_factory=list)
    stakeholders: List[str] = field(default_factory=list)

@dataclass
class DecisionOutcome:
    """Result of a decision-making process."""
    decision_id: str
    selected_option: Dict[str, Any]
    confidence: float
    reasoning: str
    alternatives_considered: List[Dict[str, Any]] = field(default_factory=list)
    risk_assessment: Dict[str, float] = field(default_factory=dict)
    expected_impact: Dict[str, Any] = field(default_factory=dict)
    execution_plan: List[Dict[str, Any]] = field(default_factory=list)
    monitoring_metrics: List[str] = field(default_factory=list)
    fallback_options: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class DecisionCriteria:
    """Criteria for evaluating decision options."""
    name: str
    weight: float
    evaluation_func: callable
    threshold: Optional[float] = None
    maximize: bool = True
    description: str = ""

class DecisionStrategy(ABC):
    """Abstract base class for decision-making strategies."""
    
    @abstractmethod
    async def evaluate_options(self, context: DecisionContext, 
                             criteria: List[DecisionCriteria]) -> List[Tuple[Dict[str, Any], float]]:
        """Evaluate available options and return scored results."""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Return the name of this strategy."""
        pass

class WeightedScoringStrategy(DecisionStrategy):
    """Multi-criteria decision analysis using weighted scoring."""
    
    def get_strategy_name(self) -> str:
        return "weighted_scoring"
    
    async def evaluate_options(self, context: DecisionContext, 
                             criteria: List[DecisionCriteria]) -> List[Tuple[Dict[str, Any], float]]:
        """Evaluate options using weighted scoring method."""
        scored_options = []
        
        # Normalize weights
        total_weight = sum(criterion.weight for criterion in criteria)
        normalized_criteria = [
            DecisionCriteria(
                name=c.name,
                weight=c.weight / total_weight,
                evaluation_func=c.evaluation_func,
                threshold=c.threshold,
                maximize=c.maximize,
                description=c.description
            ) for c in criteria
        ]
        
        for option in context.available_options:
            total_score = 0.0
            criterion_scores = {}
            
            for criterion in normalized_criteria:
                try:
                    raw_score = await self._evaluate_criterion(criterion, option, context)
                    normalized_score = self._normalize_score(raw_score, criterion)
                    weighted_score = normalized_score * criterion.weight
                    total_score += weighted_score
                    criterion_scores[criterion.name] = {
                        'raw_score': raw_score,
                        'normalized_score': normalized_score,
                        'weighted_score': weighted_score
                    }
                except Exception as e:
                    print(f"Error evaluating criterion {criterion.name}: {e}")
                    continue
            
            # Add detailed scoring information to option
            enhanced_option = option.copy()
            enhanced_option['_scoring_details'] = criterion_scores
            enhanced_option['_total_score'] = total_score
            
            scored_options.append((enhanced_option, total_score))
        
        # Sort by score (highest first)
        scored_options.sort(key=lambda x: x[1], reverse=True)
        return scored_options
    
    async def _evaluate_criterion(self, criterion: DecisionCriteria, 
                                option: Dict[str, Any], 
                                context: DecisionContext) -> float:
        """Evaluate a single criterion for an option."""
        if asyncio.iscoroutinefunction(criterion.evaluation_func):
            return await criterion.evaluation_func(option, context)
        else:
            return criterion.evaluation_func(option, context)
    
    def _normalize_score(self, raw_score: float, criterion: DecisionCriteria) -> float:
        """Normalize a raw score to 0-1 range."""
        if criterion.threshold is not None:
            # Threshold-based normalization
            if criterion.maximize:
                return 1.0 if raw_score >= criterion.threshold else raw_score / criterion.threshold
            else:
                return 1.0 if raw_score <= criterion.threshold else criterion.threshold / max(raw_score, 0.001)
        else:
            # Simple 0-1 normalization (assumes raw_score is already in reasonable range)
            return max(0.0, min(1.0, raw_score))

class AHPStrategy(DecisionStrategy):
    """Analytic Hierarchy Process for complex decision making."""
    
    def get_strategy_name(self) -> str:
        return "analytic_hierarchy_process"
    
    async def evaluate_options(self, context: DecisionContext, 
                             criteria: List[DecisionCriteria]) -> List[Tuple[Dict[str, Any], float]]:
        """Evaluate options using AHP methodology."""
        # Build pairwise comparison matrix for criteria
        criteria_matrix = self._build_criteria_comparison_matrix(criteria)
        criteria_weights = self._calculate_eigenvector_weights(criteria_matrix)
        
        scored_options = []
        
        for option in context.available_options:
            ahp_score = 0.0
            
            for i, criterion in enumerate(criteria):
                try:
                    criterion_score = await self._evaluate_criterion_ahp(criterion, option, context)
                    ahp_score += criterion_score * criteria_weights[i]
                except Exception as e:
                    print(f"AHP evaluation error for {criterion.name}: {e}")
                    continue
            
            enhanced_option = option.copy()
            enhanced_option['_ahp_score'] = ahp_score
            scored_options.append((enhanced_option, ahp_score))
        
        scored_options.sort(key=lambda x: x[1], reverse=True)
        return scored_options
    
    def _build_criteria_comparison_matrix(self, criteria: List[DecisionCriteria]) -> List[List[float]]:
        """Build pairwise comparison matrix for criteria."""
        n = len(criteria)
        matrix = [[1.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                # Simple weight-based comparison
                ratio = criteria[i].weight / criteria[j].weight
                matrix[i][j] = ratio
                matrix[j][i] = 1.0 / ratio
        
        return matrix
    
    def _calculate_eigenvector_weights(self, matrix: List[List[float]]) -> List[float]:
        """Calculate priority weights using eigenvector method."""
        n = len(matrix)
        
        # Simple approximation: geometric mean of each row
        weights = []
        for i in range(n):
            product = 1.0
            for j in range(n):
                product *= matrix[i][j]
            weights.append(product ** (1.0 / n))
        
        # Normalize weights
        total = sum(weights)
        return [w / total for w in weights]
    
    async def _evaluate_criterion_ahp(self, criterion: DecisionCriteria, 
                                    option: Dict[str, Any], 
                                    context: DecisionContext) -> float:
        """Evaluate criterion using AHP methodology."""
        if asyncio.iscoroutinefunction(criterion.evaluation_func):
            raw_score = await criterion.evaluation_func(option, context)
        else:
            raw_score = criterion.evaluation_func(option, context)
        
        return max(0.0, min(1.0, raw_score))

class MonteCarloStrategy(DecisionStrategy):
    """Monte Carlo simulation for decision making under uncertainty."""
    
    def __init__(self, num_simulations: int = 1000):
        self.num_simulations = num_simulations
    
    def get_strategy_name(self) -> str:
        return "monte_carlo"
    
    async def evaluate_options(self, context: DecisionContext, 
                             criteria: List[DecisionCriteria]) -> List[Tuple[Dict[str, Any], float]]:
        """Evaluate options using Monte Carlo simulation."""
        scored_options = []
        
        for option in context.available_options:
            simulation_results = []
            
            for _ in range(self.num_simulations):
                simulation_score = await self._run_simulation(option, criteria, context)
                simulation_results.append(simulation_score)
            
            # Calculate statistics
            mean_score = sum(simulation_results) / len(simulation_results)
            variance = sum((x - mean_score) ** 2 for x in simulation_results) / len(simulation_results)
            std_dev = math.sqrt(variance)
            
            # Risk-adjusted score (mean - penalty for high variance)
            risk_penalty = std_dev * 0.5  # Adjust penalty factor as needed
            adjusted_score = mean_score - risk_penalty
            
            enhanced_option = option.copy()
            enhanced_option['_mc_mean'] = mean_score
            enhanced_option['_mc_std_dev'] = std_dev
            enhanced_option['_mc_adjusted_score'] = adjusted_score
            
            scored_options.append((enhanced_option, adjusted_score))
        
        scored_options.sort(key=lambda x: x[1], reverse=True)
        return scored_options
    
    async def _run_simulation(self, option: Dict[str, Any], 
                            criteria: List[DecisionCriteria], 
                            context: DecisionContext) -> float:
        """Run a single Monte Carlo simulation."""
        total_score = 0.0
        total_weight = sum(c.weight for c in criteria)
        
        for criterion in criteria:
            try:
                # Add randomness to criterion evaluation
                base_score = await self._evaluate_with_uncertainty(criterion, option, context)
                weight = criterion.weight / total_weight
                total_score += base_score * weight
            except Exception as e:
                print(f"Simulation error for {criterion.name}: {e}")
                continue
        
        return total_score
    
    async def _evaluate_with_uncertainty(self, criterion: DecisionCriteria, 
                                       option: Dict[str, Any], 
                                       context: DecisionContext) -> float:
        """Evaluate criterion with added uncertainty."""
        if asyncio.iscoroutinefunction(criterion.evaluation_func):
            base_score = await criterion.evaluation_func(option, context)
        else:
            base_score = criterion.evaluation_func(option, context)
        
        # Add gaussian noise to simulate uncertainty
        uncertainty = random.gauss(0, 0.1)  # 10% standard deviation
        return max(0.0, min(1.0, base_score + uncertainty))

class LearningStrategy(DecisionStrategy):
    """Machine learning-based strategy that improves over time."""
    
    def __init__(self):
        self.decision_history: List[Tuple[DecisionContext, DecisionOutcome]] = []
        self.learned_weights: Dict[str, float] = {}
        self.success_patterns: Dict[str, float] = defaultdict(float)
    
    def get_strategy_name(self) -> str:
        return "learning_strategy"
    
    async def evaluate_options(self, context: DecisionContext, 
                             criteria: List[DecisionCriteria]) -> List[Tuple[Dict[str, Any], float]]:
        """Evaluate options using learned patterns."""
        # Update criteria weights based on historical success
        adjusted_criteria = self._adjust_criteria_weights(criteria, context)
        
        # Use weighted scoring with learned weights
        weighted_strategy = WeightedScoringStrategy()
        scored_options = await weighted_strategy.evaluate_options(context, adjusted_criteria)
        
        # Apply pattern-based adjustments
        for i, (option, score) in enumerate(scored_options):
            pattern_bonus = self._calculate_pattern_bonus(option, context)
            adjusted_score = score + pattern_bonus
            scored_options[i] = (option, adjusted_score)
        
        scored_options.sort(key=lambda x: x[1], reverse=True)
        return scored_options
    
    def _adjust_criteria_weights(self, criteria: List[DecisionCriteria], 
                               context: DecisionContext) -> List[DecisionCriteria]:
        """Adjust criteria weights based on historical success."""
        adjusted_criteria = []
        
        for criterion in criteria:
            # Look for historical success patterns for this criterion
            success_weight = self.learned_weights.get(criterion.name, 1.0)
            
            adjusted_criterion = DecisionCriteria(
                name=criterion.name,
                weight=criterion.weight * success_weight,
                evaluation_func=criterion.evaluation_func,
                threshold=criterion.threshold,
                maximize=criterion.maximize,
                description=criterion.description
            )
            adjusted_criteria.append(adjusted_criterion)
        
        return adjusted_criteria
    
    def _calculate_pattern_bonus(self, option: Dict[str, Any], 
                               context: DecisionContext) -> float:
        """Calculate bonus score based on successful patterns."""
        bonus = 0.0
        
        for pattern, success_rate in self.success_patterns.items():
            if self._option_matches_pattern(option, pattern):
                bonus += success_rate * 0.1  # 10% bonus for matching successful patterns
        
        return min(bonus, 0.3)  # Cap bonus at 30%
    
    def _option_matches_pattern(self, option: Dict[str, Any], pattern: str) -> bool:
        """Check if option matches a learned pattern."""
        # Simple pattern matching based on option properties
        option_signature = self._create_option_signature(option)
        return pattern in option_signature
    
    def _create_option_signature(self, option: Dict[str, Any]) -> str:
        """Create a signature string for an option."""
        key_features = []
        for key, value in option.items():
            if not key.startswith('_'):  # Skip internal metadata
                if isinstance(value, (str, int, float, bool)):
                    key_features.append(f"{key}:{value}")
        return "|".join(sorted(key_features))
    
    def learn_from_outcome(self, context: DecisionContext, outcome: DecisionOutcome, 
                          success_score: float) -> None:
        """Learn from a decision outcome."""
        self.decision_history.append((context, outcome))
        
        # Update criterion weights based on success
        if hasattr(outcome.selected_option, '_scoring_details'):
            for criterion_name, scoring_info in outcome.selected_option['_scoring_details'].items():
                current_weight = self.learned_weights.get(criterion_name, 1.0)
                learning_rate = 0.1
                adjustment = learning_rate * (success_score - 0.5)  # Adjust based on success
                self.learned_weights[criterion_name] = max(0.1, current_weight + adjustment)
        
        # Update success patterns
        option_signature = self._create_option_signature(outcome.selected_option)
        current_success = self.success_patterns[option_signature]
        self.success_patterns[option_signature] = (current_success + success_score) / 2
        
        # Limit history size
        if len(self.decision_history) > 1000:
            self.decision_history = self.decision_history[-500:]

class RiskAnalyzer:
    """Analyzes and quantifies risks associated with decision options."""
    
    def __init__(self):
        self.risk_factors = [
            'implementation_complexity',
            'resource_requirements',
            'time_constraints',
            'stakeholder_impact',
            'reversibility',
            'precedent_success'
        ]
    
    async def analyze_risks(self, option: Dict[str, Any], 
                          context: DecisionContext) -> Dict[str, float]:
        """Analyze risks for a decision option."""
        risk_scores = {}
        
        for factor in self.risk_factors:
            risk_score = await self._evaluate_risk_factor(factor, option, context)
            risk_scores[factor] = risk_score
        
        # Calculate overall risk score
        risk_scores['overall_risk'] = sum(risk_scores.values()) / len(self.risk_factors)
        
        return risk_scores
    
    async def _evaluate_risk_factor(self, factor: str, option: Dict[str, Any], 
                                  context: DecisionContext) -> float:
        """Evaluate a specific risk factor."""
        risk_evaluators = {
            'implementation_complexity': self._evaluate_complexity_risk,
            'resource_requirements': self._evaluate_resource_risk,
            'time_constraints': self._evaluate_time_risk,
            'stakeholder_impact': self._evaluate_stakeholder_risk,
            'reversibility': self._evaluate_reversibility_risk,
            'precedent_success': self._evaluate_precedent_risk
        }
        
        evaluator = risk_evaluators.get(factor, self._default_risk_evaluation)
        return await evaluator(option, context)
    
    async def _evaluate_complexity_risk(self, option: Dict[str, Any], 
                                      context: DecisionContext) -> float:
        """Evaluate implementation complexity risk."""
        complexity_indicators = option.get('complexity_score', 0.5)
        dependencies = len(option.get('dependencies', []))
        
        # Higher complexity and more dependencies = higher risk
        complexity_risk = min(1.0, complexity_indicators + (dependencies * 0.1))
        return complexity_risk
    
    async def _evaluate_resource_risk(self, option: Dict[str, Any], 
                                    context: DecisionContext) -> float:
        """Evaluate resource availability risk."""
        required_resources = option.get('resource_requirements', {})
        available_resources = context.context_data.get('available_resources', {})
        
        risk_score = 0.0
        for resource_type, required_amount in required_resources.items():
            available_amount = available_resources.get(resource_type, 0)
            if available_amount < required_amount:
                risk_score += 0.3  # High risk if resources not available
            elif available_amount < required_amount * 1.5:
                risk_score += 0.1  # Medium risk if resources are tight
        
        return min(1.0, risk_score)
    
    async def _evaluate_time_risk(self, option: Dict[str, Any], 
                                context: DecisionContext) -> float:
        """Evaluate time constraint risk."""
        estimated_duration = option.get('estimated_duration', 0)
        deadline = context.constraints.get('deadline')
        
        if deadline:
            time_available = (deadline - datetime.now()).total_seconds()
            if estimated_duration > time_available:
                return 1.0  # High risk - not enough time
            elif estimated_duration > time_available * 0.8:
                return 0.6  # Medium risk - tight timeline
        
        return 0.2  # Low risk
    
    async def _evaluate_stakeholder_risk(self, option: Dict[str, Any], 
                                       context: DecisionContext) -> float:
        """Evaluate stakeholder impact risk."""
        affected_stakeholders = option.get('affected_stakeholders', [])
        stakeholder_approval = option.get('stakeholder_approval_score', 0.5)
        
        # Higher impact on more stakeholders with lower approval = higher risk
        impact_factor = len(affected_stakeholders) * 0.1
        approval_factor = 1.0 - stakeholder_approval
        
        return min(1.0, impact_factor + approval_factor)
    
    async def _evaluate_reversibility_risk(self, option: Dict[str, Any], 
                                         context: DecisionContext) -> float:
        """Evaluate reversibility risk."""
        reversibility_score = option.get('reversibility_score', 0.5)
        return 1.0 - reversibility_score  # Higher reversibility = lower risk
    
    async def _evaluate_precedent_risk(self, option: Dict[str, Any], 
                                     context: DecisionContext) -> float:
        """Evaluate risk based on precedent success."""
        precedent_success_rate = option.get('precedent_success_rate', 0.5)
        return 1.0 - precedent_success_rate  # Higher precedent success = lower risk
    
    async def _default_risk_evaluation(self, option: Dict[str, Any], 
                                     context: DecisionContext) -> float:
        """Default risk evaluation for unknown factors."""
        return 0.5  # Neutral risk

class AdvancedDecisionEngine:
    """Main decision engine that coordinates all decision-making activities."""
    
    def __init__(self):
        self.strategies: Dict[str, DecisionStrategy] = {
            'weighted_scoring': WeightedScoringStrategy(),
            'ahp': AHPStrategy(),
            'monte_carlo': MonteCarloStrategy(),
            'learning': LearningStrategy()
        }
        self.risk_analyzer = RiskAnalyzer()
        self.decision_history: List[Tuple[DecisionContext, DecisionOutcome]] = []
        self.default_criteria = self._initialize_default_criteria()
    
    def _initialize_default_criteria(self) -> List[DecisionCriteria]:
        """Initialize default decision criteria."""
        return [
            DecisionCriteria(
                name="effectiveness",
                weight=0.3,
                evaluation_func=self._evaluate_effectiveness,
                maximize=True,
                description="How well the option achieves objectives"
            ),
            DecisionCriteria(
                name="efficiency",
                weight=0.25,
                evaluation_func=self._evaluate_efficiency,
                maximize=True,
                description="Resource efficiency of the option"
            ),
            DecisionCriteria(
                name="feasibility",
                weight=0.2,
                evaluation_func=self._evaluate_feasibility,
                maximize=True,
                description="Practical feasibility of implementation"
            ),
            DecisionCriteria(
                name="risk",
                weight=0.15,
                evaluation_func=self._evaluate_overall_risk,
                maximize=False,
                description="Overall risk level"
            ),
            DecisionCriteria(
                name="alignment",
                weight=0.1,
                evaluation_func=self._evaluate_strategic_alignment,
                maximize=True,
                description="Alignment with strategic objectives"
            )
        ]
    
    async def make_decision(self, context: DecisionContext, 
                          criteria: Optional[List[DecisionCriteria]] = None,
                          strategy: str = 'weighted_scoring') -> DecisionOutcome:
        """Make a decision based on context and criteria."""
        if criteria is None:
            criteria = self.default_criteria
        
        if strategy not in self.strategies:
            strategy = 'weighted_scoring'
        
        decision_strategy = self.strategies[strategy]
        
        # Evaluate options using the selected strategy
        scored_options = await decision_strategy.evaluate_options(context, criteria)
        
        if not scored_options:
            raise ValueError("No options available for decision making")
        
        # Get the best option
        best_option, best_score = scored_options[0]
        
        # Perform risk analysis
        risk_assessment = await self.risk_analyzer.analyze_risks(best_option, context)
        
        # Create execution plan
        execution_plan = await self._create_execution_plan(best_option, context)
        
        # Determine monitoring metrics
        monitoring_metrics = self._determine_monitoring_metrics(best_option, criteria)
        
        # Prepare fallback options
        fallback_options = [option for option, _ in scored_options[1:3]]  # Top 2 alternatives
        
        # Generate reasoning
        reasoning = self._generate_reasoning(best_option, scored_options, risk_assessment, strategy)
        
        # Calculate confidence based on score difference and risk
        confidence = self._calculate_confidence(scored_options, risk_assessment)
        
        outcome = DecisionOutcome(
            decision_id=context.decision_id,
            selected_option=best_option,
            confidence=confidence,
            reasoning=reasoning,
            alternatives_considered=[option for option, _ in scored_options[1:]],
            risk_assessment=risk_assessment,
            expected_impact=self._estimate_impact(best_option, context),
            execution_plan=execution_plan,
            monitoring_metrics=monitoring_metrics,
            fallback_options=fallback_options
        )
        
        # Store decision for learning
        self.decision_history.append((context, outcome))
        
        return outcome
    
    async def _evaluate_effectiveness(self, option: Dict[str, Any], 
                                    context: DecisionContext) -> float:
        """Evaluate how effectively an option achieves objectives."""
        effectiveness_score = option.get('effectiveness_score', 0.5)
        
        # Adjust based on objective alignment
        objective_alignment = 0.0
        for objective in context.objectives:
            if objective.lower() in str(option).lower():
                objective_alignment += 0.2
        
        return min(1.0, effectiveness_score + objective_alignment)
    
    async def _evaluate_efficiency(self, option: Dict[str, Any], 
                                 context: DecisionContext) -> float:
        """Evaluate resource efficiency of an option."""
        efficiency_score = option.get('efficiency_score', 0.5)
        
        # Consider resource requirements vs. expected output
        resource_req = option.get('resource_requirements', {})
        expected_output = option.get('expected_output_value', 1.0)
        
        if resource_req:
            total_resources = sum(resource_req.values()) if isinstance(resource_req, dict) else 1.0
            efficiency_ratio = expected_output / max(total_resources, 0.1)
            return min(1.0, efficiency_score + (efficiency_ratio * 0.3))
        
        return efficiency_score
    
    async def _evaluate_feasibility(self, option: Dict[str, Any], 
                                  context: DecisionContext) -> float:
        """Evaluate practical feasibility of an option."""
        feasibility_score = option.get('feasibility_score', 0.5)
        
        # Check constraints
        constraints = context.constraints
        for constraint_name, constraint_value in constraints.items():
            option_value = option.get(constraint_name)
            if option_value is not None:
                if isinstance(constraint_value, (int, float)) and isinstance(option_value, (int, float)):
                    if option_value > constraint_value:
                        feasibility_score *= 0.8  # Reduce feasibility if constraints violated
        
        return feasibility_score
    
    async def _evaluate_overall_risk(self, option: Dict[str, Any], 
                                   context: DecisionContext) -> float:
        """Evaluate overall risk level (to be minimized)."""
        risk_assessment = await self.risk_analyzer.analyze_risks(option, context)
        return risk_assessment.get('overall_risk', 0.5)
    
    async def _evaluate_strategic_alignment(self, option: Dict[str, Any], 
                                          context: DecisionContext) -> float:
        """Evaluate strategic alignment of an option."""
        alignment_score = option.get('strategic_alignment_score', 0.5)
        
        # Consider stakeholder priorities
        stakeholder_scores = option.get('stakeholder_scores', {})
        if stakeholder_scores:
            avg_stakeholder_score = sum(stakeholder_scores.values()) / len(stakeholder_scores)
            alignment_score = (alignment_score + avg_stakeholder_score) / 2
        
        return alignment_score
    
    async def _create_execution_plan(self, option: Dict[str, Any], 
                                   context: DecisionContext) -> List[Dict[str, Any]]:
        """Create execution plan for the selected option."""
        plan_template = option.get('execution_template', [])
        
        if plan_template:
            return plan_template
        
        # Generate basic execution plan
        return [
            {
                'phase': 'preparation',
                'duration_estimate': 600,  # 10 minutes
                'activities': ['Resource allocation', 'Stakeholder notification'],
                'dependencies': []
            },
            {
                'phase': 'execution',
                'duration_estimate': option.get('estimated_duration', 1800),
                'activities': ['Main implementation'],
                'dependencies': ['preparation']
            },
            {
                'phase': 'monitoring',
                'duration_estimate': 300,  # 5 minutes
                'activities': ['Performance monitoring', 'Issue detection'],
                'dependencies': ['execution']
            },
            {
                'phase': 'completion',
                'duration_estimate': 300,
                'activities': ['Results validation', 'Resource cleanup'],
                'dependencies': ['monitoring']
            }
        ]
    
    def _determine_monitoring_metrics(self, option: Dict[str, Any], 
                                    criteria: List[DecisionCriteria]) -> List[str]:
        """Determine key metrics to monitor during execution."""
        metrics = []
        
        for criterion in criteria:
            if criterion.name == 'effectiveness':
                metrics.extend(['success_rate', 'objective_achievement'])
            elif criterion.name == 'efficiency':
                metrics.extend(['resource_utilization', 'throughput'])
            elif criterion.name == 'risk':
                metrics.extend(['error_rate', 'incident_count'])
        
        # Add option-specific metrics
        custom_metrics = option.get('monitoring_metrics', [])
        metrics.extend(custom_metrics)
        
        return list(set(metrics))  # Remove duplicates
    
    def _generate_reasoning(self, selected_option: Dict[str, Any], 
                          all_options: List[Tuple[Dict[str, Any], float]],
                          risk_assessment: Dict[str, float],
                          strategy: str) -> str:
        """Generate human-readable reasoning for the decision."""
        best_score = all_options[0][1]
        
        reasoning_parts = []
        
        # Strategy used
        reasoning_parts.append(f"Decision made using {strategy} strategy.")
        
        # Why this option was selected
        if hasattr(selected_option, '_scoring_details'):
            top_criteria = sorted(
                selected_option['_scoring_details'].items(),
                key=lambda x: x[1]['weighted_score'],
                reverse=True
            )[:2]
            criteria_desc = ", ".join([f"{name} ({details['weighted_score']:.3f})" 
                                     for name, details in top_criteria])
            reasoning_parts.append(f"Selected based on strong performance in: {criteria_desc}")
        
        # Score comparison
        if len(all_options) > 1:
            second_best_score = all_options[1][1]
            score_margin = best_score - second_best_score
            reasoning_parts.append(f"Score margin over next best option: {score_margin:.3f}")
        
        # Risk considerations
        overall_risk = risk_assessment.get('overall_risk', 0.5)
        if overall_risk < 0.3:
            reasoning_parts.append("Low risk assessment supports this choice.")
        elif overall_risk > 0.7:
            reasoning_parts.append("High risk identified - careful monitoring required.")
        
        return " ".join(reasoning_parts)
    
    def _calculate_confidence(self, scored_options: List[Tuple[Dict[str, Any], float]],
                            risk_assessment: Dict[str, float]) -> float:
        """Calculate confidence level for the decision."""
        if len(scored_options) < 2:
            base_confidence = 0.6
        else:
            # Base confidence on score separation
            best_score = scored_options[0][1]
            second_score = scored_options[1][1]
            score_separation = best_score - second_score
            base_confidence = min(0.9, 0.5 + score_separation)
        
        # Adjust for risk
        overall_risk = risk_assessment.get('overall_risk', 0.5)
        risk_adjustment = (1.0 - overall_risk) * 0.3
        
        final_confidence = max(0.1, min(0.95, base_confidence + risk_adjustment))
        return final_confidence
    
    def _estimate_impact(self, option: Dict[str, Any], 
                        context: DecisionContext) -> Dict[str, Any]:
        """Estimate the expected impact of the selected option."""
        return {
            'performance_improvement': option.get('expected_performance_gain', 0.1),
            'resource_impact': option.get('resource_usage_change', 0.0),
            'stakeholder_satisfaction': option.get('stakeholder_impact_score', 0.5),
            'time_to_value': option.get('time_to_value_days', 1),
            'scalability_impact': option.get('scalability_factor', 1.0)
        }
    
    def add_strategy(self, name: str, strategy: DecisionStrategy) -> None:
        """Add a custom decision strategy."""
        self.strategies[name] = strategy
    
    def get_decision_insights(self) -> Dict[str, Any]:
        """Get insights from historical decisions."""
        if not self.decision_history:
            return {}
        
        # Analyze decision patterns
        strategy_usage = defaultdict(int)
        confidence_levels = []
        risk_levels = []
        
        for context, outcome in self.decision_history[-100:]:  # Last 100 decisions
            # This would need to track which strategy was used
            confidence_levels.append(outcome.confidence)
            risk_levels.append(outcome.risk_assessment.get('overall_risk', 0.5))
        
        return {
            'total_decisions': len(self.decision_history),
            'average_confidence': sum(confidence_levels) / len(confidence_levels) if confidence_levels else 0,
            'average_risk': sum(risk_levels) / len(risk_levels) if risk_levels else 0,
            'strategy_usage': dict(strategy_usage)
        }

def create_decision_engine() -> AdvancedDecisionEngine:
    """Factory function to create a configured decision engine."""
    return AdvancedDecisionEngine()
