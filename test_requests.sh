#!/bin/bash

# Endpoint URLs
ENDPOINT_1="http://proxy.osieltorres.xyz/categories/MLA5725"
ENDPOINT_2="http://proxy.osieltorres.xyz/categories/MLA5726"
ENDPOINT_3="http://proxy.osieltorres.xyz/categories/MLA1071"
ENDPOINT_4="http://proxy.osieltorres.xyz/categories/MLA1648"
ENDPOINT_5="http://proxy.osieltorres.xyz/sites/MLA/"
ENDPOINT_6="http://proxy.osieltorres.xyz/categories/invalid_id/"

# Number of requests for each endpoint
REQUESTS_ENDPOINT_1=10
REQUESTS_ENDPOINT_2=5
REQUESTS_ENDPOINT_3=20
REQUESTS_ENDPOINT_4=3
REQUESTS_ENDPOINT_5=7
REQUESTS_ENDPOINT_6=5

# Function to make requests to an endpoint
make_requests() {
    local ENDPOINT=$1
    local REQUESTS=$2
    for ((i = 1; i <= REQUESTS; i++)); do
        echo "Making request $i to $ENDPOINT"
        curl -s "$ENDPOINT" >/dev/null
    done
}

# Make requests for each endpoint
make_requests "$ENDPOINT_1" "$REQUESTS_ENDPOINT_1"
make_requests "$ENDPOINT_2" "$REQUESTS_ENDPOINT_2"
make_requests "$ENDPOINT_3" "$REQUESTS_ENDPOINT_3"
make_requests "$ENDPOINT_4" "$REQUESTS_ENDPOINT_4"
make_requests "$ENDPOINT_5" "$REQUESTS_ENDPOINT_5"
make_requests "$ENDPOINT_6" "$REQUESTS_ENDPOINT_6"

echo "All requests completed"
