"""
Stop A/B Test Script

This script stops an A/B test and displays the results.
"""

import requests
import sys

# Get A/B test ID from command line or use default
ab_test_id = sys.argv[1] if len(sys.argv) > 1 else "2"

print(f"Stopping A/B test with ID: {ab_test_id}")
print(f"URL: http://127.0.0.1:8000/api/v1/stop_ab_test/{ab_test_id}")

try:
    # Stop the A/B test
    response = requests.post(f"http://127.0.0.1:8000/api/v1/stop_ab_test/{ab_test_id}")
    result = response.json()
    
    print("\n" + "="*60)
    print("A/B TEST RESULTS")
    print("="*60)
    print(f"Message: {result.get('message', 'N/A')}")
    print(f"Summary: {result.get('summary', 'N/A')}")
    print("="*60)
    
    # Get the A/B test details
    print("\nFetching A/B test details...")
    ab_test_response = requests.get(f"http://127.0.0.1:8000/api/v1/abtests/{ab_test_id}")
    ab_test = ab_test_response.json()
    
    print(f"\nA/B Test: {ab_test['title']}")
    print(f"Created by: {ab_test['created_by']}")
    print(f"Started: {ab_test['created_at']}")
    print(f"Ended: {ab_test['ended_at']}")
    print(f"\nAlgorithm 1 ID: {ab_test['parent_mlalgorithm_1']}")
    print(f"Algorithm 2 ID: {ab_test['parent_mlalgorithm_2']}")
    
    # Get algorithm statuses
    print("\nFetching algorithm statuses...")
    alg1_response = requests.get(f"http://127.0.0.1:8000/api/v1/mlalgorithms/{ab_test['parent_mlalgorithm_1']}")
    alg2_response = requests.get(f"http://127.0.0.1:8000/api/v1/mlalgorithms/{ab_test['parent_mlalgorithm_2']}")
    
    alg1 = alg1_response.json()
    alg2 = alg2_response.json()
    
    print(f"\n{alg1['name']}: {alg1['current_status']}")
    print(f"{alg2['name']}: {alg2['current_status']}")
    
    print("\n✓ A/B test stopped successfully!")
    
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    sys.exit(1)
