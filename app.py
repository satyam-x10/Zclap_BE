import time
import json
from all_models.chat_with_gemini import chat_with_gemini
from all_models.chat_with_groq import chat_with_groq

# Function to get response using selected model
def get_agent_response(agent_name, agent_info, conversation_history, product_info):
    print(f"Getting response from {agent_name} using {agent_info.model}...")

    prompt = f"""
You are {agent_name}. Your role is to provide insights and suggestions based on your role.

You are participating in a collaborative marketing campaign design for this product:
Product: {product_info.name} - {product_info.description}
Target: {product_info.target_audience}
Features: {', '.join(product_info.key_features)}

Previous conversation:
{conversation_history}
You can argue with other agents, but be respectful and constructive. Make Sure to be professional.
Provide your professional input based on your role. Be brief but insightful.
"""

    try:
        if agent_info.model == "gemini-2.0-flash":
            response = chat_with_gemini(prompt)
        else:
            response = chat_with_groq(prompt, agent_info.model)
        return response
    except Exception as e:
        print(f"Error with {agent_name}: {str(e)}")
        return f"[Error getting response from {agent_name}]"

# Main simulation function
class AgentInfo:
    def __init__(self, model, role):
        self.model = model
        self.role = role

def run_chat(agents, product_info):
    print("Initializing agents...", [agent.role for agent in agents])  # Access agent names directly
    print('/n')
    print("Initializing product info...", product_info.name)
    conversation = []

    print("Starting Multi-Agent Marketing Campaign Simulation...\n")
    initial_message = f"Team, we need to create a marketing campaign for the {product_info.name} product launch. Let's collaborate on ideas."
    
    # Use dot notation to access agent properties
    print(f"{agents[0].role}: {initial_message}\n")
    conversation.append({
        "sno": 1,
        "agent": agents[0].role,  # Accessing name using dot notation
        "message": initial_message,
        "model": agents[0].model  # Accessing model using dot notation
    })

    rounds = 0
    max_rounds = 2
    serial_no = 2

    if rounds < max_rounds:
        print(f"\n--- Round {rounds + 1} ---\n")
        for agent_info in agents:
            print(agent_info)
            try:
                # Construct conversation history
                history = "\n".join([f"{msg['agent']}: {msg['message']}" for msg in conversation])

                # Get agent's response based on their role and model
                response = get_agent_response(agent_info.role, agent_info, history, product_info)

                # Record the agent's response and add it to the conversation
                agent_message = {
                    "sno": serial_no,
                    "agent": agent_info.role,
                    "message": response,
                    "model": agent_info.model
                }
                serial_no += 1
                conversation.append(agent_message)
                print(f"{agent_info.role}: {response}\n")

                # Save conversation progress after each round
                with open("backup.json", "w", encoding="utf-8") as f:
                    json.dump(conversation, f, indent=4)

                time.sleep(0.5)

            except Exception as e:
                print(f"Error in agent {agent_info.role}: {str(e)}")

        rounds += 1
        if rounds >= max_rounds:
            finish_chat = True
    else:
        print("Maximum rounds reached. Ending simulation.")               

    # Save the final conversation results to a file
    # with open("result.json", "w", encoding="utf-8") as f:
    #     json.dump(conversation, f, indent=4)

    print("Simulation complete! Results saved to result.json")

    summary_prompt = f"You are a summary agent. Please summarize the conversation in 200 words max:\n\n {history}"
    summary = chat_with_gemini(summary_prompt)
    print("Summary of the conversation:", summary)

    # with open("summary.json", "w", encoding="utf-8") as f:
    #     json.dump(summary, f, indent=4)

    # Return conversation data AND summary to be used by the API
    both = {
        "conversation": conversation,
        "summary": summary
    }
    return {"both": both}