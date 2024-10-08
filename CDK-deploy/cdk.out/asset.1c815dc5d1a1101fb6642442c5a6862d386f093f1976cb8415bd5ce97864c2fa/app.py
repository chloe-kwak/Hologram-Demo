import streamlit as st
import bedrock as glib
import os

st.set_page_config(layout="wide", page_title="홀로그램 디스플레이")
st.title("상품 홀로그램 디스플레이")

# 작업 선택
selected_task = st.radio("작업 선택", ("작업 화면", "디스플레이 화면"), horizontal=True, label_visibility="collapsed")
st.markdown("---")  # 구분선 추가


if 'final_description' not in st.session_state:
    st.session_state.final_description = ""
    
# 선택된 작업에 따른 화면 표시
if selected_task == "작업 화면":
    st.header("파일 업로드")
    
    uploaded_file = st.file_uploader("파일을 여기에 드래그 앤 드롭하세요", type=['jpg', 'jpeg', 'png'])
    st.caption("파일당 최대 200MB  JPG, JPEG, PNG 형식 지원")
    
    # 이미지 속성 추출 결과 저장 변수
    image_attributes = ""
    
    if uploaded_file:
        file_details = f"{uploaded_file.name} ({uploaded_file.size / 1e6:.1f} MB)"
        st.write(file_details)
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, width=400)  # 이미지 너비를 400픽셀로 설정 (필요에 따라 조정 가능)
        
        st.header("이미지 속성 추출하기")      
        st.caption("업로드된 파일에서 이미지 속성을 추출하고 설명을 생성합니다")
        
        with st.spinner('이미지 속성을 추출 중입니다...'):
            image_bytes = uploaded_file.getvalue()
            
            prompt_text = "자세하게 이미지의 속성과 해당 속성에 대한 설명을 한글로 제공하세요"
            image_attributes = glib.get_response_from_model(
                prompt_content = prompt_text,
                image_bytes = image_bytes
            )
            
            st.write(image_attributes)
    else:
        st.info("이미지를 업로드하면 자동으로 속성 추출이 시작됩니다.")

    
    st.header("사용자 정의하기")
    st.caption("인구통계학적 분류나 브랜드 스타일을 선택합니다 ")
    
    demo_options_dict = {
    "패밀리맨": "중년의 근로계층으로 1-3명의 자녀가 있습니다. 품질과 가치를 중요하게 여깁니다. 품질을 위해서는 약간의 추가 비용을 지불할 의향이 있지만, 브랜드에 크게 영향을 받지는 않습니다. 소박한 자동차를 운전하며, 가끔 이국적인 목적지로 휴가를 떠납니다.",
    "실버라이프": "더 이상 일하지 않으며 자녀들은 독립했습니다. 은퇴 생활을 즐기고 인생의 결실을 만끽하고자 합니다. 여행, 새로운 경험, 취미 활동을 즐깁니다. 때때로 큰 구매를 하는데, 주로 선물용입니다. 실용적인 자동차를 운전하고 소박한 옷을 입습니다. 유행에는 관심이 없으며, 검증된 것들을 선호합니다.",
    "MZ세대": "자녀가 없는 젊은 도시 전문직으로, 재미있는 경험을 추구합니다. 최고의 브랜드에 매우 관심이 있으며 품질을 위해 추가 비용을 지불할 의향이 있습니다. 고급 자동차를 운전하고, 비싼 옷을 입으며, 자신을 과시하고 싶어 합니다. 주중에는 열심히 일하고 주말에는 열정적으로 놀기를 즐깁니다. 고품질의 음식, 레시피, 레스토랑에 관심이 많습니다. 때때로 충동적이며 친구들의 영향을 쉽게 받습니다.",
    }
    
    brand_options_dict = {
    "실속":"가치에 초점을 맞추어, 소비자들이 좋은 거래를 찾고 돈을 절약하는 데 도움을 줍니다. 지출을 최소화하려는 쇼핑객들에게 어필하며, 최저 가격, 가장 다양한 선택, 그리고 돈 대비 최고의 전반적인 가치를 강조합니다.",
    "개성추구":"독특하고, 대담하며, 재미있는 특징을 가집니다. 경계를 넘어서려 하며, 브랜드의 새롭고 세련된 디자인을 예상치 못한 장난스러운 방식으로 표현하는 것을 목표로 합니다. 강력하고 스타일리시한 언어 사용을 장려하고, 혁신적이고 비관습적인 아이디어를 수용하며, 활기차고 젊은 정신을 표현합니다. 클리셰(진부한 표현), 형식주의, 그리고 유행에 휩쓸리는 것을 피하고자 합니다.",
    "신뢰":"자신감 있고, 솔직하며, 믿음직스러운 특징을 가집니다. 브랜드의 제품 품질과 가치에 대해 권위와 전문성을 가지고 소통하여 고객에게 신뢰를 심어줍니다. 전문적이면서도 친근한 음성으로, 소비자와 개인적인 수준에서 연결됩니다."
    }
    
    option_key1 = st.radio("고객 그룹", demo_options_dict, label_visibility="visible")
    option_value1 = demo_options_dict[option_key1]
   
    prompt_text = st.text_area("고객 그룹",
        value=option_value1,
        height=100,
        label_visibility="collapsed")
    
    option_key2 = st.radio("브랜드 스타일", brand_options_dict, label_visibility="visible")
    option_value2 = brand_options_dict[option_key2]

    prompt_text = st.text_area("브랜드 스타일",
        value=option_value2,
        height=100,
        label_visibility="collapsed")
        
    st.header("최종 디스플레이 ")
    st.caption("홀로그램 디스플레이에 보여질 제품 설명입니다")

    if uploaded_file and option_key1 and option_key2:
        if st.button("홀로그램 디스플레이 설명 생성"):
            with st.spinner('최종 제품 설명을 생성합니다...'):
                final_prompt = f"""
                다음 정보를 바탕으로 홀로그램 디스플레이에 보여질 제품 설명을 생성해주세요:

                1. 이미지 속성:
                {image_attributes}

                2. 고객 그룹: {option_key1}
                {demo_options_dict[option_key1]}

                3. 브랜드 스타일: {option_key2}
                {brand_options_dict[option_key2]}

                위의 정보를 종합하여, 선택된 고객 그룹과 브랜드 스타일에 맞는 제품 설명을 500자 이내로 작성해주세요. 
                설명은 홀로그램 디스플레이에 표시될 것이므로, 시각적으로 흥미롭고 간결하면서도 정보가 풍부해야 합니다.
                """

                final_response = glib.get_response_from_model(
                    prompt_content = final_prompt,
                    image_bytes = image_bytes  # 이미지를 다시 한 번 전달
                )
                
                st.session_state.final_description = final_response
                st.write(st.session_state.final_description)
    else:
        st.warning("이미지를 업로드하고 고객 그룹과 브랜드 스타일을 선택한 후 버튼을 클릭해주세요.")
    

elif selected_task == "디스플레이 화면":
    st.header("Industry Week Special Offer")
    
   # 비디오 업로드 부분
    uploaded_video = st.file_uploader("홀로그램 디스플레이용 비디오를 업로드하세요", type=['mp4', 'mov', 'avi', 'webm'])
    
    if uploaded_video is not None:
        st.video(uploaded_video)
    else:
        st.warning("비디오를 업로드해주세요.")
    
    # 작업 화면에서 생성된 설명 표시
    st.subheader("제품 설명")
    if st.session_state.final_description:
        st.write(st.session_state.final_description)
    else:
        st.write("아직 생성된 제품 설명이 없습니다. 작업 화면에서 설명을 생성해주세요.")
