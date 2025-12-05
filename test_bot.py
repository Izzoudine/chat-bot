import json
import os
from main import get_model_response, load_knowledge_base

def test_chatbot():
    print("Testing Chatbot with new API keys...")
    
    # Load KB
    kb_path = os.path.join(os.path.dirname(__file__), 'data', 'knowledge_base.json')
    knowledge_base = load_knowledge_base(kb_path)
    knowledge_base_str = json.dumps(knowledge_base, indent=2, ensure_ascii=False)
    
    # Test Question
    question = "What is the name of this project?"
    print(f"Question: {question}")
    
    # Get Response
    response = get_model_response(question, knowledge_base_str)
    print(f"Response: {response}")

if __name__ == "__main__":
    test_chatbot()
