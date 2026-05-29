import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================
# PAGE CONFIG + STYLE
# =========================
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
    .stMarkdown p, .stMarkdown li {
        font-size: 18px;
        line-height: 1.7;
        text-align: justify;
    }
    .stDataFrame {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# DATA LOADING
# =========================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

MAIN_FILE = DATA_DIR / "ket_qua_bai_1_den_6.xlsx"
SUPP_FILE = DATA_DIR / "ket_qua_bo_sung_bai_2_5.xlsx"
ADV_FILE = DATA_DIR / "ket_qua_bai_7_den_12.xlsx"

@st.cache_data
def load_excel(file_path: Path):
    return pd.read_excel(file_path, sheet_name=None)


def require_file(path: Path):
    if not path.exists():
        st.error(f"Không tìm thấy file: {path}. Hãy upload file này vào thư mục data trên GitHub.")
        st.stop()


for file in [MAIN_FILE, SUPP_FILE, ADV_FILE]:
    require_file(file)

main = load_excel(MAIN_FILE)
supp = load_excel(SUPP_FILE)
adv = load_excel(ADV_FILE)

# =========================
# HELPERS
# =========================
def section_title(title, subtitle=None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()


def show_df(df, title=None):
    if title:
        st.subheader(title)
    st.dataframe(df, use_container_width=True)


# =========================
# DISCUSSIONS
# =========================
DISCUSSIONS = {
    "bai1": """
### a) TFP của Việt Nam có xu hướng tăng hay giảm trong giai đoạn 2020-2025? Điều đó nói lên gì về chất lượng tăng trưởng?
Dựa trên output mô hình, TFP A_t tăng liên tục từ 27,75 năm 2020 lên 34,91 năm 2025. Điều này cho thấy phần tăng trưởng không được giải thích trực tiếp bởi vốn vật chất K, lao động L, số hóa D, năng lực AI và nhân lực số H có xu hướng tăng. Nói cách khác, chất lượng tăng trưởng trong mô hình có cải thiện, vì GDP không chỉ tăng nhờ mở rộng đầu vào mà còn nhờ hiệu quả tổng hợp cao hơn.

Dẫn chứng rõ hơn là trong bảng phân rã tăng trưởng, TFP đóng góp 49,08% vào tăng trưởng bình quân, cao hơn cả vốn vật chất K với 31,78%. Điều này phù hợp với bối cảnh Việt Nam đang chuyển từ mô hình tăng trưởng dựa nhiều vào vốn và lao động sang mô hình dựa nhiều hơn vào năng suất, khoa học công nghệ, đổi mới sáng tạo và chuyển đổi số. Năm 2024, NSO/GSO công bố GDP Việt Nam tăng 7,09%, trong đó công nghiệp - xây dựng và dịch vụ đóng góp lớn vào tăng trưởng, phản ánh xu hướng phục hồi và nâng cao năng lực sản xuất của nền kinh tế.

Tuy nhiên, cần lưu ý rằng TFP ở đây được tính ngược từ hàm sản xuất với hệ số giả định. Vì vậy, kết quả này nên được hiểu là chỉ báo định lượng hỗ trợ phân tích, không phải bằng chứng nhân quả tuyệt đối.
### b) Trong các yếu tố mới D, AI, H, yếu tố nào đóng góp nhiều nhất cho tăng trưởng giai đoạn vừa qua? Vì sao?
Trong ba yếu tố mới, D - mức độ số hóa đóng góp lớn nhất, đạt 10,37% tăng trưởng bình quân. Tiếp theo là AI với 6,24%, và H - nhân lực số với 2,87%.

Kết quả này hợp lý vì trong giai đoạn 2020-2025, tỷ trọng kinh tế số/GDP trong dữ liệu tăng từ 12,0% năm 2020 lên 19,5% năm 2025. Mức tăng của D rõ ràng hơn so với H, trong khi AI vẫn đang ở giai đoạn tích lũy nền tảng. Điều này phù hợp với định hướng của Quyết định 749/QĐ-TTg về Chương trình Chuyển đổi số quốc gia và Quyết định 411/QĐ-TTg về phát triển kinh tế số, xã hội số đến năm 2025, định hướng 2030.

Hàm ý chính sách là Việt Nam không nên chỉ đầu tư vào công nghệ AI riêng lẻ, mà cần đầu tư đồng bộ vào số hóa nền kinh tế, dữ liệu, hạ tầng số và nhân lực số. Nếu nhân lực số tăng chậm, AI sẽ khó phát huy đầy đủ tác động năng suất.
### c) Mục tiêu Việt Nam đạt 30% kinh tế số/GDP vào 2030 có khả thi không nếu dựa trên mô hình này? Cần ràng buộc gì?
Output mô phỏng cho thấy nếu đến năm 2030, D đạt 30%, AI đạt 100 nghìn doanh nghiệp số, H đạt 35%, K tăng 6%/năm và TFP tăng 1,2%/năm, GDP dự báo năm 2030 đạt khoảng 16.362,93 nghìn tỷ VND. So với mức GDP năm 2025 là 12.847,6 nghìn tỷ VND, đây là kịch bản tăng trưởng tích cực.

Vì vậy, mục tiêu kinh tế số đạt 30% GDP vào năm 2030 có thể xem là khả thi về mặt mô hình. Tuy nhiên, để mục tiêu này không chỉ là con số kỹ thuật, cần các ràng buộc chính sách: đầu tư hạ tầng số, mở rộng dữ liệu mở, bảo đảm an ninh mạng, đào tạo nhân lực số, hỗ trợ doanh nghiệp nhỏ và vừa chuyển đổi số, đồng thời thu hẹp khoảng cách số giữa các vùng. Nghị quyết 57-NQ/TW cũng nhấn mạnh khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số là yếu tố quyết định phát triển, đồng thời chỉ ra các hạn chế hiện nay như hạ tầng số chưa đồng bộ, nhân lực chất lượng cao còn thiếu và an toàn dữ liệu còn nhiều thách thức.""",
    "bai2": """
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
""",
 "bai3": """
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
""",

    "bai4": """
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
""",

    "bai5": """
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
""",

    "bai6": """
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
""",
    "bai7": """
### a) Khi quan sát đường biên Pareto, đánh đổi giữa tăng trưởng và bao trùm có rõ ràng không?
Có. Output Bài 7 tạo ra **120 nghiệm Pareto**, cho thấy bài toán không có một nghiệm tối ưu duy nhất mà có một tập phương án đánh đổi giữa tăng trưởng, bao trùm, môi trường và rủi ro dữ liệu. Nghiệm có **GDP_gain cao nhất** đạt khoảng **60.466,15**, nhưng đi kèm **Inequality_MAD = 969,17** và **Emission = 1.867,75**. Trong khi đó, nghiệm thỏa hiệp TOPSIS có **GDP_gain = 58.815,38**, thấp hơn khoảng **2,73%**, nhưng **Inequality_MAD giảm còn 509,46** và **Emission giảm còn 89,49**.

Điều này cho thấy đánh đổi giữa tăng trưởng và bao trùm là rất rõ: nếu chỉ tối đa hóa GDP gain, mô hình chấp nhận phân bổ không đều hơn giữa các vùng và phát thải cao hơn; nếu chọn nghiệm thỏa hiệp, Việt Nam hy sinh một phần nhỏ tăng trưởng để cải thiện đáng kể công bằng vùng và môi trường.

### b) Nghiệm thỏa hiệp TOPSIS có hợp lý không?
Nghiệm thỏa hiệp có **TOPSIS_compromise_score = 0,840491**, cao nhất trong tập nghiệm Pareto. Phương án này đạt **GDP_gain = 58.815,38**, **Inequality_MAD = 509,46**, **Emission = 89,49** và **CyberRisk_Net = -12.149,30**. So với nghiệm tăng trưởng cao nhất, GDP chỉ giảm khoảng **2,73%**, nhưng bất bình đẳng vùng giảm khoảng **47,43%**, còn phát thải giảm rất mạnh.

Cấu trúc phân bổ cũng hợp lý vì không dồn quá mức vào AI, mà ưu tiên **H - nhân lực số** và **D - chuyển đổi số doanh nghiệp**, đặc biệt ở các vùng yếu.

### c) Nghiệm tăng trưởng cao nhất hy sinh bao nhiêu về bao trùm và môi trường?
Nghiệm tăng trưởng cao nhất đạt **GDP_gain = 60.466,15**, cao hơn nghiệm thỏa hiệp **1.650,77**. Tuy nhiên, **Inequality_MAD tăng từ 509,46 lên 969,17**, cao hơn khoảng **90,23%**, và **Emission tăng từ 89,49 lên 1.867,75**, cao hơn khoảng **20,87 lần**.

### d) NSGA-II có thay thế được quyết định chính sách không?
Không. NSGA-II chỉ tạo ra tập phương án Pareto để nhìn thấy đánh đổi. Việc chọn nghiệm nào vẫn là quyết định chính trị - xã hội, phụ thuộc vào ưu tiên của Nhà nước, doanh nghiệp, địa phương và người dân.
""",
    "bai8": """
### a) Quỹ đạo tối ưu của K, D, AI, H có front-loaded hay back-loaded không?
Output Bài 8 cho thấy quỹ đạo tối ưu có tính **front-loaded đối với D và AI**. Năm 2026, tỷ trọng đầu tư vào D đạt **0,8825**, AI đạt **0,1175**. Giai đoạn 2028-2032, AI tăng rất mạnh, đạt **0,7996 năm 2032**. Đến năm 2035, cơ cấu trở về cân bằng khoảng **0,25** mỗi nhóm.

Cần diễn giải thận trọng vì K, D, AI, H có xu hướng giảm theo thời gian do đặc tả mô phỏng và khấu hao, không phải khuyến nghị thực tế để năng lực số suy giảm.

### b) Tỷ lệ đầu tư AI/H có ổn định không?
Không. H gần như bằng 0 đến 2034, trong khi AI tăng mạnh. Về chính sách, điều này cần phản biện: AI phải đi đồng thời với đào tạo nhân lực số, thậm chí ở vùng/ngành yếu thì nhân lực nên đi trước.

### c) Nếu ρ giảm từ 0,97 xuống 0,90 thì sao?
Với **ρ = 0,97**, welfare tối ưu đạt **47,8763**, cao hơn đầu tư đều (**47,7707**) và front-load giả định (**47,7513**). Nếu ρ thấp hơn, mô hình có thể ưu tiên ngắn hạn hơn và giảm đầu tư dài hạn vào AI, R&D, nhân lực.

### d) Cú sốc 2028 ảnh hưởng thế nào?
GDP năm 2028 giảm từ **355,60** xuống **327,16**. Welfare giảm từ **47,8763** xuống **47,7950**. Đến 2035, GDP shock đạt **281,59**, gần bằng không shock **281,72**. Mô hình phục hồi tốt, nhưng cú sốc còn đơn giản so với thực tế.
""",
    "bai9": """
### a) Ngành nào cần đầu tư đào tạo lại nhiều nhất?
Output Bài 9 phân bổ toàn bộ **30.000 tỷ** vào **x_H của Giáo dục-Đào tạo**, tạo **UpgradeJob = 1.650.000** và **NetJob = 1.650.000**. Điều này đúng về toán học vì ngành này có hiệu quả biên cao, nhưng chưa sát thực tế vì các ngành chế biến chế tạo, bán buôn-bán lẻ, tài chính-ngân hàng và logistics cũng cần đào tạo lại.

### b) Tài chính-Ngân hàng có risk 52% nhưng tạo việc làm mới cao, nên làm gì?
Ngành này có **risk = 52%** và **a1 = 45,8**. Chính sách phù hợp là **AI đi kèm tái đào tạo bắt buộc**, giúp chuyển lao động sang dữ liệu, kiểm soát rủi ro mô hình, an ninh mạng, tuân thủ và đạo đức AI.

### c) Có nên đầu tư AI vào Nông-Lâm-Thủy sản không?
Mô hình không chọn vì **a1 = 8,5** thấp. Tuy nhiên, nông nghiệp có **13,20 triệu lao động**, nên vẫn cần AI và số hóa quy mô phù hợp: truy xuất nguồn gốc, dự báo thời tiết, tưới tiêu thông minh, logistics lạnh, thương mại điện tử nông sản.

### d) Ràng buộc “tự động hóa không vượt năng lực đào tạo lại” là gì?
Ràng buộc là **DisplacedJobᵢ ≤ RetrainingCapacityᵢ**. Output cho thấy bài toán vẫn khả thi với ràng buộc không ngành nào mất quá 5% lao động, nhưng vì nghiệm không đầu tư AI nên DisplacedJob = 0. Cần bổ sung ràng buộc đầu tư tối thiểu vào ngành rủi ro cao.
""",
    "bai10": """
### a) SP đầu tư H nhiều hơn hay ít hơn?
First-stage dồn toàn bộ **65.000** vào **AI**. Second-stage dồn **15.000 vào D** ở kịch bản tốt và **15.000 vào H** ở kịch bản bi quan/khủng hoảng. Như vậy, H chưa được đầu tư trước, mà chỉ xuất hiện như công cụ thích nghi khi kịch bản xấu xảy ra.

### b) VSS dương nói lên điều gì? Output VSS = 0 thì sao?
VSS dương nghĩa là lời giải stochastic tốt hơn lời giải kỳ vọng. Output hiện có **SP_value = EEV_value = Wait-and-See_value = 98.575**, nên **VSS = 0** và **EVPI = 0**. Điều này không có nghĩa tư duy xác suất vô ích, mà cho thấy mô hình hiện tại chưa tạo đủ khác biệt giữa các kịch bản.

### c) Việt Nam có dưới đầu tư nhân lực số như hàng hóa bảo hiểm không?
Có rủi ro như vậy. Output cho thấy khi kịch bản xấu xảy ra, mô hình chuyển sang H. Chính sách thực tế nên đầu tư nhân lực số từ trước, không chỉ phản ứng sau cú sốc.
""",
    "bai11": """
### a) GDP thấp, D thấp, U cao thì π*(s) chọn gì?
Ở state **LowGDP_LowD_LowAI_HighU = [0, 0, 0, 2]**, mô hình chọn **Truyền thống**, nhưng **Q-value = 0**, cho thấy agent chưa học đủ ở trạng thái này. Trong thực tế, quick win nên là số hóa dịch vụ công, hỗ trợ SME chuyển đổi số và đào tạo lại ngắn hạn.

### b) GDP cao, AI cao, U thấp thì chọn gì?
Ở state **HighGDP_HighD_HighAI_LowU = [2,2,2,0]**, mô hình cũng chọn **Truyền thống**, **Q-value = 0**. Có thể hiểu một phần là consolidation, nhưng không nên xem là khuyến nghị mạnh. Kết quả đáng tin hơn là state VN_2026 chọn **Số hóa nhanh** với **Q-value = 15,2896**.

### c) Q-learning có tốt hơn chính sách cố định không?
Có. **Q_learning_policy = 8,2600**, cao hơn **Always_balanced = 7,4861**, **Always_AI_led = 7,5729** và **Random = 7,5335**.

### d) Tích hợp π* vào chính sách thế nào?
Chỉ dùng Q-learning như **hệ thống khuyến nghị**, không tự động ra quyết định. Cần chuyên gia kiểm định, hội đồng chính sách đánh giá và cơ quan có thẩm quyền quyết định.
""",
    "bai12": """
### a) Kịch bản nào có GDP_index 2030 cao nhất?
Output cho thấy **S3_AI_dan_dat** cao nhất với **GDP_index = 380,7220**. S2_So_hoa_nhanh đứng thứ hai với **380,3790**, S5_Toi_uu_can_bang đứng thứ ba với **379,4473**.

### b) Kịch bản nào phù hợp nhất với thực tiễn Việt Nam?
Nếu chỉ xét GDP, S3 tốt nhất. Nhưng xét năng lực thực thi, **S5_Toi_uu_can_bang** hoặc **S2_So_hoa_nhanh** phù hợp hơn vì cân bằng giữa D, AI và H.

### c) Cảnh báo rủi ro nói gì?
Cả 5 kịch bản đều có **cyber_risk = Trung bình**, **digital_gap_risk = Cao**, **human_capital_status = Thiếu**. Điều này cho thấy dù chọn kịch bản nào, Việt Nam vẫn cần giảm khoảng cách số, đào tạo nhân lực và bảo vệ dữ liệu.

### d) Dashboard có đáp ứng hỗ trợ ra quyết định không?
Có về cấu trúc: có dự báo, phân bổ, lao động, bất định, Q-learning và so sánh kịch bản. Nên bổ sung chức năng chỉnh trọng số, giải thích biểu đồ và giới hạn mô hình.

### e) Khuyến nghị tổng hợp là gì?
Không chọn cực đoan truyền thống hoặc AI dẫn dắt tuyệt đối. Nên chọn **S5_Toi_uu_can_bang** làm kịch bản khuyến nghị, còn S3_AI_dan_dat là kịch bản tăng trưởng cao nhưng rủi ro hấp thụ lớn hơn.
""",
}

# =========================
# SIDEBAR
# =========================
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
        "Bài 12 - Tổng hợp kịch bản",
    ],
)

