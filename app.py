import streamlit as st
import hashlib

# 核心資安升級：從系統環境變數讀取金鑰，不把密碼寫死在程式碼中
try:
    TEAM_SECRET_SALT = st.secrets["TEAM_SECRET_SALT"]
except KeyError:
    st.error("系統錯誤：找不到安全金鑰，請聯繫系統管理員。")
    st.stop()

def generate_patient_id(mrn: str, salt: str) -> str:
    mrn_clean = str(mrn).strip()
    if not mrn_clean:
        return ""
    combined_string = f"{mrn_clean}_{salt}"
    hash_object = hashlib.sha256(combined_string.encode('utf-8'))
    unique_id = hash_object.hexdigest()[:6].upper()
    return unique_id

st.title("🛡️ 臨床個案匿名轉換器")
st.markdown("請輸入病歷號，產生的 6 碼代號可用於外部資料庫追蹤。")

mrn_input = st.text_input("病歷號碼 (MRN)", type="password")

if st.button("產生專屬代碼"):
    if mrn_input:
        safe_id = generate_patient_id(mrn_input, TEAM_SECRET_SALT)
        st.success(f"該病人的專屬代碼為：**{safe_id}**")
        st.info("請複製上述代碼至共用資料庫建檔或搜尋。")
    else:
        st.warning("請先輸入病歷號碼")