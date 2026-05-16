"""
Verify A/B Test Results

This script verifies the A/B test results and displays:
- Test summary with accuracy for each algorithm
- Algorithm statuses (production vs testing)
- Winner determination
"""

import requests

def verify_ab_test(ab_test_id=2):
    print("="*70)
    print("A/B TEST VERIFICATION")
    print("="*70)
    
    # Get A/B test details
    print(f"\nFetching A/B test #{ab_test_id}...")
    ab_test_response = requests.get(f"http://127.0.0.1:8000/api/v1/abtests/{ab_test_id}")
    ab_test = ab_test_response.json()
    
    print(f"\n{'Title:':<20} {ab_test['title']}")
    print(f"{'Created by:':<20} {ab_test['created_by']}")
    print(f"{'Started:':<20} {ab_test['created_at']}")
    print(f"{'Ended:':<20} {ab_test['ended_at']}")
    print(f"\n{'SUMMARY:':<20} {ab_test['summary']}")
    
    # Get algorithm details
    print("\n" + "="*70)
    print("ALGORITHM COMPARISON")
    print("="*70)
    
    alg1_id = ab_test['parent_mlalgorithm_1']
    alg2_id = ab_test['parent_mlalgorithm_2']
    
    alg1_response = requests.get(f"http://127.0.0.1:8000/api/v1/mlalgorithms/{alg1_id}")
    alg2_response = requests.get(f"http://127.0.0.1:8000/api/v1/mlalgorithms/{alg2_id}")
    
    alg1 = alg1_response.json()
    alg2 = alg2_response.json()
    
    print(f"\nAlgorithm #1 (ID: {alg1_id})")
    print(f"  Name:        {alg1['name']}")
    print(f"  Status:      {alg1['current_status'].upper()}")
    print(f"  Version:     {alg1['version']}")
    print(f"  Description: {alg1['description']}")
    
    print(f"\nAlgorithm #2 (ID: {alg2_id})")
    print(f"  Name:        {alg2['name']}")
    print(f"  Status:      {alg2['current_status'].upper()}")
    print(f"  Version:     {alg2['version']}")
    print(f"  Description: {alg2['description']}")
    
    # Determine winner
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    if alg1['current_status'] == 'production':
        winner = alg1
        loser = alg2
        winner_num = 1
    else:
        winner = alg2
        loser = alg1
        winner_num = 2
    
    print(f"\n🏆 WINNER: Algorithm #{winner_num} - {winner['name']}")
    print(f"   Status: {winner['current_status'].upper()}")
    
    print(f"\n   Runner-up: {loser['name']}")
    print(f"   Status: {loser['current_status']}")
    
    # Get request statistics
    print("\n" + "="*70)
    print("REQUEST STATISTICS")
    print("="*70)
    
    requests_response = requests.get("http://127.0.0.1:8000/api/v1/mlrequests")
    all_requests = requests_response.json()
    
    alg1_requests = [r for r in all_requests if r['parent_mlalgorithm'] == alg1_id]
    alg2_requests = [r for r in all_requests if r['parent_mlalgorithm'] == alg2_id]
    
    print(f"\n{alg1['name']}:")
    print(f"  Total requests: {len(alg1_requests)}")
    
    print(f"\n{alg2['name']}:")
    print(f"  Total requests: {len(alg2_requests)}")
    
    print("\n" + "="*70)
    print("✓ Verification complete!")
    print("="*70)
    
    print("\nYou can view the results at:")
    print(f"  - A/B Tests:  http://127.0.0.1:8000/api/v1/abtests")
    print(f"  - Algorithms: http://127.0.0.1:8000/api/v1/mlalgorithms")
    print(f"  - Requests:   http://127.0.0.1:8000/api/v1/mlrequests")

if __name__ == "__main__":
    import sys
    ab_test_id = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    verify_ab_test(ab_test_id)
