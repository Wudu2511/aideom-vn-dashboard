import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="AIDEOM-VN Dashboard",
    page_icon="😇",
    layout="wide"
)
st.markdown(
    """
    <style>
    html, body, [class*="css"], [class*="st-"], .stMarkdown, .stText, .stDataFrame {
        font-family: "Times New Roman", Times, serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: "Times New Roman", Times, serif !important;
        font-weight: 700;
    }

    p, div, span, label, button {
        font-family: "Times New Roman", Times, serif !important;
    }

    .stMarkdown p {
        font-size: 18px;
        line-height: 1.7;
        text-align: justify;
    }

    .stMarkdown li {
        font-size: 18px;
        line-height: 1.7;
    }

    .stDataFrame {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

MAIN_FILE = DATA_DIR / "ket_qua_bai_1_den_6.xlsx"
SUPP_FILE = DATA_DIR / "ket_qua_bo_sung_bai_2_5.xlsx"
ADV_FILE = DATA_DIR / "ket_qua_bai_7_den_12.xlsx"

@st.cache_data
def load_excel(file_path):
    return pd.read_excel(file_path, sheet_name=None)


main = load_excel(MAIN_FILE)
supp = load_excel(SUPP_FILE)
adv = load_excel(ADV_FILE)


st.sidebar.title("AIDEOM-VN")
st.sidebar.caption("Dashboard kết quả Bài 1-12")

page = st.sidebar.radio(
    "Chọn nội dung",
    [
        "Tổng quan",
        "Bài 1 - Cobb-Douglas",
        "Bài 2 - LP ngân sách",
        "Bài 3 - Ưu tiên ngành",
        "Bài 4 - Phân bổ vùng",
        "Bài 5 - Lựa chọn dự án",
        "Bài 6 - TOPSIS vùng",
        "Bài 7 - Pareto NSGA-II",
        "Bài 8 - Tối ưu động",
        "Bài 9 - Lao động và AI",
        "Bài 10 - Stochastic LP",
        "Bài 11 - Q-learning",
        "Bài 12 - Tổng hợp kịch bản"
    ]
)


def section_title(title, subtitle=None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()


if page == "Tổng quan":
    section_title(
        "AIDEOM-VN Dashboard",
        "Dashboard tổng hợp kết quả mô hình ra quyết định phát triển kinh tế Việt Nam trong kỷ nguyên AI"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Số bài đã hoàn thiện", "6/12")

    with col2:
        st.metric("Nhóm mô hình", "LP, MIP, TOPSIS, Cobb-Douglas")

    with col3:
        st.metric("Dữ liệu", "Việt Nam 2020-2025")

    st.subheader("Cấu trúc dashboard")
    st.write("""
    Dashboard này trình bày kết quả chạy mô hình từ Bài 1 đến Bài 6, gồm:
    - kết quả định lượng,
    - bảng và biểu đồ,
    - diễn giải chính sách,
    - liên hệ thực tiễn Việt Nam hiện nay.
    """)


elif page == "Bài 1 - Cobb-Douglas":
    section_title(
        "Bài 1. Hàm sản xuất Cobb-Douglas mở rộng",
        "Phân tích TFP, dự báo GDP và đóng góp tăng trưởng"
    )

    df = main["Bai1_TFP"]
    decomp = main["Bai1_Growth_Decomp"]
    forecast = main["Bai1_Forecast2030"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "Kết quả TFP",
        "Phân rã tăng trưởng",
        "Dự báo 2030",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.subheader("TFP và GDP dự báo")
        st.dataframe(df, use_container_width=True)

        fig = px.line(
            df,
            x="year",
            y="TFP_A",
            markers=True,
            title="Xu hướng TFP A_t giai đoạn 2020-2025"
        )
        st.plotly_chart(fig, use_container_width=True)

        compare = df[["year", "GDP_trillion_VND", "Y_hat"]].melt(
            id_vars="year",
            var_name="Chỉ tiêu",
            value_name="GDP"
        )
        fig2 = px.line(
            compare,
            x="year",
            y="GDP",
            color="Chỉ tiêu",
            markers=True,
            title="So sánh GDP thực tế và GDP dự báo"
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("Phân rã tăng trưởng")
        st.dataframe(decomp, use_container_width=True)

        fig = px.bar(
            decomp,
            x="factor",
            y="share_of_growth_pct",
            text="share_of_growth_pct",
            title="Tỷ trọng đóng góp vào tăng trưởng GDP bình quân"
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Dự báo GDP 2030")
        st.dataframe(forecast, use_container_width=True)

    with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown("""
### a) TFP của Việt Nam có xu hướng tăng hay giảm trong giai đoạn 2020-2025? Điều đó nói lên gì về chất lượng tăng trưởng?

Dựa trên output mô hình, TFP A_t tăng liên tục từ **27,75 năm 2020** lên **34,91 năm 2025**. Điều này cho thấy phần tăng trưởng không được giải thích trực tiếp bởi vốn vật chất K, lao động L, số hóa D, năng lực AI và nhân lực số H có xu hướng tăng. Nói cách khác, chất lượng tăng trưởng trong mô hình có cải thiện, vì GDP không chỉ tăng nhờ mở rộng đầu vào mà còn nhờ hiệu quả tổng hợp cao hơn.

Dẫn chứng rõ hơn là trong bảng phân rã tăng trưởng, TFP đóng góp **49,08%** vào tăng trưởng bình quân, cao hơn cả vốn vật chất K với **31,78%**. Điều này phù hợp với bối cảnh Việt Nam đang chuyển từ mô hình tăng trưởng dựa nhiều vào vốn và lao động sang mô hình dựa nhiều hơn vào năng suất, khoa học công nghệ, đổi mới sáng tạo và chuyển đổi số. Năm 2024, NSO/GSO công bố GDP Việt Nam tăng 7,09%, trong đó công nghiệp - xây dựng và dịch vụ đóng góp lớn vào tăng trưởng, phản ánh xu hướng phục hồi và nâng cao năng lực sản xuất của nền kinh tế.

Tuy nhiên, cần lưu ý rằng TFP ở đây được tính ngược từ hàm sản xuất với hệ số giả định. Vì vậy, kết quả này nên được hiểu là chỉ báo định lượng hỗ trợ phân tích, không phải bằng chứng nhân quả tuyệt đối.

### b) Trong các yếu tố mới D, AI, H, yếu tố nào đóng góp nhiều nhất cho tăng trưởng giai đoạn vừa qua? Vì sao?
Trong ba yếu tố mới, **D - mức độ số hóa** đóng góp lớn nhất, đạt **10,37%** tăng trưởng bình quân. Tiếp theo là **AI với 6,24%**, và **H - nhân lực số với 2,87%**.

Kết quả này hợp lý vì trong giai đoạn 2020-2025, tỷ trọng kinh tế số/GDP trong dữ liệu tăng từ **12,0% năm 2020** lên **19,5% năm 2025**. Mức tăng của D rõ ràng hơn so với H, trong khi AI vẫn đang ở giai đoạn tích lũy nền tảng. Điều này phù hợp với định hướng của Quyết định 749/QĐ-TTg về Chương trình Chuyển đổi số quốc gia và Quyết định 411/QĐ-TTg về phát triển kinh tế số, xã hội số đến năm 2025, định hướng 2030.

Hàm ý chính sách là Việt Nam không nên chỉ đầu tư vào công nghệ AI riêng lẻ, mà cần đầu tư đồng bộ vào số hóa nền kinh tế, dữ liệu, hạ tầng số và nhân lực số. Nếu nhân lực số tăng chậm, AI sẽ khó phát huy đầy đủ tác động năng suất.

### c) Mục tiêu Việt Nam đạt 30% kinh tế số/GDP vào 2030 có khả thi không nếu dựa trên mô hình này? Cần ràng buộc gì?

Output mô phỏng cho thấy nếu đến năm 2030, D đạt **30%**, AI đạt **100 nghìn doanh nghiệp số**, H đạt **35%**, K tăng **6%/năm** và TFP tăng **1,2%/năm**, GDP dự báo năm 2030 đạt khoảng **16.362,93 nghìn tỷ VND**. So với mức GDP năm 2025 là **12.847,6 nghìn tỷ VND**, đây là kịch bản tăng trưởng tích cực.

Vì vậy, mục tiêu kinh tế số đạt 30% GDP vào năm 2030 có thể xem là khả thi về mặt mô hình. Tuy nhiên, để mục tiêu này không chỉ là con số kỹ thuật, cần các ràng buộc chính sách: đầu tư hạ tầng số, mở rộng dữ liệu mở, bảo đảm an ninh mạng, đào tạo nhân lực số, hỗ trợ doanh nghiệp nhỏ và vừa chuyển đổi số, đồng thời thu hẹp khoảng cách số giữa các vùng. Nghị quyết 57-NQ/TW cũng nhấn mạnh khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số là yếu tố quyết định phát triển, đồng thời chỉ ra các hạn chế hiện nay như hạ tầng số chưa đồng bộ, nhân lực chất lượng cao còn thiếu và an toàn dữ liệu còn nhiều thách thức.
""")


elif page == "Bài 2 - LP ngân sách":
    section_title(
        "Bài 2. Phân bổ ngân sách số bằng quy hoạch tuyến tính",
        "Tối ưu hóa 4 hạng mục: hạ tầng số, AI, nhân lực số và R&D"
    )

    base = main["Bai2_Base"]
    duals = main["Bai2_Duals"]
    sens = main["Bai2_Sensitivity"]
    h30 = supp["Bai2_H30"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "Nghiệm tối ưu",
        "Shadow price",
        "Độ nhạy ngân sách",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.subheader("Kết quả nghiệm tối ưu")
        st.dataframe(base, use_container_width=True)

        alloc_cols = ["x_I", "x_AI", "x_H", "x_RD"]
        alloc = base[alloc_cols].T.reset_index()
        alloc.columns = ["Hạng mục", "Ngân sách"]

        fig = px.bar(
            alloc,
            x="Hạng mục",
            y="Ngân sách",
            text="Ngân sách",
            title="Phân bổ ngân sách tối ưu"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Trường hợp ưu tiên nhân lực số x_H ≥ 30")
        st.dataframe(h30, use_container_width=True)

    with tab2:
        st.subheader("Giá đối ngẫu / Shadow price")
        st.dataframe(duals, use_container_width=True)

    with tab3:
        st.subheader("Phân tích độ nhạy theo ngân sách")
        st.dataframe(sens, use_container_width=True)

        fig = px.line(
            sens,
            x="B",
            y="Z",
            markers=True,
            title="Đường cong giá trị tối ưu Z*(B)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown("""
### a) Khi ngân sách tổng tăng thêm 1 nghìn tỷ VND, GDP kỳ vọng tăng thêm bao nhiêu? Đây có phải là cận trên hợp lý của chi phí cơ hội vốn công?

Output mô hình cho thấy nghiệm tối ưu ban đầu là: hạ tầng số **25**, AI và dữ liệu **15**, nhân lực số **20**, R&D **40** nghìn tỷ VND. Giá trị mục tiêu đạt **Z* = 112,25**.

Dẫn chứng quan trọng là shadow price của ràng buộc ngân sách tổng bằng **1,35**. Nghĩa là trong vùng nghiệm tối ưu hiện tại, nếu tăng thêm **1 nghìn tỷ VND** ngân sách, GDP kỳ vọng tăng thêm khoảng **1,35 nghìn tỷ VND**. Phân tích độ nhạy xác nhận điều này: ngân sách tăng từ **100** lên **120** làm **Z*** tăng từ **112,25** lên **139,25**; ngân sách tăng lên **140** làm **Z*** tăng lên **166,25**. Mỗi 20 nghìn tỷ tăng thêm tạo thêm 27 nghìn tỷ GDP kỳ vọng, tương ứng hệ số **1,35**.

Tuy nhiên, trong thực tiễn Việt Nam, đây chỉ là cận trên kỹ thuật của mô hình. Hiệu quả vốn công còn phụ thuộc vào năng lực giải ngân, chất lượng dự án, năng lực hấp thụ của địa phương và khả năng phối hợp giữa các cơ quan. Vì vậy, shadow price có giá trị tham khảo cho phân tích chi phí cơ hội, nhưng không nên hiểu là cứ tăng ngân sách thì GDP thực tế chắc chắn tăng tương ứng.

### b) Vì sao R&D có hệ số tác động cao nhất nhưng lại có ràng buộc tối thiểu thấp nhất?

Trong nghiệm tối ưu, R&D nhận **40 nghìn tỷ VND**, cao hơn nhiều so với mức tối thiểu **10 nghìn tỷ VND**. Nguyên nhân là R&D có hệ số tác động cao nhất, **1,35**, nên sau khi các ràng buộc tối thiểu của hạ tầng, AI và nhân lực số được đáp ứng, mô hình dồn phần ngân sách còn lại vào R&D để tối đa hóa GDP kỳ vọng.

Việc đặt sàn R&D thấp vẫn hợp lý vì R&D có độ trễ dài, rủi ro cao và phụ thuộc mạnh vào năng lực hấp thụ công nghệ của doanh nghiệp, viện nghiên cứu, trường đại học và thị trường. Trong bối cảnh Nghị quyết 57-NQ/TW nhấn mạnh đột phá khoa học công nghệ, đổi mới sáng tạo và chuyển đổi số, R&D cần được ưu tiên nhưng phải đi kèm cơ chế thương mại hóa kết quả nghiên cứu và liên kết doanh nghiệp.

### c) Giả sử Chính phủ muốn ưu tiên nhân lực số với x_H ≥ 30. Bài toán có còn khả thi không? Z* thay đổi như thế nào?

Khi tăng ràng buộc nhân lực số từ **x_H ≥ 20** lên **x_H ≥ 30**, output bổ sung cho thấy bài toán **vẫn khả thi**. Nghiệm mới là: hạ tầng số **25**, AI và dữ liệu **15**, nhân lực số **30**, R&D **30**. Giá trị mục tiêu giảm từ **112,25** xuống **108,25**, tức giảm **4,00 nghìn tỷ GDP kỳ vọng**.

Kết quả này cho thấy ưu tiên nhân lực số có chi phí cơ hội ngắn hạn, vì mô hình phải chuyển **10 nghìn tỷ** từ R&D, nơi có hệ số tác động **1,35**, sang nhân lực số, nơi có hệ số tác động **0,95**. Tuy nhiên, về dài hạn, ưu tiên nhân lực số là hợp lý vì đây là điều kiện để hấp thụ AI, vận hành hạ tầng số và triển khai R&D. Điều này phù hợp với tinh thần của Quyết định 749/QĐ-TTg và Quyết định 411/QĐ-TTg, vì chuyển đổi số không chỉ là đầu tư công nghệ mà còn là phát triển năng lực con người, doanh nghiệp và xã hội số.

### d) Tỷ lệ 35% công nghệ chiến lược AI + R&D có khả thi không?

Trong nghiệm tối ưu ban đầu, AI nhận **15** và R&D nhận **40**, tổng cộng **55 nghìn tỷ VND**, chiếm **55% tổng ngân sách**. Như vậy, ràng buộc tối thiểu **35%** cho AI + R&D không phải ràng buộc chặt, vì mô hình tự chọn mức cao hơn 35%.

Tuy nhiên, trong thực tế, ngân sách Việt Nam còn phải cân đối với hạ tầng giao thông, y tế, giáo dục, an sinh xã hội, quốc phòng, phòng chống thiên tai và chuyển đổi xanh. Vì vậy, tỷ lệ 35% cho AI + R&D nên được hiểu là định hướng chiến lược, không phải tỷ lệ cứng áp dụng máy móc.
""")

elif page == "Bài 3 - Ưu tiên ngành":
    section_title(
        "Bài 3. Chỉ số ưu tiên ngành",
        "Xếp hạng 10 ngành theo Priority Index"
    )

    ranking = main["Bai3_Ranking"]
    sens = main["Bai3_AI_Sensitivity"]
    policy = main["Bai3_Policy_Weights"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "Xếp hạng ngành",
        "Độ nhạy AI",
        "So sánh trọng số",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.dataframe(ranking, use_container_width=True)

        fig = px.bar(
            ranking,
            x="sector_name_vi",
            y="Priority",
            text="Priority",
            title="Xếp hạng chỉ số ưu tiên ngành"
        )
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.dataframe(sens, use_container_width=True)

    with tab3:
        st.dataframe(policy, use_container_width=True)

    with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown("""
### a) Theo kết quả, ba ngành nào nên ưu tiên chuyển đổi số và AI trước? Kết quả có phù hợp với định hướng hiện nay không?

Output xếp hạng Priority cho thấy ba ngành đứng đầu là: **Thông tin - Truyền thông - CNTT** với điểm **0,730**, **Công nghiệp chế biến chế tạo** với điểm **0,652**, và **Tài chính - Ngân hàng - Bảo hiểm** với điểm **0,533**.

Kết quả này hợp lý vì CNTT là ngành nền tảng cho chuyển đổi số; công nghiệp chế biến chế tạo có quy mô xuất khẩu, việc làm và chuỗi cung ứng lớn; còn tài chính - ngân hàng có dữ liệu lớn, khả năng tự động hóa cao và nhiều ứng dụng AI trong phân tích rủi ro, tín dụng, thanh toán và chống gian lận.

Kết quả cũng phù hợp với định hướng của Quyết định 127/QĐ-TTg về Chiến lược AI đến năm 2030 và Nghị quyết 57-NQ/TW về phát triển khoa học công nghệ, đổi mới sáng tạo và chuyển đổi số quốc gia.

### b) Tại sao ngành Khai khoáng có năng suất cao nhưng không nằm trong nhóm ưu tiên?

Output cho thấy **Khai khoáng xếp cuối**, với Priority chỉ **0,178**. Điều này chứng minh rằng năng suất cao không đủ để trở thành ngành ưu tiên nếu các tiêu chí khác yếu.

Khai khoáng có quy mô việc làm nhỏ, lan tỏa hạn chế, rủi ro tự động hóa cao và không phải ngành dẫn dắt chuyển đổi số toàn nền kinh tế. Trong khi đó, các ngành như CNTT, chế biến chế tạo và tài chính có khả năng lan tỏa công nghệ rộng hơn. Vì vậy, về chính sách, khai khoáng có thể cần số hóa để nâng cao an toàn, giám sát tài nguyên và giảm tác động môi trường, nhưng không nên là ngành ưu tiên hàng đầu nếu mục tiêu là lan tỏa AI và chuyển đổi số trên diện rộng.

### c) Bộ trọng số nên do ai quyết định?

Output độ nhạy cho thấy khi trọng số AI Readiness thay đổi từ **0,05** đến **0,40**, Top 3 ngành vẫn ổn định: **CNTT, chế biến chế tạo và tài chính - ngân hàng**. Tuy nhiên, khi đổi từ bộ trọng số “tăng trưởng” sang “bao trùm”, thứ hạng thay đổi mạnh: **Nông - Lâm - Thủy sản** từ hạng **10** trong định hướng tăng trưởng lên hạng **3** trong định hướng bao trùm.

Điều này chứng minh trọng số không chỉ là vấn đề kỹ thuật mà còn phản ánh lựa chọn giá trị chính sách. Nếu ưu tiên tăng trưởng, ngành công nghệ và công nghiệp sẽ dẫn đầu. Nếu ưu tiên bao trùm, ngành có nhiều lao động như nông nghiệp sẽ quan trọng hơn.

Vì vậy, bộ trọng số nên được quyết định thông qua kết hợp giữa chuyên gia kỹ thuật, hội đồng chính sách, doanh nghiệp, địa phương và đối thoại công khai. Cách này giúp bảo đảm tính minh bạch và tính chính danh của chính sách.
""")


elif page == "Bài 4 - Phân bổ vùng":
    section_title(
        "Bài 4. Phân bổ ngân sách số theo vùng",
        "So sánh mô hình có và không có ràng buộc công bằng"
    )

    fair = main["Bai4_With_Fairness"]
    nofair = main["Bai4_No_Fairness"]

    tab1, tab2, tab3 = st.tabs([
        "Có công bằng",
        "Không công bằng",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.dataframe(fair, use_container_width=True)
        fig = px.imshow(
            fair.set_index("region_name")[["I", "D", "AI", "H"]],
            text_auto=True,
            aspect="auto",
            title="Phân bổ ngân sách có ràng buộc công bằng"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.dataframe(nofair, use_container_width=True)
        fig = px.imshow(
            nofair.set_index("region_name")[["I", "D", "AI", "H"]],
            text_auto=True,
            aspect="auto",
            title="Phân bổ ngân sách không có ràng buộc công bằng"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Thảo luận chính sách")
        st.markdown("""
### a) Nếu bỏ ràng buộc công bằng, vốn sẽ chảy về vùng nào? Vì sao? Hậu quả xã hội dài hạn ra sao?

Output không có ràng buộc công bằng cho thấy vốn tập trung mạnh vào các vùng có hệ số tác động cao. Cụ thể, **Đồng bằng sông Hồng** nhận **12.000 tỷ cho AI**, **Đông Nam Bộ** nhận **12.000 tỷ cho AI**, còn các vùng khác chủ yếu nhận mức sàn hoặc tập trung vào nhân lực số.

Điều này xảy ra vì Đồng bằng sông Hồng và Đông Nam Bộ có nền tảng kinh tế, hạ tầng số, FDI, doanh nghiệp và nhân lực tốt hơn. Về hiệu quả ngắn hạn, vốn chảy vào vùng mạnh giúp tối đa hóa GDP gain. Tuy nhiên, về dài hạn, điều này có thể làm gia tăng khoảng cách số giữa vùng phát triển và vùng yếu.

Đây chính là lý do Quyết định 411/QĐ-TTg không chỉ nói về kinh tế số mà còn nhấn mạnh xã hội số, tức là chuyển đổi số cần bao trùm người dân, doanh nghiệp và địa phương, không chỉ tập trung ở các trung tâm phát triển.

### b) Ràng buộc công bằng vùng làm giảm Z* bao nhiêu? Mức giảm này có chấp nhận được không?

Khi có ràng buộc công bằng, **Z*** đạt khoảng **52.485**. Khi bỏ ràng buộc công bằng, **Z*** đạt khoảng **68.750**. Như vậy, chi phí kinh tế của công bằng vùng là **16.265**, tương đương giảm khoảng **23,66%**.

Nếu chỉ xét hiệu quả GDP ngắn hạn, mức giảm này khá lớn. Tuy nhiên, nếu xét mục tiêu phát triển bao trùm, mức giảm có thể chấp nhận được. Chính sách công không chỉ tối đa hóa tăng trưởng, mà còn phải tránh tình trạng vùng yếu bị bỏ lại phía sau. Nghị quyết 57-NQ/TW cũng chỉ ra rằng hạ tầng số còn hạn chế và chuyển đổi số chưa đồng đều là những vấn đề cần khắc phục.

### c) Tây Nguyên nên đầu tư AI hay tập trung H và I trước?

Output có ràng buộc công bằng cho thấy **Tây Nguyên nhận 12.000 tỷ cho D - chuyển đổi số**, không nhận vốn AI. Output không có ràng buộc công bằng cũng cho thấy Tây Nguyên nhận **11.000 tỷ cho H - nhân lực số**, không nhận AI.

Kết quả này cho thấy mô hình không khuyến nghị đầu tư AI trực tiếp vào Tây Nguyên ở giai đoạn đầu. Thay vào đó, vùng này nên ưu tiên chuyển đổi số doanh nghiệp, hạ tầng số và nhân lực số. Đây là cách tiếp cận hợp lý vì AI chỉ phát huy hiệu quả khi đã có dữ liệu, kỹ năng số, kết nối số và năng lực vận hành.
""")


elif page == "Bài 5 - Lựa chọn dự án":
    section_title(
        "Bài 5. MIP lựa chọn dự án chuyển đổi số",
        "Tối ưu danh mục dự án trong điều kiện ràng buộc ngân sách và chính sách"
    )

    base = main["Bai5_Selected_80k"]
    budget100 = main["Bai5_Selected_100k"]
    risk = main["Bai5_Risk_Adjusted"]
    force = supp["Bai5_Force_P1_P2"]
    no_p14 = supp["Bai5_No_P14_Required"]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Ngân sách 80k",
        "Ngân sách 100k",
        "Bắt buộc P1 & P2",
        "Rủi ro dự án",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.dataframe(base, use_container_width=True)

        fig = px.bar(
            base,
            x="name",
            y=["cost", "benefit"],
            barmode="group",
            title="Chi phí và lợi ích các dự án được chọn"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.dataframe(budget100, use_container_width=True)

    with tab3:
        st.dataframe(force, use_container_width=True)

    with tab4:
        st.dataframe(risk, use_container_width=True)

    with tab5:
        st.subheader("Thảo luận chính sách")
        st.markdown("""
### a) Vì sao mô hình chọn P15 Open Data dù quy mô nhỏ? Đây có phải kết quả mong muốn về chính sách?

Trong nghiệm cơ sở ngân sách **80.000 tỷ**, mô hình chọn **9 dự án**, tổng chi phí **59.700 tỷ** và tổng lợi ích NPV **115.400 tỷ**. **P15 Open Data** được chọn dù chi phí chỉ **1.500 tỷ** và lợi ích **3.800 tỷ**.

Điều này hợp lý vì P15 có tỷ suất lợi ích/chi phí cao, chi phí thấp và không làm căng ràng buộc ngân sách năm 1-2. Về chính sách, đây là kết quả mong muốn vì dữ liệu mở là nền tảng cho chính phủ số, AI, đổi mới sáng tạo và minh bạch hóa quản trị. Nếu thiếu dữ liệu mở, các dự án AI lớn như trung tâm AI quốc gia có thể thiếu dữ liệu đầu vào để huấn luyện, đánh giá và triển khai.

### b) Ràng buộc bắt buộc P14 an ninh mạng có làm giảm Z* không? Việc bắt buộc này có hợp lý không?

Output bổ sung cho thấy khi giữ ràng buộc bắt buộc P14, tổng lợi ích NPV của danh mục cơ sở là **115.400 tỷ**. Khi bỏ ràng buộc bắt buộc P14, tổng lợi ích tăng lên **116.300 tỷ**. Như vậy, bắt buộc P14 làm giảm khoảng **900 tỷ VND** lợi ích NPV.

Tuy nhiên, mức giảm này tương đối nhỏ so với tổng lợi ích của danh mục. Về chính sách, bắt buộc P14 vẫn hợp lý vì an ninh mạng là điều kiện nền tảng của chuyển đổi số. Khi Việt Nam triển khai định danh điện tử, dịch vụ công trực tuyến, dữ liệu mở, trung tâm dữ liệu và AI, rủi ro an toàn dữ liệu tăng lên. Nghị quyết 57-NQ/TW cũng nhấn mạnh an ninh, an toàn thông tin và bảo vệ dữ liệu còn nhiều thách thức.

### c) Giả sử Quốc hội yêu cầu phải có cả P1 và P2, bài toán còn khả thi không? Z* thay đổi ra sao?

Output bổ sung cho thấy khi bắt buộc chọn cả **P1 Trung tâm dữ liệu quốc gia Hòa Lạc** và **P2 Trung tâm dữ liệu quốc gia phía Nam**, bài toán vẫn **khả thi**. Danh mục chọn 8 dự án: **P1, P2, P4, P8, P9, P12, P14 và P15**. Tổng chi phí là **59.300 tỷ**, tổng lợi ích NPV là **113.300 tỷ**.

So với nghiệm cơ sở có lợi ích **115.400 tỷ**, phương án bắt buộc P1 và P2 làm giảm **2.100 tỷ** NPV. Đây là chi phí cơ hội của yêu cầu dự phòng hạ tầng dữ liệu. Tuy nhiên, việc có hai trung tâm dữ liệu có thể hợp lý nếu mục tiêu không chỉ là tối đa hóa NPV mà còn là bảo đảm dự phòng, an toàn hệ thống, khả năng phục hồi và chủ quyền dữ liệu.

### d) Khi nới ngân sách lên 100.000 tỷ, tập dự án có thay đổi không?

Output cho thấy khi tăng ngân sách từ **80.000** lên **100.000 tỷ**, danh mục dự án **không thay đổi**. Điều này chứng tỏ ngân sách tổng không phải ràng buộc duy nhất. Các ràng buộc khác như ngân sách năm 1-2, loại trừ P1/P2, yêu cầu tiên quyết đào tạo nhân lực, yêu cầu an ninh mạng và giới hạn số lượng dự án mới là các yếu tố giới hạn danh mục.

Hàm ý chính sách là tăng tiền chưa chắc làm tăng hiệu quả nếu năng lực triển khai, nhân lực, quản trị dự án và phối hợp thể chế chưa được cải thiện.

### e) Khi xét rủi ro hoàn thành, danh mục thay đổi thế nào?

Khi tối đa hóa lợi ích kỳ vọng có xét xác suất hoàn thành, danh mục chuyển sang chọn **P2, P3, P5, P6, P7, P12, P14 và P15**. Tổng chi phí là **58.800 tỷ**, tổng lợi ích gốc là **111.200 tỷ**, nhưng lợi ích kỳ vọng chỉ còn **91.285 tỷ**.

Điều này cho thấy khi xét rủi ro, các dự án công nghệ lớn có lợi ích danh nghĩa cao nhưng xác suất hoàn thành thấp sẽ kém hấp dẫn hơn. Đây là điểm quan trọng khi triển khai Chiến lược AI theo Quyết định 127/QĐ-TTg: muốn các dự án AI lớn thành công, Việt Nam cần đồng thời đầu tư vào dữ liệu, nhân lực, hạ tầng tính toán, an ninh mạng và cơ chế thử nghiệm chính sách.
""")


elif page == "Bài 6 - TOPSIS vùng":
    section_title(
        "Bài 6. TOPSIS xếp hạng vùng ưu tiên AI",
        "So sánh trọng số chuyên gia, Entropy và độ nhạy AI Readiness"
    )

    topsis = main["Bai6_TOPSIS"]
    sens = main["Bai6_AI_Sensitivity"]

    tab1, tab2, tab3 = st.tabs([
        "Kết quả TOPSIS",
        "Độ nhạy AI",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.dataframe(topsis, use_container_width=True)

        plot_df = topsis[["region_name_vi", "TOPSIS_expert", "TOPSIS_entropy"]].melt(
            id_vars="region_name_vi",
            var_name="Phương pháp",
            value_name="Điểm TOPSIS"
        )

        fig = px.bar(
            plot_df,
            x="region_name_vi",
            y="Điểm TOPSIS",
            color="Phương pháp",
            barmode="group",
            title="So sánh TOPSIS chuyên gia và Entropy"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.dataframe(sens, use_container_width=True)

    with tab3:
        st.subheader("Thảo luận chính sách")
        st.markdown("""
### a) Vùng nào dẫn đầu theo TOPSIS với trọng số chuyên gia? Đây có phải vùng nên triển khai trung tâm AI đầu tiên không?

Output TOPSIS với trọng số chuyên gia cho thấy **Đông Nam Bộ** xếp hạng 1 với điểm **0,940**, **Đồng bằng sông Hồng** xếp hạng 2 với điểm **0,898**, và **Bắc Trung Bộ và duyên hải miền Trung** xếp hạng 3 với điểm **0,360**.

Đông Nam Bộ dẫn đầu vì có GRDP/người cao, FDI lớn, chỉ số số hóa cao, AI readiness cao và tỷ lệ lao động qua đào tạo tốt. Đồng bằng sông Hồng cũng có lợi thế lớn về nhân lực, trung tâm nghiên cứu, cơ quan quản lý và hạ tầng số.

Tuy nhiên, không nên hiểu rằng chỉ vùng xếp hạng 1 mới được triển khai trung tâm AI. Quyết định 127/QĐ-TTg đặt mục tiêu phát triển và ứng dụng AI đến năm 2030, nên chính sách hợp lý hơn là xây dựng mạng lưới trung tâm AI theo chức năng vùng: Đông Nam Bộ thiên về ứng dụng doanh nghiệp - công nghiệp - logistics; Đồng bằng sông Hồng thiên về nghiên cứu, chính sách và dữ liệu công.

### b) Khi dùng trọng số Entropy, vùng nào thay đổi xếp hạng lớn nhất? Vì sao?

Output cho thấy khi dùng trọng số Entropy, thứ hạng tổng thể **không thay đổi**: Đông Nam Bộ vẫn xếp thứ 1, Đồng bằng sông Hồng thứ 2, Bắc Trung Bộ và duyên hải miền Trung thứ 3, Đồng bằng sông Cửu Long thứ 4, Trung du miền núi phía Bắc thứ 5 và Tây Nguyên thứ 6.

Điều này cho thấy kết quả TOPSIS khá ổn định. Nguyên nhân là chênh lệch giữa các vùng về GRDP/người, FDI, chỉ số số hóa, AI readiness và lao động qua đào tạo khá lớn. Dù dùng trọng số chuyên gia hay trọng số khách quan, hai vùng phát triển nhất vẫn có ưu thế rõ rệt.

### c) TOPSIS giả định độc lập tuyến tính giữa các tiêu chí. Nếu AI Readiness và Internet penetration tương quan cao thì ảnh hưởng thế nào?

Nếu AI Readiness và Internet penetration tương quan cao, TOPSIS có thể “đếm trùng” lợi thế của các vùng phát triển. Ví dụ, Đông Nam Bộ và Đồng bằng sông Hồng vừa có Internet penetration cao, vừa có AI readiness cao, nên điểm số có thể được cộng hưởng từ hai tiêu chí phản ánh cùng một nền tảng số.

Điều này có thể làm vùng mạnh càng mạnh hơn trong kết quả xếp hạng, trong khi vùng yếu bị đánh giá thấp hơn. Để xử lý, có thể kiểm tra ma trận tương quan, gộp tiêu chí trùng lặp, dùng PCA hoặc bổ sung tiêu chí “khoảng cách số” để phản ánh nhu cầu hỗ trợ.

### d) Nếu Việt Nam xây dựng 3 trung tâm AI lớn, nên chọn 3 vùng nào? Có cần điều chỉnh thêm tiêu chí địa - chính trị không?

Dựa trên output TOPSIS và phân tích độ nhạy, Top 3 ổn định khi trọng số AI thay đổi từ **0,10** đến **0,40**: **Đông Nam Bộ**, **Đồng bằng sông Hồng**, và **Bắc Trung Bộ và duyên hải miền Trung**.

Nếu chỉ dựa vào mô hình, đây là ba vùng phù hợp nhất để ưu tiên trung tâm AI. Tuy nhiên, quyết định thực tế cần xét thêm địa - chính trị, an ninh dữ liệu, cân bằng vùng, hạ tầng năng lượng, rủi ro thiên tai, khả năng kết nối quốc tế và vai trò liên kết vùng. Vì vậy, TOPSIS nên được xem là công cụ hỗ trợ ra quyết định, không phải quyết định cuối cùng.
""")
elif page == "Bài 7 - Pareto NSGA-II":
    section_title(
        "Bài 7. Tối ưu đa mục tiêu Pareto với NSGA-II",
        "Phân tích đánh đổi giữa tăng trưởng, công bằng vùng, phát thải và rủi ro dữ liệu"
    )

    pareto = adv["Bai7_Pareto"]
    compromise = adv["Bai7_Compromise"]
    allocation = adv["Bai7_Allocation"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "Biên Pareto",
        "Nghiệm thỏa hiệp",
        "Phân bổ ngân sách",
        "Thảo luận chính sách"
        
    ])

    with tab1:
        st.subheader("Tập nghiệm Pareto")
        st.dataframe(pareto, use_container_width=True)

        fig = px.scatter_3d(
            pareto,
            x="GDP_gain",
            y="Inequality_MAD",
            z="Emission",
            color="TOPSIS_compromise_score",
            title="Biên Pareto 3D: GDP gain - Bất bình đẳng - Phát thải"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Nghiệm thỏa hiệp theo TOPSIS")
        st.dataframe(compromise, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        row = compromise.iloc[0]

        col1.metric("GDP gain", f"{row['GDP_gain']:,.2f}")
        col2.metric("Inequality MAD", f"{row['Inequality_MAD']:,.2f}")
        col3.metric("Emission", f"{row['Emission']:,.2f}")
        col4.metric("TOPSIS score", f"{row['TOPSIS_compromise_score']:.3f}")

    with tab3:
        st.subheader("Phân bổ ngân sách tại nghiệm thỏa hiệp")
        st.dataframe(allocation, use_container_width=True)

        fig = px.imshow(
            allocation.set_index("region")[["I", "D", "AI", "H"]],
            text_auto=True,
            aspect="auto",
            title="Heatmap phân bổ ngân sách theo vùng và hạng mục"
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(
            allocation,
            x="region",
            y=["I", "D", "AI", "H"],
            barmode="stack",
            title="Cơ cấu phân bổ ngân sách theo vùng"
        )
        st.plotly_chart(fig2, use_container_width=True)
 with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown(""" 
### a) Khi quan sát đường biên Pareto, đánh đổi giữa tăng trưởng và bao trùm có rõ ràng không?

Có. Output Bài 7 tạo ra **120 nghiệm Pareto**, cho thấy bài toán không có một nghiệm tối ưu duy nhất mà có một tập phương án đánh đổi giữa tăng trưởng, bao trùm, môi trường và rủi ro dữ liệu. Nghiệm có **GDP_gain cao nhất** đạt khoảng **60.466,15**, nhưng đi kèm **Inequality_MAD = 969,17** và **Emission = 1.867,75**. Trong khi đó, nghiệm thỏa hiệp TOPSIS có **GDP_gain = 58.815,38**, thấp hơn khoảng **2,73%**, nhưng **Inequality_MAD giảm còn 509,46** và **Emission giảm còn 89,49**.

Điều này cho thấy đánh đổi giữa tăng trưởng và bao trùm là rất rõ: nếu chỉ tối đa hóa GDP gain, mô hình chấp nhận phân bổ không đều hơn giữa các vùng và phát thải cao hơn; nếu chọn nghiệm thỏa hiệp, Việt Nam hy sinh một phần nhỏ tăng trưởng để cải thiện đáng kể công bằng vùng và môi trường. Cách tiếp cận này phù hợp với yêu cầu của đề bài: Bài 7 dùng NSGA-II để tạo tập nghiệm Pareto, sau đó dùng TOPSIS để chọn nghiệm thỏa hiệp theo trọng số chính sách **0,40 cho tăng trưởng, 0,25 cho bao trùm, 0,20 cho môi trường và 0,15 cho an ninh**.

Về thực tiễn, Nghị quyết 57-NQ/TW xác định khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số là đột phá phát triển quốc gia, nhưng đồng thời cũng chỉ ra hạn chế về hạ tầng số, nhân lực chất lượng cao và an toàn dữ liệu. Vì vậy, nghiệm thỏa hiệp hợp lý hơn nghiệm chỉ tối đa hóa tăng trưởng, vì chính sách chuyển đổi số không thể bỏ qua công bằng vùng và an toàn hệ thống.

### b) Nghiệm thỏa hiệp TOPSIS có hợp lý không?

Nghiệm thỏa hiệp có **TOPSIS_compromise_score = 0,840491**, cao nhất trong tập nghiệm Pareto. Phương án này đạt **GDP_gain = 58.815,38**, **Inequality_MAD = 509,46**, **Emission = 89,49** và **CyberRisk_Net = -12.149,30**. So với nghiệm tăng trưởng cao nhất, GDP chỉ giảm khoảng **2,73%**, nhưng bất bình đẳng vùng giảm khoảng **47,43%**, còn phát thải giảm rất mạnh.

Cấu trúc phân bổ của nghiệm thỏa hiệp cũng hợp lý. Mô hình không dồn vốn quá mức vào AI, mà ưu tiên nhiều cho **H - nhân lực số** và **D - chuyển đổi số doanh nghiệp**. Ví dụ: Trung du miền núi phía Bắc nhận khoảng **8.009,75** cho H; Tây Nguyên nhận khoảng **9.602,87** cho H; Đông Nam Bộ nhận khoảng **4.149,79** cho D. Điều này phù hợp với logic phát triển bao trùm: vùng yếu không nên nhảy thẳng vào AI khi chưa có hạ tầng dữ liệu, kỹ năng số và năng lực hấp thụ.

Về chính sách, đây là phương án có tính cân bằng tốt hơn, vì Quyết định 411/QĐ-TTg không chỉ đặt vấn đề kinh tế số mà còn nhấn mạnh phát triển xã hội số, tức là chuyển đổi số phải bao phủ người dân, doanh nghiệp và địa phương chứ không chỉ tập trung vào các vùng mạnh.

### c) Nghiệm tăng trưởng cao nhất hy sinh bao nhiêu về bao trùm và môi trường so với nghiệm thỏa hiệp?

Nghiệm tăng trưởng cao nhất đạt **GDP_gain = 60.466,15**, cao hơn nghiệm thỏa hiệp **1.650,77** đơn vị. Tuy nhiên, chi phí đi kèm rất lớn. **Inequality_MAD tăng từ 509,46 lên 969,17**, tức cao hơn khoảng **90,23%** so với nghiệm thỏa hiệp. **Emission tăng từ 89,49 lên 1.867,75**, tức cao hơn khoảng **20,87 lần**.

Như vậy, phần tăng thêm về GDP gain là tương đối nhỏ so với phần hy sinh về môi trường và công bằng vùng. Trong bối cảnh Việt Nam đã cam kết chuyển đổi xanh và phát triển bền vững, chính sách chỉ tối đa hóa tăng trưởng ngắn hạn có thể tạo chi phí dài hạn về môi trường, xã hội và năng lực hấp thụ số giữa các vùng.

### d) NSGA-II có thay thế được quyết định chính sách không?

Không. NSGA-II chỉ là công cụ tạo ra tập phương án Pareto, giúp nhà hoạch định chính sách nhìn thấy các đánh đổi. Việc chọn nghiệm nào vẫn là quyết định chính trị - xã hội, phụ thuộc vào ưu tiên của Nhà nước, doanh nghiệp, địa phương và người dân.

Đặc biệt, trọng số TOPSIS **0,40 cho tăng trưởng, 0,25 cho bao trùm, 0,20 cho môi trường và 0,15 cho an ninh** không phải là “chân lý kỹ thuật”, mà là lựa chọn giá trị. Nếu Chính phủ ưu tiên chuyển đổi xanh hơn, trọng số môi trường cần tăng; nếu ưu tiên vùng yếu, trọng số bao trùm cần tăng. Vì vậy, mô hình nên được dùng như công cụ hỗ trợ ra quyết định, không phải công cụ tự động quyết định chính sách.
""")

elif page == "Bài 8 - Tối ưu động":
    section_title(
        "Bài 8. Tối ưu động phân bổ vốn 2026-2035",
        "Theo dõi quỹ đạo K, D, AI, H, GDP và tiêu dùng qua thời gian"
    )

    opt = adv["Bai8_Optimal_Path"]
    shock = adv["Bai8_Shock_2028"]
    compare = adv["Bai8_Strategy_Compare"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "Quỹ đạo tối ưu",
        "Cú sốc 2028",
        "So sánh chiến lược",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.subheader("Quỹ đạo tối ưu 2026-2035")
        st.dataframe(opt, use_container_width=True)

        fig = px.line(
            opt,
            x="year",
            y=["K", "D", "AI", "H"],
            markers=True,
            title="Quỹ đạo K, D, AI, H"
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.line(
            opt,
            x="year",
            y=["Y", "C"],
            markers=True,
            title="Quỹ đạo sản lượng Y và tiêu dùng C"
        )
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.line(
            opt,
            x="year",
            y=["share_K", "share_D", "share_AI", "share_H"],
            markers=True,
            title="Tỷ trọng đầu tư tối ưu theo thời gian"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.subheader("Kịch bản có cú sốc năm 2028")
        st.dataframe(shock, use_container_width=True)

        shock_compare = opt[["year", "Y", "C"]].copy()
        shock_compare = shock_compare.rename(columns={"Y": "Y_no_shock", "C": "C_no_shock"})
        shock_compare["Y_shock"] = shock["Y"]
        shock_compare["C_shock"] = shock["C"]

        fig = px.line(
            shock_compare,
            x="year",
            y=["Y_no_shock", "Y_shock"],
            markers=True,
            title="So sánh sản lượng Y: không sốc và có sốc 2028"
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.line(
            shock_compare,
            x="year",
            y=["C_no_shock", "C_shock"],
            markers=True,
            title="So sánh tiêu dùng C: không sốc và có sốc 2028"
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("So sánh các chiến lược")
        st.dataframe(compare, use_container_width=True)

        fig = px.bar(
            compare,
            x="strategy",
            y="welfare",
            text="welfare",
            title="So sánh welfare giữa các chiến lược"
        )
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(
            compare,
            x="strategy",
            y="GDP_2035",
            text="GDP_2035",
            title="GDP năm 2035 theo từng chiến lược"
        )
        fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)
with tab3:
 st.subheader("Thảo luận chính sách")
        st.markdown("""
        ### a) Quỹ đạo tối ưu của K, D, AI, H có front-loaded hay back-loaded không?

Output Bài 8 cho thấy quỹ đạo tối ưu có tính **front-loaded đối với D và AI**. Năm 2026, tỷ trọng đầu tư vào D đạt **0,8825**, AI đạt **0,1175**, trong khi K và H gần như bằng 0. Sang các năm 2028-2032, tỷ trọng đầu tư vào AI tăng rất mạnh: **0,3978 năm 2028**, **0,5717 năm 2029**, **0,7012 năm 2030**, **0,7736 năm 2031** và **0,7996 năm 2032**. Đến năm 2035, mô hình trở về cơ cấu cân bằng hơn, mỗi nhóm K, D, AI, H khoảng **0,25**.

Điều này cho thấy mô hình ưu tiên số hóa và AI ở giai đoạn đầu để tạo tác động năng suất về sau. Kết quả này phù hợp với định hướng của Quyết định 749/QĐ-TTg về Chương trình Chuyển đổi số quốc gia đến năm 2025, định hướng đến năm 2030, và Quyết định 411/QĐ-TTg về phát triển kinh tế số, xã hội số.

Tuy nhiên, cần diễn giải thận trọng. Trong output, các biến trạng thái như K, D, AI, H có xu hướng giảm theo thời gian, ví dụ K giảm từ **27.500 năm 2026** xuống **17.332,09 năm 2035**, D giảm từ **20,3** xuống **8,41**, AI giảm từ **86** xuống **34,50**. Đây là hệ quả của cách đặc tả mô phỏng và khấu hao trong code, không nên hiểu là khuyến nghị thực tế để năng lực số suy giảm. Khi đưa vào báo cáo, cần ghi rõ mô hình nên bổ sung ràng buộc “không suy giảm năng lực tối thiểu” cho D, AI và H.

### b) Tỷ lệ đầu tư AI/H theo thời gian có ổn định không? Mô hình ngụ ý đào tạo nhân lực nên đi trước hay đồng thời với AI?

Tỷ lệ đầu tư AI/H trong output **không ổn định**. Giai đoạn 2026-2034, tỷ trọng H gần như bằng 0, trong khi AI tăng rất mạnh. Đặc biệt, AI chiếm **0,7012 năm 2030**, **0,7736 năm 2031** và **0,7996 năm 2032**. Đến năm 2035, H mới tăng lên khoảng **0,25**.

Nếu chỉ đọc máy móc, mô hình có vẻ khuyến nghị “AI đi trước, nhân lực đi sau”. Nhưng về chính sách, kết quả này cần phản biện. AI không thể phát huy hiệu quả nếu thiếu nhân lực số, chuyên gia dữ liệu, kỹ sư AI, chuyên gia an ninh mạng và lực lượng lao động có khả năng sử dụng công nghệ. Nghị quyết 57-NQ/TW cũng chỉ rõ nguồn nhân lực chất lượng cao còn thiếu là một trong các điểm nghẽn của phát triển khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số.

Vì vậy, hàm ý chính sách phù hợp hơn là **đầu tư AI phải đi đồng thời với đào tạo nhân lực số**, thậm chí ở các ngành/vùng có năng lực hấp thụ thấp thì nhân lực số nên đi trước. Nếu không, đầu tư AI có thể tạo ra “năng lực công nghệ trên giấy” nhưng khó chuyển hóa thành năng suất thực tế.

### c) Hệ số chiết khấu ρ = 0,97 ngụ ý chính phủ quan tâm dài hạn. Nếu ρ = 0,90 thì kết quả có thể thay đổi thế nào?

Với **ρ = 0,97**, mô hình coi trọng phúc lợi dài hạn, nên có xu hướng chấp nhận đầu tư sớm vào D và AI để tạo lợi ích về sau. Output cho thấy welfare của chiến lược tối ưu đạt **47,8763**, cao hơn chiến lược đầu tư đều (**47,7707**) và chiến lược front-load giả định (**47,7513**).

Nếu giảm ρ xuống **0,90**, tức Chính phủ quan tâm ngắn hạn hơn, mô hình thường sẽ ưu tiên các khoản đầu tư có hiệu quả tức thời hoặc giữ tiêu dùng hiện tại, thay vì đầu tư dài hạn vào AI, R&D và nhân lực số. Đây là một lý do các chính phủ có thể “dưới đầu tư” vào R&D và nhân lực: chi phí phát sinh ngay, nhưng lợi ích xuất hiện chậm, vượt ra ngoài nhiệm kỳ hoặc chu kỳ ngân sách.

Hàm ý chính sách là Việt Nam cần cơ chế bảo vệ các khoản đầu tư dài hạn, như ngân sách trung hạn cho khoa học công nghệ, quỹ đổi mới sáng tạo, đặt hàng nghiên cứu, hợp tác công tư và các chương trình đào tạo lại lao động dài hạn.

### d) Cú sốc năm 2028 ảnh hưởng thế nào đến kết quả?

Khi thêm cú sốc năm 2028, GDP năm 2028 giảm từ **355,60** xuống **327,16**. Welfare giảm từ **47,8763** xuống **47,7950**. Tuy nhiên đến năm 2035, GDP trong kịch bản shock đạt **281,59**, gần bằng kịch bản không shock là **281,72**.

Điều này cho thấy mô hình có khả năng phục hồi sau cú sốc, nhưng mức chênh lệch nhỏ cũng cho thấy cú sốc trong mô hình còn khá nhẹ và đơn giản. Trong thực tế, các cú sốc như COVID-19, bão Yagi, biến động xuất khẩu, suy giảm FDI hoặc đứt gãy chuỗi cung ứng có thể tạo tác động mạnh hơn. Năm 2024, GDP Việt Nam tăng **7,09%**, nhưng nền kinh tế vẫn chịu ảnh hưởng của thiên tai và biến động bên ngoài; điều này cho thấy mô hình cần bổ sung thêm các cú sốc thực tế như xuất khẩu, FDI, lạm phát, thiên tai và năng lượng.
""")

elif page == "Bài 9 - Lao động và AI":
    section_title(
        "Bài 9. Tác động AI tới thị trường lao động Việt Nam",
        "Tối ưu phân bổ đầu tư AI và đào tạo lại để bảo đảm NetJob"
    )

    labor = adv["Bai9_Labor_Result"]
    threshold = adv["Bai9_Threshold"]
    feasibility = adv["Bai9_Feasibility"]
    sankey = adv["Bai9_Sankey"]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Kết quả lao động",
        "Ngưỡng đào tạo",
        "Tính khả thi",
        "Sankey lao động",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.subheader("Kết quả NetJob theo ngành")
        st.dataframe(labor, use_container_width=True)

        fig = px.bar(
            labor,
            x="sector",
            y=["NewJob", "UpgradeJob", "DisplacedJob", "NetJob"],
            barmode="group",
            title="Việc làm mới, nâng cấp, dịch chuyển và NetJob"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(
            labor,
            x="sector",
            y=["x_AI", "x_H"],
            barmode="group",
            title="Phân bổ đầu tư AI và đào tạo lại theo ngành"
        )
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("Ngưỡng đầu tư đào tạo tối thiểu")
        st.dataframe(threshold, use_container_width=True)

    with tab3:
        st.subheader("Kiểm tra tính khả thi khi thêm ràng buộc an sinh")
        st.dataframe(feasibility, use_container_width=True)

    with tab4:
        st.subheader("Luồng dịch chuyển lao động nhóm dễ tổn thương")
        st.dataframe(sankey, use_container_width=True)

        labels = list(pd.unique(sankey[["source", "target"]].values.ravel()))
        label_to_id = {label: i for i, label in enumerate(labels)}

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                label=labels
            ),
            link=dict(
                source=sankey["source"].map(label_to_id),
                target=sankey["target"].map(label_to_id),
                value=sankey["value"]
            )
        )])

        fig.update_layout(title_text="Sankey: luồng dịch chuyển lao động", font_size=12)
        st.plotly_chart(fig, use_container_width=True)
with tab5:
 st.subheader("Thảo luận chính sách")
        st.markdown("""
        ### a) Ngành nào cần đầu tư đào tạo lại nhiều nhất theo kết quả tối ưu? Có khớp với cảm nhận thực tế ở Việt Nam không?

Theo output Bài 9, mô hình phân bổ toàn bộ **30.000 tỷ** vào **x_H của ngành Giáo dục-Đào tạo**, tạo **UpgradeJob = 1.650.000** và **NetJob = 1.650.000**. Các ngành còn lại có x_AI = 0, x_H = 0 và NetJob = 0.

Về mặt toán học, kết quả này xảy ra vì ngành Giáo dục-Đào tạo có hệ số tạo việc làm nâng cấp từ đào tạo lại rất cao, nên mô hình tuyến tính dồn ngân sách vào ngành có hiệu quả biên lớn nhất. Tuy nhiên, kết quả này chưa hoàn toàn khớp với thực tế Việt Nam nếu hiểu là chỉ ngành giáo dục cần đào tạo lại. Trên thực tế, các ngành như **Công nghiệp chế biến chế tạo, Bán buôn-bán lẻ, Tài chính-Ngân hàng và Logistics-Vận tải** cũng chịu rủi ro tự động hóa cao và cần đào tạo lại lớn.

Vì vậy, cần phản biện mô hình: output hiện tại đúng về kỹ thuật nhưng còn thiếu ràng buộc chính sách. Để sát thực tế hơn, nên thêm ràng buộc phân bổ tối thiểu cho các ngành có lao động lớn hoặc rủi ro tự động hóa cao, chẳng hạn CN chế biến chế tạo, bán buôn-bán lẻ và logistics. Quyết định 1446/QĐ-TTg về đào tạo, đào tạo lại, nâng cao kỹ năng nguồn nhân lực đáp ứng yêu cầu Cách mạng công nghiệp lần thứ tư cũng cho thấy đào tạo lại là vấn đề liên ngành, không chỉ riêng giáo dục.

### b) Ngành Tài chính-Ngân hàng có nguy cơ thay thế 52% nhưng cũng có hệ số tạo việc làm mới rất cao. Mô hình khuyến nghị chiến lược gì?

Trong dữ liệu mô hình, ngành Tài chính-Ngân hàng có **risk = 52%**, cao nhất trong 8 ngành, nhưng hệ số tạo việc làm mới từ AI cũng cao, **a1 = 45,8**. Điều này cho thấy ngành tài chính là ngành có hai mặt: vừa dễ bị tự động hóa ở các tác vụ lặp lại, vừa có khả năng tạo việc làm mới trong dữ liệu, quản trị rủi ro, phân tích tín dụng, chống gian lận, bảo mật và tài chính số.

Output hiện tại không phân bổ vốn cho tài chính-ngân hàng vì nghiệm tối ưu dồn toàn bộ vào Giáo dục-Đào tạo. Tuy nhiên, về chính sách, không nên kết luận rằng tài chính-ngân hàng không cần đầu tư. Chiến lược phù hợp là **AI đi kèm tái đào tạo bắt buộc**: cho phép ứng dụng AI trong phân tích dữ liệu và dịch vụ tài chính, nhưng phải đào tạo lại nhân viên sang các kỹ năng như dữ liệu, kiểm soát rủi ro mô hình, an ninh mạng, tuân thủ và đạo đức AI.

Điều này phù hợp với Quyết định 127/QĐ-TTg về Chiến lược quốc gia về nghiên cứu, phát triển và ứng dụng AI đến năm 2030, vì AI được định hướng là công nghệ quan trọng, nhưng cần đi cùng nhân lực và hệ sinh thái ứng dụng.

### c) Có nên đầu tư x_AI vào ngành Nông-Lâm-Thủy sản không?

Theo output, ngành Nông-Lâm-Thủy sản không được phân bổ x_AI hay x_H trong nghiệm tối ưu. Nguyên nhân là hệ số tạo việc làm mới từ AI của ngành này thấp, **a1 = 8,5**, trong khi mục tiêu của mô hình là tối đa hóa tổng NetJob. Vì vậy, mô hình không chọn đầu tư AI vào nông nghiệp nếu chỉ xét số việc làm ròng ngắn hạn.

Tuy nhiên, về chính sách, không nên hiểu là nông nghiệp không cần AI. Nông-Lâm-Thủy sản có **13,20 triệu lao động**, là ngành có quy mô lao động lớn nhất trong bảng. Dù hệ số tạo việc làm AI thấp, AI và số hóa vẫn có thể tạo lợi ích về năng suất, truy xuất nguồn gốc, dự báo thời tiết, tưới tiêu thông minh, logistics lạnh, thương mại điện tử nông sản và giảm rủi ro thiên tai. Do đó, với ngành này, chính sách nên ưu tiên chuyển đổi số phù hợp quy mô nhỏ, đào tạo kỹ năng số cơ bản và các ứng dụng AI chi phí thấp, thay vì đầu tư AI quy mô lớn như trong tài chính hay CNTT.

### d) “Tốc độ tự động hóa không nên vượt quá năng lực đào tạo lại” được biểu diễn bằng ràng buộc nào? Có nên bổ sung ràng buộc gì?

Trong mô hình, phát biểu này được biểu diễn bằng ràng buộc:

**DisplacedJobᵢ ≤ RetrainingCapacityᵢ**

Nghĩa là số lao động bị dịch chuyển do tự động hóa ở ngành i không được vượt quá năng lực đào tạo lại của ngành đó. Output cũng kiểm tra thêm ràng buộc “không ngành nào mất quá 5% lao động”, và kết quả cho thấy bài toán vẫn khả thi với **objective_total_netjob = 1.650.000** trong cả hai trường hợp Base và With_DisplacedJob_5pct_Labor_Cap.

Tuy nhiên, vì nghiệm tối ưu hiện tại không đầu tư AI vào ngành nào nên DisplacedJob bằng 0, làm cho ràng buộc an sinh chưa thực sự phát huy tác dụng. Để mô hình có ý nghĩa chính sách mạnh hơn, nên bổ sung: ràng buộc đầu tư tối thiểu vào ngành rủi ro cao; ràng buộc tỷ lệ ngân sách đào tạo lại tối thiểu cho CN chế biến chế tạo, bán buôn-bán lẻ, logistics; và ràng buộc không ngành nào nhận dưới một ngưỡng hỗ trợ nếu có rủi ro tự động hóa trên 35%.
""")
        

elif page == "Bài 10 - Stochastic LP":
    section_title(
        "Bài 10. Quy hoạch ngẫu nhiên hai giai đoạn",
        "Phân tích first-stage, second-stage, wait-and-see, VSS và EVPI"
    )

    first = adv["Bai10_First_Stage"]
    second = adv["Bai10_Second_Stage"]
    waitsee = adv["Bai10_Wait_See"]
    summary = adv["Bai10_VSS_EVPI"]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "First-stage",
        "Second-stage",
        "Wait-and-see",
        "VSS và EVPI",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.subheader("Quyết định first-stage")
        st.dataframe(first, use_container_width=True)

        fig = px.bar(
            first,
            x="item",
            y="first_stage_x",
            text="first_stage_x",
            title="Phân bổ first-stage"
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Quyết định second-stage theo kịch bản")
        st.dataframe(second, use_container_width=True)

        second_melt = second.melt(
            id_vars="scenario",
            var_name="item",
            value_name="second_stage_value"
        )

        fig = px.bar(
            second_melt,
            x="scenario",
            y="second_stage_value",
            color="item",
            barmode="group",
            title="Second-stage theo từng kịch bản"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Kết quả wait-and-see")
        st.dataframe(waitsee, use_container_width=True)

        fig = px.bar(
            waitsee,
            x="scenario",
            y="scenario_value",
            text="scenario_value",
            title="Giá trị theo từng kịch bản wait-and-see"
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("VSS và EVPI")
        st.dataframe(summary, use_container_width=True)

        fig = px.bar(
            summary,
            x="metric",
            y="value",
            text="value",
            title="SP, EEV, Wait-and-see, VSS và EVPI"
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
with tab5:
 st.subheader("Thảo luận chính sách")
        st.markdown("""
        ### a) So với lời giải xác định, lời giải SP có xu hướng đầu tư H nhiều hơn hay ít hơn? Vì sao?

Output Bài 10 cho thấy quyết định first-stage của mô hình SP phân bổ toàn bộ **65.000** vào **AI**, trong khi **I = 0, D = 0, H = 0**. Ở second-stage, mô hình phân bổ **15.000 vào D** trong kịch bản lạc quan và cơ sở; phân bổ **15.000 vào H** trong kịch bản bi quan và khủng hoảng.

Như vậy, ở giai đoạn đầu, lời giải SP không đầu tư H nhiều hơn, mà dồn vào AI do hệ số lợi ích cơ bản của AI cao nhất. Tuy nhiên, khi xảy ra kịch bản xấu, mô hình chuyển sang H, vì trong bảng hệ số của đề bài, H có hệ số cao hơn trong kịch bản khủng hoảng, phản ánh vai trò của lao động qua đào tạo trong khả năng chuyển đổi việc làm và hấp thụ cú sốc.

Về chính sách, kết quả này có thể hiểu là: AI hấp dẫn trong điều kiện bình thường, nhưng nhân lực số đóng vai trò hàng hóa bảo hiểm khi bất định xảy ra. Tuy nhiên, việc không đầu tư H ở first-stage là điểm cần phản biện, vì nếu khủng hoảng xảy ra mà mới bắt đầu đầu tư H thì có thể quá muộn. Chính sách thực tế nên đầu tư nhân lực số từ trước, không chỉ phản ứng sau cú sốc.

### b) VSS dương nói lên điều gì? Nhưng output hiện tại VSS = 0 thì nên diễn giải thế nào?

Theo lý thuyết, **VSS dương** cho thấy lời giải stochastic có giá trị hơn lời giải dựa trên kỳ vọng, tức là tư duy xác suất giúp chính sách tốt hơn trong môi trường bất định. Đề bài yêu cầu tính VSS và EVPI để đánh giá giá trị của mô hình stochastic và thông tin hoàn hảo.

Tuy nhiên, output của bạn cho thấy **SP_value = 98.575, EEV_value = 98.575, Wait-and-See_value = 98.575**, nên **VSS = 0** và **EVPI = 0**. Điều này không có nghĩa là tư duy xác suất vô ích trong thực tế; nó chỉ cho thấy trong phiên bản mô hình hiện tại, các kịch bản chưa đủ khác biệt hoặc ràng buộc chưa đủ mạnh để tạo ra khác biệt giữa lời giải stochastic và lời giải kỳ vọng.

Vì vậy, khi viết báo cáo, nên diễn giải thận trọng: mô hình đã cài đặt được cấu trúc stochastic LP, nhưng cần làm bất định mạnh hơn để VSS và EVPI phản ánh rõ giá trị của thông tin. Có thể tăng khác biệt giữa các hệ số kịch bản, thêm penalty khi điều chỉnh quá mức, thêm ràng buộc dự phòng nhân lực, hoặc thêm rủi ro làm giảm hiệu quả AI trong kịch bản khủng hoảng.

### c) COVID-19 và bão Yagi cho thấy Việt Nam có đang “dưới đầu tư” vào nhân lực số như một hàng hóa bảo hiểm không?

Có thể nói là có rủi ro dưới đầu tư. Output Bài 10 cho thấy khi kịch bản bi quan hoặc khủng hoảng xảy ra, mô hình chuyển second-stage sang **H = 15.000**, tức nhân lực trở thành lựa chọn thích nghi trong cú sốc. Điều này phù hợp với thực tế: khi xảy ra COVID-19, thiên tai hoặc đứt gãy chuỗi cung ứng, lao động có kỹ năng số và khả năng chuyển đổi việc làm sẽ giúp nền kinh tế linh hoạt hơn.

Bão Yagi năm 2024 là ví dụ cho thấy cú sốc thiên tai có thể ảnh hưởng đến sản xuất, logistics, nông nghiệp và đời sống doanh nghiệp. Cục Thống kê công bố GDP năm 2024 vẫn tăng **7,09%**, nhưng nền kinh tế chịu tác động bởi bối cảnh bên ngoài và thiên tai, cho thấy khả năng chống chịu là vấn đề chính sách quan trọng.

Vì vậy, nhân lực số nên được xem như một khoản đầu tư bảo hiểm xã hội - kinh tế, không chỉ là chi phí đào tạo. Việt Nam cần đầu tư trước vào đào tạo lại, kỹ năng số cơ bản, kỹ năng dữ liệu, kỹ năng an ninh mạng và năng lực học suốt đời. Quyết định 1446/QĐ-TTg về đào tạo, đào tạo lại nguồn nhân lực cho Cách mạng công nghiệp lần thứ tư là căn cứ chính sách phù hợp cho hướng này.
""")

elif page == "Bài 11 - Q-learning":
    section_title(
        "Bài 11. Q-learning cho chính sách kinh tế thích nghi",
        "So sánh chính sách học tăng cường với các chính sách cố định"
    )

    policy = adv["Bai11_Q_Policy"]
    compare = adv["Bai11_Policy_Compare"]
    curve = adv["Bai11_Learning_Curve"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "Chính sách học được",
        "So sánh chính sách",
        "Learning curve",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.subheader("Chính sách tối ưu theo một số trạng thái")
        st.dataframe(policy, use_container_width=True)

    with tab2:
        st.subheader("So sánh phần thưởng giữa các chính sách")
        st.dataframe(compare, use_container_width=True)

        fig = px.bar(
            compare,
            x="policy",
            y="avg_total_reward",
            error_y="std_total_reward",
            text="avg_total_reward",
            title="So sánh avg_total_reward"
        )
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Learning curve Q-learning")
        st.dataframe(curve.tail(500), use_container_width=True)

        fig = px.line(
            curve,
            x="episode",
            y="rolling_reward_200",
            title="Đường học Q-learning, rolling reward 200 episodes"
        )
        st.plotly_chart(fig, use_container_width=True)
with tab4:
 st.subheader("Thảo luận chính sách")
        st.markdown("""
        ### a) Khi nền kinh tế ở trạng thái GDP growth thấp, D thấp, U cao, chính sách π*(s) chọn hành động gì? Có khớp với “quick win” không?

Output `Bai11_Q_Policy` cho thấy ở trạng thái **LowGDP_LowD_LowAI_HighU = [0, 0, 0, 2]**, chính sách chọn **best_action_id = 0**, tức **Truyền thống**. Tuy nhiên, Q-value ở trạng thái này bằng **0**, cho thấy agent gần như chưa học được kinh nghiệm rõ ràng tại trạng thái này hoặc trạng thái này xuất hiện ít trong quá trình huấn luyện.

Về chính sách, lựa chọn “Truyền thống” trong trạng thái GDP thấp, D thấp và thất nghiệp cao chưa thật sự khớp với logic “quick win”. Trong thực tế, khi D thấp và rủi ro thất nghiệp cao, chính sách quick win nên ưu tiên các hành động có khả năng tạo tác động nhanh như số hóa dịch vụ công, hỗ trợ doanh nghiệp nhỏ chuyển đổi số, đào tạo lại lao động ngắn hạn và mở rộng kỹ năng số cơ bản. Do đó, kết quả này cần được xem là tín hiệu mô hình còn cần huấn luyện thêm hoặc cần cải thiện thiết kế phần thưởng.

Đề bài cũng nhấn mạnh Q-learning chỉ minh họa kỹ thuật ra quyết định thích nghi, không nhằm tự động hóa hoạch định chính sách.

### b) Khi GDP growth cao, AI cao, U thấp, chính sách chọn gì? Có phù hợp với “consolidation” không?

Ở trạng thái **HighGDP_HighD_HighAI_LowU = [2, 2, 2, 0]**, output cũng cho thấy chính sách chọn **Truyền thống**, với **Q-value = 0**. Nếu diễn giải theo logic chính sách, khi GDP cao, D cao, AI cao và thất nghiệp thấp, chính sách “consolidation” thường nên giảm tốc độ mở rộng AI quá nhanh, chuyển sang củng cố thể chế, an ninh dữ liệu, hạ tầng nền tảng, nhân lực và kiểm soát rủi ro. Hành động “Truyền thống” có thể phù hợp một phần nếu hiểu là giảm rủi ro công nghệ và quay về củng cố nền tảng.

Tuy nhiên, vì Q-value = 0, không nên diễn giải đây là khuyến nghị mạnh của mô hình. Kết quả đáng tin cậy hơn nằm ở trạng thái **VN_2026 = [1,1,0,1]**, nơi mô hình chọn **Số hóa nhanh** với **Q-value = 15,2896**. Điều này hợp lý hơn với thực tiễn Việt Nam: khi năng lực AI còn thấp nhưng nền kinh tế đang chuyển đổi, ưu tiên số hóa nhanh là bước đi phù hợp trước khi mở rộng AI dẫn dắt.

### c) Q-learning có tốt hơn chính sách cố định không?

Có, trong output của bạn, Q-learning có kết quả tốt hơn các baseline. **Q_learning_policy** đạt **avg_total_reward = 8,2600**, cao hơn **Always_balanced_a1 = 7,4861**, **Always_AI_led_a3 = 7,5729** và **Random = 7,5335**. Điều này cho thấy chính sách thích nghi theo trạng thái có thể tạo phúc lợi cao hơn chính sách cố định.

Tuy nhiên, kết quả cũng cho thấy một số trạng thái có Q-value = 0, tức agent chưa học đầy đủ toàn bộ không gian trạng thái. Vì vậy, mô hình cần được cải tiến bằng cách tăng số episode, cải thiện hàm thưởng, kiểm tra tần suất ghé thăm trạng thái và bổ sung ràng buộc an sinh, phát thải, an ninh dữ liệu rõ hơn.

### d) Tích hợp π* vào hoạch định chính sách Việt Nam như thế nào để không vi phạm nguyên tắc “AI không thay thế quyết định chính trị - xã hội”?

Cách phù hợp là tích hợp Q-learning như **hệ thống khuyến nghị chính sách**, không phải hệ thống tự động ra quyết định. Quy trình nên gồm 4 bước: mô hình đề xuất hành động theo trạng thái; chuyên gia kiểm định giả định và dữ liệu; hội đồng chính sách đánh giá tác động xã hội - ngân sách - pháp lý; cuối cùng cơ quan có thẩm quyền quyết định và chịu trách nhiệm.

Điều này đặc biệt quan trọng vì phần thưởng trong Q-learning phản ánh trọng số chủ quan: tăng trưởng, thất nghiệp, rủi ro mạng và phát thải. Nếu trọng số thay đổi, chính sách tối ưu cũng thay đổi. Do đó, AI chỉ nên đóng vai trò hỗ trợ minh bạch hóa các đánh đổi, không thay thế trách nhiệm chính trị, trách nhiệm giải trình và tham vấn xã hội.
""")

elif page == "Bài 12 - Tổng hợp kịch bản":
    section_title(
        "Bài 12. Dashboard tích hợp AIDEOM-VN",
        "So sánh 5 kịch bản chính sách đến năm 2030"
    )

    path = adv["Bai12_Scenario_Path"]
    kpi = adv["Bai12_KPI_2030"]
    risk = adv["Bai12_Risk_Warning"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "Đường kịch bản",
        "KPI năm 2030",
        "Cảnh báo rủi ro",
        "Thảo luận chính sách"
    ])

    with tab1:
        st.subheader("Đường phát triển theo kịch bản")
        st.dataframe(path, use_container_width=True)

        fig = px.line(
            path,
            x="year",
            y="GDP_index",
            color="scenario",
            markers=True,
            title="GDP index theo 5 kịch bản"
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.line(
            path,
            x="year",
            y="D",
            color="scenario",
            markers=True,
            title="Mức độ số hóa D theo kịch bản"
        )
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.line(
            path,
            x="year",
            y="AI",
            color="scenario",
            markers=True,
            title="Năng lực AI theo kịch bản"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.subheader("KPI năm 2030")
        st.dataframe(kpi, use_container_width=True)

        fig = px.bar(
            kpi,
            x="scenario",
            y="GDP_index",
            text="GDP_index",
            title="GDP index năm 2030 theo kịch bản"
        )
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(
            kpi,
            x="scenario",
            y=["D", "AI", "H", "A"],
            barmode="group",
            title="So sánh D, AI, H, A năm 2030"
        )
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Cảnh báo rủi ro theo kịch bản")
        st.dataframe(risk, use_container_width=True)
with tab4:
 st.subheader("Thảo luận chính sách")
        st.markdown("""
        ### a) Kịch bản nào cho kết quả GDP_index năm 2030 cao nhất?

Output `Bai12_KPI_2030` cho thấy kịch bản có **GDP_index cao nhất** là **S3_AI_dan_dat**, đạt **380,7220**, xếp hạng 1. Kịch bản đứng thứ 2 là **S2_So_hoa_nhanh**, đạt **380,3790**; đứng thứ 3 là **S5_Toi_uu_can_bang**, đạt **379,4473**. Kịch bản thấp nhất là **S1_Truyen_thong**, đạt **377,7788**.

Điều này cho thấy trong mô hình, chiến lược AI dẫn dắt có thể tạo tăng trưởng cao nhất đến năm 2030, nhờ tăng mạnh năng lực AI lên **90,5915**. Kết quả phù hợp với Quyết định 127/QĐ-TTg, trong đó Việt Nam đặt mục tiêu phát triển nghiên cứu, ứng dụng AI đến năm 2030.

Tuy nhiên, chênh lệch GDP_index giữa S3 và S2 không quá lớn, chỉ khoảng **0,3430 điểm**. Điều này hàm ý chiến lược AI dẫn dắt không vượt trội tuyệt đối so với số hóa nhanh. Nếu xét thêm rủi ro nhân lực, khoảng cách số và an ninh dữ liệu, chiến lược số hóa nhanh hoặc tối ưu cân bằng có thể thực tế hơn.

### b) Kịch bản nào phù hợp nhất với thực tiễn Việt Nam hiện nay?

Nếu chỉ xét GDP_index, **S3_AI_dan_dat** là tốt nhất. Nhưng nếu xét năng lực thực thi, Việt Nam có thể phù hợp hơn với **S5_Toi_uu_can_bang** hoặc **S2_So_hoa_nhanh**. S2 giúp D đạt **21,5976**, cao nhất trong 5 kịch bản, phù hợp với mục tiêu kinh tế số và xã hội số. S5 có kết quả cân bằng hơn: **GDP_index = 379,4473**, **D = 20,6641**, **AI = 84,7566**, **H = 29,6657**.

Quyết định 749/QĐ-TTg và Quyết định 411/QĐ-TTg đều nhấn mạnh chuyển đổi số là quá trình đồng bộ giữa chính phủ số, kinh tế số và xã hội số, không chỉ là đầu tư vào một công nghệ đơn lẻ. Vì vậy, chiến lược cân bằng giữa D, AI và H có tính khả thi cao hơn chiến lược chỉ nhấn mạnh AI.

### c) Cảnh báo rủi ro trong output nói lên điều gì?

Output `Bai12_Risk_Warning` cho thấy cả 5 kịch bản đều có **cyber_risk = Trung bình**, **digital_gap_risk = Cao**, và **human_capital_status = Thiếu**. Đây là kết quả rất quan trọng: dù kịch bản nào được chọn, mô hình đều cảnh báo Việt Nam vẫn đối mặt với khoảng cách số và thiếu hụt nhân lực.

Điều này phù hợp với Nghị quyết 57-NQ/TW, trong đó nêu rõ hạ tầng số còn hạn chế, nguồn nhân lực chất lượng cao còn thiếu, an ninh - an toàn thông tin và bảo vệ dữ liệu còn nhiều thách thức. Vì vậy, khuyến nghị chính sách không nên chỉ là “chọn kịch bản GDP cao nhất”, mà phải đi kèm chương trình giảm khoảng cách số, đào tạo lại lao động và tăng cường an toàn dữ liệu.

### d) Dashboard AIDEOM-VN có đáp ứng yêu cầu hỗ trợ ra quyết định không?

Về cấu trúc, dashboard đã đáp ứng yêu cầu cơ bản: có các module từ dự báo, phân bổ, lao động, bất định, Q-learning đến so sánh kịch bản. Đề bài yêu cầu module M6 là dashboard web bằng Streamlit hoặc Plotly Dash, tối thiểu gồm các tab Tổng quan, Phân bổ, Kịch bản so sánh và Cảnh báo rủi ro. Output hiện tại đã có **Bai12_Scenario_Path**, **Bai12_KPI_2030** và **Bai12_Risk_Warning**, đủ để xây dựng các tab này.

Tuy nhiên, để dashboard có chất lượng cao hơn, cần thêm ba cải tiến. Thứ nhất, cho phép người dùng điều chỉnh trọng số chính sách và xem thay đổi kết quả. Thứ hai, thêm giải thích dưới mỗi biểu đồ để tránh người xem hiểu nhầm mô hình là quyết định cuối cùng. Thứ ba, bổ sung phần giới hạn mô hình, đặc biệt là các giả định đơn giản hóa trong Bài 8, Bài 10 và Bài 11.

### e) Khuyến nghị chính sách tổng hợp từ Bài 12 là gì?

Từ output Bài 12, khuyến nghị chính sách hợp lý nhất là không chọn cực đoan “truyền thống” hoặc “AI dẫn dắt tuyệt đối”, mà nên chọn chiến lược **tối ưu cân bằng có điều chỉnh**. Cụ thể, Việt Nam nên ưu tiên số hóa nền kinh tế và chính phủ số; mở rộng AI ở các ngành/vùng có năng lực hấp thụ cao; đầu tư mạnh hơn vào nhân lực số; và kiểm soát khoảng cách số giữa các vùng.

Nếu cần chọn một kịch bản để trình bày trên dashboard, có thể chọn **S5_Toi_uu_can_bang** làm kịch bản khuyến nghị chính sách, còn **S3_AI_dan_dat** là kịch bản tăng trưởng cao nhưng rủi ro hấp thụ lớn hơn. Cách trình bày này cân bằng giữa mục tiêu tăng trưởng, khả năng thực thi và phát triển bao trùm.
""")
