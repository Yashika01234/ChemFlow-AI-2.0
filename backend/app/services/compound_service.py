from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, Crippen

FUNCTIONAL_GROUPS = {
    "alcohol": "[OX2H][CX4]",
    "phenol": "[OX2H]c",
    "aldehyde": "[CX3H1](=O)[#6]",
    "ketone": "[#6][CX3](=O)[#6]",
    "carboxylic_acid": "[CX3](=O)[OX2H1]",
    "ester": "[CX3](=O)[OX2H0][#6]",
    "amide": "[NX3][CX3](=[OX1])[#6]",
    "amine": "[NX3;H2,H1;!$(NC=O)]",
    "alkene": "[CX3]=[CX3]",
    "alkyne": "[CX2]#[CX2]",
    "nitrile": "[CX2]#N",
    "ether": "[OD2]([#6])[#6]",
    "halide": "[F,Cl,Br,I]",
    "aromatic_ring": "a1aaaaa1",
}

SMARTS = {name: Chem.MolFromSmarts(pattern) for name, pattern in FUNCTIONAL_GROUPS.items()}

def analyze_compound(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES. Check atom symbols, brackets, and bond notation.")
    canonical = Chem.MolToSmiles(mol)
    formula = rdMolDescriptors.CalcMolFormula(mol)
    groups = []
    for name, pattern in SMARTS.items():
        if pattern and mol.HasSubstructMatch(pattern):
            groups.append(name)
    return {
        "canonical_smiles": canonical,
        "formula": formula,
        "molecular_weight": round(Descriptors.MolWt(mol), 4),
        "exact_mass": round(Descriptors.ExactMolWt(mol), 4),
        "logp": round(Crippen.MolLogP(mol), 4),
        "tpsa": round(rdMolDescriptors.CalcTPSA(mol), 4),
        "h_bond_donors": rdMolDescriptors.CalcNumHBD(mol),
        "h_bond_acceptors": rdMolDescriptors.CalcNumHBA(mol),
        "rotatable_bonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
        "heavy_atoms": mol.GetNumHeavyAtoms(),
        "functional_groups": groups,
    }

def classify_organic(smiles: list[str]):
    results = [analyze_compound(s) for s in smiles]
    groups = sorted({g for item in results for g in item["functional_groups"]})
    if "alkene" in groups:
        reaction_type = "addition"
        explanation = "At least one reactant contains a carbon-carbon double bond; addition reactions are a common reaction family to investigate."
    elif "carboxylic_acid" in groups and "alcohol" in groups:
        reaction_type = "condensation_esterification_candidate"
        explanation = "A carboxylic acid and an alcohol are present; esterification is a plausible textbook transformation under suitable conditions."
    elif "alcohol" in groups:
        reaction_type = "oxidation_or_substitution_candidate"
        explanation = "An alcohol is present. Depending on its class and reagents, oxidation or substitution may be relevant."
    else:
        reaction_type = "unclassified"
        explanation = "No rule in this small educational classifier matched the detected groups."
    return {"reactants": results, "detected_groups": groups,
            "reaction_family": reaction_type, "explanation": explanation}
