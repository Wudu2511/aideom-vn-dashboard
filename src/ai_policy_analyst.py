import pandas as pd
import streamlit as st


def _fmt_number(x):
    try:
        if abs(x) >= 1000:
            return f"{x:,.2f}"
        return f"{x:.4f}"
    except Exception:
        return str(x)


def _find_label_col(df: pd.DataFrame):
    preferred_cols = [
        "sector_name_vi", "region_name_vi", "region_name",
        "scenario", "name", "project", "item", "policy",
        "factor", "metric", "year", "sector", "region"
    ]

    for col in preferred_cols:
        if col in df.columns:
            return col

    object_cols = df.select_dtypes(include=["object"]).columns.tolist()
    if object_cols:
        return object_cols[0]

    return None


def _important_numeric_cols(df: pd.DataFrame):
    keywords = [
        "GDP", "TFP", "Priority", "TOPSIS", "score", "Z", "benefit",
        "cost", "welfare", "NetJob", "Displaced", "Emission",
        "Risk", "AI", "H", "D", "value", "reward"
    ]

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    selected = []
    for col in numeric_cols:
        col_lower = str(col).lower()
        if any(k.lower() in col_lower for k in keywords):
            selected.append(col)

    if not selected:
        selected = numeric_cols[:3]

    return selected[:4]


def _summarize_table(table_name: str, df: pd.DataFrame):
    if df is None or df.empty:
        return f"- Bảng **{table_name}** không có dữ liệu để phân tích."

    label_col = _find_label_col(df)
    numeric_cols = _important_numeric_cols(df)

    lines = []
    lines.append(f"- Bảng **{table_name}** có **{len(df)} dòng** và **{len(df.columns)} cột**.")

    for col in numeric_cols:
        try:
            clean_df = df[[col] + ([label_col] if label_col else [])].dropna()
            if clean_df.empty:
                continue

            max_idx = clean_df[col].idxmax()
            min_idx = clean_df[col].idxmin()

            max_label = clean_df.loc[max_idx, label_col] if label_col else f"dòng {max_idx}"
            min_label = clean_df.loc[min_idx, label_col] if label_col else f"dòng {min_idx}"

            max_val = clean_df.loc[max_idx, col]
            min_val = clean_df.loc[min_idx, col]

            lines.append(
                f"  - Chỉ tiêu **{col}** cao nhất ở **{max_label}** "
                f"({_fmt_number(max_val)}), thấp nhất ở **{min_label}** "
                f"({_fmt_number(min_val)})."
            )
        except Exception:
            continue

    return "\n".join(lines)


