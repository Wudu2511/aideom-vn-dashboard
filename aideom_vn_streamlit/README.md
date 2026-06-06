# AIDEOM-VN Dashboard

Đây là dashboard Streamlit trình bày kết quả tính toán cho bộ bài tập cuối kì môn Các mô hình ra quyết định.

## 1. Mục tiêu dự án

Dự án xây dựng nguyên mẫu AIDEOM-VN nhằm tổng hợp kết quả của 12 bài thực hành, bao gồm các nhóm mô hình:

- Hàm sản xuất Cobb-Douglas mở rộng
- Quy hoạch tuyến tính LP
- Quy hoạch nguyên hỗn hợp MIP
- TOPSIS
- Tối ưu đa mục tiêu Pareto NSGA-II
- Tối ưu động
- Mô phỏng lao động dưới tác động AI
- Quy hoạch ngẫu nhiên
- Q-learning
- Dashboard tích hợp kịch bản chính sách

## 2. Cấu trúc thư mục

```text
aideom-vn-dashboard/
├── aideom_vn_streamlit/
│   ├── app.py
│   ├── requirements.txt
│   └── data/
│       ├── ket_qua_bai_1_den_6.xlsx
│       ├── ket_qua_bai_7_den_12.xlsx
│       └── ket_qua_bo_sung_bai_2_5.xlsx
├── src/
│   ├── m1_forecast.py
│   ├── m2_readiness.py
│   ├── m3_allocation.py
│   ├── m4_labor.py
│   ├── m5_risk.py
│   └── scenario_runner.py
├── tests/
│   └── test_basic.py
├── devcontainer.json
└── README.md
