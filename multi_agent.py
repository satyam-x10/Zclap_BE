import ollama
import time
import os

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

# Function to get response from Ollama with minimal complexity
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
        # Simplified API call
        response = ollama.chat(model="mistral", messages=[
            {"role": "user", "content": prompt}
        ])
        return response['message']['content']
    except Exception as e:
        print(f"Error with {agent_name}: {str(e)}")
        return f"[Error getting response from {agent_name}]"

# Run the simulation
def run_chat():
    conversation = []
    
    # Starting message
    print("Starting Multi-Agent Marketing Campaign Simulation...\n")
    initial_message = "Team, we need to create a marketing campaign for the EcoSmart Home Hub product launch. Let's collaborate on ideas."
    print(f"BrandManager: {initial_message}\n")
    conversation.append(f"BrandManager: {initial_message}")
    
    # Agent order
    agents = ["ContentWriter", "GraphicDesigner", "DataAnalyst", "BrandManager"]
    
    # Just two rounds to keep it simple
    for round in range(2):
        print(f"\n--- Round {round+1} ---\n")
        
        for agent in agents:
            try:
                # Get conversation history as text
                history = "\n".join(conversation)
                
                # Get agent's response
                response = get_agent_response(agent, history, PRODUCT)
                
                # Add to history and display
                agent_message = f"{agent}: {response}"
                conversation.append(agent_message)
                print(f"{agent_message}\n")
                
                # Save progress after each message in case of crash
                with open("conversation_backup.txt", "w", encoding="utf-8") as f:
                    f.write("\n\n".join(conversation))
                
                # Brief pause
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error in agent {agent}: {str(e)}")
    
    # Save final conversation
    with open("marketing_campaign_results.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(conversation))
    
    print("Simulation complete! Results saved to marketing_campaign_results.txt")

if __name__ == "__main__":
    run_chat()