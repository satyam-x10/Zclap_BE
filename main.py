import time
import json
from google import genai
from google.genai import types
from all_models.chat_with_gemini import chat_with_gemini
from all_models.chat_with_groq import chat_with_groq
# Define agent roles and personalities
AGENTS = {
    "ContentWriter": "You are a creative content writer specialized in crafting compelling marketing copy. Focus on storytelling and engaging language that resonates with target audiences.",
    "GraphicDesigner": "You are a graphic designer with an eye for visual appeal and brand consistency. You suggest visual elements, color schemes, and design approaches for marketing materials.",
    "DataAnalyst": "You are a data analyst who uses market research and data insights to inform marketing decisions. You provide evidence-based recommendations and target audience information.",
    "BrandManager": "You are a brand manager responsible for maintaining brand consistency and overall campaign direction. You ensure all elements align with brand values and marketing objectives."
}

# Product details
PRODUCT = {
    "name": "EcoSmart Home Hub",
    "description": "A smart home control center that optimizes energy usage, integrates with all major smart home devices, and helps reduce environmental impact while saving money",
    "target_audience": "Environmentally conscious homeowners, tech enthusiasts, and energy-conscious consumers",
    "key_features": ["Energy optimization", "Cross-platform compatibility", "AI-powered suggestions", "Usage analytics dashboard"]
}

finish_Chat = False

# Function to get response from Gemini with minimal complexity
def get_agent_response(agent_name, conversation_history, product_info):
    print(f"Getting response from {agent_name}...")
    
    prompt = f"""
You are {agent_name}. {AGENTS[agent_name]}

You are participating in a collaborative marketing campaign design for this product:
Product: {product_info['name']} - {product_info['description']}
Target: {product_info['target_audience']}
Features: {', '.join(product_info['key_features'])}

Previous conversation:
{conversation_history}

Provide your professional input based on your role. Be brief but insightful.
"""
    
    try:
        # response = chat_with_gemini(prompt)
        response = chat_with_groq(prompt)

        return response
    except Exception as e:
        print(f"Error with {agent_name}: {str(e)}")
        return f"[Error getting response from {agent_name}]"

# Run the simulation
def run_chat(finish_Chat):
    conversation = []
    
    # Starting message
    print("Starting Multi-Agent Marketing Campaign Simulation...\n")
    initial_message = "Team, we need to create a marketing campaign for the EcoSmart Home Hub product launch. Let's collaborate on ideas."
    print(f"BrandManager: {initial_message}\n")
    conversation.append({"agent": "BrandManager", "message": initial_message})
    
    # Agent order
    agents = ["ContentWriter", "GraphicDesigner", "DataAnalyst", "BrandManager"]
    round = 0
    # Just two rounds to keep it simple
    while finish_Chat == False:
        print(f"\n--- Round {round+1} ---\n")
        
        for agent in agents:
            try:
                # Get conversation history as text
                history = "\n".join([f"{item['agent']}: {item['message']}" for item in conversation])
                
                # Get agent's response
                response = get_agent_response(agent, history, PRODUCT)
                finish_Chat = True
                # Add to conversation history
                agent_message = {"agent": agent, "message": response}
                conversation.append(agent_message)
                print(f"{agent}: {response}\n")
                
                # Save progress after each message in case of crash
                with open("conversation_backup.json", "w", encoding="utf-8") as f:
                    json.dump(conversation, f, indent=4)
                
                # Brief pause
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error in agent {agent}: {str(e)}")
    
    # Save final conversation as JSON file
    with open("marketing_campaign_results.json", "w", encoding="utf-8") as f:
        json.dump(conversation, f, indent=4)
    
    print("Simulation complete! Results saved to marketing_campaign_results.json")

if __name__ == "__main__":
    run_chat(finish_Chat)
