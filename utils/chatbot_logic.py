import random
import re

def is_gibberish(text):
    """
    Simple heuristic to detect keyboard mashing or nonsense.
    """
    if len(text) > 15 and " " not in text:
        return True
    if len(text) > 0:
        non_alpha = sum(1 for char in text if not char.isalnum() and not char.isspace())
        if non_alpha / len(text) > 0.4:
            return True
    if re.search(r'(.)\1{4,}', text):
        return True
    return False

def check_severity(text):
    """
    Detects urgent keywords that require immediate vet attention.
    """
    urgent_keywords = [
        "blood", "bleeding", "pus", "oozing", "open wound", "deep cut", 
        "fever", "lethargic", "not eating", "vomit", "seizure", "crying", 
        "pain", "swollen face", "breathing", "collapse"
    ]
    if any(word in text for word in urgent_keywords):
        return True
    return False

def get_knowledge_base():
    """
    Returns a dictionary of diseases, keywords, and structured responses.
    """
    return {
        "fleas": {
            "keywords": ["flea", "fleas", "black specks", "tail base", "biting tail"],
            "title": "🦟 Flea Allergy Dermatitis (FAD)",
            "analysis": "This is the most common skin disease in dogs. Even a single flea bite can cause a reaction.",
            "symptoms": "Intense scratching (especially at the tail base), hair loss, scabs, and 'flea dirt' (looks like pepper).",
            "remedy": "Use a flea comb with soapy water. Wash all bedding in hot water.",
            "medicine": "OTC: Capstar (kills adult fleas instantly). Prescription: Bravecto/NexGard (prevention).",
            "vet_trigger": "If gums are pale (anemia) or scratching causes bleeding."
        },
        "hot_spot": {
            "keywords": ["hot spot", "moist", "wet", "oozing", "warm patch", "sticky"],
            "title": "🔥 Acute Moist Dermatitis (Hot Spots)",
            "analysis": "Hot spots are painful, red, moist lesions that appear suddenly, often due to self-chewing.",
            "symptoms": "Red, wet, painful patch of skin. Hair loss in that specific spot. Very warm to the touch.",
            "remedy": "Trim hair around the area to let it breathe. Clean with cool water. prevent licking (Use a Cone/E-Collar).",
            "medicine": "OTC: Hydrocortisone spray (to stop itch) or Chlorhexidine spray (to clean).",
            "vet_trigger": "If the spot is spreading rapidly or looking infected (pus)."
        },
        "ringworm": {
            "keywords": ["ringworm", "circular", "circle", "round patch", "bald patch"],
            "title": "🦠 Ringworm (Fungal Infection)",
            "analysis": "Not a worm, but a fungus! It is highly contagious to humans and other pets.",
            "symptoms": "Circular, hairless patches. The center may look scaly or healing while edges are red.",
            "remedy": "Isolate the dog. Wash hands thoroughly after touching. Clean environment with diluted bleach.",
            "medicine": "OTC: Miconazole or Clotrimazole cream (anti-fungal) applied twice daily.",
            "vet_trigger": "If it spreads to multiple spots or other pets."
        },
        "yeast": {
            "keywords": ["yeast", "smell", "odor", "stinky", "cheesy", "greasy", "black skin", "elephant skin"],
            "title": "🍄 Yeast Dermatitis (Malassezia)",
            "analysis": "Yeast thrives in warm, moist areas like ears, paws, and skin folds.",
            "symptoms": "Musty 'corn chip' smell, greasy/oily skin, thickened black skin ('elephant skin'), intense itching.",
            "remedy": "Keep skin folds dry. Bathe with anti-fungal shampoo.",
            "medicine": "OTC: Chlorhexidine + Ketoconazole Shampoo (e.g., KetoChlor).",
            "vet_trigger": "If the smell persists after bathing or ears are filled with debris."
        },
        "mange": {
            "keywords": ["mange", "demodex", "scabies", "mites", "crusty ear"],
            "title": "🕷️ Mange (Mites)",
            "analysis": "Caused by microscopic mites. 'Demodex' is genetic/immune-related; 'Scabies' is contagious and intensely itchy.",
            "symptoms": "Patchy hair loss (face/eyes), crusty ear tips (Scabies), or general thinning hair.",
            "remedy": "Boost immune system with Omega-3s and good diet. Wash bedding.",
            "medicine": "OTC: Lime Sulfur Dip (messy but effective). Prescription is usually required (Simparica/Bravecto).",
            "vet_trigger": "Always see a vet for mange to identify the mite type via skin scrape."
        },
        "hives": {
            "keywords": ["hives", "bumps", "swollen", "swelling", "puffy", "sting"],
            "title": "🐝 Hives (Urticaria) / Allergic Reaction",
            "analysis": "A sudden reaction to an insect bite, vaccine, or plant.",
            "symptoms": "Raised bumps over the body, swollen face/eyelids.",
            "remedy": "Apply a cool compress.",
            "medicine": "OTC: Benadryl (Diphenhydramine) - *1 mg per pound of body weight*. (Consult vet first).",
            "vet_trigger": "IMMEDIATE VET: If dog has trouble breathing, vomiting, or collapses."
        },
        "dandruff": {
            "keywords": ["dandruff", "flakes", "dry skin", "white specks", "scaling", "seborrhea"],
            "title": "❄️ Seborrhea (Dandruff/Dry Skin)",
            "analysis": "Can be genetic or caused by dry weather/lack of nutrition.",
            "symptoms": "White flakes on fur, dull coat, sometimes greasy odor.",
            "remedy": "Humidifier in the room. Add Omega-3 fish oil to food.",
            "medicine": "OTC: Moisturizing oatmeal shampoo or Humilac spray.",
            "vet_trigger": "If accompanied by hair loss or sores."
        }
    }

