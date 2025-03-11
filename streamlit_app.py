import streamlit as st
import random
import time

# Configuration de la page
st.set_page_config(
    page_title="mIAm - Assistant de Recettes",
    page_icon="🍲",
    layout="wide"
)

# Personnalisation du thème
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B6B;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4ECDC4;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de l'historique du chat dans session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialiser d'autres variables d'état
if "first_interaction" not in st.session_state:
    st.session_state.first_interaction = True

def main():
    # En-tête de l'application avec logo et titre
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("images/imagemIAm.webp", width=100)  # Placeholder pour logo
    with col2:
        st.markdown("<h1 class='main-header'>mIAm</h1>", unsafe_allow_html=True)
        st.markdown("<h3 class='sub-header'>Votre assistant de recettes alimenté par l'IA</h3>", unsafe_allow_html=True)

    # Sidebar pour les options
    with st.sidebar:
        st.header("Options")
        
        # Filtres pour les recettes
        st.subheader("Préférences alimentaires")
        diet_preference = st.selectbox(
            "Régime alimentaire", 
            ["Tous", "Végétarien", "Vegan", "Sans gluten", "Faible en glucides"]
        )
        
        # Bouton pour effacer l'historique
        if st.button("Effacer l'historique de chat"):
            st.session_state.messages = []
            st.session_state.first_interaction = True
            st.experimental_rerun()
    
    # Section principale de chat
    st.subheader("Chat avec mIAm")

    # Message de bienvenue pour les premières interactions
    if st.session_state.first_interaction:
        with st.chat_message("assistant"):
            st.markdown("👋 Bonjour ! Je suis mIAm, votre assistant de cuisine. Que souhaitez-vous cuisiner aujourd'hui ?")
        st.session_state.first_interaction = False
        st.session_state.messages.append({"role": "assistant", "content": "👋 Bonjour ! Je suis mIAm, votre assistant de cuisine. Que souhaitez-vous cuisiner aujourd'hui ?"})

    # Afficher les messages de l'historique
    display_chat_history()
    
    # Zone de saisie pour le chat
    process_user_input()
    
