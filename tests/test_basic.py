from src.scenario_runner import compare_scenarios, run_scenario


def test_compare_scenarios_has_five_scenarios():
    results = compare_scenarios()
    assert len(results) == 5


def test_s1_budget_sum():
    result = run_scenario("S1 - Truyền thống", budget=100000)
    total = result["K"] + result["D"] + result["AI"] + result["H"]
    assert total == 100000


def test_s3_has_high_ai_allocation():
    result = run_scenario("S3 - AI dẫn dắt", budget=100000)
    assert result["AI"] == 45000


def test_s5_balanced_scenario():
    result = run_scenario("S5 - Tối ưu cân bằng", budget=100000)
    assert result["K"] == 40000
    assert result["D"] == 25000
    assert result["AI"] == 15000
    assert result["H"] == 20000