def get_local_response(user_input):
    """
    Simulates an advanced AI response using structured knowledge and logic.
    """
    user_input = user_input.lower().strip()
    
    # --- 0. GIBBERISH DETECTION ---
    if is_gibberish(user_input):
        return "I didn't quite catch that. Could you please type the symptoms clearly? (e.g., 'red spots', 'itching')."

    # --- 1. SEVERITY CHECK (Safety First) ---
    if check_severity(user_input):
        return (
            "🚨 **URGENT ADVICE** 🚨\n\n"
            "Your description includes signs of a potentially serious condition (bleeding, lethargy, or pain). "
            "**Please do not rely on home remedies.**\n\n"
            "👉 **Take your dog to a Veterinarian immediately.**"
        )

    # --- 2. GREETINGS & CONTEXT ---
    greetings = ["hi", "hello", "hey", "good morning", "yo"]
    if any(user_input == w for w in greetings) or user_input.startswith(("hi ", "hello ")):
        return (
            "Hello! 🐾 I'm your Smart Vet Assistant.\n"
            "Tell me about your dog's symptoms."
        )

    # --- 3. VAGUE INPUT CLARIFICATION (Interactive) ---
    # If the user types very little, ask for more info
    short_triggers = ["itch", "scratch", "skin", "help", "dog", "sick", "spots"]
    if len(user_input.split()) <= 2 and any(x in user_input for x in short_triggers):
        return (
            "I can help with that, but I need a little more detail to give you the best advice.\n\n"
            "1. **Where** is the problem? (Ears, paws, tail, belly?)\n"
            "2. **What** does it look like? (Red, crusty, oozing, bald?)\n"
            "3. **Is there a smell?**"
        )

    # --- 4. KNOWLEDGE BASE LOOKUP ---
    kb = get_knowledge_base()
    
    for key, data in kb.items():
        # Check if any keyword from the disease exists in user input
        if any(k in user_input for k in data['keywords']):
            return (
                f"{data['title']}\n\n"
                f"**🔍 Analysis:** {data['analysis']}\n"
                f"**📋 Symptoms:** {data['symptoms']}\n\n"
                f"**🏡 Home Care:** {data['remedy']}\n"
                f"**💊 OTC Meds:** {data['medicine']}\n\n"
                f"**⚠️ When to see a Vet:** {data['vet_trigger']}"
            )

    # --- 5. GENERAL CATEGORY MATCHING ---
    
    # Food/Diet
    if "food" in user_input or "diet" in user_input or "chicken" in user_input:
        return (
            "🥩 **Dietary Advice**\n\n"
            "Food allergies often cause itchy paws and ears.\n"
            "- **Common Triggers:** Chicken, Beef, Wheat, Dairy.\n"
            "- **Try:** Switching to a 'Novel Protein' (like Lamb, Salmon, or Duck) for 8 weeks.\n"
            "- **Supplement:** Add Fish Oil (Omega-3) to meals to reduce skin inflammation."
        )

    # Ear Infections (Common specific request)
    if "ear" in user_input or "shaking head" in user_input:
        return (
            "👂 **Ear Infection (Otitis)**\n\n"
            "**Signs:** Head shaking, scratching ears, dark discharge (coffee grounds), or bad smell.\n"
            "**Home Care:** specific dog ear cleaner (do NOT use water or alcohol).\n"
            "**Medicine:** Zymox Otic (OTC enzymatic cleaner).\n"
            "**⚠️ Note:** If the ear is red/swollen, it might be a bacterial infection requiring vet antibiotics."
        )

    # Paws/Licking
    if "paw" in user_input or "licking" in user_input or "feet" in user_input:
        return (
            "🐾 **Paw Licking (Pododermatitis)**\n\n"
            "Constant paw licking is usually a sign of **environmental allergies** (grass/pollen) or **yeast**.\n"
            "**Remedy:** Soak paws in a mixture of water and Betadine (weak tea color) or Apple Cider Vinegar (50/50 mix) for 5 mins.\n"
            "**Prevention:** Wipe paws after walks."
        )

    # --- 6. FALLBACK (Smart Default) ---
    return (
        "I'm not 100% sure based on that description. 🤔\n\n"
        "Could you describe the **appearance** of the skin? (e.g., Is it red, black, flaky, or bleeding?)\n"
        "Or mention where on the body it is located."
    )