import streamlit as st
import hashlib

# 讀取環境變數 (包含加密金鑰與網頁進入密碼)
try:
    TEAM_SECRET_SALT = st.secrets["TEAM_SECRET_SALT"]
    APP_PASSWORD = st.secrets["APP_PASSWORD"]
except KeyError:
    st.error("系統錯誤：找不到安全設定，請聯繫系統管理員。")
    st.stop()

st.title("🛡️ 臨床個案匿名轉換器")

# ================= 網頁密碼鎖 =================
user_password = st.text_input("🔒 請輸入團隊專屬密碼以解鎖", type="password")

if user_password != APP_PASSWORD:
    st.warning("請輸入正確密碼。")
    st.stop()  # 密碼錯誤時，程式會在這裡停止，完全不顯示下方的轉換器

# ================= 原本的轉換器 =================
st.success("解鎖成功！")
st.markdown("請輸入 **7 碼** 病歷號，產生的 6 碼代號可用於外部資料庫追蹤。")

mrn_input = st.text_input("病歷號碼 (MRN)", type="password", max_chars=7)

def generate_patient_id(mrn: str, salt: str) -> str:
    mrn_clean = str(mrn).strip()
    if len(mrn_clean) != 7 or not mrn_clean.isdigit():
        return "ERROR_FORMAT"
    combined_string = f"{mrn_clean}_{salt}"
    hash_object = hashlib.sha256(combined_string.encode('utf-8'))
    return hash_object.hexdigest()[:6].upper()

if st.button("產生專屬代碼"):
    if mrn_input:
        safe_id = generate_patient_id(mrn_input, TEAM_SECRET_SALT)
        if safe_id == "ERROR_FORMAT":
            st.error("格式錯誤：請確保輸入的是完整的「7 碼數字」。")
        else:
            st.success(f"該病人的專屬代碼為：**{safe_id}**")
            st.info("請複製上述代碼至 Notion 資料庫建檔。")
    else:
        st.warning("請先輸入病歷號碼")
