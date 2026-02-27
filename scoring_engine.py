#!/usr/bin/env python3
"""Pure numerology scoring logic shared by apps."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple

TRAITS = [
    "Execution",
    "Detail Precision",
    "Loyalty",
    "Politics Safe",
    "Ownership",
    "Discipline",
    "Communication",
    "Analytical",
    "Strategy",
]

CORE_TRAITS = [
    "Execution",
    "Detail Precision",
    "Loyalty",
    "Politics Safe",
    "Ownership",
    "Discipline",
    "Communication",
    "Analytical",
    "Strategy",
]

NEW_ATTRIBUTES = [
    "Authority",
    "Dominance",
    "Integrity",
    "Emotional Stability",
    "Aggression",
    "Risk Appetite",
    "Consistency",
    "Obedience",
    "Assertiveness",
    "Enforcement Ability",
]

ATTRIBUTE_KEYS = CORE_TRAITS + NEW_ATTRIBUTES

DESTINY_MATRIX: Dict[int, Dict[str, float]] = {
    1: {"Execution": 6, "Detail Precision": 5, "Loyalty": 4, "Politics Safe": 5, "Ownership": 7, "Communication": 8, "Analytical": 6, "Strategy": 9, "Authority": 9, "Dominance": 9, "Integrity": 7, "Emotional Stability": 6, "Aggression": 8, "Risk Appetite": 9, "Consistency": 7, "Obedience": 4, "Assertiveness": 9, "Enforcement Ability": 8},
    2: {"Execution": 5, "Detail Precision": 5, "Loyalty": 7, "Politics Safe": 7, "Ownership": 6, "Communication": 7, "Analytical": 5, "Strategy": 5, "Authority": 4, "Dominance": 3, "Integrity": 8, "Emotional Stability": 5, "Aggression": 3, "Risk Appetite": 4, "Consistency": 7, "Obedience": 8, "Assertiveness": 4, "Enforcement Ability": 4},
    3: {"Execution": 4, "Detail Precision": 4, "Loyalty": 4, "Politics Safe": 4, "Ownership": 4, "Communication": 9, "Analytical": 4, "Strategy": 8, "Authority": 5, "Dominance": 5, "Integrity": 6, "Emotional Stability": 5, "Aggression": 5, "Risk Appetite": 7, "Consistency": 4, "Obedience": 5, "Assertiveness": 6, "Enforcement Ability": 4},
    4: {"Execution": 9, "Detail Precision": 8, "Loyalty": 9, "Politics Safe": 9, "Ownership": 9, "Communication": 4, "Analytical": 8, "Strategy": 4, "Authority": 8, "Dominance": 7, "Integrity": 9, "Emotional Stability": 7, "Aggression": 8, "Risk Appetite": 6, "Consistency": 9, "Obedience": 7, "Assertiveness": 7, "Enforcement Ability": 9},
    5: {"Execution": 3, "Detail Precision": 3, "Loyalty": 3, "Politics Safe": 3, "Ownership": 3, "Communication": 6, "Analytical": 4, "Strategy": 6, "Authority": 5, "Dominance": 5, "Integrity": 5, "Emotional Stability": 5, "Aggression": 6, "Risk Appetite": 8, "Consistency": 3, "Obedience": 4, "Assertiveness": 6, "Enforcement Ability": 4},
    6: {"Execution": 6, "Detail Precision": 6, "Loyalty": 8, "Politics Safe": 8, "Ownership": 8, "Communication": 6, "Analytical": 5, "Strategy": 5, "Authority": 6, "Dominance": 6, "Integrity": 9, "Emotional Stability": 8, "Aggression": 6, "Risk Appetite": 5, "Consistency": 8, "Obedience": 7, "Assertiveness": 6, "Enforcement Ability": 7},
    7: {"Execution": 5, "Detail Precision": 6, "Loyalty": 4, "Politics Safe": 3, "Ownership": 5, "Communication": 3, "Analytical": 9, "Strategy": 7, "Authority": 4, "Dominance": 3, "Integrity": 9, "Emotional Stability": 8, "Aggression": 3, "Risk Appetite": 4, "Consistency": 6, "Obedience": 6, "Assertiveness": 4, "Enforcement Ability": 4},
    8: {"Execution": 8, "Detail Precision": 8, "Loyalty": 9, "Politics Safe": 8, "Ownership": 9, "Communication": 6, "Analytical": 7, "Strategy": 6, "Authority": 9, "Dominance": 8, "Integrity": 8, "Emotional Stability": 9, "Aggression": 8, "Risk Appetite": 7, "Consistency": 9, "Obedience": 6, "Assertiveness": 8, "Enforcement Ability": 9},
    9: {"Execution": 7.5, "Detail Precision": 6, "Loyalty": 9, "Politics Safe": 9, "Ownership": 9, "Communication": 6, "Analytical": 8, "Strategy": 8, "Authority": 7, "Dominance": 7, "Integrity": 9, "Emotional Stability": 7, "Aggression": 7, "Risk Appetite": 8, "Consistency": 7, "Obedience": 5, "Assertiveness": 7, "Enforcement Ability": 7},
}

BIRTH_CORE_MATRIX: Dict[int, Dict[str, float]] = {
    1: {"Execution": 6, "Detail Precision": 5, "Loyalty": 5, "Politics Safe": 6, "Ownership": 7, "Communication": 8, "Analytical": 6, "Strategy": 9},
    2: {"Execution": 5, "Detail Precision": 5, "Loyalty": 7, "Politics Safe": 7, "Ownership": 6, "Communication": 7, "Analytical": 5, "Strategy": 5},
    3: {"Execution": 4, "Detail Precision": 4, "Loyalty": 4, "Politics Safe": 4, "Ownership": 4, "Communication": 9, "Analytical": 4, "Strategy": 8},
    4: {"Execution": 9, "Detail Precision": 9, "Loyalty": 9, "Politics Safe": 9, "Ownership": 8, "Communication": 4, "Analytical": 8, "Strategy": 4},
    5: {"Execution": 5, "Detail Precision": 4, "Loyalty": 5, "Politics Safe": 5, "Ownership": 5, "Communication": 7, "Analytical": 5, "Strategy": 6},
    6: {"Execution": 6, "Detail Precision": 6, "Loyalty": 8, "Politics Safe": 8, "Ownership": 8, "Communication": 6, "Analytical": 5, "Strategy": 5},
    7: {"Execution": 5, "Detail Precision": 7, "Loyalty": 5, "Politics Safe": 4, "Ownership": 5, "Communication": 3, "Analytical": 9, "Strategy": 7},
    8: {"Execution": 8, "Detail Precision": 8, "Loyalty": 9, "Politics Safe": 8, "Ownership": 9, "Communication": 6, "Analytical": 7, "Strategy": 6},
    9: {"Execution": 7, "Detail Precision": 5, "Loyalty": 8, "Politics Safe": 8, "Ownership": 8, "Communication": 7, "Analytical": 8, "Strategy": 8},
}

MONTH_CORE_MATRIX: Dict[int, Dict[str, float]] = {
    1: {"Execution": 7, "Detail Precision": 6, "Loyalty": 7, "Politics Safe": 7, "Ownership": 7, "Communication": 7, "Analytical": 6, "Strategy": 8},
    2: {"Execution": 5, "Detail Precision": 5, "Loyalty": 8, "Politics Safe": 7, "Ownership": 6, "Communication": 7, "Analytical": 5, "Strategy": 5},
    3: {"Execution": 4, "Detail Precision": 4, "Loyalty": 4, "Politics Safe": 3, "Ownership": 4, "Communication": 9, "Analytical": 4, "Strategy": 8},
    4: {"Execution": 8, "Detail Precision": 8, "Loyalty": 8, "Politics Safe": 9, "Ownership": 8, "Communication": 4, "Analytical": 7, "Strategy": 4},
    5: {"Execution": 4, "Detail Precision": 4, "Loyalty": 4, "Politics Safe": 3, "Ownership": 4, "Communication": 7, "Analytical": 5, "Strategy": 6},
    6: {"Execution": 6, "Detail Precision": 6, "Loyalty": 8, "Politics Safe": 8, "Ownership": 8, "Communication": 6, "Analytical": 5, "Strategy": 5},
    7: {"Execution": 5, "Detail Precision": 6, "Loyalty": 3, "Politics Safe": 2, "Ownership": 5, "Communication": 3, "Analytical": 9, "Strategy": 7},
    8: {"Execution": 8, "Detail Precision": 8, "Loyalty": 9, "Politics Safe": 8, "Ownership": 9, "Communication": 6, "Analytical": 7, "Strategy": 6},
    9: {"Execution": 7, "Detail Precision": 5, "Loyalty": 8, "Politics Safe": 8, "Ownership": 8, "Communication": 7, "Analytical": 8, "Strategy": 8},
}

BIRTH_MULTIPLIERS = {
    "Authority": 1.1,
    "Dominance": 1.1,
    "Aggression": 1.15,
    "Assertiveness": 1.1,
    "Enforcement Ability": 1.1,
    "Integrity": 1.0,
    "Consistency": 1.0,
    "Obedience": 0.95,
    "Risk Appetite": 1.1,
    "Emotional Stability": 0.95,
}

MONTH_MULTIPLIERS = {
    "Authority": 0.85,
    "Dominance": 0.85,
    "Aggression": 0.85,
    "Assertiveness": 0.9,
    "Enforcement Ability": 0.9,
    "Integrity": 0.95,
    "Consistency": 0.9,
    "Obedience": 1.05,
    "Risk Appetite": 0.9,
    "Emotional Stability": 1.1,
}


def _build_augmented_matrix(
    core_matrix: Dict[int, Dict[str, float]],
    destiny_matrix: Dict[int, Dict[str, float]],
    multipliers: Dict[str, float],
) -> Dict[int, Dict[str, float]]:
    out: Dict[int, Dict[str, float]] = {}
    for n in range(1, 10):
        row = dict(core_matrix[n])
        for attr in NEW_ATTRIBUTES:
            value = destiny_matrix[n][attr] * multipliers[attr]
            value = max(0.0, min(10.0, value))
            row[attr] = value
        out[n] = row
    return out


BIRTH_MATRIX = _build_augmented_matrix(BIRTH_CORE_MATRIX, DESTINY_MATRIX, BIRTH_MULTIPLIERS)
MONTH_MATRIX = _build_augmented_matrix(MONTH_CORE_MATRIX, DESTINY_MATRIX, MONTH_MULTIPLIERS)

DISCIPLINE_MATRIX: Dict[int, Dict[str, float]] = {
    1: {"Process": 8, "Value": 7, "General": 9, "External Enforcement": 8, "Self Control": 7, "Rule Compliance": 8},
    2: {"Process": 6, "Value": 8, "General": 6, "External Enforcement": 5, "Self Control": 6, "Rule Compliance": 8},
    3: {"Process": 4, "Value": 4, "General": 4, "External Enforcement": 4, "Self Control": 4, "Rule Compliance": 4},
    4: {"Process": 9, "Value": 8, "General": 9, "External Enforcement": 9, "Self Control": 9, "Rule Compliance": 9},
    5: {"Process": 4, "Value": 5, "General": 4, "External Enforcement": 4, "Self Control": 5, "Rule Compliance": 4},
    6: {"Process": 7, "Value": 9, "General": 7, "External Enforcement": 7, "Self Control": 8, "Rule Compliance": 9},
    7: {"Process": 5, "Value": 7, "General": 5, "External Enforcement": 5, "Self Control": 7, "Rule Compliance": 7},
    8: {"Process": 9, "Value": 8, "General": 8, "External Enforcement": 9, "Self Control": 9, "Rule Compliance": 8},
    9: {"Process": 7, "Value": 9, "General": 7, "External Enforcement": 7, "Self Control": 8, "Rule Compliance": 9},
}

ATTRIBUTE_WEIGHTS = {
    "Authority": {"Birth": 0.5, "Destiny": 0.4, "Month": 0.1},
    "Dominance": {"Birth": 0.5, "Destiny": 0.4, "Month": 0.1},
    "Integrity": {"Birth": 0.4, "Destiny": 0.4, "Month": 0.2},
    "Emotional Stability": {"Birth": 0.4, "Destiny": 0.4, "Month": 0.2},
    "Aggression": {"Birth": 0.5, "Destiny": 0.3, "Month": 0.2},
    "Risk Appetite": {"Birth": 0.5, "Destiny": 0.3, "Month": 0.2},
    "Consistency": {"Birth": 0.4, "Destiny": 0.4, "Month": 0.2},
    "Obedience": {"Birth": 0.5, "Destiny": 0.3, "Month": 0.2},
    "Assertiveness": {"Birth": 0.5, "Destiny": 0.4, "Month": 0.1},
    "Enforcement Ability": {"Birth": 0.5, "Destiny": 0.4, "Month": 0.1},
}

TRAIT_ATTRIBUTE_MAP: Dict[str, Dict[str, float]] = {
    "Contractor Control Ability": {"Authority": 0.30, "Dominance": 0.25, "Enforcement Ability": 0.25, "Emotional Stability": 0.20},
    "Workforce Control Ability": {"Authority": 0.30, "Enforcement Ability": 0.30, "Dominance": 0.20, "Consistency": 0.20},
    "Disciplinary Enforcement": {"Enforcement Ability": 0.40, "Authority": 0.30, "Consistency": 0.20, "Aggression": 0.10},
    "Rule Enforcement": {"Enforcement Ability": 0.40, "Integrity": 0.30, "Consistency": 0.30},
    "Corruption Resistance": {"Integrity": 0.50, "Consistency": 0.30, "Emotional Stability": 0.20},
    "Confidentiality": {"Integrity": 0.50, "Obedience": 0.30, "Consistency": 0.20},
    "Financial Honesty": {"Integrity": 0.60, "Consistency": 0.25, "Detail Precision": 0.15},
    "Loyalty to Employer": {"Loyalty": 0.50, "Obedience": 0.30, "Integrity": 0.20},
    "Political Neutrality": {"Politics Safe": 0.60, "Integrity": 0.20, "Emotional Stability": 0.20},
    "Leadership Ability": {"Authority": 0.30, "Assertiveness": 0.30, "Dominance": 0.20, "Risk Appetite": 0.20},
    "Decision Making Ability": {"Strategy": 0.30, "Authority": 0.30, "Risk Appetite": 0.20, "Emotional Stability": 0.20},
    "Crisis Leadership": {"Authority": 0.30, "Emotional Stability": 0.30, "Aggression": 0.20, "Strategy": 0.20},
    "Task Completion Reliability": {"Execution": 0.50, "Consistency": 0.30, "Obedience": 0.20},
    "Deadline Reliability": {"Execution": 0.40, "Consistency": 0.40, "Emotional Stability": 0.20},
    "Operational Discipline": {"Consistency": 0.40, "Execution": 0.30, "Integrity": 0.30},
    "Emotional Control": {"Emotional Stability": 0.60, "Consistency": 0.40},
    "Stress Tolerance": {"Emotional Stability": 0.60, "Consistency": 0.20, "Authority": 0.20},
    "Impulse Control": {"Emotional Stability": 0.50, "Integrity": 0.30, "Consistency": 0.20},
    "Problem Solving Ability": {"Analytical": 0.50, "Strategy": 0.30, "Execution": 0.20},
    "Strategic Thinking": {"Strategy": 0.60, "Analytical": 0.40},
    "Planning Ability": {"Strategy": 0.50, "Consistency": 0.30, "Execution": 0.20},
    "Instruction Compliance": {"Obedience": 0.50, "Consistency": 0.30, "Execution": 0.20},
    "Assertive Communication": {"Assertiveness": 0.60, "Communication": 0.40},
    "Persuasion Ability": {"Communication": 0.50, "Assertiveness": 0.30, "Authority": 0.20},
    "Authority Presence": {"Authority": 0.60, "Dominance": 0.40},
    "Command Capability": {"Authority": 0.40, "Enforcement Ability": 0.30, "Dominance": 0.30},
    "Control Orientation": {"Dominance": 0.40, "Authority": 0.30, "Aggression": 0.30},
    "Risk Taking Ability": {"Risk Appetite": 0.60, "Authority": 0.20, "Assertiveness": 0.20},
    "Calculated Risk Ability": {"Risk Appetite": 0.40, "Strategy": 0.40, "Analytical": 0.20},
    "Ownership Mentality": {"Ownership": 0.60, "Consistency": 0.40},
    "Responsibility Acceptance": {"Ownership": 0.50, "Integrity": 0.30, "Consistency": 0.20},
    "Attention to Detail": {"Detail Precision": 0.70, "Consistency": 0.30},
    "Quality Orientation": {"Detail Precision": 0.50, "Consistency": 0.30, "Integrity": 0.20},
    "Work Ethic": {"Execution": 0.40, "Consistency": 0.40, "Integrity": 0.20},
    "Reliability": {"Consistency": 0.50, "Integrity": 0.30, "Execution": 0.20},
    "Compliance Orientation": {"Obedience": 0.50, "Integrity": 0.30, "Consistency": 0.20},
    "Supervisory Ability": {"Authority": 0.30, "Enforcement Ability": 0.30, "Dominance": 0.20, "Consistency": 0.20},
    "Hierarchy Respect": {"Obedience": 0.50, "Integrity": 0.30, "Consistency": 0.20},
    "Follow Through Ability": {"Execution": 0.50, "Consistency": 0.30, "Ownership": 0.20},
    "Independent Thinking": {"Analytical": 0.40, "Strategy": 0.40, "Risk Appetite": 0.20},
    "Conflict Handling": {"Emotional Stability": 0.40, "Authority": 0.30, "Assertiveness": 0.30},
    "Negotiation Ability": {"Communication": 0.40, "Strategy": 0.30, "Assertiveness": 0.30},
    "Organizational Ability": {"Consistency": 0.40, "Strategy": 0.30, "Execution": 0.30},
    "Focus Stability": {"Consistency": 0.50, "Emotional Stability": 0.30, "Execution": 0.20},
    "Self Motivation": {"Ownership": 0.40, "Execution": 0.30, "Risk Appetite": 0.30},
    "Persistence": {"Consistency": 0.50, "Execution": 0.30, "Authority": 0.20},
    "Learning Ability": {"Analytical": 0.40, "Ownership": 0.30, "Execution": 0.30},
    "Adaptability": {"Emotional Stability": 0.40, "Analytical": 0.30, "Execution": 0.30},
    "Initiative": {"Ownership": 0.40, "Execution": 0.30, "Risk Appetite": 0.30},
    "Situational Awareness": {"Analytical": 0.40, "Emotional Stability": 0.30, "Politics Safe": 0.30},
}

ROLE_WEIGHTS = {
    "Execution Focused": {
        "Finish Execution": 0.25,
        "Loyalty": 0.25,
        "Self Ownership": 0.15,
        "Politics Safe": 0.15,
        "Communication": 0.05,
        "Strategy & Analytical": 0.15,
    },
    "Strategy Focused": {
        "Finish Execution": 0.05,
        "Loyalty": 0.20,
        "Self Ownership": 0.15,
        "Politics Safe": 0.15,
        "Communication": 0.20,
        "Strategy & Analytical": 0.25,
    },
}


@dataclass
class ScoreResult:
    candidate_numbers: Dict[str, int]
    leader_numbers: Dict[str, int]
    trait_scores: Dict[str, float]
    composite_scores: Dict[str, float]
    loyalty_meta: Dict[str, float]
    risk_status: str
    risk_flags: List[str]
    overall_score_100: float
    verdict: str
    flags: List[str]


def clamp(value: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, value))


def digital_root(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 0
    while n > 9:
        n = sum(int(ch) for ch in str(n))
    return n


def validate_dob(dob: str) -> str:
    try:
        parsed = datetime.strptime(dob.strip(), "%d/%m/%Y")
    except ValueError as exc:
        raise ValueError("DOB must be in dd/mm/yyyy format and be a valid date.") from exc
    return parsed.strftime("%d/%m/%Y")


def numerology_numbers(dob: str) -> Dict[str, int]:
    day, month, year = map(int, dob.split("/"))
    birth = digital_root(day)
    month_total = digital_root(month)
    destiny = digital_root(sum(int(ch) for ch in f"{day:02d}{month:02d}{year:04d}"))

    if birth == 0:
        birth = 9
    if month_total == 0:
        month_total = 9
    if destiny == 0:
        destiny = 9

    return {"birth": birth, "month": month_total, "destiny": destiny}


def calculate_numbers_from_dob(dob: str) -> Tuple[int, int, int]:
    normalized = validate_dob(dob)
    nums = numerology_numbers(normalized)
    return nums["birth"], nums["destiny"], nums["month"]


def calculate_attribute_score(attribute: str, birth: int, destiny: int, month: int) -> float:
    weights = ATTRIBUTE_WEIGHTS[attribute]
    score = (
        BIRTH_MATRIX[birth][attribute] * weights["Birth"]
        + DESTINY_MATRIX[destiny][attribute] * weights["Destiny"]
        + MONTH_MATRIX[month][attribute] * weights["Month"]
    )
    return round(clamp(score), 2)


def calculate_all_attribute_scores(numbers: Dict[str, int], base_traits: Dict[str, float]) -> Dict[str, float]:
    values: Dict[str, float] = {k: float(v) for k, v in base_traits.items()}
    for attribute in NEW_ATTRIBUTES:
        values[attribute] = calculate_attribute_score(
            attribute=attribute,
            birth=numbers["birth"],
            destiny=numbers["destiny"],
            month=numbers["month"],
        )
    return values


def calculate_authority_alignment(attr: Dict[str, float]) -> float:
    score = (
        attr["Authority"] * 0.30
        + attr["Integrity"] * 0.25
        + attr["Obedience"] * 0.20
        + attr["Consistency"] * 0.15
        + attr["Emotional Stability"] * 0.10
    )
    return clamp(score)


def calculate_peer_influence(attr: Dict[str, float]) -> float:
    score = (
        (10 - attr["Emotional Stability"]) * 0.35
        + (10 - attr["Dominance"]) * 0.25
        + (10 - attr["Assertiveness"]) * 0.15
        + attr["Risk Appetite"] * 0.15
        + attr["Aggression"] * 0.10
    )
    return clamp(score)


def compute_trait_scores(destiny: int, birth: int, month: int) -> Dict[str, float]:
    base_traits = {
        trait: (
            DESTINY_MATRIX[destiny][trait] * 0.5
            + BIRTH_MATRIX[birth][trait] * 0.3
            + MONTH_MATRIX[month][trait] * 0.2
        )
        for trait in TRAITS
        if trait != "Discipline"
    }

    process_score = (
        DISCIPLINE_MATRIX[destiny]["Process"] * 0.5
        + DISCIPLINE_MATRIX[birth]["Process"] * 0.3
        + DISCIPLINE_MATRIX[month]["Process"] * 0.2
    )
    value_score = (
        DISCIPLINE_MATRIX[destiny]["Value"] * 0.5
        + DISCIPLINE_MATRIX[birth]["Value"] * 0.3
        + DISCIPLINE_MATRIX[month]["Value"] * 0.2
    )
    general_score = (
        DISCIPLINE_MATRIX[destiny]["General"] * 0.5
        + DISCIPLINE_MATRIX[birth]["General"] * 0.3
        + DISCIPLINE_MATRIX[month]["General"] * 0.2
    )
    discipline_score = clamp(process_score * 0.4 + value_score * 0.35 + general_score * 0.25)
    base_traits["Discipline"] = discipline_score
    return base_traits


def apply_adjustments(trait_scores: Dict[str, float], candidate_numbers: Dict[str, int]) -> List[str]:
    flags: List[str] = []

    if (
        candidate_numbers["destiny"] == 9
        and candidate_numbers["birth"] == 9
        and candidate_numbers["month"] == 9
    ):
        flags.append("Triple 9: Soft firing / compassion bias")

    if candidate_numbers["destiny"] in {4, 8, 9}:
        trait_scores["Ownership"] = clamp(trait_scores["Ownership"] + 0.5)
        flags.append("Bonus: Destiny in {4,8,9} -> Ownership +0.5")

    if candidate_numbers["month"] == 1:
        trait_scores["Discipline"] = clamp(trait_scores["Discipline"] + 0.3)
        flags.append("Bonus: Month 1 -> Self-discipline +0.3")

    return flags


def compute_loyalty_pillar(
    traits: Dict[str, float],
    candidate_numbers: Dict[str, int],
    leader_numbers: Dict[str, int],
    attribute_scores: Dict[str, float],
) -> Dict[str, float]:
    baseline_loyalty = (traits["Loyalty"] + traits["Politics Safe"]) / 2

    org_loyalty = baseline_loyalty
    if candidate_numbers["destiny"] in {4, 8, 9}:
        org_loyalty += 0.5
    org_loyalty = clamp(org_loyalty)

    leadership_penalty = 0.0
    no_penalty_triggered = True
    if candidate_numbers["destiny"] == 1 and leader_numbers["destiny"] == 1:
        leadership_penalty -= 2.0
        no_penalty_triggered = False
    if candidate_numbers["month"] == 7:
        leadership_penalty -= 1.0
        no_penalty_triggered = False
    if candidate_numbers["destiny"] == 5:
        leadership_penalty -= 1.0
        no_penalty_triggered = False
    if candidate_numbers["destiny"] in {4, 8, 9} and no_penalty_triggered:
        leadership_penalty += 0.3

    authority_alignment = calculate_authority_alignment(attribute_scores)
    peer_influence = calculate_peer_influence(attribute_scores)
    leadership_loyalty = (
        baseline_loyalty * 0.50
        + authority_alignment * 0.35
        - peer_influence * 0.18
        + leadership_penalty
    )
    leadership_loyalty = clamp(leadership_loyalty)
    final_loyalty = clamp(org_loyalty * 0.6 + leadership_loyalty * 0.4)

    return {
        "baseline_loyalty": baseline_loyalty,
        "org_loyalty": org_loyalty,
        "leadership_loyalty_base": baseline_loyalty,
        "leadership_penalty": leadership_penalty,
        "leadership_loyalty": leadership_loyalty,
        "final_loyalty": final_loyalty,
        "authority_alignment": authority_alignment,
        "peer_influence": peer_influence,
    }


def compute_composites(traits: Dict[str, float], loyalty_score: float) -> Dict[str, float]:
    return {
        "Finish Execution": (traits["Execution"] + traits["Detail Precision"]) / 2,
        "Self Ownership": (traits["Ownership"] + traits["Discipline"]) / 2,
        "Strategy & Analytical": (traits["Strategy"] + traits["Analytical"]) / 2,
        "Loyalty": loyalty_score,
        "Politics Safe": traits["Politics Safe"],
        "Communication": traits["Communication"],
    }


def compute_overall(composites: Dict[str, float], role_type: str) -> float:
    overall_10 = sum(composites[name] * ROLE_WEIGHTS[role_type][name] for name in ROLE_WEIGHTS[role_type])
    return overall_10 * 10.0


def compute_risk_gate(composites: Dict[str, float], traits: Dict[str, float]) -> Tuple[str, List[str]]:
    risk_flags: List[str] = []
    loyalty = composites["Loyalty"]
    politics_safe = composites["Politics Safe"]
    self_ownership = composites["Self Ownership"]
    discipline = traits["Discipline"]

    if loyalty < 6.5:
        risk_flags.append("Low Loyalty")
    if politics_safe < 6.5:
        risk_flags.append("Political Risk")
    if self_ownership < 6.5:
        risk_flags.append("Low Self Ownership")
    if discipline < 6:
        risk_flags.append("Low Discipline")

    risk_status = "FAIL" if risk_flags else "PASS"
    return risk_status, risk_flags


def verdict_from_score(score_100: float) -> str:
    if score_100 >= 80:
        return "Strong Hire"
    if score_100 >= 65:
        return "Hire w/ Guardrails"
    return "Weak / Risk"


def calculate_role_score_weighted(trait_scores: Dict[str, float], role_trait_weights: Dict[str, float]) -> float:
    total_score = 0.0
    total_weight = 0.0
    for trait, weight in role_trait_weights.items():
        total_score += trait_scores.get(trait, 0.0) * weight
        total_weight += weight
    if total_weight <= 0:
        return 0.0
    return round(clamp(total_score / total_weight), 2)


def evaluate_candidate_for_role(
    birth: int,
    destiny: int,
    month: int,
    role_name: str,
    role_description: str,
    role_type: str = "Execution Focused",
    leader_dob: str = "03/11/1994",
) -> ScoreResult:
    del role_name, role_description
    candidate_numbers = {"birth": int(birth), "destiny": int(destiny), "month": int(month)}
    leader_numbers = numerology_numbers(validate_dob(leader_dob))

    trait_scores = compute_trait_scores(
        destiny=candidate_numbers["destiny"],
        birth=candidate_numbers["birth"],
        month=candidate_numbers["month"],
    )
    attribute_scores = calculate_all_attribute_scores(candidate_numbers, trait_scores)
    loyalty_meta = compute_loyalty_pillar(
        traits=trait_scores,
        candidate_numbers=candidate_numbers,
        leader_numbers=leader_numbers,
        attribute_scores=attribute_scores,
    )
    flags = apply_adjustments(trait_scores=trait_scores, candidate_numbers=candidate_numbers)
    composite_scores = compute_composites(trait_scores, loyalty_meta["final_loyalty"])
    risk_status, risk_flags = compute_risk_gate(composite_scores, trait_scores)
    overall_100 = compute_overall(composite_scores, role_type)
    final_verdict = "High Risk – Do Not Proceed" if risk_status == "FAIL" else verdict_from_score(overall_100)

    return ScoreResult(
        candidate_numbers=candidate_numbers,
        leader_numbers=leader_numbers,
        trait_scores=trait_scores,
        composite_scores=composite_scores,
        loyalty_meta=loyalty_meta,
        risk_status=risk_status,
        risk_flags=risk_flags,
        overall_score_100=overall_100,
        verdict=final_verdict,
        flags=flags,
    )
