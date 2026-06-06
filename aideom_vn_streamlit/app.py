import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from io import BytesIO

# ============================================================
# AIDEOM-VN STREAMLIT APP - HIỂN THỊ THEO TỪNG BÀI 1-12
# ============================================================

st.set_page_config(
    page_title="AIDEOM-VN | Mô hình ra quyết định",
    page_icon="🇻🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# STYLE
# ============================================================
st.markdown("""
<style>
html, body, .stApp, .stMarkdown, .stText, .stDataFrame {
    font-family: "Times New Roman", Times, serif !important;
    font-size: 15px;
}
.stApp {
    background: linear-gradient(135deg, #F8FBFF 0%, #EAF3FF 100%);
    color: #1F2933;
}
.block-container {padding-top: 1.4rem; padding-bottom: 2.5rem; max-width: 1380px;}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1F3A 0%, #123B62 100%);
    border-right: 1px solid rgba(255,255,255,0.14);
}
section[data-testid="stSidebar"] * {color: #FFFFFF !important;}
section[data-testid="stSidebar"] label {font-size: 14px !important; font-weight: 700 !important;}
div[role="radiogroup"] label {
    padding: 8px 10px; border-radius: 11px; margin-bottom: 4px; font-size: 14px !important;
}
div[role="radiogroup"] label:hover {background: rgba(255,255,255,0.12);}
h1 {color:#0B1F3A; font-weight:800; font-size:27px !important; letter-spacing:-0.2px;}
h2 {color:#123B62; font-weight:800; font-size:22px !important;}
h3 {color:#123B62; font-weight:800; font-size:19px !important;}
h4 {color:#123B62; font-weight:800; font-size:17px !important;}
.stMarkdown p, .stMarkdown li {font-size:15px; line-height:1.62; color:#1F2933;}
.title-card {
    background:#FFFFFF; padding:20px 24px; border-radius:18px; margin-bottom:18px;
    box-shadow:0 8px 24px rgba(16,37,66,.08); border:1px solid #E5E7EB; border-left:6px solid #2F80ED;
}
.title-card h1 {margin:0 0 8px 0; color:#0B1F3A; font-size:27px !important; line-height:1.25;}
.title-card p {margin:0; color:#5B6B82; font-size:15px; line-height:1.55; text-align:left;}
.info-card, .metric-card, .mini-card {
    background:#FFFFFF; padding:16px 18px; border-radius:16px; border:1px solid #E5E7EB;
    box-shadow:0 6px 18px rgba(16,37,66,.07); margin-bottom:14px;
}
.info-card {border-left:5px solid #2F80ED;}
.info-card h4, .mini-card h4 {margin:0 0 8px 0; color:#123B62;}
.info-card p, .mini-card p {margin:0; color:#334155; text-align:left;}
.badge {
    display:inline-block; padding:5px 10px; border-radius:999px; background:#EAF3FF; color:#123B62;
    font-weight:700; font-size:13px; margin:3px 4px 3px 0; border:1px solid #CFE4FF;
}
.caption-text {color:#64748B; font-size:14px; margin-top:-4px; margin-bottom:12px;}
div[data-testid="stMetric"] {
    background:#FFFFFF; padding:14px 16px; border-radius:16px; box-shadow:0 6px 18px rgba(16,37,66,.07);
    border:1px solid #E5E7EB;
}
div[data-testid="stMetricLabel"] {font-size:14px; font-weight:700; color:#64748B;}
div[data-testid="stMetricValue"] {font-size:23px; font-weight:800; color:#0B1F3A;}
button[data-baseweb="tab"] {
    font-size:14px; font-weight:700; background-color:#FFFFFF; border-radius:12px 12px 0 0;
    padding:8px 14px; color:#123B62; border:1px solid #E5E7EB;
}
button[data-baseweb="tab"][aria-selected="true"] {color:#FFFFFF !important; background-color:#2F80ED !important; border-color:#2F80ED !important;}
div[data-testid="stDataFrame"] {
    border-radius:15px; overflow:hidden; box-shadow:0 5px 16px rgba(16,37,66,.08);
    border:1px solid #E5E7EB; background:white; font-size:14px !important;
}
div[data-testid="stPlotlyChart"] {
    background:#FFFFFF; padding:12px; border-radius:16px; box-shadow:0 5px 16px rgba(16,37,66,.08);
    border:1px solid #E5E7EB; margin-top:10px; margin-bottom:18px;
}
div[data-testid="stAlert"] {border-radius:13px; font-size:15px; line-height:1.6;}
.stDownloadButton > button, .stButton > button {
    background-color:#2F80ED; color:#FFFFFF; border-radius:11px; border:none; padding:8px 18px;
    font-weight:700; font-size:14px; box-shadow:0 4px 12px rgba(47,128,237,.25);
}
.stDownloadButton > button:hover, .stButton > button:hover {background-color:#1C64C7; color:#FFFFFF;}
.streamlit-expanderHeader {font-size:15px; font-weight:700; color:#102542;}
.material-symbols-rounded,.material-symbols-outlined,.material-icons,span[class*="material"],i[class*="material"],button span[class*="material"],[data-testid="collapsedControl"] *,[data-testid="stToolbar"] * {
    font-family:"Material Symbols Rounded", "Material Icons" !important; font-weight:normal !important; font-style:normal !important;
    text-transform:none !important; letter-spacing:normal !important; line-height:1 !important;
    -webkit-font-feature-settings:"liga" !important; font-feature-settings:"liga" !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================
BASE_DIR = Path(__file__).parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "data"

FILE_CANDIDATES = {
    "main": [
        DATA_DIR / "ket_qua_bai_1_den_6.xlsx",
        DATA_DIR / "ket_qua_bai_1_den_6 (1).xlsx",
        BASE_DIR / "ket_qua_bai_1_den_6.xlsx",
        BASE_DIR / "ket_qua_bai_1_den_6 (1).xlsx",
    ],
    "supp": [
        DATA_DIR / "ket_qua_bo_sung_bai_2_5.xlsx",
        BASE_DIR / "ket_qua_bo_sung_bai_2_5.xlsx",
    ],
    "adv": [
        DATA_DIR / "ket_qua_bai_7_den_12.xlsx",
        BASE_DIR / "ket_qua_bai_7_den_12.xlsx",
    ],
}

def find_file(key: str) -> Path | None:
    for p in FILE_CANDIDATES[key]:
        if p.exists():
            return p
    return None

@st.cache_data(show_spinner=False)
def load_excel(path_str: str) -> dict[str, pd.DataFrame]:
    return pd.read_excel(path_str, sheet_name=None)

def load_all_data():
    paths = {k: find_file(k) for k in FILE_CANDIDATES}
    missing = [k for k, v in paths.items() if v is None]
    if missing:
        st.error("Thiếu file dữ liệu. Hãy đặt 3 file Excel vào thư mục `data/` rồi chạy lại app.")
        st.code("""data/
  ket_qua_bai_1_den_6.xlsx
  ket_qua_bo_sung_bai_2_5.xlsx
  ket_qua_bai_7_den_12.xlsx""")
        st.stop()
    return load_excel(str(paths["main"])), load_excel(str(paths["supp"])), load_excel(str(paths["adv"])), paths

main, supp, adv, DATA_PATHS = load_all_data()

# ============================================================
# DISCUSSIONS
# ============================================================
DISCUSSIONS = {
    "bai1": r"""# Bài 1. Hàm sản xuất Cobb-Douglas mở rộng với AI và số hóa

## a) TFP của Việt Nam có xu hướng tăng hay giảm trong giai đoạn 2020-2025? Điều đó nói lên gì về chất lượng tăng trưởng?

Theo output Bài 1, TFP của Việt Nam có xu hướng **tăng** trong giai đoạn 2020-2025. Cụ thể, TFP A\_t tăng từ khoảng **27,75 năm 2020** lên khoảng **34,91 năm 2025**. Điều này cho thấy tăng trưởng GDP không chỉ đến từ việc tăng vốn vật chất K và lao động L, mà còn đến từ việc nền kinh tế sử dụng các nguồn lực hiệu quả hơn.

Về mặt chất lượng tăng trưởng, xu hướng TFP tăng là tín hiệu tích cực. Nó cho thấy Việt Nam đang dần chuyển từ mô hình tăng trưởng dựa vào mở rộng đầu vào sang mô hình tăng trưởng dựa vào năng suất, công nghệ, số hóa và năng lực tổ chức sản xuất. Điều này phù hợp với thực tiễn khi năm 2024 GDP Việt Nam tăng **7,09%**, trong đó khu vực công nghiệp - xây dựng và dịch vụ tiếp tục đóng góp lớn vào tăng trưởng. ()

Tuy nhiên, cần lưu ý TFP trong bài là kết quả tính ngược từ hàm Cobb-Douglas với hệ số giả định. Vì vậy, đây là chỉ báo phân tích mô hình, không phải bằng chứng nhân quả tuyệt đối.

## b) Trong các yếu tố mới D, AI, H, yếu tố nào đóng góp nhiều nhất cho tăng trưởng giai đoạn vừa qua? Vì sao?

Theo output phân rã tăng trưởng, trong ba yếu tố mới **D, AI, H**, yếu tố **D - mức độ số hóa** đóng góp lớn nhất. D đóng góp khoảng **10,37%** vào tăng trưởng bình quân, cao hơn AI khoảng **6,24%** và H khoảng **2,87%**.

Điều này hợp lý vì trong giai đoạn 2020-2025, quá trình chuyển đổi số ở Việt Nam diễn ra rộng hơn so với việc ứng dụng AI chuyên sâu. Tỷ trọng kinh tế số/GDP trong dữ liệu tăng từ **12,0% năm 2020** lên **19,5% năm 2025**, trong khi AI và nhân lực số vẫn đang ở giai đoạn hình thành năng lực. Quyết định 749/QĐ-TTg cũng xác định chuyển đổi số quốc gia là định hướng lớn đến năm 2025, định hướng 2030; Quyết định 411/QĐ-TTg tiếp tục đặt mục tiêu phát triển kinh tế số và xã hội số. ()

Vì vậy, kết quả mô hình cho thấy: muốn AI tạo tác động lớn hơn, Việt Nam cần đầu tư đồng thời vào hạ tầng số, dữ liệu, kỹ năng số và nhân lực số.

## c) Mục tiêu Việt Nam đạt 30% kinh tế số/GDP vào 2030 có khả thi không nếu dựa trên mô hình này? Cần ràng buộc gì?

Theo output dự báo Bài 1, nếu đến năm 2030 D đạt **30%**, AI đạt **100 nghìn doanh nghiệp số**, H đạt **35%**, K tăng **6%/năm** và TFP tăng **1,2%/năm**, GDP dự báo năm 2030 đạt khoảng **16.362,93 nghìn tỷ VND**. Như vậy, xét riêng theo mô hình, mục tiêu kinh tế số đạt 30% GDP vào năm 2030 là **có khả thi**.

Tuy nhiên, mục tiêu này chỉ khả thi nếu có các ràng buộc đi kèm. Thứ nhất là ràng buộc về hạ tầng số, vì không thể tăng tỷ trọng kinh tế số nếu kết nối, dữ liệu và nền tảng số chưa đủ mạnh. Thứ hai là ràng buộc về nhân lực số, vì AI và số hóa không thể vận hành nếu thiếu kỹ sư, chuyên gia dữ liệu, chuyên gia an ninh mạng và lao động có kỹ năng số. Thứ ba là ràng buộc về công bằng vùng, để chuyển đổi số không chỉ tập trung ở Hà Nội, TP.HCM, Đông Nam Bộ và Đồng bằng sông Hồng. Nghị quyết 57-NQ/TW cũng nhấn mạnh khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số là đột phá phát triển quốc gia. ()

---""",

    "bai2": r"""# Bài 2. Phân bổ ngân sách đơn giản theo 4 hạng mục đầu tư số

## a) Khi ngân sách tổng tăng thêm 1 tỷ VND, GDP kỳ vọng tăng thêm bao nhiêu? Đây có phải là cận trên hợp lý của chi phí cơ hội của vốn công?

Trong mô hình Bài 2, đơn vị ngân sách là **nghìn tỷ VND**. Output cho thấy shadow price của ràng buộc ngân sách tổng là **1,35**. Nghĩa là nếu ngân sách tăng thêm **1 nghìn tỷ VND**, GDP kỳ vọng tăng thêm khoảng **1,35 nghìn tỷ VND**, trong vùng nghiệm tối ưu hiện tại.

Nếu quy đổi theo câu hỏi “1 tỷ VND”, thì về mặt tỷ lệ, GDP kỳ vọng tăng khoảng **1,35 tỷ VND**. Kết quả này cũng được xác nhận bởi phân tích độ nhạy: khi ngân sách tăng từ 100 lên 120, Z tăng từ **112,25** lên **139,25**; tức tăng 20 đơn vị ngân sách làm Z tăng 27, tương ứng hệ số **1,35**.

Tuy nhiên, đây chỉ là cận trên trong mô hình toán học. Trong thực tế, hiệu quả vốn công phụ thuộc vào năng lực giải ngân, chất lượng dự án, khả năng phối hợp liên ngành và năng lực hấp thụ của doanh nghiệp. Vì vậy, shadow price có ý nghĩa tham khảo cho chi phí cơ hội vốn công, nhưng không nên hiểu là cứ tăng ngân sách thì GDP thực tế chắc chắn tăng đúng 1,35 lần.

## b) Vì sao R&D có hệ số tác động cao nhất nhưng lại có ràng buộc tối thiểu thấp nhất?

Trong mô hình, R&D có hệ số tác động cao nhất là **1,35**, nhưng ràng buộc tối thiểu chỉ là **10**. Output cho thấy nghiệm tối ưu vẫn tự động phân bổ **40 nghìn tỷ VND** cho R&D, cao hơn rất nhiều mức tối thiểu. Điều này chứng tỏ ràng buộc tối thiểu thấp không có nghĩa là R&D không quan trọng; ngược lại, do hệ số tác động cao nên mô hình tự chọn đầu tư nhiều vào R&D sau khi đáp ứng các mức sàn của hạ tầng số, AI và nhân lực số.

Trong thực tiễn, R&D thường có độ trễ dài, rủi ro cao và khó đo lường kết quả ngay. Vì vậy, Nhà nước có thể đặt sàn thấp để bảo đảm tính khả thi ngân sách, nhưng vẫn cần cơ chế khuyến khích R&D qua quỹ đổi mới sáng tạo, đặt hàng nghiên cứu, hợp tác viện - trường - doanh nghiệp. Nghị quyết 57-NQ/TW cũng nhấn mạnh khoa học, công nghệ và đổi mới sáng tạo là động lực then chốt của phát triển. ()

## c) Trong thực tiễn quản lý, tỷ lệ 35% công nghệ chiến lược AI + R&D có khả thi không khi ngân sách nhà nước Việt Nam 2025 ưu tiên hạ tầng giao thông và an sinh xã hội?

Theo output, nghiệm tối ưu ban đầu phân bổ AI = **15** và R&D = **40**, tổng cộng **55 nghìn tỷ VND**, tương đương **55% tổng ngân sách**. Như vậy, trong mô hình, tỷ lệ tối thiểu 35% cho AI + R&D là khả thi và không phải ràng buộc chặt.

Nhưng trong thực tiễn quản lý ngân sách, tỷ lệ này cần được hiểu linh hoạt. Ngân sách nhà nước còn phải ưu tiên hạ tầng giao thông, y tế, giáo dục, an sinh xã hội, quốc phòng, phòng chống thiên tai và chuyển đổi xanh. Do đó, 35% cho AI + R&D có thể khả thi trong một chương trình chuyên biệt về kinh tế số, nhưng khó áp dụng cứng cho toàn bộ ngân sách nhà nước.

Cách hợp lý là coi 35% là **định hướng chiến lược**, không phải con số máy móc. Việt Nam nên ưu tiên AI và R&D, nhưng phải bảo đảm không làm suy giảm các nhiệm vụ xã hội thiết yếu.

---""",

    "bai3": r"""# Bài 3. Tính chỉ số ưu tiên ngành Priorityᵢ

## a) Theo kết quả, ba ngành nào nên được ưu tiên đẩy mạnh chuyển đổi số và AI trước? Kết quả này có phù hợp với Nghị quyết 57-NQ/TW không?

Theo output Bài 3, ba ngành có điểm Priority cao nhất là **Thông tin - Truyền thông - CNTT**, **Công nghiệp chế biến chế tạo**, và **Tài chính - Ngân hàng - Bảo hiểm**. Cụ thể, CNTT-Truyền thông đạt khoảng **0,730**, Công nghiệp chế biến chế tạo đạt khoảng **0,652**, và Tài chính - Ngân hàng đạt khoảng **0,533**.

Kết quả này phù hợp với thực tiễn. CNTT-Truyền thông là ngành nền tảng của chuyển đổi số; công nghiệp chế biến chế tạo có quy mô xuất khẩu và lao động lớn; tài chính - ngân hàng có dữ liệu lớn và khả năng ứng dụng AI cao trong tín dụng, thanh toán, quản trị rủi ro và chống gian lận.

Kết quả cũng phù hợp với Nghị quyết 57-NQ/TW, vì Nghị quyết xem khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số là đột phá quan trọng để phát triển lực lượng sản xuất hiện đại. ()

## b) Tại sao ngành Khai khoáng có năng suất rất cao nhưng vẫn không nằm trong nhóm ưu tiên?

Ngành Khai khoáng có năng suất lao động cao, nhưng trong output lại không nằm trong nhóm ưu tiên. Nguyên nhân là chỉ số Priority không chỉ xét năng suất, mà còn xét tăng trưởng, lan tỏa, xuất khẩu, việc làm, AI readiness và rủi ro tự động hóa.

Khai khoáng có năng suất cao nhưng quy mô việc làm nhỏ, mức lan tỏa công nghệ thấp, rủi ro môi trường cao và không phải ngành dẫn dắt chuyển đổi số toàn nền kinh tế. Trong khi đó, CNTT, chế biến chế tạo và tài chính có khả năng lan tỏa công nghệ rộng hơn, tác động đến nhiều doanh nghiệp và chuỗi giá trị hơn.

Vì vậy, khai khoáng vẫn cần số hóa để quản lý tài nguyên, an toàn lao động và giảm tác động môi trường, nhưng không nên là ngành ưu tiên hàng đầu nếu mục tiêu là lan tỏa AI và chuyển đổi số trên diện rộng.

## c) Bộ trọng số nên do ai quyết định: chuyên gia kỹ thuật, hội đồng chính sách, hay quy trình đối thoại công khai?

Bộ trọng số không nên chỉ do chuyên gia kỹ thuật quyết định. Output Bài 3 cho thấy khi thay đổi trọng số theo định hướng “tăng trưởng” hoặc “bao trùm”, thứ hạng ngành có thể thay đổi rõ. Ví dụ, nếu ưu tiên bao trùm và việc làm, các ngành có nhiều lao động như nông nghiệp có thể được xếp cao hơn; nếu ưu tiên tăng trưởng và xuất khẩu, công nghiệp và CNTT sẽ nổi bật hơn.

Vì vậy, bộ trọng số nên được quyết định bằng cách kết hợp ba nhóm: chuyên gia kỹ thuật, hội đồng chính sách và đối thoại công khai. Chuyên gia giúp bảo đảm tính đúng đắn của phương pháp. Hội đồng chính sách giúp gắn trọng số với mục tiêu phát triển quốc gia. Đối thoại công khai giúp tăng tính minh bạch và tính chính danh.

Nói ngắn gọn, trọng số là lựa chọn chính sách, không chỉ là bài toán kỹ thuật.

---""",

    "bai4": r"""# Bài 4. Quy hoạch tuyến tính phân bổ ngân sách số theo ngành - vùng

## a) Nếu bỏ ràng buộc công bằng, vốn sẽ chảy về vùng nào? Tại sao? Hậu quả xã hội dài hạn ra sao?

Theo output Bài 4, khi bỏ ràng buộc công bằng, vốn có xu hướng chảy mạnh về **Đồng bằng sông Hồng** và **Đông Nam Bộ**, đặc biệt vào các hạng mục có hệ số tác động cao như AI và chuyển đổi số doanh nghiệp. Đây là các vùng có nền tảng kinh tế, FDI, hạ tầng, doanh nghiệp và nhân lực tốt hơn.

Lý do là mô hình tối đa hóa GDP gain, nên vốn sẽ tự động đi đến nơi có hiệu quả biên cao nhất. Đông Nam Bộ và Đồng bằng sông Hồng có digital index và AI readiness cao hơn, vì vậy đầu tư vào đây tạo hiệu quả ngắn hạn lớn hơn.

Tuy nhiên, hậu quả xã hội dài hạn là khoảng cách số giữa vùng mạnh và vùng yếu có thể bị nới rộng. Các vùng như Tây Nguyên, Trung du miền núi phía Bắc và Đồng bằng sông Cửu Long có thể bị bỏ lại phía sau. Điều này đi ngược tinh thần phát triển xã hội số bao trùm trong Quyết định 411/QĐ-TTg. ()

## b) Ràng buộc trần ngân sách mỗi vùng C3 có thể coi như một “chính sách phân quyền”. Nó làm giảm Z\* bao nhiêu phần trăm? Mức giảm này có chấp nhận được không?

Theo output, khi có ràng buộc công bằng, Z\* đạt khoảng **52.485**. Khi bỏ ràng buộc công bằng, Z\* đạt khoảng **68.750**. Như vậy, ràng buộc công bằng làm giảm khoảng **16.265**, tương đương khoảng **23,66%** GDP gain.

Nếu chỉ xét hiệu quả kinh tế ngắn hạn, mức giảm này là lớn. Nhưng nếu xét mục tiêu phát triển bao trùm, mức giảm này có thể chấp nhận được. Chính sách công không chỉ tối đa hóa GDP, mà còn phải bảo đảm cơ hội phát triển giữa các vùng.

Có thể xem C3 là một chính sách phân quyền vì nó ngăn việc ngân sách bị hút hết vào một vài vùng mạnh. Nhờ đó, các vùng yếu vẫn có nguồn lực tối thiểu để phát triển hạ tầng số, nhân lực số và năng lực hấp thụ công nghệ.

## c) Tây Nguyên có sàn 5.000 tỷ nhưng hệ số AI rất thấp 0,45. Nên đầu tư AI hay tập trung H và I trước? Mô hình trả lời như thế nào?

Theo output, Tây Nguyên không nên ưu tiên AI ngay từ đầu. Khi có ràng buộc công bằng, mô hình chủ yếu phân bổ cho Tây Nguyên vào **D - chuyển đổi số** hoặc **H - nhân lực số**, thay vì AI. Điều này phù hợp vì hệ số AI của Tây Nguyên chỉ **0,45**, thấp nhất trong các vùng.

Về chính sách, Tây Nguyên nên tập trung vào hạ tầng số, kỹ năng số, dữ liệu cơ bản, chuyển đổi số doanh nghiệp nhỏ và dịch vụ công trước. Khi các nền tảng này đủ mạnh, đầu tư AI mới có khả năng tạo hiệu quả.

Nói cách khác, mô hình trả lời rằng: **không nên nhảy thẳng vào AI ở vùng có năng lực hấp thụ thấp**. Tây Nguyên cần H và I trước, AI sau.

---""",

    "bai5": r"""# Bài 5. Quy hoạch nguyên hỗn hợp MIP lựa chọn dự án chuyển đổi số

## a) Vì sao mô hình bỏ qua dự án P15 Open Data dù tỷ suất lợi ích/chi phí rất cao? Đây có phải là kết quả mong muốn về mặt chính sách?

Theo output của bạn, trong nghiệm cơ sở ngân sách 80.000 tỷ, mô hình **không bỏ qua P15** mà đã chọn **P15 Open Data + dữ liệu mở quốc gia**. P15 có chi phí chỉ **1.500 tỷ**, lợi ích **3.800 tỷ**, nên tỷ suất lợi ích/chi phí rất cao.

Vì vậy, với output hiện tại, câu trả lời là: mô hình chọn P15 là kết quả hợp lý. Về chính sách, đây là kết quả mong muốn, vì dữ liệu mở là nền tảng cho chính phủ số, doanh nghiệp số, AI, nghiên cứu đổi mới sáng tạo và minh bạch hóa quản trị.

Nếu một mô hình nào đó bỏ qua P15, nguyên nhân có thể là do ràng buộc số lượng dự án, ngân sách năm 1-2, hoặc các ràng buộc tiên quyết khiến P15 không còn nằm trong tổ hợp tối ưu. Nhưng với output của bạn, P15 được chọn, nên cần viết đúng theo kết quả này.

## b) Ràng buộc “bắt buộc P14 an ninh mạng” có làm giảm Z\* không? Việc bắt buộc này có hợp lý không?

Theo output bổ sung, khi bắt buộc P14, tổng lợi ích của danh mục cơ sở là **115.400 tỷ VND**. Khi bỏ ràng buộc bắt buộc P14, tổng lợi ích tăng lên **116.300 tỷ VND**. Như vậy, bắt buộc P14 làm giảm Z\* khoảng **900 tỷ VND**.

Tuy nhiên, việc bắt buộc P14 vẫn hợp lý. Khi Việt Nam phát triển định danh điện tử, dịch vụ công trực tuyến, trung tâm dữ liệu, dữ liệu mở và AI, rủi ro an ninh mạng tăng lên. Một dự án an ninh mạng có thể không tạo NPV cao nhất, nhưng đóng vai trò bảo vệ toàn hệ thống.

Nghị quyết 57-NQ/TW cũng nhấn mạnh yêu cầu phát triển khoa học công nghệ và chuyển đổi số gắn với bảo đảm an toàn, an ninh và chủ quyền số. ()

## c) Mô hình giả định các dự án độc lập về lợi ích, nhưng trên thực tế P8 AI quốc gia và P13 bán dẫn có lợi ích cộng hưởng. Làm thế nào để mô hình hóa hiệu ứng cộng hưởng này?

Để mô hình hóa cộng hưởng giữa P8 và P13, có thể thêm một biến nhị phân mới, ví dụ **z\_8\_13**. Biến này bằng 1 nếu cả P8 và P13 cùng được chọn. Sau đó thêm các ràng buộc:

z\_8\_13 ≤ y8\
z\_8\_13 ≤ y13\
z\_8\_13 ≥ y8 + y13 - 1

Sau đó, trong hàm mục tiêu, cộng thêm phần lợi ích cộng hưởng, ví dụ:

Z = Σ Bᵢyᵢ + S\_8\_13 z\_8\_13

Trong đó S\_8\_13 là lợi ích tăng thêm khi trung tâm AI quốc gia và khu công nghiệp bán dẫn cùng được triển khai. Cách này làm mô hình thực tế hơn, vì nhiều dự án công nghệ không tạo lợi ích độc lập mà tạo giá trị lớn hơn khi kết hợp với nhau.

---""",

    "bai6": r"""# Bài 6. TOPSIS xếp hạng 6 vùng kinh tế Việt Nam theo ưu tiên đầu tư AI

## a) Vùng nào dẫn đầu theo TOPSIS với trọng số chuyên gia? Đây có phải vùng nên triển khai trung tâm AI quốc gia đầu tiên không?

Theo output Bài 6, vùng dẫn đầu là **Đông Nam Bộ**, với điểm TOPSIS chuyên gia khoảng **0,940**. Xếp thứ hai là **Đồng bằng sông Hồng**, với điểm khoảng **0,898**. Xếp thứ ba là **Bắc Trung Bộ và duyên hải miền Trung**, với điểm khoảng **0,360**.

Đông Nam Bộ dẫn đầu vì có GRDP/người cao, FDI lớn, digital index cao, AI readiness cao, tỷ lệ lao động qua đào tạo cao và internet penetration tốt. Vì vậy, nếu chỉ xét hiệu quả triển khai AI, Đông Nam Bộ là vùng rất phù hợp để đặt trung tâm AI hoặc sandbox AI đầu tiên.

Tuy nhiên, không nên chỉ có một trung tâm AI ở Đông Nam Bộ. Theo Quyết định 127/QĐ-TTg, Việt Nam đặt mục tiêu phát triển nghiên cứu, ứng dụng AI đến năm 2030, nên hợp lý hơn là xây mạng lưới trung tâm AI theo chức năng vùng: Đông Nam Bộ thiên về ứng dụng doanh nghiệp, logistics, công nghiệp; Đồng bằng sông Hồng thiên về nghiên cứu, chính sách, dữ liệu công và nhân lực. ()

## b) Khi dùng trọng số Entropy, vùng nào có sự thay đổi xếp hạng lớn nhất? Vì sao?

Theo output, khi dùng trọng số Entropy, thứ hạng gần như **không thay đổi** so với trọng số chuyên gia. Đông Nam Bộ vẫn xếp thứ nhất, Đồng bằng sông Hồng xếp thứ hai, Bắc Trung Bộ và duyên hải miền Trung xếp thứ ba, Đồng bằng sông Cửu Long xếp thứ tư, Trung du miền núi phía Bắc xếp thứ năm và Tây Nguyên xếp thứ sáu.

Như vậy, không có vùng nào thay đổi xếp hạng lớn. Điều này cho thấy kết quả TOPSIS khá ổn định. Lý do là khoảng cách giữa nhóm vùng dẫn đầu và nhóm vùng còn lại khá rõ ràng về GRDP/người, FDI, digital index, AI readiness, R&D và internet penetration.

Điều này làm tăng độ tin cậy của kết quả: dù dùng trọng số chủ quan hay khách quan, Đông Nam Bộ và Đồng bằng sông Hồng vẫn là hai vùng có nền tảng AI tốt nhất.

## c) TOPSIS giả định độc lập tuyến tính giữa các tiêu chí. Nếu AI Readiness và Internet penetration tương quan rất cao thì ảnh hưởng thế nào? Đề xuất cách xử lý.

Nếu AI Readiness và Internet penetration tương quan rất cao, TOPSIS có thể bị “đếm trùng” lợi thế của các vùng phát triển. Ví dụ, Đông Nam Bộ và Đồng bằng sông Hồng vừa có internet penetration cao, vừa có AI readiness cao. Nếu hai tiêu chí này phản ánh cùng một nền tảng số, mô hình có thể cộng điểm hai lần cho cùng một lợi thế.

Điều này làm vùng mạnh càng mạnh hơn trong bảng xếp hạng, còn vùng yếu càng bị đẩy xuống thấp. Để xử lý, có thể kiểm tra ma trận tương quan giữa các tiêu chí. Nếu hai tiêu chí tương quan quá cao, có thể gộp chúng thành một chỉ số tổng hợp, giảm trọng số một trong hai tiêu chí, hoặc dùng PCA để rút gọn biến.

Ngoài ra, nếu mục tiêu chính sách là phát triển bao trùm, nên bổ sung tiêu chí “nhu cầu hỗ trợ” hoặc “khoảng cách số” để vùng yếu không bị loại hoàn toàn khỏi ưu tiên đầu tư.

## d) Nếu Việt Nam xây dựng 3 trung tâm AI lớn, nên chọn 3 vùng nào? Có cần điều chỉnh thêm tiêu chí địa - chính trị không?

Dựa trên output TOPSIS, ba vùng nên chọn là **Đông Nam Bộ**, **Đồng bằng sông Hồng**, và **Bắc Trung Bộ và duyên hải miền Trung**. Kết quả này ổn định cả khi thay đổi trọng số AI từ 0,10 đến 0,40.

Tuy nhiên, quyết định thực tế cần điều chỉnh thêm tiêu chí địa - chính trị. Cần xét đến an ninh dữ liệu, cân bằng vùng miền, hạ tầng năng lượng, rủi ro thiên tai, khả năng kết nối quốc tế và vai trò liên kết vùng. Ví dụ, Đồng bằng sông Hồng có lợi thế về cơ quan quản lý, đại học và viện nghiên cứu; Đông Nam Bộ có lợi thế về doanh nghiệp và ứng dụng; miền Trung có thể đóng vai trò trung tâm kết nối và giảm tập trung quá mức vào hai cực Bắc - Nam.

Vì vậy, TOPSIS là công cụ hỗ trợ lựa chọn, không phải quyết định cuối cùng.

---""",

    "bai7": r"""# Bài 7. Tối ưu đa mục tiêu Pareto với NSGA-II

## a) Khi quan sát đường biên Pareto, đánh đổi giữa tăng trưởng và bao trùm có rõ ràng không? Mức đánh đổi đó nói lên điều gì về cơ cấu kinh tế Việt Nam?

Có. Output Bài 7 tạo ra **120 nghiệm Pareto**, cho thấy không có một nghiệm tối ưu duy nhất. Nghiệm có GDP\_gain cao nhất đạt khoảng **60.466,15**, nhưng đi kèm Inequality\_MAD khoảng **969,17** và Emission khoảng **1.867,75**. Trong khi đó, nghiệm thỏa hiệp TOPSIS đạt GDP\_gain khoảng **58.815,38**, thấp hơn khoảng **2,73%**, nhưng Inequality\_MAD giảm còn **509,46** và Emission giảm còn **89,49**.

Điều này cho thấy đánh đổi giữa tăng trưởng và bao trùm là rõ ràng. Nếu chỉ tối đa hóa tăng trưởng, vốn sẽ có xu hướng tập trung vào vùng có năng lực hấp thụ cao, làm tăng khoảng cách vùng. Nếu chọn nghiệm thỏa hiệp, Việt Nam chấp nhận giảm một phần nhỏ tăng trưởng để cải thiện công bằng vùng và môi trường.

Về cơ cấu kinh tế, kết quả này phản ánh thực tế Việt Nam: năng lực số, FDI, hạ tầng và nhân lực chất lượng cao tập trung nhiều ở các vùng phát triển. Vì vậy, chính sách chuyển đổi số nếu không có ràng buộc bao trùm sẽ dễ làm khoảng cách vùng miền lớn hơn.

## b) Trọng số 0,40; 0,25; 0,20; 0,15 có phản ánh đúng ưu tiên hiện tại của Việt Nam không? Nên điều chỉnh thế nào để phù hợp với COP26 và Quyết định 127/QĐ-TTg?

Bộ trọng số **0,40 tăng trưởng; 0,25 bao trùm; 0,20 môi trường; 0,15 an ninh** phản ánh khá đúng ưu tiên phát triển hiện nay của Việt Nam, vì tăng trưởng vẫn là mục tiêu quan trọng, nhưng không còn là mục tiêu duy nhất. Bao trùm, môi trường và an ninh dữ liệu ngày càng quan trọng trong bối cảnh chuyển đổi số.

Tuy nhiên, nếu muốn phù hợp hơn với cam kết Net Zero 2050 tại COP26, nên tăng trọng số môi trường từ **0,20** lên khoảng **0,25 hoặc 0,30**. Nếu muốn phù hợp hơn với Quyết định 127/QĐ-TTg về AI, có thể tăng trọng số an ninh dữ liệu và năng lực quản trị AI, vì phát triển AI không thể tách rời bảo vệ dữ liệu, an toàn hệ thống và chủ quyền số. ()

Một bộ trọng số điều chỉnh có thể là: tăng trưởng **0,35**, bao trùm **0,25**, môi trường **0,25**, an ninh **0,15**. Nếu nhấn mạnh an toàn AI hơn, có thể dùng: tăng trưởng **0,35**, bao trùm **0,25**, môi trường **0,20**, an ninh **0,20**.

## c) Vai trò của NSGA-II khác gì so với LP đơn mục tiêu? Nó có thay thế được quyết định chính trị không?

LP đơn mục tiêu tìm một nghiệm tối ưu duy nhất theo một hàm mục tiêu, ví dụ tối đa hóa GDP gain. Trong khi đó, NSGA-II tìm một tập nghiệm Pareto, cho thấy các phương án đánh đổi giữa tăng trưởng, bao trùm, môi trường và an ninh dữ liệu.

Vì vậy, NSGA-II phù hợp hơn với bài toán chính sách phức tạp, nơi các mục tiêu thường xung đột nhau. Nó giúp nhà hoạch định chính sách nhìn thấy nếu tăng trưởng thêm thì phải hy sinh bao nhiêu về công bằng hoặc môi trường.

Tuy nhiên, NSGA-II không thay thế được quyết định chính trị. Việc chọn nghiệm nào phụ thuộc vào ưu tiên xã hội, tham vấn công chúng, chiến lược quốc gia và trách nhiệm giải trình của Nhà nước. Mô hình chỉ hỗ trợ ra quyết định, không tự quyết định thay con người.

---""",

    "bai8": r"""# Bài 8. Tối ưu động phân bổ liên thời gian 2026-2035

## a) Quỹ đạo tối ưu của K, D, AI, H có front-loaded hay back-loaded không? Vì sao mô hình đề xuất như vậy?

Theo output Bài 8, quỹ đạo tối ưu có tính **front-loaded** đối với D và AI. Năm 2026, tỷ trọng đầu tư vào D là **0,8825**, AI là **0,1175**, còn K và H gần như bằng 0. Từ 2028 đến 2032, tỷ trọng AI tăng rất mạnh, đạt **0,3978 năm 2028**, **0,7012 năm 2030** và **0,7996 năm 2032**. Đến năm 2035, mô hình trở lại phân bổ cân bằng hơn, mỗi nhóm khoảng **0,25**.

Mô hình đề xuất như vậy vì đầu tư số hóa và AI tạo tác động lan tỏa đến năng suất trong các năm sau. Nếu đầu tư sớm, nền kinh tế có thêm thời gian tích lũy lợi ích từ công nghệ. Điều này phù hợp với định hướng của Quyết định 749/QĐ-TTg và Quyết định 411/QĐ-TTg về chuyển đổi số, kinh tế số và xã hội số. ()

Tuy nhiên, cần lưu ý output có hiện tượng K, D, AI, H giảm theo thời gian do cách đặc tả mô phỏng và khấu hao. Vì vậy, trong báo cáo nên nói rõ mô hình cần bổ sung ràng buộc không để năng lực số suy giảm dưới mức tối thiểu.

## b) Tỷ lệ đầu tư AI/đầu tư H theo thời gian có ổn định không? Mô hình ngụ ý gì về việc đào tạo nhân lực nên đi trước hay đồng thời với đầu tư AI?

Tỷ lệ AI/H không ổn định. Trong giai đoạn 2026-2034, H gần như bằng 0, trong khi AI tăng mạnh. Đến năm 2035, H mới tăng lên khoảng **0,25**.

Nếu đọc máy móc, mô hình có vẻ ưu tiên AI trước, nhân lực sau. Nhưng về chính sách, điều này cần được phản biện. AI không thể phát huy hiệu quả nếu thiếu nhân lực số, chuyên gia dữ liệu, kỹ sư AI, chuyên gia an ninh mạng và lực lượng lao động có kỹ năng sử dụng công nghệ.

Do đó, kết luận hợp lý hơn là: đào tạo nhân lực phải đi **đồng thời** với đầu tư AI, thậm chí ở nhiều vùng và ngành, nhân lực số cần đi trước. Nghị quyết 57-NQ/TW cũng nhấn mạnh phát triển nguồn nhân lực chất lượng cao là điều kiện quan trọng cho khoa học, công nghệ, đổi mới sáng tạo và chuyển đổi số. ()

## c) Hệ số chiết khấu ρ = 0,97 ngụ ý chính phủ quan tâm nhiều đến dài hạn. Nếu ρ = 0,90 thì kết quả thay đổi thế nào? Đây có phải lý do các chính phủ thường “dưới đầu tư” vào R&D?

Với ρ = **0,97**, mô hình coi trọng lợi ích dài hạn, nên sẵn sàng đầu tư sớm vào D và AI để tạo tác động năng suất về sau. Output cho thấy chiến lược tối ưu đạt welfare **47,8763**, cao hơn đầu tư đều và front-load giả định.

Nếu ρ giảm xuống **0,90**, nghĩa là chính phủ coi trọng ngắn hạn hơn, mô hình có thể ưu tiên tiêu dùng hiện tại hoặc các khoản đầu tư có hiệu quả nhanh, thay vì đầu tư dài hạn vào R&D, AI và nhân lực. Khi đó, đầu tư vào các lĩnh vực có độ trễ dài như R&D có thể giảm.

Đây đúng là một lý do khiến chính phủ thường “dưới đầu tư” vào R&D: chi phí xuất hiện ngay, nhưng lợi ích thường đến muộn, khó đo lường và có thể vượt qua nhiệm kỳ ngân sách. Vì vậy, Việt Nam cần các cơ chế đầu tư dài hạn như quỹ đổi mới sáng tạo, ngân sách trung hạn cho khoa học công nghệ và hợp tác công - tư.

---""",

    "bai9": r"""# Bài 9. Tác động AI tới thị trường lao động Việt Nam

## a) Ngành nào cần đầu tư đào tạo lại nhiều nhất theo kết quả tối ưu? Có khớp với cảm nhận thực tế ở Việt Nam không?

Theo output Bài 9, mô hình phân bổ toàn bộ **30.000 tỷ** vào đào tạo lại x\_H của ngành **Giáo dục - Đào tạo**. Kết quả tạo ra **1.650.000 việc làm nâng cấp** và NetJob cũng bằng **1.650.000**.

Về mặt toán học, kết quả này xảy ra vì ngành Giáo dục - Đào tạo có hệ số tạo việc làm nâng cấp từ đào tạo lại rất cao. Mô hình tuyến tính sẽ dồn ngân sách vào nơi có hiệu quả biên lớn nhất.

Nhưng nếu xét thực tế Việt Nam, kết quả này chưa hoàn toàn hợp lý nếu hiểu là chỉ giáo dục cần đào tạo lại. Các ngành như công nghiệp chế biến chế tạo, bán buôn - bán lẻ, logistics và tài chính - ngân hàng cũng có rủi ro tự động hóa cao. Vì vậy, mô hình cần bổ sung ràng buộc phân bổ tối thiểu cho các ngành có nhiều lao động hoặc có nguy cơ tự động hóa cao.

## b) Ngành Tài chính - Ngân hàng có nguy cơ thay thế 52% nhưng cũng có hệ số tạo việc làm mới rất cao. Mô hình khuyến nghị chiến lược gì cho ngành này?

Trong dữ liệu mô hình, Tài chính - Ngân hàng có rủi ro tự động hóa **52%**, cao nhất trong các ngành. Nhưng ngành này cũng có hệ số tạo việc làm mới từ AI khá cao, **a1 = 45,8**.

Điều này cho thấy tài chính - ngân hàng là ngành có hai mặt. AI có thể thay thế các công việc lặp lại như nhập liệu, xử lý hồ sơ, giao dịch đơn giản. Nhưng AI cũng tạo ra việc làm mới trong phân tích dữ liệu, quản trị rủi ro, chống gian lận, an ninh mạng, tín dụng số và tài chính cá nhân hóa.

Vì vậy, chiến lược phù hợp là **không né AI**, nhưng phải đi kèm tái đào tạo bắt buộc. Nhân viên tài chính cần được đào tạo về dữ liệu, kiểm soát rủi ro mô hình, an ninh mạng, đạo đức AI và tuân thủ. Cách này phù hợp với định hướng phát triển AI trong Quyết định 127/QĐ-TTg. ()

## c) Có nên đầu tư x\_AI vào ngành Nông-Lâm-Thủy sản không, vì hệ số tạo việc làm AI thấp 8,5 nhưng số lao động dịch chuyển lại rất lớn? Mô hình nói gì?

Theo output, mô hình không phân bổ x\_AI vào Nông-Lâm-Thủy sản. Lý do là hệ số tạo việc làm AI của ngành này thấp, chỉ **8,5**, trong khi mục tiêu của mô hình là tối đa hóa NetJob.

Tuy nhiên, về chính sách, không nên kết luận rằng nông nghiệp không cần AI. Nông-Lâm-Thủy sản có **13,20 triệu lao động**, là ngành có quy mô lao động rất lớn. AI và số hóa có thể hỗ trợ dự báo thời tiết, truy xuất nguồn gốc, tối ưu tưới tiêu, quản lý sâu bệnh, logistics lạnh và thương mại điện tử nông sản.

Vì vậy, với nông nghiệp, nên đầu tư AI ở mức phù hợp, đi kèm chuyển đổi số quy mô nhỏ và đào tạo kỹ năng số cơ bản. Mục tiêu không chỉ là tạo việc làm AI mới, mà là nâng năng suất và giảm rủi ro cho nông dân.

## d) “Tốc độ tự động hóa không nên vượt quá năng lực đào tạo lại” được biểu diễn bằng ràng buộc nào? Có nên bổ sung ràng buộc nào để bảo đảm an sinh xã hội không?

Phát biểu này được biểu diễn bằng ràng buộc:

**DisplacedJobᵢ ≤ RetrainingCapacityᵢ**

Nghĩa là số lao động bị thay thế bởi tự động hóa ở mỗi ngành không được vượt quá năng lực đào tạo lại của ngành đó.

Output cũng kiểm tra thêm ràng buộc “không ngành nào mất quá 5% lao động”, và bài toán vẫn khả thi. Tuy nhiên, vì nghiệm tối ưu hiện tại không đầu tư AI vào ngành nào, DisplacedJob bằng 0 nên ràng buộc an sinh chưa thực sự phát huy tác dụng.

Để mô hình sát thực tế hơn, nên bổ sung ràng buộc: mỗi ngành có rủi ro tự động hóa trên 35% phải nhận một mức đào tạo tối thiểu; ngành có quy mô lao động lớn phải có ngân sách hỗ trợ tối thiểu; và DisplacedJob không chỉ giới hạn theo ngành mà còn theo nhóm lao động dễ tổn thương như lao động phổ thông, phụ nữ, lao động lớn tuổi.

---""",

    "bai10": r"""# Bài 10. Quy hoạch ngẫu nhiên hai giai đoạn dưới bất định

## a) So với lời giải xác định, lời giải SP có xu hướng đầu tư H nhiều hơn hay ít hơn? Vì sao?

Theo output Bài 10, quyết định first-stage của mô hình SP phân bổ toàn bộ **65.000** vào AI, còn I, D và H đều bằng 0. Ở second-stage, mô hình phân bổ **15.000 vào D** trong kịch bản lạc quan và cơ sở, còn trong kịch bản bi quan và khủng hoảng thì phân bổ **15.000 vào H**.

Như vậy, ở giai đoạn đầu, SP đầu tư H **ít hơn**, vì mô hình dồn vào AI do hệ số lợi ích cơ bản của AI cao. Nhưng khi kịch bản xấu xảy ra, mô hình chuyển sang đầu tư H, vì nhân lực giúp nền kinh tế thích nghi tốt hơn với cú sốc.

Về chính sách, kết quả này cho thấy nhân lực số đóng vai trò như một loại “hàng hóa bảo hiểm”. Tuy nhiên, không nên đợi đến khi khủng hoảng mới đầu tư vào H, vì đào tạo nhân lực cần thời gian. Do đó, trong thực tế, Việt Nam nên đầu tư nhân lực số ngay từ giai đoạn đầu.

## b) VSS dương nói lên điều gì về giá trị của tư duy xác suất trong hoạch định chính sách Việt Nam?

Về lý thuyết, VSS dương cho thấy lời giải stochastic tốt hơn lời giải dựa trên kịch bản kỳ vọng. Nói cách khác, nếu VSS dương, việc tính đến bất định giúp chính sách tốt hơn.

Tuy nhiên, output của bạn cho thấy **SP\_value = 98.575**, **EEV\_value = 98.575**, **Wait-and-See\_value = 98.575**, nên **VSS = 0** và **EVPI = 0**. Điều này không có nghĩa là tư duy xác suất không quan trọng. Nó chỉ cho thấy trong phiên bản mô hình hiện tại, các kịch bản chưa đủ khác biệt hoặc ràng buộc chưa đủ mạnh để tạo ra khác biệt giữa các lời giải.

Khi viết báo cáo, nên nói rằng mô hình đã cài đặt được cấu trúc stochastic LP, nhưng cần làm bất định mạnh hơn để VSS và EVPI thể hiện rõ hơn. Ví dụ, có thể thêm chi phí điều chỉnh, thêm rủi ro AI thất bại trong khủng hoảng, hoặc bắt buộc đầu tư H tối thiểu ở giai đoạn đầu.

## c) COVID-19 và bão Yagi là các cú sốc thực tế. Việt Nam có đang dưới đầu tư vào nhân lực số như một hàng hóa bảo hiểm không?

Có thể nói là có rủi ro dưới đầu tư. Output cho thấy trong kịch bản xấu, mô hình chuyển second-stage sang H = **15.000**, tức nhân lực trở thành công cụ thích nghi khi cú sốc xảy ra.

Thực tế COVID-19 và bão Yagi cho thấy nền kinh tế cần khả năng thích nghi nhanh. Lao động có kỹ năng số có thể chuyển sang làm việc từ xa, thương mại điện tử, dịch vụ số, logistics số và các mô hình sản xuất linh hoạt. Năm 2024, dù GDP Việt Nam tăng **7,09%**, nền kinh tế vẫn chịu tác động của thiên tai, biến động bên ngoài và yêu cầu phục hồi sản xuất. ()

Vì vậy, nhân lực số nên được xem là khoản đầu tư bảo hiểm dài hạn. Việt Nam không nên chỉ đầu tư vào hạ tầng hoặc AI, mà cần đầu tư đều vào kỹ năng số cơ bản, đào tạo lại lao động và năng lực học suốt đời.

---""",

    "bai11": r"""# Bài 11. Q-learning cho chính sách kinh tế thích nghi

## a) Khi nền kinh tế ở trạng thái GDP growth thấp, D thấp, U cao, chính sách π\*(s) chọn hành động gì? Có khớp với “quick win” không?

Theo output Bài 11, ở trạng thái **LowGDP\_LowD\_LowAI\_HighU = [0,0,0,2]**, mô hình chọn hành động **Truyền thống**, với Q-value bằng **0**.

Kết quả này chưa khớp với logic “quick win”. Khi GDP thấp, số hóa thấp và thất nghiệp cao, chính sách quick win thường nên là số hóa dịch vụ công, hỗ trợ doanh nghiệp nhỏ chuyển đổi số, đào tạo kỹ năng số ngắn hạn và hỗ trợ việc làm. Những chính sách này có thể tạo hiệu quả nhanh hơn so với quay về đầu tư truyền thống.

Tuy nhiên, vì Q-value = 0, có thể hiểu rằng agent chưa học đủ ở trạng thái này. Do đó, không nên xem đây là khuyến nghị chính sách mạnh, mà nên xem là dấu hiệu mô hình Q-learning cần huấn luyện thêm, cải thiện hàm thưởng và tăng số lần agent trải nghiệm các trạng thái xấu.

## b) Khi GDP growth cao, AI cao, U thấp, chính sách chọn gì? Phù hợp với “consolidation” không?

Theo output, ở trạng thái **HighGDP\_HighD\_HighAI\_LowU = [2,2,2,0]**, mô hình cũng chọn **Truyền thống**, với Q-value = **0**.

Nếu diễn giải chính sách, trong trạng thái GDP cao, AI cao và thất nghiệp thấp, lựa chọn “Truyền thống” có thể được hiểu là giai đoạn củng cố: giảm tốc độ mở rộng AI quá nhanh, tập trung ổn định hệ thống, kiểm soát rủi ro, đầu tư hạ tầng nền và bảo đảm an toàn dữ liệu.

Tuy nhiên, vì Q-value vẫn bằng 0, kết quả này chưa đủ mạnh để kết luận. Output đáng tin cậy hơn là trạng thái **VN\_2026 = [1,1,0,1]**, nơi mô hình chọn **Số hóa nhanh** với Q-value khoảng **15,2896**. Điều này hợp lý với Việt Nam hiện nay: khi năng lực AI còn đang phát triển, ưu tiên số hóa nhanh là bước đi phù hợp trước khi mở rộng AI mạnh hơn.

## c) AI không thay thế quyết định chính trị - xã hội. Tích hợp π\* vào quy trình hoạch định chính sách Việt Nam thế nào?

Q-learning nên được dùng như một **hệ thống khuyến nghị chính sách**, không phải hệ thống tự động ra quyết định. Mô hình có thể gợi ý hành động tốt nhất trong từng trạng thái kinh tế, nhưng quyết định cuối cùng vẫn phải do con người và cơ quan có thẩm quyền chịu trách nhiệm.

Quy trình phù hợp là: mô hình đề xuất chính sách; chuyên gia kiểm định dữ liệu và giả định; hội đồng chính sách đánh giá tác động kinh tế - xã hội - pháp lý; sau đó cơ quan quản lý quyết định và công khai giải trình. Cách này bảo đảm AI hỗ trợ minh bạch hóa đánh đổi, nhưng không thay thế trách nhiệm chính trị.

Output cũng cho thấy Q-learning có avg\_total\_reward **8,2600**, cao hơn các chính sách cố định như Always balanced và Always AI-led. Điều đó chứng minh chính sách thích nghi có tiềm năng tốt hơn chính sách cứng nhắc, nhưng vẫn phải nằm trong khuôn khổ quản trị công.

---""",

    "bai12": r"""# Bài 12. Đồ án tích hợp AIDEOM-VN

Trong đề, Bài 12 không có mục “Câu hỏi thảo luận chính sách” riêng như Bài 1-11. Tuy nhiên, dựa trên yêu cầu đồ án và output của bạn, có thể viết phần thảo luận tổng hợp như sau. Đề yêu cầu Bài 12 tích hợp các kỹ thuật từ Bài 1-11 thành hệ thống AIDEOM-VN gồm 6 module và dashboard có các tab tối thiểu như Tổng quan, Phân bổ, Kịch bản so sánh và Cảnh báo rủi ro.

## a) Kịch bản nào cho kết quả GDP\_index năm 2030 cao nhất?

Theo output Bài 12, kịch bản có GDP\_index năm 2030 cao nhất là **S3\_AI\_dan\_dat**, đạt **380,7220**. Xếp thứ hai là **S2\_So\_hoa\_nhanh**, đạt **380,3790**. Xếp thứ ba là **S5\_Toi\_uu\_can\_bang**, đạt **379,4473**. Kịch bản thấp nhất là **S1\_Truyen\_thong**, đạt **377,7788**.

Điều này cho thấy trong mô hình, chiến lược AI dẫn dắt có thể tạo tăng trưởng cao nhất. Tuy nhiên, khoảng cách giữa S3 và S2 khá nhỏ, chỉ khoảng **0,343 điểm**. Vì vậy, AI dẫn dắt không vượt trội tuyệt đối so với số hóa nhanh.

## b) Kịch bản nào phù hợp nhất với thực tiễn Việt Nam hiện nay?

Nếu chỉ xét GDP\_index, S3\_AI\_dan\_dat là cao nhất. Nhưng nếu xét tính khả thi, Việt Nam có thể phù hợp hơn với **S5\_Toi\_uu\_can\_bang** hoặc **S2\_So\_hoa\_nhanh**.

S2 giúp chỉ số D đạt **21,5976**, cao nhất trong các kịch bản, phù hợp với định hướng chuyển đổi số và phát triển kinh tế số. S5 có kết quả cân bằng hơn giữa GDP, D, AI và H. Điều này hợp với thực tế Việt Nam vì AI cần hạ tầng số, dữ liệu và nhân lực đi kèm. Quyết định 749/QĐ-TTg và Quyết định 411/QĐ-TTg đều nhấn mạnh chuyển đổi số là quá trình đồng bộ, không chỉ đầu tư vào một công nghệ riêng lẻ. ()

Vì vậy, nếu phải chọn một kịch bản khuyến nghị chính sách, nên chọn **S5\_Toi\_uu\_can\_bang**. Còn S3 có thể trình bày như kịch bản tăng trưởng cao nhưng rủi ro hấp thụ lớn hơn.

## c) Cảnh báo rủi ro trong output nói lên điều gì?

Output Bài 12 cho thấy cả 5 kịch bản đều có **cyber\_risk = Trung bình**, **digital\_gap\_risk = Cao**, và **human\_capital\_status = Thiếu**. Đây là kết quả rất quan trọng.

Nó cho thấy dù chọn kịch bản nào, Việt Nam vẫn đối mặt với ba vấn đề: rủi ro an ninh mạng, khoảng cách số giữa vùng mạnh và vùng yếu, và thiếu hụt nhân lực số. Điều này phù hợp với Nghị quyết 57-NQ/TW, vì Nghị quyết nhấn mạnh chuyển đổi số phải gắn với phát triển nguồn nhân lực, bảo đảm an toàn dữ liệu và nâng cao năng lực quốc gia. ()

Vì vậy, dashboard không nên chỉ hiển thị kịch bản có GDP cao nhất. Nó cần cảnh báo rằng nếu không xử lý nhân lực, khoảng cách số và an ninh mạng, tăng trưởng AI có thể thiếu bền vững.

## d) Hướng mở rộng nghiên cứu sau đồ án nên là gì?

Có bốn hướng mở rộng phù hợp. Thứ nhất, chọn một use case cụ thể như Đồng bằng sông Cửu Long hoặc ngành chế biến chế tạo để viết báo cáo nghiên cứu sâu hơn. Thứ hai, mở rộng mô hình sang CGE hoặc DSGE-AI để phản ánh cân bằng tổng thể. Thứ ba, tích hợp dữ liệu thời gian thực từ dữ liệu mở, hải quan, thị trường lao động và đầu tư. Thứ tư, mở rộng Q-learning thành Multi-Agent RL, trong đó mỗi agent đại diện cho một bộ, ngành hoặc vùng.

Trong thực tế, hướng mở rộng quan trọng nhất là tích hợp dữ liệu thời gian thực và cho phép người dùng thay đổi trọng số chính sách trên dashboard. Như vậy, AIDEOM-VN sẽ không chỉ là bài tập mô phỏng, mà trở thành công cụ hỗ trợ ra quyết định có thể cập nhật theo bối cảnh mới."""

}

# ============================================================
# METADATA THEO TỪNG BÀI
# ============================================================
LESSON_META = {
    1: {"title": "Bài 1. Hàm sản xuất Cobb-Douglas mở rộng", "level": "Dễ", "skills": ["Growth accounting", "TFP", "Forecast 2030"], "objective": "Tính TFP, so sánh GDP thực tế - dự báo và phân rã đóng góp tăng trưởng của K, L, D, AI, H."},
    2: {"title": "Bài 2. Phân bổ ngân sách số", "level": "Dễ", "skills": ["LP", "Shadow price", "Sensitivity"], "objective": "Giải bài toán quy hoạch tuyến tính 4 hạng mục đầu tư số và phân tích giá đối ngẫu."},
    3: {"title": "Bài 3. Chỉ số ưu tiên ngành", "level": "Dễ", "skills": ["Min-max", "MCDM", "Sensitivity"], "objective": "Xếp hạng 10 ngành theo chỉ số ưu tiên chuyển đổi số và AI."},
    4: {"title": "Bài 4. Phân bổ ngân sách theo vùng", "level": "Trung bình", "skills": ["LP", "Fairness constraint", "Heatmap"], "objective": "Phân bổ ngân sách cho 6 vùng và 4 hạng mục, so sánh có/không có ràng buộc công bằng."},
    5: {"title": "Bài 5. MIP lựa chọn dự án chuyển đổi số", "level": "Trung bình", "skills": ["MIP", "Binary variables", "Project portfolio"], "objective": "Chọn danh mục dự án tối ưu trong ngân sách và các ràng buộc đặc thù."},
    6: {"title": "Bài 6. TOPSIS xếp hạng vùng ưu tiên AI", "level": "Trung bình", "skills": ["TOPSIS", "Entropy", "Regional ranking"], "objective": "Xếp hạng 6 vùng kinh tế theo mức độ ưu tiên đầu tư AI."},
    7: {"title": "Bài 7. Tối ưu đa mục tiêu Pareto", "level": "Khá khó", "skills": ["NSGA-II", "Pareto", "TOPSIS compromise"], "objective": "Phân tích đánh đổi giữa tăng trưởng, công bằng, phát thải và rủi ro dữ liệu."},
    8: {"title": "Bài 8. Tối ưu động liên thời gian", "level": "Khá khó", "skills": ["Dynamic optimization", "Welfare", "Shock scenario"], "objective": "Mô phỏng quỹ đạo tối ưu 2026-2035 và so sánh chiến lược đầu tư."},
    9: {"title": "Bài 9. Tác động AI tới lao động", "level": "Khá khó", "skills": ["Labor simulation", "Retraining", "Net jobs"], "objective": "Đánh giá việc làm mới, việc làm bị thay thế và năng lực đào tạo lại theo ngành."},
    10: {"title": "Bài 10. Quy hoạch ngẫu nhiên hai giai đoạn", "level": "Khó", "skills": ["Stochastic LP", "VSS", "EVPI"], "objective": "So sánh quyết định first-stage, second-stage và giá trị của thông tin dưới bất định."},
    11: {"title": "Bài 11. Q-learning cho chính sách thích nghi", "level": "Khó", "skills": ["Q-learning", "Policy comparison", "Learning curve"], "objective": "Học chính sách thích nghi theo trạng thái kinh tế và so sánh với chính sách cố định."},
    12: {"title": "Bài 12. Đồ án tích hợp AIDEOM-VN", "level": "Khó", "skills": ["Dashboard", "Scenario comparison", "Risk warning"], "objective": "Tích hợp các mô hình thành dashboard phân tích kịch bản, KPI và cảnh báo rủi ro."},
}

# ============================================================
# HELPERS
# ============================================================
def section_title(title: str, subtitle: str | None = None):
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div class="title-card">
        <h1>{title}</h1>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def badges(items):
    return "".join([f'<span class="badge">{x}</span>' for x in items])

def intro_box(n: int):
    m = LESSON_META[n]
    st.markdown(f"""
    <div class="info-card">
        <h4>Mục tiêu & kỹ năng chính</h4>
        <p><b>Cấp độ:</b> {m['level']}</p>
        <p><b>Mục tiêu:</b> {m['objective']}</p>
        <div style="margin-top:8px;">{badges(m['skills'])}</div>
    </div>
    """, unsafe_allow_html=True)

def show_df(df: pd.DataFrame, title: str | None = None, height: int | None = None):
    if title:
        st.subheader(title)
    st.dataframe(df, use_container_width=True, height=height)

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")

def download_df(df: pd.DataFrame, file_name: str, label: str = "Tải bảng CSV"):
    st.download_button(label, data=to_csv_bytes(df), file_name=file_name, mime="text/csv")

def numeric_cols(df: pd.DataFrame):
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

def first_existing(data: dict[str, pd.DataFrame], names: list[str]):
    for n in names:
        if n in data:
            return data[n]
    return pd.DataFrame()

def format_number(x):
    try:
        return f"{float(x):,.2f}"
    except Exception:
        return str(x)

def quick_metrics(df: pd.DataFrame, items: list[tuple[str, str]]):
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)

def safe_plot_line(df, x, y, title, color=None, markers=True):
    if all(c in df.columns for c in ([x, y] + ([color] if color else []))):
        st.plotly_chart(px.line(df, x=x, y=y, color=color, markers=markers, title=title), use_container_width=True)

def safe_plot_bar(df, x, y, title, color=None, text=None, barmode=None):
    if isinstance(y, list):
        needed = [x] + y
    else:
        needed = [x, y]
    if all(c in df.columns for c in needed):
        fig = px.bar(df, x=x, y=y, color=color, text=text, barmode=barmode, title=title)
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

def discussion(key: str):
    st.markdown(DISCUSSIONS.get(key, "Chưa có nội dung thảo luận cho bài này."))

def model_summary(text: str):
    st.markdown(f"""
    <div class="mini-card">
        <h4>Mô hình / logic chính</h4>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)

def generic_data_tab(sheets: dict[str, pd.DataFrame], sheet_names: list[str], prefix: str):
    selected = st.selectbox("Chọn bảng dữ liệu", sheet_names, key=f"select_{prefix}")
    df = sheets[selected]
    show_df(df, selected)
    download_df(df, f"{selected}.csv")

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown("""
<div style="text-align:center; padding:12px 4px 20px 4px;">
    <div style="background:rgba(255,255,255,.12); border-radius:18px; padding:16px 12px; border:1px solid rgba(255,255,255,.18);">
        <h2 style="margin:0; color:white;">AIDEOM-VN</h2>
        <p style="margin-top:8px; color:#CBD5E1; font-size:15px; line-height:1.45;">Dashboard theo từng bài 1-12</p>
    </div>
</div>
""", unsafe_allow_html=True)

page_options = ["Tổng quan"] + [LESSON_META[i]["title"] for i in range(1, 13)]
page = st.sidebar.radio("Chọn nội dung", page_options)

with st.sidebar.expander("Dữ liệu đang dùng", expanded=False):
    st.write(f"Main: `{DATA_PATHS['main'].name}`")
    st.write(f"Supplement: `{DATA_PATHS['supp'].name}`")
    st.write(f"Advanced: `{DATA_PATHS['adv'].name}`")

# ============================================================
# PAGE: OVERVIEW
# ============================================================
if page == "Tổng quan":
    section_title(
        "AIDEOM-VN Dashboard",
        "Hiển thị kết quả theo từng bài trong bộ bài tập Mô hình ra quyết định phát triển kinh tế Việt Nam trong kỷ nguyên AI.",
    )
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Số bài", "12/12")
    col2.metric("Nhóm dữ liệu", "3 Excel")
    col3.metric("Mốc thời gian", "2020-2035")
    col4.metric("Công cụ", "Streamlit")

    st.markdown("""
    <div class="info-card">
        <h4>Cách sử dụng</h4>
        <p>Chọn từng bài ở thanh bên trái. Mỗi bài được chia thành các tab: mục tiêu - mô hình, dữ liệu, kết quả, biểu đồ, thảo luận chính sách và tải dữ liệu.</p>
    </div>
    """, unsafe_allow_html=True)

    overview = pd.DataFrame([
        {"Bài": i, "Tên bài": LESSON_META[i]["title"].replace(f"Bài {i}. ", ""), "Cấp độ": LESSON_META[i]["level"], "Kỹ năng": ", ".join(LESSON_META[i]["skills"])}
        for i in range(1, 13)
    ])
    show_df(overview, "Bản đồ 12 bài")
    fig = px.histogram(overview, x="Cấp độ", color="Cấp độ", title="Phân bố cấp độ bài tập")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# BÀI 1
# ============================================================
elif page == LESSON_META[1]["title"]:
    section_title(LESSON_META[1]["title"], "TFP, phân rã tăng trưởng và dự báo GDP 2030")
    intro_box(1)
    df, decomp, forecast = main["Bai1_TFP"], main["Bai1_Growth_Decomp"], main["Bai1_Forecast2030"]
    t1, t2, t3, t4, t5, t6 = st.tabs(["Mục tiêu & mô hình", "Dữ liệu", "TFP", "Phân rã", "Dự báo 2030", "Thảo luận"])
    with t1:
        model_summary("Hàm sản xuất Cobb-Douglas mở rộng đưa thêm D - số hóa, AI - năng lực AI và H - nhân lực số vào bên cạnh K và L. TFP được tính ngược từ GDP thực tế.")
    with t2:
        show_df(df, "Dữ liệu và kết quả tính TFP")
        download_df(df, "bai1_tfp.csv")
    with t3:
        quick_metrics(df, [("TFP 2020", format_number(df.iloc[0]["TFP_A"])), ("TFP 2025", format_number(df.iloc[-1]["TFP_A"])), ("MAPE TB", format_number(df["APE_pct"].mean()) + "%")])
        safe_plot_line(df, "year", "TFP_A", "Xu hướng TFP A_t")
        compare = df[["year", "GDP_trillion_VND", "Y_hat"]].melt(id_vars="year", var_name="Chỉ tiêu", value_name="GDP")
        safe_plot_line(compare, "year", "GDP", "GDP thực tế và GDP dự báo", color="Chỉ tiêu")
    with t4:
        show_df(decomp, "Phân rã tăng trưởng")
        safe_plot_bar(decomp, "factor", "share_of_growth_pct", "Tỷ trọng đóng góp vào tăng trưởng", text="share_of_growth_pct")
    with t5:
        show_df(forecast, "Dự báo 2030")
        download_df(forecast, "bai1_forecast2030.csv")
    with t6:
        discussion("bai1")

# ============================================================
# BÀI 2
# ============================================================
elif page == LESSON_META[2]["title"]:
    section_title(LESSON_META[2]["title"], "LP ngân sách số, shadow price và độ nhạy ngân sách")
    intro_box(2)
    base, duals, sens, h30 = main["Bai2_Base"], main["Bai2_Duals"], main["Bai2_Sensitivity"], supp["Bai2_H30"]
    t1, t2, t3, t4, t5 = st.tabs(["Mục tiêu & mô hình", "Nghiệm tối ưu", "Shadow price", "Độ nhạy", "Thảo luận"])
    with t1:
        model_summary("Tối đa hóa GDP kỳ vọng từ 4 hạng mục đầu tư: hạ tầng số, AI, nhân lực số và R&D trong ràng buộc ngân sách, mức sàn và tỷ trọng công nghệ chiến lược.")
    with t2:
        show_df(base, "Nghiệm cơ sở")
        alloc = base[["x_I", "x_AI", "x_H", "x_RD"]].T.reset_index()
        alloc.columns = ["Hạng mục", "Ngân sách"]
        safe_plot_bar(alloc, "Hạng mục", "Ngân sách", "Phân bổ ngân sách tối ưu", text="Ngân sách")
        show_df(h30, "Trường hợp ưu tiên nhân lực số x_H ≥ 30")
    with t3:
        show_df(duals, "Giá đối ngẫu và slack")
        safe_plot_bar(duals, "constraint", "shadow_price", "Shadow price của các ràng buộc", text="shadow_price")
    with t4:
        show_df(sens, "Độ nhạy ngân sách")
        safe_plot_line(sens, "B", "Z", "Đường cong Z*(B)")
    with t5:
        discussion("bai2")

# ============================================================
# BÀI 3
# ============================================================
elif page == LESSON_META[3]["title"]:
    section_title(LESSON_META[3]["title"], "Xếp hạng ngành bằng chỉ số Priority")
    intro_box(3)
    ranking, sens, policy = main["Bai3_Ranking"], main["Bai3_AI_Sensitivity"], main["Bai3_Policy_Weights"]
    t1, t2, t3, t4 = st.tabs(["Xếp hạng", "Độ nhạy AI", "So sánh trọng số", "Thảo luận"])
    with t1:
        show_df(ranking, "Bảng xếp hạng ngành")
        safe_plot_bar(ranking, "sector_name_vi", "Priority", "Priority Index theo ngành", text="Priority")
    with t2:
        show_df(sens, "Top 3 khi thay đổi trọng số AI")
    with t3:
        show_df(policy, "So sánh định hướng tăng trưởng và bao trùm")
        if {"sector_name_vi", "Priority_growth_oriented", "Priority_inclusive_oriented"}.issubset(policy.columns):
            plot_df = policy[["sector_name_vi", "Priority_growth_oriented", "Priority_inclusive_oriented"]].melt("sector_name_vi", var_name="Bộ trọng số", value_name="Priority")
            safe_plot_bar(plot_df, "sector_name_vi", "Priority", "So sánh Priority theo 2 bộ trọng số", color="Bộ trọng số", barmode="group")
    with t4:
        discussion("bai3")

# ============================================================
# BÀI 4
# ============================================================
elif page == LESSON_META[4]["title"]:
    section_title(LESSON_META[4]["title"], "Phân bổ ngân sách số theo 6 vùng")
    intro_box(4)
    fair, nofair = main["Bai4_With_Fairness"], main["Bai4_No_Fairness"]
    t1, t2, t3, t4 = st.tabs(["Có công bằng", "Không công bằng", "So sánh", "Thảo luận"])
    with t1:
        show_df(fair, "Nghiệm có ràng buộc công bằng")
        st.plotly_chart(px.imshow(fair.set_index("region_name")[["I", "D", "AI", "H"]], text_auto=True, aspect="auto", title="Heatmap phân bổ có công bằng"), use_container_width=True)
    with t2:
        show_df(nofair, "Nghiệm không có ràng buộc công bằng")
        st.plotly_chart(px.imshow(nofair.set_index("region_name")[["I", "D", "AI", "H"]], text_auto=True, aspect="auto", title="Heatmap phân bổ không công bằng"), use_container_width=True)
    with t3:
        comp = fair[["region_name", "Total"]].merge(nofair[["region_name", "Total"]], on="region_name", suffixes=("_fair", "_no_fair"))
        comp["diff_no_fair_minus_fair"] = comp["Total_no_fair"] - comp["Total_fair"]
        show_df(comp, "So sánh tổng ngân sách theo vùng")
        st.plotly_chart(px.bar(comp, x="region_name", y=["Total_fair", "Total_no_fair"], barmode="group", title="Có công bằng vs không công bằng"), use_container_width=True)
    with t4:
        discussion("bai4")

# ============================================================
# BÀI 5
# ============================================================
elif page == LESSON_META[5]["title"]:
    section_title(LESSON_META[5]["title"], "Danh mục dự án tối ưu theo ngân sách và rủi ro")
    intro_box(5)
    base80, base100, risk = main["Bai5_Selected_80k"], main["Bai5_Selected_100k"], main["Bai5_Risk_Adjusted"]
    force, no_p14 = supp["Bai5_Force_P1_P2"], supp["Bai5_No_P14_Required"]
    t1, t2, t3, t4, t5, t6 = st.tabs(["80k", "100k", "Bắt buộc P1-P2", "Điều chỉnh rủi ro", "Không bắt buộc P14", "Thảo luận"])
    for tab, df, title in [(t1, base80, "Ngân sách 80.000 tỷ"), (t2, base100, "Ngân sách 100.000 tỷ"), (t3, force, "Bắt buộc P1 & P2"), (t4, risk, "Tính theo lợi ích điều chỉnh rủi ro"), (t5, no_p14, "Không bắt buộc P14")]:
        with tab:
            show_df(df, title)
            quick_metrics(df, [("Số dự án", str(len(df))), ("Tổng chi phí", format_number(df["cost"].sum())), ("Tổng lợi ích", format_number(df["benefit"].sum()))])
            safe_plot_bar(df, "P", ["cost", "benefit"], f"Chi phí và lợi ích - {title}", barmode="group")
    with t6:
        discussion("bai5")

# ============================================================
# BÀI 6
# ============================================================
elif page == LESSON_META[6]["title"]:
    section_title(LESSON_META[6]["title"], "TOPSIS trọng số chuyên gia và Entropy")
    intro_box(6)
    topsis, sens = main["Bai6_TOPSIS"], main["Bai6_AI_Sensitivity"]
    t1, t2, t3, t4 = st.tabs(["Kết quả TOPSIS", "Biểu đồ", "Độ nhạy AI", "Thảo luận"])
    with t1:
        show_df(topsis, "Bảng TOPSIS")
    with t2:
        plot_df = topsis[["region_name_vi", "TOPSIS_expert", "TOPSIS_entropy"]].melt("region_name_vi", var_name="Phương pháp", value_name="Điểm")
        safe_plot_bar(plot_df, "region_name_vi", "Điểm", "So sánh điểm TOPSIS", color="Phương pháp", barmode="group")
    with t3:
        show_df(sens, "Top 3 khi thay đổi trọng số AI")
    with t4:
        discussion("bai6")

# ============================================================
# BÀI 7
# ============================================================
elif page == LESSON_META[7]["title"]:
    section_title(LESSON_META[7]["title"], "Biên Pareto và nghiệm thỏa hiệp")
    intro_box(7)
    pareto, compromise, alloc = adv["Bai7_Pareto"], adv["Bai7_Compromise"], adv["Bai7_Allocation"]
    t1, t2, t3, t4 = st.tabs(["Biên Pareto", "Nghiệm thỏa hiệp", "Phân bổ", "Thảo luận"])
    with t1:
        show_df(pareto, "Tập nghiệm Pareto", height=360)
        fig = px.scatter_3d(pareto, x="GDP_gain", y="Inequality_MAD", z="Emission", color="TOPSIS_compromise_score", title="Pareto 3D")
        st.plotly_chart(fig, use_container_width=True)
    with t2:
        show_df(compromise, "Nghiệm thỏa hiệp TOPSIS")
        row = compromise.iloc[0]
        quick_metrics(compromise, [("GDP gain", format_number(row["GDP_gain"])), ("Inequality", format_number(row["Inequality_MAD"])), ("Emission", format_number(row["Emission"])), ("TOPSIS", format_number(row["TOPSIS_compromise_score"]))])
    with t3:
        show_df(alloc, "Phân bổ tại nghiệm thỏa hiệp")
        safe_plot_bar(alloc, "region", ["I", "D", "AI", "H"], "Cơ cấu phân bổ theo vùng", barmode="stack")
    with t4:
        discussion("bai7")

# ============================================================
# BÀI 8
# ============================================================
elif page == LESSON_META[8]["title"]:
    section_title(LESSON_META[8]["title"], "Quỹ đạo tối ưu 2026-2035")
    intro_box(8)
    opt, shock, compare = adv["Bai8_Optimal_Path"], adv["Bai8_Shock_2028"], adv["Bai8_Strategy_Compare"]
    t1, t2, t3, t4, t5 = st.tabs(["Quỹ đạo tối ưu", "Cơ cấu đầu tư", "Cú sốc 2028", "So sánh chiến lược", "Thảo luận"])
    with t1:
        show_df(opt, "Optimal path")
        safe_plot_line(opt, "year", "Y", "GDP/Y theo quỹ đạo tối ưu")
    with t2:
        share_cols = ["share_K", "share_D", "share_AI", "share_H"]
        st.plotly_chart(px.area(opt, x="year", y=share_cols, title="Tỷ trọng đầu tư theo thời gian"), use_container_width=True)
    with t3:
        show_df(shock, "Kịch bản shock 2028")
        safe_plot_line(shock, "year", "Y", "GDP/Y khi có cú sốc 2028")
    with t4:
        show_df(compare, "So sánh chiến lược")
        safe_plot_bar(compare, "strategy", "welfare", "Welfare theo chiến lược", text="welfare")
    with t5:
        discussion("bai8")

# ============================================================
# BÀI 9
# ============================================================
elif page == LESSON_META[9]["title"]:
    section_title(LESSON_META[9]["title"], "AI, việc làm và đào tạo lại")
    intro_box(9)
    labor, threshold, feas, sankey = adv["Bai9_Labor_Result"], adv["Bai9_Threshold"], adv["Bai9_Feasibility"], adv["Bai9_Sankey"]
    t1, t2, t3, t4, t5 = st.tabs(["Kết quả lao động", "Biểu đồ", "Ngưỡng đào tạo", "Tính khả thi", "Thảo luận"])
    with t1:
        show_df(labor, "Kết quả theo ngành")
        quick_metrics(labor, [("NewJob", format_number(labor["NewJob"].sum())), ("UpgradeJob", format_number(labor["UpgradeJob"].sum())), ("DisplacedJob", format_number(labor["DisplacedJob"].sum())), ("NetJob", format_number(labor["NetJob"].sum()))])
    with t2:
        safe_plot_bar(labor, "sector", ["NewJob", "UpgradeJob", "DisplacedJob", "NetJob"], "Tác động việc làm theo ngành", barmode="group")
    with t3:
        show_df(threshold, "Ngưỡng đào tạo lại")
    with t4:
        show_df(feas, "Kiểm tra tính khả thi")
        show_df(sankey, "Dữ liệu Sankey")
    with t5:
        discussion("bai9")

# ============================================================
# BÀI 10
# ============================================================
elif page == LESSON_META[10]["title"]:
    section_title(LESSON_META[10]["title"], "Stochastic LP dưới bất định")
    intro_box(10)
    first, second, waitsee, vss = adv["Bai10_First_Stage"], adv["Bai10_Second_Stage"], adv["Bai10_Wait_See"], adv["Bai10_VSS_EVPI"]
    t1, t2, t3, t4, t5 = st.tabs(["First-stage", "Second-stage", "Wait-and-see", "VSS/EVPI", "Thảo luận"])
    with t1:
        show_df(first, "Quyết định giai đoạn 1")
        safe_plot_bar(first, "item", "first_stage_x", "First-stage allocation", text="first_stage_x")
    with t2:
        show_df(second, "Quyết định giai đoạn 2 theo kịch bản")
        safe_plot_bar(second, "scenario", ["I", "D", "AI", "H"], "Second-stage theo kịch bản", barmode="stack")
    with t3:
        show_df(waitsee, "Wait-and-see")
        safe_plot_bar(waitsee, "scenario", "scenario_value", "Giá trị theo kịch bản", text="scenario_value")
    with t4:
        show_df(vss, "VSS và EVPI")
    with t5:
        discussion("bai10")

# ============================================================
# BÀI 11
# ============================================================
elif page == LESSON_META[11]["title"]:
    section_title(LESSON_META[11]["title"], "Q-learning cho chính sách thích nghi")
    intro_box(11)
    qpol, pcomp, curve = adv["Bai11_Q_Policy"], adv["Bai11_Policy_Compare"], adv["Bai11_Learning_Curve"]
    t1, t2, t3, t4 = st.tabs(["Chính sách Q-learning", "So sánh chính sách", "Learning curve", "Thảo luận"])
    with t1:
        show_df(qpol, "Chính sách học được theo trạng thái")
        safe_plot_bar(qpol, "state_name", "Q_value", "Q-value theo trạng thái", color="best_action", text="Q_value")
    with t2:
        show_df(pcomp, "So sánh chính sách")
        safe_plot_bar(pcomp, "policy", "avg_total_reward", "Average total reward", text="avg_total_reward")
    with t3:
        show_df(curve.head(300), "300 episode đầu tiên", height=280)
        safe_plot_line(curve, "episode", "rolling_reward_200", "Đường học rolling reward 200 episode")
    with t4:
        discussion("bai11")

# ============================================================
# BÀI 12
# ============================================================
elif page == LESSON_META[12]["title"]:
    section_title(LESSON_META[12]["title"], "Dashboard tích hợp kịch bản, KPI và cảnh báo rủi ro")
    intro_box(12)
    path, kpi, risk = adv["Bai12_Scenario_Path"], adv["Bai12_KPI_2030"], adv["Bai12_Risk_Warning"]
    t1, t2, t3, t4, t5 = st.tabs(["Tổng quan hệ thống", "Đường kịch bản", "KPI 2030", "Cảnh báo rủi ro", "Thảo luận"])
    with t1:
        model_summary("Bài 12 tích hợp kết quả từ các mô hình trước thành dashboard AIDEOM-VN. Người xem có thể so sánh các kịch bản phát triển và nhận diện rủi ro về an ninh mạng, khoảng cách số và thiếu nhân lực.")
        quick_metrics(kpi, [("Số kịch bản", str(kpi["scenario"].nunique())), ("GDP_index cao nhất", format_number(kpi["GDP_index"].max())), ("D cao nhất", format_number(kpi["D"].max())), ("AI cao nhất", format_number(kpi["AI"].max()))])
    with t2:
        show_df(path, "Đường phát triển kịch bản")
        safe_plot_line(path, "year", "GDP_index", "GDP_index theo kịch bản", color="scenario")
    with t3:
        show_df(kpi, "KPI năm 2030")
        safe_plot_bar(kpi, "scenario", "GDP_index", "GDP_index năm 2030", color="scenario", text="GDP_index")
        radar_cols = ["GDP_index", "D", "AI", "H", "A"]
        radar_df = kpi.copy()
        for c in radar_cols:
            maxv = radar_df[c].max()
            radar_df[c] = radar_df[c] / maxv if maxv else radar_df[c]
        fig = go.Figure()
        for _, row in radar_df.iterrows():
            fig.add_trace(go.Scatterpolar(r=[row[c] for c in radar_cols], theta=radar_cols, fill='toself', name=row['scenario']))
        fig.update_layout(title="Radar chuẩn hóa KPI 2030", polar=dict(radialaxis=dict(visible=True, range=[0,1])), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    with t4:
        show_df(risk, "Cảnh báo rủi ro")
        for _, row in risk.iterrows():
            st.markdown(f"""
            <div class="mini-card">
                <h4>{row['scenario']}</h4>
                <p><b>Cyber risk:</b> {row['cyber_risk']} | <b>Digital gap:</b> {row['digital_gap_risk']} | <b>Nhân lực:</b> {row['human_capital_status']}</p>
            </div>
            """, unsafe_allow_html=True)
    with t5:
        discussion("bai12")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("AIDEOM-VN Dashboard | Streamlit | Hiển thị theo từng bài 1-12")
