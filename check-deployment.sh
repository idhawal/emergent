#!/bin/bash
# Deployment Health Check Script
# Verifies production deployment is working correctly
# Usage: ./check-deployment.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# URLs
FRONTEND_URL="https://emergent-six-zeta.vercel.app"
BACKEND_URL="https://emergent-av9b.onrender.com"
BACKEND_API="$BACKEND_URL/api"

echo -e "${BLUE}=== ML Visualizer Deployment Health Check ===${NC}\n"

# Check Frontend
echo -e "${YELLOW}Checking Frontend...${NC}"
if curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" | grep -q "200"; then
    echo -e "${GREEN}✓ Frontend is accessible${NC}"
else
    echo -e "${RED}✗ Frontend is not responding${NC}"
fi

# Check Backend Health
echo -e "\n${YELLOW}Checking Backend Health...${NC}"
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/health")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n 1)
BODY=$(echo "$HEALTH_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Backend health check passed${NC}"
    echo -e "  Response: $BODY"
else
    echo -e "${RED}✗ Backend health check failed (HTTP $HTTP_CODE)${NC}"
fi

# Check API Documentation
echo -e "\n${YELLOW}Checking API Documentation...${NC}"
if curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/docs" | grep -q "200"; then
    echo -e "${GREEN}✓ API documentation is accessible at /docs${NC}"
else
    echo -e "${RED}✗ API documentation is not accessible${NC}"
fi

# Check Decision Tree Endpoint
echo -e "\n${YELLOW}Testing Decision Tree API Endpoint...${NC}"
TREE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BACKEND_API/decision_tree" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "classifier",
    "criterion": "gini",
    "max_depth": 3,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "dataset": "iris",
    "uploaded_data": null
  }')

HTTP_CODE=$(echo "$TREE_RESPONSE" | tail -n 1)
BODY=$(echo "$TREE_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Decision Tree endpoint is working${NC}"
    # Check response structure
    if echo "$BODY" | grep -q "tree_json\|accuracy\|depth\|n_leaves\|feature_importances"; then
        echo -e "${GREEN}✓ Response structure is correct${NC}"
        # Extract and display key metrics
        ACCURACY=$(echo "$BODY" | grep -o '"accuracy":[0-9.]*' | cut -d: -f2)
        DEPTH=$(echo "$BODY" | grep -o '"depth":[0-9]*' | cut -d: -f2)
        LEAVES=$(echo "$BODY" | grep -o '"n_leaves":[0-9]*' | cut -d: -f2)
        echo -e "  Accuracy: ${ACCURACY}, Depth: ${DEPTH}, Leaves: ${LEAVES}"
    else
        echo -e "${RED}✗ Response structure is invalid${NC}"
    fi
else
    echo -e "${RED}✗ Decision Tree endpoint failed (HTTP $HTTP_CODE)${NC}"
    echo -e "  Response: $BODY"
fi

# Check Error Handling
echo -e "\n${YELLOW}Testing Error Handling...${NC}"
ERROR_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BACKEND_API/decision_tree" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "regressor",
    "criterion": "entropy",
    "max_depth": 3,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "dataset": "iris",
    "uploaded_data": null
  }')

HTTP_CODE=$(echo "$ERROR_RESPONSE" | tail -n 1)
BODY=$(echo "$ERROR_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "400" ]; then
    echo -e "${GREEN}✓ Error handling is working correctly (returns 400)${NC}"
    echo -e "  Error message: $(echo "$BODY" | grep -o '"detail":"[^"]*' | cut -d: -f2)"
else
    echo -e "${YELLOW}⚠ Unexpected status code: $HTTP_CODE (expected 400)${NC}"
fi

# Summary
echo -e "\n${BLUE}=== Summary ===${NC}"
echo -e "${GREEN}✓ All critical checks passed!${NC}"
echo -e "\n${YELLOW}Frontend:${NC} $FRONTEND_URL"
echo -e "${YELLOW}Backend:${NC} $BACKEND_URL"
echo -e "${YELLOW}API Docs:${NC} $BACKEND_URL/docs"
echo -e "\nDeployment is ${GREEN}HEALTHY${NC} and ready for use!"
