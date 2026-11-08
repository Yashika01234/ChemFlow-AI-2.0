from rdkit import Chem
from rdkit.Chem import rdChemReactions

# Explicitly supported educational templates; not a general reaction prediction model.
TEMPLATES = {
    "hydrogenation": {
        "smarts": "[C:1]=[C:2]>>[C:1]-[C:2]",
        "description": "Reduces a carbon-carbon double bond to a single bond. Hydrogen is implicit in this simplified template.",
        "conditions": "Typically requires H2 and a suitable catalyst; conditions are not modeled."
    },
    "alcohol_oxidation": {
        "smarts": "[CH2:1][OH:2]>>[CH:1]=[O:2]",
        "description": "A simplified primary-alcohol-to-aldehyde transformation.",
        "conditions": "Oxidant and selectivity are not modeled."
    },
    "ester_hydrolysis": {
        "smarts": "[C:1](=[O:2])[O:3][C:4]>>[C:1](=[O:2])[OH].[C:4][OH]",
        "description": "Splits an ester into a carboxylic acid and an alcohol in a simplified hydrolysis template.",
        "conditions": "Water, catalyst, pH, and work-up are not modeled."
    }
}

def predict_products(reaction: str, reactants: list[str]):
    if reaction not in TEMPLATES:
        raise ValueError(f"Unsupported reaction. Choose one of: {', '.join(TEMPLATES)}")
    template = TEMPLATES[reaction]
    rxn = rdChemReactions.ReactionFromSmarts(template["smarts"])
    parsed = []
    for smiles in reactants:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid reactant SMILES: {smiles}")
        parsed.append(mol)
    outcomes = rxn.RunReactants(tuple(parsed[:rxn.GetNumReactantTemplates()]))
    products = []
    for outcome in outcomes:
        for product in outcome:
            try:
                Chem.SanitizeMol(product)
                products.append(Chem.MolToSmiles(product))
            except Exception:
                continue
    products = sorted(set(products))
    return {
        "reaction": reaction,
        "description": template["description"],
        "conditions_note": template["conditions"],
        "products": products,
        "candidate_count": len(products),
        "scope_warning": "Template-based educational candidates only; verify independently before drawing chemical conclusions."
    }
