"""
prompt_assembler.py - Builds LLM prompt from query and context
"""

def default_prompt_assembler(user_query, context_text, history):
    messages = [{"role": "system", "content": "You are a helpful healthcare assistant."}]
    
    # Inject chat history
    messages += history
    
    # Inject retrieved knowledge
    messages.append({"role": "system", "content": f"[KNOWLEDGE]: {context_text}"})
    
    # Add current user message
    messages.append({"role": "user", "content": user_query})
    
    return messages
