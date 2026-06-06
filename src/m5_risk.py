"""
M5 - Đánh giá rủi ro.

Module này đại diện cho phần đánh giá rủi ro trong hệ thống AIDEOM-VN,
bao gồm rủi ro môi trường, rủi ro an ninh dữ liệu và rủi ro bất định kịch bản.
"""

def get_module_name():
    return "M5 - Đánh giá rủi ro"


def summarize():
    return {
        "module": "M5",
        "name": "Đánh giá rủi ro",
        "method": "Pareto, stochastic programming và cảnh báo rủi ro",
        "input": "Tham số rủi ro, kịch bản và kết quả mô hình",
        "output": "Cảnh báo rủi ro và đánh đổi chính sách"
    }
