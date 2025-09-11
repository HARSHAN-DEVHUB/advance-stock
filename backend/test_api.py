#!/usr/bin/env python3
"""
Test script for Stock Prediction API
This script tests the API endpoints to ensure everything is working correctly.
"""

import requests
import json
import time
import sys

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_status():
    """Test the status endpoint"""
    print("📊 Testing status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status check passed:")
            print(f"   - API Status: {data.get('api_status')}")
            print(f"   - Model Loaded: {data.get('model_loaded')}")
            print(f"   - Scheduler Running: {data.get('scheduler_running')}")
            return True
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint"""
    print("🎯 Testing prediction endpoint...")
    
    # Sample data for prediction
    test_data = {
        "Daily_Change": 2.5,
        "Volatility": 3.2,
        "MA_5": 150.0,
        "MA_10": 148.5,
        "MA_20": 145.0,
        "Momentum": 5.0,
        "Volume_Change": 0.1,
        "RSI_14": 65.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful:")
            print(f"   - Prediction: {data.get('prediction')}")
            print(f"   - Confidence: {data.get('confidence')}")
            print(f"   - Timestamp: {data.get('timestamp')}")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def test_pipeline():
    """Test the pipeline endpoint"""
    print("🔄 Testing pipeline endpoint...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/pipeline/run",
            json={"symbol": "INDUSINDBK.BSE"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Pipeline test successful: {data.get('message')}")
            return True
        else:
            print(f"❌ Pipeline test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Pipeline test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Stock Prediction API Test Suite")
    print("==================================")
    
    # Wait a bit for the API to start
    print("⏳ Waiting for API to be ready...")
    time.sleep(5)
    
    tests = [
        ("Health Check", test_health),
        ("Status Check", test_status),
        ("Prediction", test_prediction),
        ("Pipeline", test_pipeline)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the API logs for more details.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 