import streamlit as st
import hashlib

# 從 Streamlit 系統環境變數讀取金鑰
try:
    TEAM_SECRET_SALT = st.secrets["TEAM_SECRET_SALT"]
except KeyError:
    st.error("系統錯誤：找不到安全金鑰，請聯繫系統管理員。")
    st.stop()

def generate_patient_id(mrn: str, salt: str) -> str:
    mrn_clean = str(mrn).strip()
    
    # 【新增防呆機制】檢查是否剛好為 7 碼，且全部都是數字
    if len(mrn_clean) != 7 or not mrn_clean.isdigit():
        return "ERROR_FORMAT"
        
    combined_string = f"{mrn_clean}_{salt}"
    hash_object = hashlib.sha256(combined_string.encode('utf-8'))
    unique_id = hash_object.hexdigest()[:6].upper()
    return unique_id

st.title("🛡️ 臨床個案匿名轉換器")
st.markdown("請輸入 **7 碼** 病歷號，產生的 6 碼代號可用於外部資料庫追蹤。")

# 【新增限制】限制輸入框最多只能輸入 7 個字元
mrn_input = st.text_input("病歷號碼 (MRN)", type="password", max_chars=7)

if st.button("產生專屬代碼"):
    if mrn_input:
        safe_id = generate_patient_id(mrn_input, TEAM_SECRET_SALT)
        
        # 根據回傳結果給予對應提示
        if safe_id == "ERROR_FORMAT":
            st.error("格式錯誤：請確保輸入的是完整的「7 碼數字」病歷號。")
        else:
            st.success(f"該病人的專屬代碼為：**{safe_id}**")
            st.info("請複製上述代碼至 Notion 資料庫建檔或搜尋。")
    else:
        st.warning("請先輸入病歷號碼")
