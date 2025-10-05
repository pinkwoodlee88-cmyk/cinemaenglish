import streamlit as st
from google import genai
from google.genai.errors import APIError

# --- 앱 설정 ---
st.set_page_config(
    page_title="Gemini 일일 영어 학습 앱",
    layout="wide"
)

st.title("🎬 Gemini 일일 생활 영어 대화")
st.markdown("영화 한 장면 같은 생생한 대화로 오늘 하루 영어 공부를 시작해 보세요!")

# --- 1. API 키 입력 처리 ---
st.sidebar.header("🔑 Gemini API Key 입력")
# st.text_input을 사용하여 사용자로부터 API 키를 안전하게 입력받습니다.
api_key = st.sidebar.text_input(
    "여기에 API 키를 입력하고 Enter를 누르세요.",
    type="password",
    key="gemini_api_key_input"
)

if not api_key:
    st.warning("왼쪽 사이드바에 Gemini API 키를 입력해 주세요.")
else:
    try:
        # API 키로 클라이언트 초기화 시도
        client = genai.Client(api_key=api_key)
        
        # --- 2. Gemini 프롬프트 정의 ---
        # 구체적인 프롬프트를 통해 원하는 형태의 응답 유도
        system_prompt = (
            "당신은 사용자에게 매일 영화 한 장면의 일상적인 생활 영어를 제시하는 유능한 영어 교사입니다. "
            "응답은 반드시 아래 형식으로만 작성해 주세요:\n"
            "1. **대화**: 두 사람(A와 B)의 짧은 대화문 3~4줄.\n"
            "2. **한국어 해석**: 대화 내용의 자연스러운 한국어 해석.\n"
            "3. **핵심 표현**: 대화에서 배울 만한 주요 표현 1~2가지와 그 예시.\n"
            "4. **발음 팁**: 발음이나 억양 관련 팁 1가지."
        )

        user_prompt = "오늘의 일상생활 영어 대화문을 영화 속 한 장면처럼 랜덤하게 제시해 주세요."
        
        # --- 3. 영어 대화 생성 버튼 ---
        if st.button("✨ 오늘의 대화 생성"):
            st.info("Gemini AI가 오늘의 대화를 생성 중입니다... 잠시만 기다려 주세요.")
            
            try:
                # Gemini API 호출 (gemini-2.5-flash 권장)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[{"role": "user", "parts": [{"text": user_prompt}]}],
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.7 # 창의적인 대화를 위해 온도 설정
                    )
                )

                # 응답 결과 표시
                st.subheader("📝 오늘의 생활 영어 대화")
                st.markdown(response.text)
                
                # 추가 학습 제안
                st.markdown("---")
                st.subheader("💡 추가 학습 제안")
                st.write("이 대화문을 소리 내어 읽고, 친구와 역할극을 해보세요!")
                
            except APIError as e:
                st.error(f"Gemini API 호출 중 오류가 발생했습니다: {e}")
                st.error("API 키가 올바른지, 사용량 제한에 걸리지는 않았는지 확인해 주세요.")
            except Exception as e:
                st.error(f"예상치 못한 오류가 발생했습니다: {e}")
                
    except Exception:
        # API 키 자체 문제로 초기화 실패 시 (예: 잘못된 포맷 등)
        st.error("입력된 API 키가 유효하지 않거나 문제가 있습니다. 다시 확인해 주세요.")
