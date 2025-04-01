import time
import json
from google import genai
from all_models.chat_with_gemini import chat_with_gemini
from all_models.chat_with_groq import chat_with_groq

# Function to get response using selected model
def get_agent_response(agent_name, agent_info, conversation_history, product_info):
    print(f"Getting response from {agent_name} using {agent_info.model}...")

    prompt = f"""
You are {agent_name}. {agent_info.role}

You are participating in a collaborative marketing campaign design for this product:
Product: {product_info.name} - {product_info.description}
Target: {product_info.target_audience}
Features: {', '.join(product_info.key_features)}

Previous conversation:
{conversation_history}

Provide your professional input based on your role. Be brief but insightful.
"""

    try:
        if agent_info.model == "gemini":
            response = chat_with_gemini(prompt)
        else:
            response = chat_with_groq(prompt)
        return response
    except Exception as e:
        print(f"Error with {agent_name}: {str(e)}")
        return f"[Error getting response from {agent_name}]"

# Main simulation function
class AgentInfo:
    def __init__(self, role, model, name):
        self.role = role
        self.model = model
        self.name = name

def run_chat(agents, product_info):
    print("Initializing agents...", [agent.name for agent in agents])  # Access agent names directly
    print('/n')
    print("Initializing product info...", product_info.name)
    conversation = []

    print("Starting Multi-Agent Marketing Campaign Simulation...\n")
    initial_message = "Team, we need to create a marketing campaign for the EcoSmart Home Hub product launch. Let's collaborate on ideas."
    
    # Use dot notation to access agent properties
    print(f"{agents[0].name}: {initial_message}\n")
    conversation.append({
        "sno": 1,
        "agent": agents[0].name,  # Accessing name using dot notation
        "message": initial_message,
        "model": agents[0].model  # Accessing model using dot notation
    })

    rounds = 0
    max_rounds = 2
    serial_no = 2

    while rounds < max_rounds:
        print(f"\n--- Round {rounds + 1} ---\n")
        for agent_info in agents:
            print(agent_info)
            try:
                # Construct conversation history
                history = "\n".join([f"{msg['agent']}: {msg['message']}" for msg in conversation])

                # Get agent's response based on their role and model
                response = get_agent_response(agent_info.name, agent_info, history, product_info)

                # Record the agent's response and add it to the conversation
                agent_message = {
                    "sno": serial_no,
                    "agent": agent_info.name,
                    "message": response,
                    "model": agent_info.model
                }
                serial_no += 1
                conversation.append(agent_message)
                print(f"{agent_info.name}: {response}\n")

                # Save conversation progress after each round
                with open("backup.json", "w", encoding="utf-8") as f:
                    json.dump(conversation, f, indent=4)

                time.sleep(0.5)

            except Exception as e:
                print(f"Error in agent {agent_info.name}: {str(e)}")

        rounds += 1
        if rounds >= max_rounds:
            finish_chat = True

    # Save the final conversation results to a file
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(conversation, f, indent=4)

    print("Simulation complete! Results saved to result.json")
    
    # Return conversation data to be used by the API
    return {agent["agent"]: agent["message"] for agent in conversation if agent["sno"] > 1}