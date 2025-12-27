import sys
import os

# Add current directory to path so we can import modules
sys.path.append(os.getcwd())

from agents.onboarding_agent import invoke_agent

def test_agent():
    print("--- Testing Agent Tools ---")
    
    # Test 1: Search Sellers
    print("\n[Test 1] User: ' Find any seller with name 'Acme''")
    response1 = invoke_agent("Find any seller with name 'Acme'")
    print(f"Agent: {response1['response']}")
    
    # Test 2: Check Documents (Global)
    print("\n[Test 2] User: 'Check document status'")
    response2 = invoke_agent("Check document status")
    print(f"Agent: {response2['response']}")
    
    # Test 3: Analyze Document (Simulated ID 999)
    print("\n[Test 3] User: 'Analyze document 999'")
    response3 = invoke_agent("Analyze document with ID 999")
    print(f"Agent: {response3['response']}")

if __name__ == "__main__":
    test_agent()