# =========================
# PAGES
# =========================
if page == "Tổng quan":
    section_title(
        "AIDEOM-VN Dashboard",
        "Dashboard tổng hợp kết quả mô hình ra quyết định phát triển kinh tế Việt Nam trong kỷ nguyên AI",
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Số bài đã hoàn thiện", "12/12")
    col2.metric("Nhóm mô hình", "LP, MIP, TOPSIS, NSGA-II, RL")
    col3.metric("Dữ liệu", "Việt Nam 2020-2035")
    st.write(
        """
        Dashboard trình bày kết quả định lượng, bảng, biểu đồ và thảo luận chính sách cho 12 bài.
        Các kết quả được đọc từ 3 file Excel trong thư mục `data`.
        """
    )

elif page == "Bài 1 - Cobb-Douglas":
    section_title("Bài 1. Hàm sản xuất Cobb-Douglas mở rộng", "Phân tích TFP, dự báo GDP và đóng góp tăng trưởng")
    df = main["Bai1_TFP"]
    decomp = main["Bai1_Growth_Decomp"]
    forecast = main["Bai1_Forecast2030"]
    tab1, tab2, tab3, tab4 = st.tabs(["Kết quả TFP", "Phân rã tăng trưởng", "Dự báo 2030", "Thảo luận chính sách"])
    with tab1:
        show_df(df, "TFP và GDP dự báo")
        st.plotly_chart(px.line(df, x="year", y="TFP_A", markers=True, title="Xu hướng TFP A_t"), use_container_width=True)
        compare = df[["year", "GDP_trillion_VND", "Y_hat"]].melt(id_vars="year", var_name="Chỉ tiêu", value_name="GDP")
        st.plotly_chart(px.line(compare, x="year", y="GDP", color="Chỉ tiêu", markers=True, title="GDP thực tế và dự báo"), use_container_width=True)
    with tab2:
        show_df(decomp, "Phân rã tăng trưởng")
        fig = px.bar(decomp, x="factor", y="share_of_growth_pct", text="share_of_growth_pct", title="Tỷ trọng đóng góp tăng trưởng")
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with tab3:
        show_df(forecast, "Dự báo GDP 2030")
    with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai1"])

elif page == "Bài 2 - LP ngân sách":
    section_title("Bài 2. Phân bổ ngân sách số bằng quy hoạch tuyến tính", "Tối ưu 4 hạng mục: hạ tầng số, AI, nhân lực số và R&D")
    base = main["Bai2_Base"]
    duals = main["Bai2_Duals"]
    sens = main["Bai2_Sensitivity"]
    h30 = supp["Bai2_H30"]
    tab1, tab2, tab3, tab4 = st.tabs(["Nghiệm tối ưu", "Shadow price", "Độ nhạy ngân sách", "Thảo luận chính sách"])
    with tab1:
        show_df(base, "Nghiệm tối ưu")
        alloc = base[["x_I", "x_AI", "x_H", "x_RD"]].T.reset_index()
        alloc.columns = ["Hạng mục", "Ngân sách"]
        st.plotly_chart(px.bar(alloc, x="Hạng mục", y="Ngân sách", text="Ngân sách", title="Phân bổ ngân sách tối ưu"), use_container_width=True)
        show_df(h30, "Trường hợp ưu tiên nhân lực số x_H ≥ 30")
    with tab2:
        show_df(duals, "Shadow price")
    with tab3:
        show_df(sens, "Độ nhạy ngân sách")
        st.plotly_chart(px.line(sens, x="B", y="Z", markers=True, title="Đường cong Z*(B)"), use_container_width=True)
    with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai2"])

elif page == "Bài 3 - Ưu tiên ngành":
    section_title("Bài 3. Chỉ số ưu tiên ngành", "Xếp hạng 10 ngành theo Priority Index")
    ranking = main["Bai3_Ranking"]
    sens = main["Bai3_AI_Sensitivity"]
    policy = main["Bai3_Policy_Weights"]
    tab1, tab2, tab3, tab4 = st.tabs(["Xếp hạng ngành", "Độ nhạy AI", "So sánh trọng số", "Thảo luận chính sách"])
    with tab1:
        show_df(ranking)
        fig = px.bar(ranking, x="sector_name_vi", y="Priority", text="Priority", title="Xếp hạng chỉ số ưu tiên ngành")
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        show_df(sens)
    with tab3:
        show_df(policy)
    with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai3"])

elif page == "Bài 4 - Phân bổ vùng":
    section_title("Bài 4. Phân bổ ngân sách số theo vùng", "So sánh có và không có ràng buộc công bằng")
    fair = main["Bai4_With_Fairness"]
    nofair = main["Bai4_No_Fairness"]
    tab1, tab2, tab3 = st.tabs(["Có công bằng", "Không công bằng", "Thảo luận chính sách"])
    with tab1:
        show_df(fair)
        st.plotly_chart(px.imshow(fair.set_index("region_name")[["I", "D", "AI", "H"]], text_auto=True, aspect="auto", title="Có ràng buộc công bằng"), use_container_width=True)
    with tab2:
        show_df(nofair)
        st.plotly_chart(px.imshow(nofair.set_index("region_name")[["I", "D", "AI", "H"]], text_auto=True, aspect="auto", title="Không có ràng buộc công bằng"), use_container_width=True)
    with tab3:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai4"])

elif page == "Bài 5 - Lựa chọn dự án":
    section_title("Bài 5. MIP lựa chọn dự án chuyển đổi số", "Tối ưu danh mục dự án trong điều kiện ràng buộc")
    base = main["Bai5_Selected_80k"]
    budget100 = main["Bai5_Selected_100k"]
    risk = main["Bai5_Risk_Adjusted"]
    force = supp["Bai5_Force_P1_P2"]
    no_p14 = supp["Bai5_No_P14_Required"]
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Ngân sách 80k", "Ngân sách 100k", "Bắt buộc P1 & P2", "Rủi ro dự án", "Không bắt buộc P14", "Thảo luận chính sách"])
    with tab1:
        show_df(base)
        fig = px.bar(base, x="name", y=["cost", "benefit"], barmode="group", title="Chi phí và lợi ích các dự án được chọn")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        show_df(budget100)
    with tab3:
        show_df(force)
    with tab4:
        show_df(risk)
    with tab5:
        show_df(no_p14)
    with tab6:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai5"])

elif page == "Bài 6 - TOPSIS vùng":
    section_title("Bài 6. TOPSIS xếp hạng vùng ưu tiên AI", "So sánh trọng số chuyên gia, Entropy và độ nhạy AI")
    topsis = main["Bai6_TOPSIS"]
    sens = main["Bai6_AI_Sensitivity"]
    tab1, tab2, tab3 = st.tabs(["Kết quả TOPSIS", "Độ nhạy AI", "Thảo luận chính sách"])
    with tab1:
        show_df(topsis)
        plot_df = topsis[["region_name_vi", "TOPSIS_expert", "TOPSIS_entropy"]].melt(id_vars="region_name_vi", var_name="Phương pháp", value_name="Điểm TOPSIS")
        fig = px.bar(plot_df, x="region_name_vi", y="Điểm TOPSIS", color="Phương pháp", barmode="group", title="So sánh TOPSIS")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        show_df(sens)
    with tab3:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai6"])

elif page == "Bài 7 - Pareto NSGA-II":
    section_title("Bài 7. Tối ưu đa mục tiêu Pareto với NSGA-II", "Đánh đổi giữa tăng trưởng, công bằng vùng, phát thải và rủi ro dữ liệu")
    pareto = adv["Bai7_Pareto"]
    compromise = adv["Bai7_Compromise"]
    allocation = adv["Bai7_Allocation"]
    tab1, tab2, tab3, tab4 = st.tabs(["Biên Pareto", "Nghiệm thỏa hiệp", "Phân bổ ngân sách", "Thảo luận chính sách"])
    with tab1:
        show_df(pareto, "Tập nghiệm Pareto")
        fig = px.scatter_3d(pareto, x="GDP_gain", y="Inequality_MAD", z="Emission", color="TOPSIS_compromise_score", title="Biên Pareto 3D")
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        show_df(compromise, "Nghiệm thỏa hiệp theo TOPSIS")
        row = compromise.iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("GDP gain", f"{row['GDP_gain']:,.2f}")
        col2.metric("Inequality MAD", f"{row['Inequality_MAD']:,.2f}")
        col3.metric("Emission", f"{row['Emission']:,.2f}")
        col4.metric("TOPSIS score", f"{row['TOPSIS_compromise_score']:.3f}")
    with tab3:
        show_df(allocation, "Phân bổ ngân sách tại nghiệm thỏa hiệp")
        st.plotly_chart(px.imshow(allocation.set_index("region")[["I", "D", "AI", "H"]], text_auto=True, aspect="auto", title="Heatmap phân bổ"), use_container_width=True)
        st.plotly_chart(px.bar(allocation, x="region", y=["I", "D", "AI", "H"], barmode="stack", title="Cơ cấu phân bổ ngân sách"), use_container_width=True)
    with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai7"])

elif page == "Bài 8 - Tối ưu động":
    section_title("Bài 8. Tối ưu động phân bổ vốn 2026-2035", "Quỹ đạo K, D, AI, H, GDP và tiêu dùng")
    opt = adv["Bai8_Optimal_Path"]
    shock = adv["Bai8_Shock_2028"]
    compare = adv["Bai8_Strategy_Compare"]
    tab1, tab2, tab3, tab4 = st.tabs(["Quỹ đạo tối ưu", "Cú sốc 2028", "So sánh chiến lược", "Thảo luận chính sách"])
    with tab1:
        show_df(opt, "Quỹ đạo tối ưu 2026-2035")
        st.plotly_chart(px.line(opt, x="year", y=["K", "D", "AI", "H"], markers=True, title="Quỹ đạo K, D, AI, H"), use_container_width=True)
        st.plotly_chart(px.line(opt, x="year", y=["Y", "C"], markers=True, title="Sản lượng Y và tiêu dùng C"), use_container_width=True)
        st.plotly_chart(px.line(opt, x="year", y=["share_K", "share_D", "share_AI", "share_H"], markers=True, title="Tỷ trọng đầu tư tối ưu"), use_container_width=True)
    with tab2:
        show_df(shock, "Kịch bản có cú sốc năm 2028")
        shock_compare = opt[["year", "Y", "C"]].rename(columns={"Y": "Y_no_shock", "C": "C_no_shock"}).copy()
        shock_compare["Y_shock"] = shock["Y"]
        shock_compare["C_shock"] = shock["C"]
        st.plotly_chart(px.line(shock_compare, x="year", y=["Y_no_shock", "Y_shock"], markers=True, title="Sản lượng: không sốc và có sốc"), use_container_width=True)
        st.plotly_chart(px.line(shock_compare, x="year", y=["C_no_shock", "C_shock"], markers=True, title="Tiêu dùng: không sốc và có sốc"), use_container_width=True)
    with tab3:
        show_df(compare, "So sánh chiến lược")
        fig = px.bar(compare, x="strategy", y="welfare", text="welfare", title="Welfare theo chiến lược")
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        fig2 = px.bar(compare, x="strategy", y="GDP_2035", text="GDP_2035", title="GDP 2035 theo chiến lược")
        fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)
    with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai8"])