def _policy_recommendation(exercise_id: str):
    recommendations = {
        "bai1": """
**Khuyến nghị chính sách:** Kết quả Bài 1 nên được dùng để đánh giá vai trò của TFP, số hóa, AI và nhân lực số trong tăng trưởng. Cần thận trọng vì hệ số Cobb-Douglas là giả định, không phải bằng chứng nhân quả tuyệt đối.
""",
        "bai2": """
**Khuyến nghị chính sách:** Kết quả phân bổ ngân sách cần được hiểu như một gợi ý định lượng. Nếu mô hình dồn vốn quá nhiều vào một hạng mục, cần kiểm tra thêm khả năng hấp thụ, năng lực triển khai và rủi ro giải ngân.
""",
        "bai3": """
**Khuyến nghị chính sách:** Chỉ số ưu tiên ngành phụ thuộc mạnh vào bộ trọng số. Vì vậy, trọng số không nên chỉ do kỹ thuật viên quyết định mà cần có tham vấn chuyên gia, nhà quản lý và các bên liên quan.
""",
        "bai4": """
**Khuyến nghị chính sách:** Nếu bỏ ràng buộc công bằng, vốn thường chảy về vùng có hiệu quả biên cao. Do đó, cần cân bằng giữa tối đa hóa tăng trưởng và thu hẹp khoảng cách số vùng miền.
""",
        "bai5": """
**Khuyến nghị chính sách:** Danh mục dự án tối ưu không chỉ nên xét NPV, mà còn phải xét dự án nền tảng như dữ liệu mở, an ninh mạng và đào tạo nhân lực, vì các dự án này tạo điều kiện cho hệ sinh thái số.
""",
        "bai6": """
**Khuyến nghị chính sách:** TOPSIS giúp xếp hạng vùng theo mức độ sẵn sàng AI, nhưng quyết định đặt trung tâm AI cần bổ sung tiêu chí địa chính trị, an ninh dữ liệu, năng lượng và cân bằng vùng.
""",
        "bai7": """
**Khuyến nghị chính sách:** Tập nghiệm Pareto cho thấy không có phương án tối ưu tuyệt đối. Nhà hoạch định chính sách phải lựa chọn mức đánh đổi giữa tăng trưởng, bao trùm, môi trường và an ninh dữ liệu.
""",
        "bai8": """
**Khuyến nghị chính sách:** Tối ưu động cho thấy đầu tư sớm vào số hóa, AI và nhân lực có thể tạo lợi ích dài hạn. Tuy nhiên, cần tránh kết luận máy móc nếu mô hình chưa đủ ràng buộc thực tế.
""",
        "bai9": """
**Khuyến nghị chính sách:** Mô hình lao động cần được đọc cùng với yếu tố an sinh xã hội. Không nên chỉ tối đa hóa NetJob tổng, mà cần bảo vệ các nhóm lao động dễ bị tổn thương.
""",
        "bai10": """
**Khuyến nghị chính sách:** Quy hoạch ngẫu nhiên giúp chính sách chuẩn bị tốt hơn trước bất định. Nếu VSS hoặc EVPI thấp, cần xem lại cấu trúc kịch bản, xác suất và chi phí điều chỉnh.
""",
        "bai11": """
**Khuyến nghị chính sách:** Q-learning chỉ nên đóng vai trò khuyến nghị chính sách thích nghi. AI không thay thế trách nhiệm ra quyết định của con người và cơ quan quản lý.
""",
        "bai12": """
**Khuyến nghị chính sách:** Kịch bản tối ưu cân bằng thường phù hợp hơn kịch bản cực đoan, vì phát triển AI cần đồng thời có hạ tầng số, nhân lực số, an ninh dữ liệu và kiểm soát khoảng cách vùng.
"""
    }

    return recommendations.get(
        exercise_id,
        "**Khuyến nghị chính sách:** Kết quả mô hình nên được xem là công cụ hỗ trợ ra quyết định, không phải quyết định cuối cùng."
    )


def generate_policy_analysis(exercise_id: str, exercise_name: str, tables: dict):
    lines = []

    lines.append("### AI Policy Analyst")
    lines.append("")
    lines.append(
        "Tác nhân này tự đọc các bảng kết quả đầu ra, phát hiện điểm nổi bật và đưa ra nhận xét chính sách. "
        "Kết quả phân tích mang tính hỗ trợ, không thay thế quyết định của nhà quản lý."
    )

    lines.append("")
    lines.append("#### 1. Tóm tắt dữ liệu đầu vào")
    for table_name, df in tables.items():
        if isinstance(df, pd.DataFrame):
            lines.append(_summarize_table(table_name, df))

    lines.append("")
    lines.append("#### 2. Nhận xét chính")
    lines.append(
        f"Kết quả của **{exercise_name}** cho thấy mô hình đã tạo ra các chỉ báo định lượng có thể dùng để so sánh phương án, "
        "nhận diện phương án nổi bật và phát hiện các đánh đổi chính sách."
    )

    lines.append("")
    lines.append("#### 3. Cảnh báo khi diễn giải")
    lines.append(
        "Các kết quả phụ thuộc vào giả định mô hình, trọng số, ràng buộc và chất lượng dữ liệu đầu vào. "
        "Vì vậy, cần tránh diễn giải kết quả như một kết luận tuyệt đối."
    )

    lines.append("")
    lines.append("#### 4. Khuyến nghị")
    lines.append(_policy_recommendation(exercise_id))

    return "\n".join(lines)


def render_ai_policy_agent(exercise_id: str, exercise_name: str, tables: dict):
    st.markdown(
        """
        <div style="
            background: #F8FBFF;
            border: 1px solid #D7E7FF;
            border-left: 6px solid #2F80ED;
            border-radius: 14px;
            padding: 16px 18px;
            margin: 14px 0 18px 0;
        ">
            <h3 style="margin-top:0; color:#102542;">🤖 AI Policy Analyst</h3>
            <p style="margin-bottom:0; color:#334155;">
                Tác nhân phân tích kết quả mô hình và gợi ý diễn giải chính sách.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Chạy tác nhân phân tích", key=f"agent_{exercise_id}"):
        analysis = generate_policy_analysis(exercise_id, exercise_name, tables)
        st.markdown(analysis)

    with st.expander("Dữ liệu mà tác nhân sử dụng"):
        for name, df in tables.items():
            if isinstance(df, pd.DataFrame):
                st.write(f"**{name}**")
                st.dataframe(df.head(10), use_container_width=True)
