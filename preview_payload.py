#!/usr/bin/env python3

import os
import sys
import pandas as pd
import json

def load_env_file(file_path='dev.env'):
    """Load environment variables from .env file."""
    env_vars = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    return env_vars

def main():
    print("=" * 80)
    print("Test Invite Payload Preview")
    print("=" * 80)

    # Load environment variables from dev.env
    env_vars = load_env_file('dev.env')

    # Get configuration from environment
    pennsieve_host = os.environ.get('PENNSIEVE_HOST', env_vars.get('PENNSIEVE_HOST'))
    org_id = os.environ.get('ORG_ID', env_vars.get('ORG_ID'))

    csv_file = './data/output/test_invite.csv'
    permission = "manager"  # Default permission
    custom_message = "Welcome to the Pennsieve Hackathon"

    if not os.path.exists(csv_file):
        print(f"ERROR: CSV file not found: {csv_file}")
        sys.exit(1)

    print(f"\nConfiguration:")
    print(f"  Pennsieve Host: {pennsieve_host}")
    print(f"  Organization ID: {org_id}")
    print(f"  CSV File: {csv_file}")
    print(f"  Default Permission: {permission}")

    # Load CSV file
    print(f"\nLoading invites from: {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"Found {len(df)} users to invite")

    # Prepare invites list (same logic as send_invites.py)
    invites = []
    for idx, row in df.iterrows():
        email = str(row.get('Email', '')).strip()
        name = str(row.get('Name', '')).strip()

        # Try to split name into first and last
        name_parts = name.split(' ', 1)
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        if not email or email.lower() == 'nan':
            print(f"\nSkipping row {idx+1}: No email address")
            continue

        invites.append({
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "customMessage": custom_message,
            "inviteRole": "1"  # Default role
        })

    # Construct the payload
    payload = {
        "invites": invites,
        "role": permission
    }

    # Display the API call details
    url = f"{pennsieve_host}/organizations/{org_id}/members"

    print("\n" + "=" * 80)
    print("API CALL DETAILS")
    print("=" * 80)
    print(f"\nEndpoint: POST {url}")
    print(f"\nHeaders:")
    print(f"  Authorization: Bearer [API_KEY]")
    print(f"  Content-Type: application/json")

    print(f"\n" + "=" * 80)
    print("PAYLOAD")
    print("=" * 80)
    print(json.dumps(payload, indent=2))

    print(f"\n" + "=" * 80)
    print("INVITE DETAILS")
    print("=" * 80)
    for idx, invite in enumerate(invites, 1):
        print(f"\n{idx}. {invite['firstName']} {invite['lastName']}")
        print(f"   Email: {invite['email']}")
        print(f"   Role: {payload['role']}")
        print(f"   Message: {invite['customMessage']}")

if __name__ == '__main__':
    main()
