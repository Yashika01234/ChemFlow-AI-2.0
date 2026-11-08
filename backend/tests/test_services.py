import pytest
from app.services.compound_service import analyze_compound
from app.services.stoichiometry_service import balance_equation, limiting_reagent
from app.services.simulation_service import monte_carlo_yield

def test_compound_analysis_ethanol():
    result = analyze_compound("CCO")
    assert result["formula"] == "C2H6O"
    assert "alcohol" in result["functional_groups"]
    assert result["molecular_weight"] > 40

def test_invalid_smiles():
    with pytest.raises(ValueError):
        analyze_compound("not-a-smiles")

def test_balance_iron_oxide():
    result = balance_equation("Fe + O2 -> Fe2O3")
    assert result["balanced_equation"] == "4Fe + 3O2 -> 2Fe2O3"

def test_limiting_reagent():
    result = limiting_reagent({"H2": 2, "O2": 1}, {"H2": 2, "O2": 1}, 2, 18.015)
    assert result["limiting_reagent"] == "H2"
    assert result["theoretical_product_moles"] == 2

def test_monte_carlo_reproducible():
    a = monte_carlo_yield(.75, .05, 1000, 4)
    b = monte_carlo_yield(.75, .05, 1000, 4)
    assert a == b
    assert 0 <= a["p05"] <= a["p95"] <= 1
