import streamlit as st
import requests
import json
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="mIAm - Recipe Assistant",
    page_icon="🍲",
    layout="wide"
)

# --- Session State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "current_recipe" not in st.session_state:
    st.session_state.current_recipe = None
    
if "shopping_list" not in st.session_state:
    st.session_state.shopping_list = []

# --- Styling ---
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 20px;
    }
    .recipe-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .shopping-item {
        padding: 8px;
        border-bottom: 1px solid #eee;
        display: flex;
        justify-content: space-between;
    }
    .chat-container {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def send_message_to_backend(message):
    """
    Send user message to backend and get response
    In a real app, this would be an API call to your backend
    """
    # Mock API call for now
    # Replace with actual API call when backend is ready
    try:
        # Example: response = requests.post("http://your-backend-api/chat", json={"message": message})
        # For now, return a mock response
        if "recipe" in message.lower():
            return {
                "message": "I found a pasta recipe you might like!",
                "recipe": {
                    "title": "Spaghetti Carbonara",
                    "ingredients": ["200g spaghetti", "100g pancetta", "2 eggs", "50g parmesan", "Black pepper"],
                    "instructions": "1. Cook pasta\n2. Fry pancetta\n3. Mix eggs and cheese\n4. Combine everything"
                }
            }
        elif "shopping" in message.lower():
            return {
                "message": "I can help with your shopping list. What would you like to add?",
                "shopping_items": []
            }
        else:
            return {"message": "How can I help you with recipes or shopping today?"}
    except Exception as e:
        return {"message": f"Sorry, I encountered an error: {str(e)}"}

def add_to_shopping_list(item):
    """Add an item to the shopping list"""
    if item and item not in [i["name"] for i in st.session_state.shopping_list]:
        st.session_state.shopping_list.append({
            "name": item,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed": False
        })

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("## mIAm 🍲")
    st.markdown("Your personal recipe assistant")
    
    selected_page = st.radio(
        "Navigation",
        ["Chat", "My Recipes", "Shopping List"]
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("mIAm helps you find recipes and organize your grocery shopping.")

# --- Main Content Area ---
if selected_page == "Chat":
    st.markdown("<h1 class='main-title'>Talk to mIAm</h1>", unsafe_allow_html=True)
    
    # Display chat messages
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask me about recipes or grocery shopping..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response from backend
        response_data = send_message_to_backend(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response_data["message"])
            
            # If response contains a recipe, store and display it
            if "recipe" in response_data:
                st.session_state.current_recipe = response_data["recipe"]
                with st.expander("View Recipe", expanded=True):
                    st.subheader(response_data["recipe"]["title"])
                    st.markdown("**Ingredients:**")
                    for ingredient in response_data["recipe"]["ingredients"]:
                        st.markdown(f"- {ingredient}")
                    st.markdown("**Instructions:**")
                    st.write(response_data["recipe"]["instructions"])
                    if st.button("Add ingredients to shopping list", key="add_ingredients"):
                        for ingredient in response_data["recipe"]["ingredients"]:
                            add_to_shopping_list(ingredient)
                        st.success("Added ingredients to shopping list!")
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_data["message"]})

elif selected_page == "My Recipes":
    st.markdown("<h1 class='main-title'>My Recipes</h1>", unsafe_allow_html=True)
    
    # Display current recipe if available
    if st.session_state.current_recipe:
        with st.container():
            st.markdown("<div class='recipe-card'>", unsafe_allow_html=True)
            st.subheader(st.session_state.current_recipe["title"])
            st.markdown("**Ingredients:**")
            for ingredient in st.session_state.current_recipe["ingredients"]:
                st.markdown(f"- {ingredient}")
            st.markdown("**Instructions:**")
            st.write(st.session_state.current_recipe["instructions"])
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No recipes saved yet. Chat with mIAm to discover recipes!")

elif selected_page == "Shopping List":
    st.markdown("<h1 class='main-title'>Shopping List</h1>", unsafe_allow_html=True)
    
    # Shopping list input
    col1, col2 = st.columns([3, 1])
    with col1:
        new_item = st.text_input("Add item to shopping list")
    with col2:
        if st.button("Add") and new_item:
            add_to_shopping_list(new_item)
            st.success(f"Added {new_item} to your shopping list!")
    
    # Display shopping list
    if st.session_state.shopping_list:
        for i, item in enumerate(st.session_state.shopping_list):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"<div class='shopping-item'>{item['name']}</div>", unsafe_allow_html=True)
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.shopping_list.pop(i)
                    st.rerun()  # Changed from experimental_rerun() to rerun()
    else:
        st.info("Your shopping list is empty.")

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 mIAm Project | Made with Streamlit")