def display_chat_history():
    """Affiche l'historique des messages du chat."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def process_user_input():
    """Traite l'entrée de l'utilisateur et génère une réponse."""
    if prompt := st.chat_input("Quelle recette souhaitez-vous aujourd'hui?"):
        # Ajouter le message de l'utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Afficher le message de l'utilisateur
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Générer la réponse avec effet de chargement
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Simuler la génération de réponse
            response = generate_bot_response(prompt)
            words = response.split()
            
            # Afficher la réponse mot par mot pour l'effet de frappe
            for word in words:
                full_response += word + " "
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.05)  # Ajustez pour contrôler la vitesse
                
            # Afficher la réponse finale
            message_placeholder.markdown(full_response)
        
        # Ajouter la réponse à l'historique
        st.session_state.messages.append({"role": "assistant", "content": response})

def generate_bot_response(prompt):
    """
    Génère une réponse du chatbot (version simulée).
    À remplacer par l'intégration réelle du backend plus tard.
    """
    # Simulation de réponses plus détaillées
    prompt_lower = prompt.lower()
    
    # Réponses pour les pizzas
    if "pizza" in prompt_lower:
        pizza_responses = [
            "**Pizza Margherita** - Un classique italien! Voici ce dont vous aurez besoin:\n\n"
            "**Ingrédients:**\n"
            "- 1 pâte à pizza\n"
            "- 150g de sauce tomate\n"
            "- 200g de mozzarella fraîche\n"
            "- Quelques feuilles de basilic frais\n"
            "- 2 cuillères à soupe d'huile d'olive\n"
            "- Sel et poivre\n\n"
            "Souhaitez-vous voir les instructions de préparation?",
            
            "**Pizza Pepperoni** - Un favori de tous les temps! Voici les ingrédients:\n\n"
            "**Ingrédients:**\n"
            "- 1 pâte à pizza\n"
            "- 150g de sauce tomate\n"
            "- 180g de mozzarella râpée\n"
            "- 100g de tranches de pepperoni\n"
            "- 1 poivron vert émincé (optionnel)\n"
            "- Origan séché\n\n"
            "Voulez-vous connaître les étapes de préparation?"
        ]
        return random.choice(pizza_responses)
    
    # Réponses pour les pâtes
    elif "pasta" in prompt_lower or "pâtes" in prompt_lower:
        pasta_responses = [
            "**Spaghetti Carbonara** - Un plat romain traditionnel! Voici les ingrédients:\n\n"
            "**Ingrédients (pour 2 personnes):**\n"
            "- 200g de spaghetti\n"
            "- 100g de pancetta ou de lardons\n"
            "- 2 gros œufs\n"
            "- 30g de pecorino romano râpé\n"
            "- 30g de parmesan râpé\n"
            "- Poivre noir fraîchement moulu\n\n"
            "Voulez-vous connaître la méthode de préparation?",
            
            "**Pennes à l'Arrabiata** - Une sauce épicée et savoureuse! Voici ce qu'il vous faut:\n\n"
            "**Ingrédients (pour 4 personnes):**\n"
            "- 400g de pennes\n"
            "- 2 boîtes de tomates concassées\n"
            "- 4 gousses d'ail émincées\n"
            "- 2 piments rouges (ajustez selon votre tolérance)\n"
            "- Huile d'olive extra vierge\n"
            "- Sel et poivre\n"
            "- Persil frais haché\n\n"
            "Souhaitez-vous voir les instructions de préparation?"
        ]
        return random.choice(pasta_responses)
    
    # Réponses pour les plats végétariens/vegans
    elif "végétarien" in prompt_lower or "vegan" in prompt_lower:
        veg_responses = [
            "**Salade de Quinoa aux Légumes Grillés** - Nutritive et délicieuse! Voici les ingrédients:\n\n"
            "**Ingrédients (pour 4 personnes):**\n"
            "- 200g de quinoa\n"
            "- 1 courgette\n"
            "- 1 aubergine\n"
            "- 1 poivron rouge\n"
            "- 1 oignon rouge\n"
            "- 150g de tomates cerises\n"
            "- Jus d'un citron\n"
            "- Huile d'olive\n"
            "- Sel et poivre\n\n"
            "Voulez-vous la recette complète?",
            
            "**Curry de Pois Chiches** - Un plat réconfortant! Voici ce dont vous aurez besoin:\n\n"
            "**Ingrédients:**\n"
            "- 2 boîtes de pois chiches\n"
            "- 1 oignon\n"
            "- 3 gousses d'ail\n"
            "- 1 boîte de tomates concassées\n"
            "- 1 boîte de lait de coco\n"
            "- 2 c. à café de curry en poudre\n"
            "- 1 c. à café de cumin\n"
            "- Sel et poivre\n\n"
            "Souhaitez-vous connaître les étapes de préparation?"
        ]
        return random.choice(veg_responses)
    
    # Réponse par défaut avec suggestions
    else:
        default_responses = [
            "Je serais ravi de vous suggérer des recettes! Quel type de cuisine vous intéresse?\n\n"
            "Voici quelques options:\n"
            "- **Cuisine italienne**: pizza, pasta, risotto\n"
            "- **Cuisine française**: quiche, ratatouille, coq au vin\n"
            "- **Cuisine asiatique**: curry, stir-fry, sushi\n"
            "- **Cuisine mexicaine**: tacos, enchiladas, guacamole\n\n"
            "Ou dites-moi simplement quels ingrédients vous avez sous la main!",
            
            "Je peux vous aider à trouver la recette parfaite! Avez-vous une préférence pour:\n\n"
            "- Un petit-déjeuner énergétique?\n"
            "- Un déjeuner léger?\n"
            "- Un dîner complet?\n"
            "- Des desserts ou pâtisseries?\n\n"
            "Je peux aussi vous proposer des idées basées sur des ingrédients spécifiques."
        ]
        return random.choice(default_responses)

if __name__ == "__main__":
    main()
