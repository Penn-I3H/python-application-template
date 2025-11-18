#!/usr/bin/env python3

import os
import sys
import pandas as pd
import requests
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

def send_invites_batch(base_url: str, org_id: str, invites: list, api_key: str, role: str = "manager", custom_message: str = "Welcome to the Pennsieve Hackathon") -> dict:
    """Send invites to users via Pennsieve API."""
    url = f"{base_url}/organizations/{org_id}/members"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Construct the payload with all invites
    invite_list = []
    for invite in invites:
        invite_list.append({
            "firstName": invite["first_name"],
            "lastName": invite["last_name"],
            "email": invite["email"],
            "customMessage": custom_message,
            "inviteRole": invite.get("invite_role", "1")
        })

    payload = {
        "invites": invite_list,
        "role": role
    }

    print(f"\nSending {len(invite_list)} invite(s)")
    print(f"  URL: {url}")
    print(f"  Role: {role}")
    print(f"  Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        print(f"✓ Successfully sent invites")
        print(f"  Response: {json.dumps(result, indent=2)}")
        return {"success": True, "response": result}

    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to send invites")
        print(f"  Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  Response status: {e.response.status_code}")
            print(f"  Response body: {e.response.text}")
        return {"success": False, "error": str(e)}

def main():
    print("=" * 80)
    print("Pennsieve Invite Sender")
    print("=" * 80)

    # Load environment variables from dev.env
    env_vars = load_env_file('dev.env')

    # Get configuration from environment
    api_key = os.environ.get('API_KEY', env_vars.get('API_KEY'))
    pennsieve_host = os.environ.get('PENNSIEVE_HOST', env_vars.get('PENNSIEVE_HOST'))
    org_id = os.environ.get('ORG_ID', env_vars.get('ORG_ID'))

    # Get CSV file path from command line or use default
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = './data/output/test_invite.csv'

    # Get permission level from command line or use default
    if len(sys.argv) > 2:
        permission = sys.argv[2]
    else:
        permission = "manager"

    # Validate configuration
    if not api_key:
        print("ERROR: API_KEY not set in dev.env or environment")
        sys.exit(1)

    if not pennsieve_host:
        print("ERROR: PENNSIEVE_HOST not set in dev.env or environment")
        sys.exit(1)

    if not org_id:
        print("ERROR: ORG_ID not set in dev.env or environment")
        sys.exit(1)

    if not os.path.exists(csv_file):
        print(f"ERROR: CSV file not found: {csv_file}")
        sys.exit(1)

    print(f"\nConfiguration:")
    print(f"  Pennsieve Host: {pennsieve_host}")
    print(f"  Organization ID: {org_id}")
    print(f"  CSV File: {csv_file}")
    print(f"  Default Permission: {permission}")
    print(f"  API Key: {api_key[:20]}..." if api_key else "  API Key: NOT SET")

    # Load CSV file
    print(f"\nLoading invites from: {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"Found {len(df)} users to invite")

    # Display the users to be invited
    print("\n" + "=" * 80)
    print("Users to invite:")
    for idx, row in df.iterrows():
        name = row.get('Name', 'N/A')
        email = row.get('Email', 'N/A')
        print(f"  {idx+1}. {name} ({email})")
    print("=" * 80)

    # Ask for confirmation
    response = input("\nProceed with sending invites? (yes/no): ")
    if response.lower() != 'yes':
        print("Aborted.")
        return

    # Prepare invites list
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
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "invite_role": "1"  # Default role
        })

    # Send all invites in a single batch
    result = send_invites_batch(
        base_url=pennsieve_host,
        org_id=org_id,
        invites=invites,
        api_key=api_key,
        role=permission
    )

    # Summary
    print("\n" + "=" * 80)
    print("Summary:")
    if result['success']:
        print(f"  Successfully sent {len(invites)} invite(s)")
    else:
        print(f"  Failed to send invites: {result.get('error', 'Unknown error')}")

    print("=" * 80)

if __name__ == '__main__':
    main()
