"""
M3 - Tối ưu phân bổ.

Module này đại diện cho các bài toán tối ưu phân bổ ngân sách,
bao gồm quy hoạch tuyến tính LP, quy hoạch nguyên hỗn hợp MIP
và tối ưu phân bổ theo ngành - vùng - thời gian.
"""

def get_module_name():
    return "M3 - Tối ưu phân bổ"


def summarize():
    return {
        "module": "M3",
        "name": "Tối ưu phân bổ",
        "method": "LP, MIP, tối ưu động",
        "input": "Ngân sách, hệ số tác động, ràng buộc chính sách",
        "output": "Phân bổ ngân sách tối ưu"
    }
