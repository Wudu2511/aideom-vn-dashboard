"""
Module chạy 5 kịch bản chính sách của AIDEOM-VN.

Các kịch bản gồm:
S1 - Truyền thống
S2 - Số hóa nhanh
S3 - AI dẫn dắt
S4 - Bao trùm số
S5 - Tối ưu cân bằng
"""

SCENARIOS = {
    "S1 - Truyền thống": {
        "description": "Tập trung vốn vật chất, FDI, hạ tầng truyền thống và xuất khẩu",
        "K": 0.70,
        "D": 0.10,
        "AI": 0.10,
        "H": 0.10
    },
    "S2 - Số hóa nhanh": {
        "description": "Tăng đầu tư vào chính phủ số, doanh nghiệp số và thanh toán số",
        "K": 0.25,
        "D": 0.45,
        "AI": 0.15,
        "H": 0.15
    },
    "S3 - AI dẫn dắt": {
        "description": "Ưu tiên AI, dữ liệu lớn, bán dẫn và trung tâm dữ liệu",
        "K": 0.20,
        "D": 0.20,
        "AI": 0.45,
        "H": 0.15
    },
    "S4 - Bao trùm số": {
        "description": "Ưu tiên vùng yếu, SME, giáo dục số và nông nghiệp số",
        "K": 0.30,
        "D": 0.20,
        "AI": 0.10,
        "H": 0.40
    },
    "S5 - Tối ưu cân bằng": {
        "description": "Cân bằng giữa tăng trưởng, số hóa, AI, nhân lực và rủi ro",
        "K": 0.40,
        "D": 0.25,
        "AI": 0.15,
        "H": 0.20
    }
}


def run_scenario(name, budget=100000):
    """
    Tính phân bổ ngân sách theo một kịch bản.

    Parameters
    ----------
    name : str
        Tên kịch bản.
    budget : float
        Tổng ngân sách giả định.

    Returns
    -------
    dict
        Kết quả phân bổ ngân sách theo K, D, AI, H.
    """
    if name not in SCENARIOS:
        raise ValueError("Tên kịch bản không hợp lệ.")

    scenario = SCENARIOS[name]

    return {
        "scenario": name,
        "description": scenario["description"],
        "K": budget * scenario["K"],
        "D": budget * scenario["D"],
        "AI": budget * scenario["AI"],
        "H": budget * scenario["H"],
        "total": budget
    }


def compare_scenarios(budget=100000):
    """
    So sánh toàn bộ 5 kịch bản chính sách.
    """
    return [run_scenario(name, budget) for name in SCENARIOS]