elif page == "Bài 9 - Lao động và AI":
    section_title("Bài 9. Tác động AI tới thị trường lao động Việt Nam", "Tối ưu đầu tư AI và đào tạo lại để bảo đảm NetJob")
    labor = adv["Bai9_Labor_Result"]
    threshold = adv["Bai9_Threshold"]
    feasibility = adv["Bai9_Feasibility"]
    sankey = adv["Bai9_Sankey"]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Kết quả lao động", "Ngưỡng đào tạo", "Tính khả thi", "Sankey lao động", "Thảo luận chính sách"])
    with tab1:
        show_df(labor, "NetJob theo ngành")
        fig = px.bar(labor, x="sector", y=["NewJob", "UpgradeJob", "DisplacedJob", "NetJob"], barmode="group", title="Việc làm mới, nâng cấp, dịch chuyển và NetJob")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        fig2 = px.bar(labor, x="sector", y=["x_AI", "x_H"], barmode="group", title="Đầu tư AI và đào tạo lại")
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
    with tab2:
        show_df(threshold, "Ngưỡng đào tạo")
    with tab3:
        show_df(feasibility, "Tính khả thi khi thêm ràng buộc an sinh")
    with tab4:
        show_df(sankey, "Luồng dịch chuyển lao động nhóm dễ tổn thương")
        labels = list(pd.unique(sankey[["source", "target"]].values.ravel()))
        label_to_id = {label: i for i, label in enumerate(labels)}
        fig = go.Figure(data=[go.Sankey(
            node=dict(pad=15, thickness=20, label=labels),
            link=dict(source=sankey["source"].map(label_to_id), target=sankey["target"].map(label_to_id), value=sankey["value"]),
        )])
        fig.update_layout(title_text="Sankey: luồng dịch chuyển lao động", font_size=12)
        st.plotly_chart(fig, use_container_width=True)
    with tab5:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai9"])

