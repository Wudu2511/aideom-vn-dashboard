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
    page_icon="🇻🇳 🗂",
    layout="wide"
)
# =========================
# ACADEMIC BLUE THEME
# =========================
st.markdown(
    """
    <style>
/* ===== FONT & GLOBAL ===== */
html, body, .stApp, .stMarkdown, .stText, .stDataFrame {
    font-family: "Times New Roman", Times, serif !important;
    font-size: 15px;
}

.stApp {
    background: linear-gradient(135deg, #F7F9FC 0%, #EAF3FF 100%);
    color: #1F2933;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2.6rem;
    max-width: 1350px;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102542 0%, #153B5C 100%);
    border-right: 1px solid rgba(255,255,255,0.12);
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] label {
    font-size: 14px !important;
    font-weight: 700 !important;
}

div[data-testid="stSidebarNav"] {
    background-color: transparent;
}

/* Radio options in sidebar */
div[role="radiogroup"] label {
    padding: 7px 9px;
    border-radius: 10px;
    margin-bottom: 3px;
    font-size: 14px !important;
}

div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.12);
}

/* ===== HEADINGS ===== */
h1 {
    color: #102542;
    font-weight: 700;
    letter-spacing: -0.2px;
    font-size: 26px !important;
}

h2 {
    color: #153B5C;
    font-weight: 700;
    font-size: 22px !important;
}

h3 {
    color: #153B5C;
    font-weight: 700;
    font-size: 19px !important;
}

h4 {
    color: #153B5C;
    font-weight: 700;
    font-size: 17px !important;
}

/* ===== MARKDOWN TEXT ===== */
.stMarkdown p {
    font-size: 15px;
    line-height: 1.65;
    text-align: justify;
    color: #1F2933;
}

.stMarkdown li {
    font-size: 15px;
    line-height: 1.6;
    color: #1F2933;
}

.stMarkdown strong {
    color: #102542;
}

/* ===== TITLE CARD ===== */
.title-card {
    background: #FFFFFF;
    padding: 20px 24px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 6px 18px rgba(16, 37, 66, 0.08);
    border: 1px solid #E5E7EB;
    border-left: 5px solid #2F80ED;
}

.title-card h1 {
    margin: 0 0 8px 0;
    color: #102542;
    font-size: 26px !important;
    line-height: 1.25;
}

.title-card p {
    margin: 0;
    color: #64748B;
    font-size: 15px;
    line-height: 1.55;
}

/* ===== INSIGHT BOX ===== */
.insight-box {
    background: #EAF3FF;
    border-left: 5px solid #2F80ED;
    padding: 14px 18px;
    border-radius: 13px;
    margin: 12px 0 20px 0;
    color: #102542;
    font-size: 15px;
    line-height: 1.6;
    box-shadow: 0 4px 12px rgba(16, 37, 66, 0.06);
}

/* ===== METRIC CARDS ===== */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 14px 16px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(16, 37, 66, 0.08);
    border: 1px solid #E5E7EB;
}

div[data-testid="stMetricLabel"] {
    font-size: 14px;
    font-weight: 700;
    color: #64748B;
}

div[data-testid="stMetricValue"] {
    font-size: 22px;
    font-weight: 700;
    color: #102542;
}

/* ===== TABS ===== */
button[data-baseweb="tab"] {
    font-size: 14px;
    font-weight: 700;
    background-color: #FFFFFF;
    border-radius: 12px 12px 0 0;
    padding: 8px 14px;
    color: #153B5C;
    border: 1px solid #E5E7EB;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
    background-color: #2F80ED !important;
    border-color: #2F80ED !important;
}

/* ===== DATAFRAME ===== */
div[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 16px rgba(16, 37, 66, 0.08);
    border: 1px solid #E5E7EB;
    background: white;
    font-size: 14px !important;
}

/* ===== PLOTLY CHART ===== */
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    padding: 12px;
    border-radius: 16px;
    box-shadow: 0 5px 16px rgba(16, 37, 66, 0.08);
    border: 1px solid #E5E7EB;
    margin-top: 12px;
    margin-bottom: 20px;
}

/* ===== INFO / WARNING BOXES ===== */
div[data-testid="stAlert"] {
    border-radius: 13px;
    font-size: 15px;
    line-height: 1.6;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background-color: #2F80ED;
    color: #FFFFFF;
    border-radius: 11px;
    border: none;
    padding: 8px 18px;
    font-weight: 700;
    font-size: 14px;
    box-shadow: 0 4px 12px rgba(47, 128, 237, 0.25);
}

.stButton > button:hover {
    background-color: #1C64C7;
    color: #FFFFFF;
}

/* ===== EXPANDERS ===== */
.streamlit-expanderHeader {
    font-size: 15px;
    font-weight: 700;
    color: #102542;
}

/* ===== SMALL CAPTION ===== */
.caption-text {
    color: #64748B;
    font-size: 14px;
    margin-top: -6px;
    margin-bottom: 12px;
}

/* ===== FIX STREAMLIT ICONS ===== */
.material-symbols-rounded,
.material-symbols-outlined,
.material-icons,
span[class*="material"],
i[class*="material"],
button span[class*="material"],
[data-testid="collapsedControl"] *,
[data-testid="stToolbar"] * {
    font-family: "Material Symbols Rounded", "Material Icons" !important;
    font-weight: normal !important;
    font-style: normal !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    line-height: 1 !important;
    -webkit-font-feature-settings: "liga" !important;
    font-feature-settings: "liga" !important;
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
BAI9_FILE = DATA_DIR / "ket_qua_bai9_chay_lai.xlsx"
@st.cache_data
def load_excel(file_path: Path):
    return pd.read_excel(file_path, sheet_name=None)


def require_file(path: Path):
    if not path.exists():
        st.error(f"Không tìm thấy file: {path}. Hãy upload file này vào thư mục data trên GitHub.")
        st.stop()


for file in [MAIN_FILE, SUPP_FILE, ADV_FILE, BAI9_FILE]:
    require_file(file)

main = load_excel(MAIN_FILE)
supp = load_excel(SUPP_FILE)
adv = load_excel(ADV_FILE)
bai9_new = load_excel(BAI9_FILE)

# =========================
# HELPERS
# =========================
def section_title(title, subtitle=None):
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="title-card">
            <h1>{title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True
    )

def show_df(df, title=None):
    if title:
        st.subheader(title)
    st.dataframe(df, use_container_width=True)


# =========================
# DISCUSSIONS
# =========================
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

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 14px 4px 22px 4px;">
        <div style="
            background: rgba(255,255,255,0.12);
            border-radius: 18px;
            padding: 16px 12px;
            border: 1px solid rgba(255,255,255,0.18);
        ">
            <h2 style="margin: 0; color: white;">AIDEOM-VN</h2>
            <p style="
                margin-top: 8px;
                color: #CBD5E1;
                font-size: 15px;
                line-height: 1.45;
            ">
                Bài tập 1-12
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Chọn nội dung",
    [
        "Tổng quan",
        "Bài 1 - Hàm sản xuất mở rộng",
        "Bài 2 - Phân bổ ngân sách",
        "Bài 3 - Ưu tiên ngành",
        "Bài 4 - Phân bổ theo vùng",
        "Bài 5 - Lựa chọn dự án",
        "Bài 6 - Xếp hạng vùng bằng TOPSIS",
        "Bài 7 - Tối ưu đa mục tiêu",
        "Bài 8 - Tối ưu động",
        "Bài 9 - Lao động và AI",
        "Bài 10 - Quy hoạch ngẫu nhiên",
        "Bài 11 - Học tăng cường",
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

    with col1:
        st.markdown(
            """
            <div style="
                background: #FFFFFF;
                padding: 16px 18px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(16, 37, 66, 0.08);
                border: 1px solid #E5E7EB;
                min-height: 105px;
            ">
                <div style="font-size: 14px; font-weight: 700; color: #64748B;">
                    Số bài đã hoàn thiện
                </div>
                <div style="font-size: 26px; font-weight: 700; color: #102542; margin-top: 8px;">
                    12/12
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="
                background: #FFFFFF;
                padding: 16px 18px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(16, 37, 66, 0.08);
                border: 1px solid #E5E7EB;
                min-height: 105px;
            ">
                <div style="font-size: 14px; font-weight: 700; color: #64748B;">
                    Nhóm mô hình
                </div>
                <div style="font-size: 22px; font-weight: 700; color: #102542; margin-top: 8px; line-height: 1.35;">
                    LP, MIP, TOPSIS,<br>
                    NSGA-II, RL
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div style="
                background: #FFFFFF;
                padding: 16px 18px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(16, 37, 66, 0.08);
                border: 1px solid #E5E7EB;
                min-height: 105px;
            ">
                <div style="font-size: 14px; font-weight: 700; color: #64748B;">
                    Dữ liệu
                </div>
                <div style="font-size: 26px; font-weight: 700; color: #102542; margin-top: 8px;">
                    Việt Nam 2020-2035
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write(
        """
        Dashboard trình bày kết quả định lượng, bảng, biểu đồ và thảo luận chính sách cho 12 bài.
        Các kết quả được đọc từ 3 file Excel trong thư mục `data`.
        """
    )

elif page == "Bài 1 - Hàm sản xuất mở rộng":
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

elif page == "Bài 2 - Phân bổ ngân sách":
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

elif page == "Bài 4 - Phân bổ theo vùng":
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

elif page == "Bài 6 - Xếp hạng vùng bằng TOPSIS":
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

elif page == "Bài 7 - Tối ưu đa mục tiêu":
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
    sankey = bai9_new["Bai9_Sankey_Potential"]
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
        st.subheader("Nguy cơ lao động bị ảnh hưởng bởi tự động hóa")

        sankey = bai9_new["Bai9_Sankey_Potential"].copy()
        sankey["value"] = pd.to_numeric(sankey["value"], errors="coerce").fillna(0)

        show_df(sankey, "Dữ liệu nguy cơ tiềm năng")

        fig = px.bar(
            sankey,
            x="value",
            y="target",
            orientation="h",
            text="value",
            title="Nguy cơ lao động bị ảnh hưởng bởi tự động hóa theo nhóm dễ tổn thương")

        fig.update_traces(
            texttemplate="%{text:.3f} triệu lao động",
            textposition="outside"
            )

        fig.update_layout(
            xaxis_title="Số lao động có nguy cơ bị ảnh hưởng, triệu người",
            yaxis_title="Nhóm ngành",
            height=420,
            showlegend=False,
            margin=dict(l=20, r=100, t=70, b=40)
            )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            <div class="insight-box">
            Biểu đồ trên không phải là nghiệm tối ưu trực tiếp của mô hình, mà là kịch bản nguy cơ tiềm năng.
            Trong nghiệm tối ưu, mô hình ưu tiên đào tạo lại nên DisplacedJob bằng 0, khiến Sankey gốc không có luồng để hiển thị.
            </div>
            """,
            unsafe_allow_html=True
        )

    with tab5:
        st.subheader("Thảo luận chính sách")
        st.markdown(DISCUSSIONS["bai9"])

elif page == "Bài 10 - Quy hoạch ngẫu nhiên":
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

elif page == "Bài 11 - Học tăng cường":
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Đường kịch bản", "KPI năm 2030", "Cảnh báo rủi ro", "Thảo luận chính sách", "Khuyến nghị chính sách"]) 
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
    with tab5:
        st.subheader("Khuyến nghị chính sách tổng hợp")

        st.success(
            "Kịch bản S5 - Tối ưu cân bằng được khuyến nghị vì dung hòa giữa tăng trưởng GDP, "
            "chuyển đổi số, phát triển AI, nhân lực số và kiểm soát rủi ro."
        )

        st.markdown(
            """
            Từ kết quả mô hình AIDEOM-VN, có thể rút ra một số khuyến nghị chính sách chính:

            1. **Không nên chỉ ưu tiên tăng trưởng GDP**, mà cần kết hợp mục tiêu tăng trưởng với công bằng vùng miền, nhân lực số và an ninh dữ liệu.

            2. **Đầu tư AI cần đi kèm đào tạo nhân lực số**, vì nếu thiếu nhân lực, AI khó tạo ra tác động lan tỏa bền vững.

            3. **Chuyển đổi số nên là nền tảng trước khi mở rộng AI quy mô lớn**, đặc biệt ở các vùng có năng lực hấp thụ công nghệ còn thấp.

            4. **Cần kiểm soát rủi ro an ninh mạng và khoảng cách số**, vì output cảnh báo các kịch bản đều có rủi ro liên quan đến dữ liệu, nhân lực và chênh lệch vùng.

            5. **Dashboard AIDEOM-VN nên được dùng như công cụ hỗ trợ ra quyết định**, không thay thế quyết định chính sách của con người.
            """
        )
