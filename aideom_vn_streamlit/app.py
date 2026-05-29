import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="AIDEOM-VN Dashboard",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

MAIN_FILE = DATA_DIR / "ket_qua_bai_1_den_6.xlsx"
SUPP_FILE = DATA_DIR / "ket_qua_bo_sung_bai_2_5.xlsx"

@st.cache_data
def load_excel(file_path):
    return pd.read_excel(file_path, sheet_name=None)


main = load_excel(MAIN_FILE)
supp = load_excel(SUPP_FILE)


st.sidebar.title("📊 AIDEOM-VN")
st.sidebar.caption("Dashboard kết quả Bài 1-6")

page = st.sidebar.radio(
    "Chọn nội dung",
    [
        "Tổng quan",
        "Bài 1 - Cobb-Douglas",
        "Bài 2 - LP ngân sách",
        "Bài 3 - Ưu tiên ngành",
        "Bài 4 - Phân bổ vùng",
        "Bài 5 - Lựa chọn dự án",
        "Bài 6 - TOPSIS vùng"
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

Output mô hình cho thấy nghiệm tối ưu ban đầu là: hạ tầng số 25, AI và dữ liệu 15, nhân lực số 20, R&D 40 nghìn tỷ VND. Giá trị mục tiêu đạt Z = 112,25*.

Dẫn chứng quan trọng là shadow price của ràng buộc ngân sách tổng bằng 1,35. Nghĩa là trong vùng nghiệm tối ưu hiện tại, nếu tăng thêm 1 nghìn tỷ VND ngân sách, GDP kỳ vọng tăng thêm khoảng 1,35 nghìn tỷ VND. Phân tích độ nhạy xác nhận điều này: ngân sách tăng từ 100 lên 120 làm Z* tăng từ 112,25 lên 139,25; ngân sách tăng lên 140 làm Z* tăng lên 166,25. Mỗi 20 nghìn tỷ tăng thêm tạo thêm 27 nghìn tỷ GDP kỳ vọng, tương ứng hệ số 1,35.

Tuy nhiên, trong thực tiễn Việt Nam, đây chỉ là cận trên kỹ thuật của mô hình. Hiệu quả vốn công còn phụ thuộc vào năng lực giải ngân, chất lượng dự án, năng lực hấp thụ của địa phương và khả năng phối hợp giữa các cơ quan. Vì vậy, shadow price có giá trị tham khảo cho phân tích chi phí cơ hội, nhưng không nên hiểu là cứ tăng ngân sách thì GDP thực tế chắc chắn tăng tương ứng.

### b) Vì sao R&D có hệ số tác động cao nhất nhưng lại có ràng buộc tối thiểu thấp nhất?

Trong nghiệm tối ưu, R&D nhận 40 nghìn tỷ VND, cao hơn nhiều so với mức tối thiểu 10 nghìn tỷ VND. Nguyên nhân là R&D có hệ số tác động cao nhất, 1,35, nên sau khi các ràng buộc tối thiểu của hạ tầng, AI và nhân lực số được đáp ứng, mô hình dồn phần ngân sách còn lại vào R&D để tối đa hóa GDP kỳ vọng.

Việc đặt sàn R&D thấp vẫn hợp lý vì R&D có độ trễ dài, rủi ro cao và phụ thuộc mạnh vào năng lực hấp thụ công nghệ của doanh nghiệp, viện nghiên cứu, trường đại học và thị trường. Trong bối cảnh Nghị quyết 57-NQ/TW nhấn mạnh đột phá khoa học công nghệ, đổi mới sáng tạo và chuyển đổi số, R&D cần được ưu tiên nhưng phải đi kèm cơ chế thương mại hóa kết quả nghiên cứu và liên kết doanh nghiệp.

### c) Giả sử Chính phủ muốn ưu tiên nhân lực số với x_H ≥ 30. Bài toán có còn khả thi không? Z* thay đổi như thế nào?

Khi tăng ràng buộc nhân lực số từ x_H ≥ 20 lên x_H ≥ 30, output bổ sung cho thấy bài toán vẫn khả thi. Nghiệm mới là: hạ tầng số 25, AI và dữ liệu 15, nhân lực số 30, R&D 30. Giá trị mục tiêu giảm từ 112,25 xuống 108,25, tức giảm 4,00 nghìn tỷ GDP kỳ vọng.

Kết quả này cho thấy ưu tiên nhân lực số có chi phí cơ hội ngắn hạn, vì mô hình phải chuyển 10 nghìn tỷ từ R&D, nơi có hệ số tác động 1,35, sang nhân lực số, nơi có hệ số tác động 0,95. Tuy nhiên, về dài hạn, ưu tiên nhân lực số là hợp lý vì đây là điều kiện để hấp thụ AI, vận hành hạ tầng số và triển khai R&D. Điều này phù hợp với tinh thần của Quyết định 749/QĐ-TTg và Quyết định 411/QĐ-TTg, vì chuyển đổi số không chỉ là đầu tư công nghệ mà còn là phát triển năng lực con người, doanh nghiệp và xã hội số.

### d) Tỷ lệ 35% công nghệ chiến lược AI + R&D có khả thi không?

Trong nghiệm tối ưu ban đầu, AI nhận 15 và R&D nhận 40, tổng cộng 55 nghìn tỷ VND, chiếm 55% tổng ngân sách. Như vậy, ràng buộc tối thiểu 35% cho AI + R&D không phải ràng buộc chặt, vì mô hình tự chọn mức cao hơn 35%.

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
### a) Ba ngành nào nên được ưu tiên?

Kết quả xếp hạng cho thấy ba ngành ưu tiên cao nhất là: **Thông tin - Truyền thông - CNTT**, **Công nghiệp chế biến chế tạo**, và **Tài chính - Ngân hàng - Bảo hiểm**.

Kết quả này hợp lý vì các ngành này có năng lực số, khả năng ứng dụng AI và tác động lan tỏa lớn. CNTT là ngành nền tảng; chế biến chế tạo có vai trò lớn trong xuất khẩu và chuỗi cung ứng; tài chính - ngân hàng có dữ liệu lớn và khả năng ứng dụng AI cao.

### b) Vì sao Khai khoáng không nằm trong nhóm ưu tiên?

Khai khoáng có thể có năng suất cao nhưng lại có tăng trưởng thấp, lan tỏa hạn chế, việc làm thấp và rủi ro tự động hóa cao. Do đó, ngành này không phù hợp để ưu tiên hàng đầu nếu mục tiêu là lan tỏa chuyển đổi số và AI trên diện rộng.

### c) Ai nên quyết định bộ trọng số?

Kết quả cho thấy khi thay đổi từ định hướng tăng trưởng sang định hướng bao trùm, thứ hạng một số ngành thay đổi đáng kể. Vì vậy, trọng số không chỉ là vấn đề kỹ thuật mà còn phản ánh lựa chọn chính sách.

Do đó, bộ trọng số nên được quyết định bởi sự kết hợp giữa chuyên gia kỹ thuật, hội đồng chính sách, doanh nghiệp, địa phương và đối thoại công khai.
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
### a) Nếu bỏ ràng buộc công bằng, vốn sẽ chảy về đâu?

Khi không có ràng buộc công bằng, ngân sách tập trung mạnh vào các vùng có hệ số tác động cao như **Đồng bằng sông Hồng** và **Đông Nam Bộ**, đặc biệt ở hạng mục AI.

Điều này hợp lý về hiệu quả kinh tế ngắn hạn, nhưng có thể làm gia tăng khoảng cách số giữa các vùng.

### b) Chi phí của công bằng vùng là bao nhiêu?

Khi có công bằng, Z* đạt khoảng **52.485**. Khi bỏ công bằng, Z* đạt khoảng **68.750**. Như vậy, chi phí kinh tế của công bằng vùng là khoảng **16.265**, tương đương giảm khoảng **23,66%**.

Mức giảm này lớn, nhưng có thể chấp nhận được nếu mục tiêu chính sách là phát triển bao trùm và tránh để vùng yếu bị bỏ lại phía sau.

### c) Tây Nguyên nên đầu tư AI hay H và I trước?

Kết quả cho thấy Tây Nguyên không được ưu tiên đầu tư AI trực tiếp. Mô hình gợi ý cần tập trung vào **nhân lực số, hạ tầng số và chuyển đổi số doanh nghiệp** trước.

Điều này phù hợp với logic chính sách: vùng có nền tảng số thấp cần xây dựng năng lực hấp thụ trước khi đầu tư AI quy mô lớn.
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
### a) Vì sao mô hình chọn P15 Open Data?

P15 được chọn dù chi phí chỉ **1.500 tỷ VND** vì có tỷ suất lợi ích/chi phí cao và không làm căng ràng buộc ngân sách. Về chính sách, đây là kết quả hợp lý vì dữ liệu mở là nền tảng cho chính phủ số, AI và đổi mới sáng tạo.

### b) Bắt buộc P14 an ninh mạng có làm giảm Z* không?

Khi giữ ràng buộc P14, tổng lợi ích NPV đạt **115.400 tỷ**. Khi bỏ ràng buộc bắt buộc P14, tổng lợi ích tăng lên **116.300 tỷ**. Như vậy, bắt buộc P14 làm giảm khoảng **900 tỷ VND** NPV.

Tuy nhiên, mức giảm này có thể chấp nhận được vì an ninh mạng là dự án bảo hiểm hệ thống cho toàn bộ chuyển đổi số quốc gia.

### c) Bắt buộc chọn cả P1 và P2 có khả thi không?

Khi bắt buộc chọn cả P1 và P2, bài toán vẫn khả thi. Danh mục chọn 8 dự án với tổng chi phí **59.300 tỷ** và tổng lợi ích **113.300 tỷ**.

So với nghiệm cơ sở **115.400 tỷ**, phương án này làm giảm **2.100 tỷ** NPV. Tuy nhiên, việc có hai trung tâm dữ liệu có thể hợp lý để bảo đảm dự phòng, an toàn hệ thống và chủ quyền dữ liệu.

### d) Khi nới ngân sách lên 100.000 tỷ, danh mục có đổi không?

Kết quả cho thấy danh mục không thay đổi. Điều này cho thấy ngân sách tổng không phải ràng buộc duy nhất. Các ràng buộc về ngân sách năm 1-2, tiên quyết nhân lực, loại trừ dự án và giới hạn số lượng dự án cũng rất quan trọng.

### e) Khi xét rủi ro hoàn thành, danh mục thay đổi thế nào?

Khi xét xác suất hoàn thành, danh mục chuyển sang các dự án có rủi ro triển khai thấp hơn như 5G, y tế số, giáo dục số, đào tạo kỹ sư, an ninh mạng và dữ liệu mở.

Điều này cho thấy không nên chỉ dựa vào NPV danh nghĩa, mà phải xét thêm rủi ro tiến độ, năng lực thực hiện và khả năng hấp thụ công nghệ.
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
### a) Vùng nào dẫn đầu theo TOPSIS?

Theo trọng số chuyên gia, **Đông Nam Bộ** xếp hạng 1 với điểm khoảng **0,940**, tiếp theo là **Đồng bằng sông Hồng** với khoảng **0,898**.

Đây là kết quả hợp lý vì hai vùng này có GRDP/người, FDI, chỉ số số hóa, AI readiness và lao động qua đào tạo cao.

### b) Khi dùng Entropy, thứ hạng có thay đổi lớn không?

Kết quả Entropy không làm thay đổi đáng kể thứ hạng tổng thể. Điều này cho thấy kết quả TOPSIS khá ổn định.

Tuy nhiên, sự vượt trội của Đông Nam Bộ và Đồng bằng sông Hồng cũng phản ánh khoảng cách năng lực số giữa vùng mạnh và vùng yếu.

### c) AI Readiness và Internet penetration tương quan cao thì ảnh hưởng thế nào?

Nếu hai tiêu chí này tương quan cao, TOPSIS có thể đếm trùng lợi thế của vùng phát triển. Điều này làm tăng điểm của các vùng vốn đã mạnh.

Có thể xử lý bằng cách kiểm tra tương quan, gộp tiêu chí, dùng PCA hoặc bổ sung tiêu chí khoảng cách số để phản ánh nhu cầu hỗ trợ.

### d) Nếu chọn 3 vùng xây trung tâm AI?

Dựa trên kết quả TOPSIS, ba vùng phù hợp nhất là **Đông Nam Bộ**, **Đồng bằng sông Hồng**, và **Bắc Trung Bộ + Duyên hải miền Trung**.

Tuy nhiên, quyết định cuối cùng cần xét thêm an ninh dữ liệu, địa - chính trị, rủi ro thiên tai, năng lượng và vai trò liên kết vùng.
""")
