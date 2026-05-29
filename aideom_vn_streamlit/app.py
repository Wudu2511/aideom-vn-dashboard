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
### a) TFP của Việt Nam có xu hướng tăng hay giảm trong giai đoạn 2020-2025?
Dựa trên output mô hình, TFP A_t tăng từ **27,75 năm 2020** lên **34,91 năm 2025**. Trong phân rã tăng trưởng, **TFP đóng góp 49,08%**, cao hơn vốn K với **31,78%**. Điều này cho thấy chất lượng tăng trưởng trong mô hình có cải thiện, không chỉ dựa vào mở rộng vốn và lao động.

### b) Trong D, AI, H, yếu tố nào đóng góp nhiều nhất?
Trong ba yếu tố mới, **D - mức độ số hóa** đóng góp lớn nhất, khoảng **10,37%**; tiếp theo là **AI 6,24%** và **H 2,87%**. Điều này phù hợp với giai đoạn Việt Nam thúc đẩy kinh tế số, dịch vụ công trực tuyến, thương mại điện tử và chuyển đổi số doanh nghiệp.

### c) Mục tiêu kinh tế số đạt 30% GDP vào 2030 có khả thi không?
Kịch bản mô phỏng cho thấy nếu D đạt **30%**, AI đạt **100 nghìn doanh nghiệp số**, H đạt **35%**, K tăng **6%/năm** và TFP tăng **1,2%/năm**, GDP 2030 đạt khoảng **16.362,93 nghìn tỷ VND**. Mục tiêu này khả thi về mặt mô hình, nhưng cần hạ tầng số, nhân lực số, dữ liệu mở, an ninh mạng và chính sách thu hẹp khoảng cách số.
""",
    "bai2": """
### a) Khi ngân sách tăng thêm 1 nghìn tỷ VND, GDP kỳ vọng tăng thêm bao nhiêu?
Output cho thấy nghiệm tối ưu ban đầu: hạ tầng số **25**, AI và dữ liệu **15**, nhân lực số **20**, R&D **40** nghìn tỷ VND. Giá trị mục tiêu **Z* = 112,25**. Shadow price ngân sách tổng bằng **1,35**, tức tăng thêm 1 nghìn tỷ VND ngân sách làm GDP kỳ vọng tăng khoảng **1,35 nghìn tỷ VND** trong vùng nghiệm hiện tại.

### b) Vì sao R&D có hệ số cao nhất nhưng sàn tối thiểu thấp?
R&D nhận **40 nghìn tỷ**, cao hơn sàn **10 nghìn tỷ** vì có hệ số tác động **1,35**. Sàn thấp vẫn hợp lý vì R&D có độ trễ dài, rủi ro cao và phụ thuộc năng lực hấp thụ của doanh nghiệp, viện nghiên cứu và thị trường.

### c) Nếu ưu tiên nhân lực số với x_H ≥ 30 thì sao?
Bài toán vẫn khả thi. Z* giảm từ **112,25** xuống **108,25**, tức giảm **4,00 nghìn tỷ GDP kỳ vọng**. Đây là chi phí cơ hội ngắn hạn, nhưng nhân lực số là điều kiện để hấp thụ AI, vận hành hạ tầng số và triển khai R&D.

### d) Tỷ lệ 35% AI + R&D có khả thi không?
Trong nghiệm tối ưu, AI + R&D = **55 nghìn tỷ**, chiếm **55% ngân sách**, cao hơn ràng buộc 35%. Tuy nhiên, trong thực tế cần cân đối với giao thông, y tế, giáo dục, an sinh xã hội và chuyển đổi xanh.
""",
    "bai3": """
### a) Ba ngành nào nên ưu tiên?
Top 3 theo Priority là **Thông tin - Truyền thông - CNTT** (**0,730**), **Công nghiệp chế biến chế tạo** (**0,652**) và **Tài chính - Ngân hàng - Bảo hiểm** (**0,533**). Đây là các ngành có năng lực số, dữ liệu, xuất khẩu hoặc tác động lan tỏa lớn.

### b) Vì sao Khai khoáng không thuộc nhóm ưu tiên?
Khai khoáng xếp cuối với **Priority = 0,178**. Năng suất cao không đủ để trở thành ngành ưu tiên nếu tăng trưởng, lan tỏa, việc làm và AI readiness thấp hoặc rủi ro tự động hóa cao.