elif page == "Bài 10 - Stochastic LP":
    section_title("Bài 10. Quy hoạch ngẫu nhiên hai giai đoạn", "First-stage, second-stage, wait-and-see, VSS và EVPI")
    first = adv["Bai10_First_Stage"]
    second = adv["Bai10_Second_Stage"]
    waitsee = adv["Bai10_Wait_See"]
    summary = adv["Bai10_VSS_EVPI"]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["First-stage", "Second-stage", "Wait-and-see", "VSS và EVPI", "Thảo luận chính sách"])
    with tab1:
        show_df(first, "Quyết định first-stage")
        fig = px.bar(first, x="item", y="first_stage_x", text="first_stage_x", title="Phân bổ first-stage")
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        show_df(second, "Second-stage theo kịch bản")
        second_melt = second.melt(id_vars="scenario", var_name="item", value_name="second_stage_value")
        st.plotly_chart(px.bar(second_melt, x="scenario", y="second_stage_value", color="item", barmode="group", title="Second-stage theo kịch bản"), use_container_width=True)
    with tab3:
        show_df(waitsee, "Wait-and-see")
        fig = px.bar(waitsee, x="scenario", y="scenario_value", text="scenario_value", title="Giá trị từng kịch bản")
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with tab4:
        show_df(summary, "VSS và EVPI")
        fig = px.bar(summary, x="metric", y="value", text="value", title="SP, EEV, Wait-and-see, VSS, EVPI")
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with tab5:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai10"])

