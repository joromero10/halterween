import streamlit as st 

# title of the screen
st.set_page_config(page_title= "AI Stylist",
                   page_icon= "👗",
                   layout= "wide")
st.title("👗Halterween")
st.caption("Need ideas for a halloween costume? Type in your vision and I will send you recommendations based on your budget, wardrobe, & avalible time")

# input section

with st.form("costume_form"):
    st.subheader("Choose your ideas 🗩 ")
    idea = st.text_area("Describe your idea", placeholder= "eg. I have a black shirt and brown pants. that will not take me too much time putting together ")
    location = st.text_input("📍 Location")
    col1, col2 = st.columns(2)

    with col1:
         budget = st.number_input("🪙 Budget ($), min: 1 max: 500 ", min_value= 0, max_value= 500, value= 5)

    with col2: 
         style = st.selectbox("🪄Preferred Style", ["Scary", "Funny", "Classic Halloween", "Unique"])

    submitted = st.form_submit_button(label="Submit", help="Generate Your Costume")

# once it's submitted

if submitted:
    if not idea or not location:
              st.error("Please fill in all the required fields!!")
              st.stop()    
    else:
        st.success("🤓 Generating you ideal Costume....")
        st.write("My idea:", idea)
        st.write("Location:", location)
        st.write("Budget:", budget)
        st.write("Style:", style)

      