### c) Bộ trọng số nên do ai quyết định?
Khi đổi từ trọng số tăng trưởng sang bao trùm, Nông - Lâm - Thủy sản tăng mạnh trong thứ hạng. Vì vậy, trọng số không chỉ là kỹ thuật mà phản ánh lựa chọn giá trị chính sách. Nên kết hợp chuyên gia, nhà hoạch định chính sách, doanh nghiệp, địa phương và đối thoại công khai.
""",
    "bai4": """
### a) Nếu bỏ ràng buộc công bằng, vốn chảy về đâu?
Không có công bằng, vốn tập trung vào vùng có hệ số tác động cao như **Đồng bằng sông Hồng** và **Đông Nam Bộ**, đặc biệt cho AI. Điều này tối đa hóa hiệu quả ngắn hạn nhưng có thể làm tăng khoảng cách số.

### b) Công bằng vùng làm giảm Z* bao nhiêu?
Có công bằng, Z* khoảng **52.485**; bỏ công bằng, Z* khoảng **68.750**. Chi phí công bằng là **16.265**, tương đương khoảng **23,66%**. Mức giảm lớn nhưng có thể chấp nhận nếu mục tiêu là phát triển bao trùm.

### c) Tây Nguyên nên đầu tư AI hay H/I trước?
Output cho thấy Tây Nguyên không nhận AI trực tiếp, mà nhận D hoặc H. Điều này hàm ý vùng có nền tảng số thấp nên ưu tiên hạ tầng số, chuyển đổi số doanh nghiệp và nhân lực trước khi đầu tư AI quy mô lớn.
""",
    "bai5": """
### a) Vì sao chọn P15 Open Data dù quy mô nhỏ?
P15 được chọn vì chi phí thấp (**1.500 tỷ**) và lợi ích tương đối tốt (**3.800 tỷ**). Dữ liệu mở là nền tảng cho chính phủ số, AI và đổi mới sáng tạo.

### b) P14 an ninh mạng có làm giảm Z* không?
Có. Khi bắt buộc P14, tổng lợi ích là **115.400 tỷ**; bỏ bắt buộc P14, tổng lợi ích là **116.300 tỷ**. Mức giảm khoảng **900 tỷ**, nhưng P14 vẫn hợp lý vì an ninh mạng là điều kiện nền tảng của chuyển đổi số.

### c) Bắt buộc chọn cả P1 và P2 có khả thi không?
Có. Danh mục chọn 8 dự án, tổng chi phí **59.300 tỷ**, lợi ích **113.300 tỷ**. So với nghiệm cơ sở **115.400 tỷ**, giảm **2.100 tỷ** do chi phí dự phòng hạ tầng dữ liệu.

### d) Nới ngân sách lên 100.000 tỷ có đổi danh mục không?
Không. Điều này cho thấy ngân sách tổng không phải ràng buộc duy nhất; ngân sách năm 1-2, ràng buộc dự án, nhân lực và an ninh mạng cũng giới hạn danh mục.

### e) Khi xét rủi ro hoàn thành, danh mục thay đổi thế nào?
Danh mục chuyển sang các dự án có rủi ro thực thi thấp hơn. Tổng lợi ích kỳ vọng còn **91.285 tỷ**, cho thấy không nên chỉ nhìn NPV danh nghĩa mà cần xét xác suất hoàn thành.
""",
    "bai6": """
### a) Vùng nào dẫn đầu TOPSIS?
Theo trọng số chuyên gia, **Đông Nam Bộ** đứng đầu với **0,940**, **Đồng bằng sông Hồng** đứng thứ hai với **0,898**. Hai vùng này có GRDP/người, FDI, AI readiness, hạ tầng số và nhân lực tốt.

### b) Dùng Entropy có thay đổi thứ hạng lớn không?
Không. Thứ hạng tổng thể vẫn ổn định. Điều này cho thấy khoảng cách nền tảng số giữa vùng mạnh và vùng yếu khá rõ.

### c) Nếu AI Readiness và Internet penetration tương quan cao thì sao?
TOPSIS có thể đếm trùng lợi thế số của vùng phát triển. Cần kiểm tra tương quan, gộp tiêu chí hoặc dùng PCA.

### d) Nếu xây 3 trung tâm AI lớn nên chọn vùng nào?
Theo TOPSIS và độ nhạy, Top 3 là **Đông Nam Bộ**, **Đồng bằng sông Hồng**, **Bắc Trung Bộ và duyên hải miền Trung**. Tuy nhiên cần xét thêm an ninh dữ liệu, địa - chính trị, năng lượng và rủi ro thiên tai.
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
