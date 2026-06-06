"""
M1 - Dự báo kinh tế.

Module này đại diện cho phần dự báo kinh tế của hệ thống AIDEOM-VN.
Nội dung chính gồm tổng hợp kết quả GDP, TFP, lao động và các chỉ tiêu kinh tế vĩ mô.
"""

def get_module_name():
    return "M1 - Dự báo kinh tế"


def summarize():
    return {
        "module": "M1",
        "name": "Dự báo kinh tế",
        "method": "Cobb-Douglas mở rộng",
        "input": "Dữ liệu vĩ mô Việt Nam 2020-2025",
        "output": "GDP, TFP, lao động và dự báo kinh tế"
    }
