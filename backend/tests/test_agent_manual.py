import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.onboarding_agent import check_document_status

def test_document_tool():
    print("Testing check_document_status tool...")
    # Test without seller_id (Global count)
    result = check_document_status.invoke({"seller_id": None})
    print(f"Global Result: {result}")
    
    # Test with seller_id (Should be empty or mocked)
    result_specific = check_document_status.invoke({"seller_id": 999})
    print(f"Specific Result: {result_specific}")

if __name__ == "__main__":
    try:
        test_document_tool()
        print("✅ Agent tool test passed")
    except Exception as e:
        print(f"❌ Agent tool test failed: {e}")
        sys.exit(1)