elif page == "Bài 11 - Q-learning":
    section_title("Bài 11. Q-learning cho chính sách kinh tế thích nghi", "So sánh chính sách học tăng cường với chính sách cố định")
    policy = adv["Bai11_Q_Policy"]
    compare = adv["Bai11_Policy_Compare"]
    curve = adv["Bai11_Learning_Curve"]
    tab1, tab2, tab3, tab4 = st.tabs(["Chính sách học được", "So sánh chính sách", "Learning curve", "Thảo luận chính sách"])
    with tab1:
        show_df(policy, "Chính sách tối ưu theo trạng thái")
    with tab2:
        show_df(compare, "So sánh phần thưởng")
        fig = px.bar(compare, x="policy", y="avg_total_reward", error_y="std_total_reward", text="avg_total_reward", title="So sánh avg_total_reward")
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with tab3:
        show_df(curve.tail(500), "Learning curve, 500 dòng cuối")
        st.plotly_chart(px.line(curve, x="episode", y="rolling_reward_200", title="Rolling reward 200 episodes"), use_container_width=True)
    with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai11"])

elif page == "Bài 12 - Tổng hợp kịch bản":
    section_title("Bài 12. Dashboard tích hợp AIDEOM-VN", "So sánh 5 kịch bản chính sách đến năm 2030")
    path = adv["Bai12_Scenario_Path"]
    kpi = adv["Bai12_KPI_2030"]
    risk = adv["Bai12_Risk_Warning"]
    tab1, tab2, tab3, tab4 = st.tabs(["Đường kịch bản", "KPI năm 2030", "Cảnh báo rủi ro", "Thảo luận chính sách"])
    with tab1:
        show_df(path, "Đường phát triển theo kịch bản")
        st.plotly_chart(px.line(path, x="year", y="GDP_index", color="scenario", markers=True, title="GDP index theo kịch bản"), use_container_width=True)
        st.plotly_chart(px.line(path, x="year", y="D", color="scenario", markers=True, title="Mức độ số hóa D"), use_container_width=True)
        st.plotly_chart(px.line(path, x="year", y="AI", color="scenario", markers=True, title="Năng lực AI"), use_container_width=True)
    with tab2:
        show_df(kpi, "KPI năm 2030")
        fig = px.bar(kpi, x="scenario", y="GDP_index", text="GDP_index", title="GDP index 2030")
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        fig2 = px.bar(kpi, x="scenario", y=["D", "AI", "H", "A"], barmode="group", title="D, AI, H, A năm 2030")
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
    with tab3:
        show_df(risk, "Cảnh báo rủi ro theo kịch bản")
    with tab4:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai12"])
