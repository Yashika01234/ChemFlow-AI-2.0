import re
from collections import defaultdict
from sympy import Matrix
from sympy import lcm
from functools import reduce

TOKEN = re.compile(r"([A-Z][a-z]?)(\d*)")

def parse_formula(formula: str):
    # Supports ordinary molecular formulae, parentheses, and nested groups.
    tokens = re.findall(r"[A-Z][a-z]?|\d+|[()]", formula)
    if "".join(tokens) != formula:
        raise ValueError(f"Unsupported formula syntax: {formula}")
    stack = [defaultdict(int)]
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == "(":
            stack.append(defaultdict(int)); i += 1
        elif tok == ")":
            if len(stack) == 1:
                raise ValueError("Unmatched closing parenthesis")
            group = stack.pop(); i += 1
            mult = int(tokens[i]) if i < len(tokens) and tokens[i].isdigit() else 1
            if mult != 1 or (i < len(tokens) and tokens[i].isdigit()): i += 1
            for el, n in group.items(): stack[-1][el] += n * mult
        elif tok.isdigit():
            raise ValueError("A coefficient cannot appear inside a formula")
        else:
            el = tok; i += 1
            n = int(tokens[i]) if i < len(tokens) and tokens[i].isdigit() else 1
            if i < len(tokens) and tokens[i].isdigit(): i += 1
            stack[-1][el] += n
    if len(stack) != 1:
        raise ValueError("Unmatched opening parenthesis")
    return dict(stack[0])

def split_equation(equation: str):
    sides = re.split(r"\s*(?:->|→|=)\s*", equation)
    if len(sides) != 2:
        raise ValueError("Use one reaction arrow, e.g. H2 + O2 -> H2O")
    return [[x.strip() for x in side.split("+")] for side in sides]

def balance_equation(equation: str):
    left, right = split_equation(equation)
    compounds = left + right
    parsed = [parse_formula(x) for x in compounds]
    elements = sorted({e for f in parsed for e in f})
    rows = []
    for element in elements:
        rows.append([f.get(element, 0) * (1 if i < len(left) else -1)
                     for i, f in enumerate(parsed)])
    null = Matrix(rows).nullspace()
    if not null:
        raise ValueError("Could not find a balance for this equation")
    vec = null[0]
    denom = 1
    for value in vec: denom = lcm(denom, value.q)
    coeffs = [int(value * denom) for value in vec]
    if all(c < 0 for c in coeffs): coeffs = [-c for c in coeffs]
    if any(c <= 0 for c in coeffs):
        raise ValueError("Equation does not have a positive stoichiometric solution")
    divisor = reduce(lambda a, b: __import__("math").gcd(a, b), coeffs)
    coeffs = [c // divisor for c in coeffs]
    formatted = []
    for i, species in enumerate(compounds):
        coefficient = "" if coeffs[i] == 1 else str(coeffs[i])
        formatted.append(coefficient + species)
    return {"balanced_equation": " + ".join(formatted[:len(left)]) + " -> " + " + ".join(formatted[len(left):]),
            "coefficients": coeffs, "elements": elements}

def limiting_reagent(moles: dict[str, float], coefficients: dict[str, float],
                     product_coefficient: float, product_molar_mass: float):
    if not moles or not coefficients:
        raise ValueError("Provide moles and balanced reactant coefficients")
    ratios = {name: amount / coefficients[name] for name, amount in moles.items()
              if name in coefficients and amount >= 0 and coefficients[name] > 0}
    if len(ratios) != len(moles):
        raise ValueError("Every reactant needs a positive balanced coefficient and non-negative moles")
    limiting = min(ratios, key=ratios.get)
    extent = ratios[limiting]
    product_moles = extent * product_coefficient
    return {
        "limiting_reagent": limiting,
        "reaction_extent_moles": round(extent, 8),
        "theoretical_product_moles": round(product_moles, 8),
        "theoretical_product_grams": round(product_moles * product_molar_mass, 6),
    }
