#!/usr/bin/env python3

import os
import sys
import pandas as pd
import requests

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

def get_existing_members(base_url: str, org_id: str, api_key: str):
    """Fetch existing members from Pennsieve API."""
    url = f"{base_url}/organizations/{org_id}/members"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    print(f"\nFetching existing members from Pennsieve API...")
    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        members = response.json()

        # Extract emails from existing members
        existing_emails = set()
        member_details = {}
        for member in members:
            if 'email' in member:
                email = member['email'].lower()
                existing_emails.add(email)
                member_details[email] = {
                    'name': f"{member.get('firstName', '')} {member.get('lastName', '')}".strip(),
                    'role': member.get('role', 'N/A')
                }

        print(f"Found {len(existing_emails)} existing members")
        return existing_emails, member_details

    except requests.exceptions.RequestException as e:
        print(f"Error fetching members: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        sys.exit(1)

def main():
    print("=" * 80)
    print("Test Invite Verification - Checking Against Existing Members")
    print("=" * 80)

    # Load environment variables from dev.env
    env_vars = load_env_file('dev.env')

    # Get configuration from environment
    api_key = os.environ.get('API_KEY', env_vars.get('API_KEY'))
    pennsieve_host = os.environ.get('PENNSIEVE_HOST', env_vars.get('PENNSIEVE_HOST'))
    org_id = os.environ.get('ORG_ID', env_vars.get('ORG_ID'))

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

    csv_file = './data/output/test_invite.csv'

    if not os.path.exists(csv_file):
        print(f"ERROR: CSV file not found: {csv_file}")
        sys.exit(1)

    print(f"\nConfiguration:")
    print(f"  Pennsieve Host: {pennsieve_host}")
    print(f"  Organization ID: {org_id}")
    print(f"  CSV File: {csv_file}")

    # Load test invite CSV
    print(f"\nLoading test invites from: {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"Found {len(df)} participants in test invite list")

    # Get existing members
    existing_members, member_details = get_existing_members(pennsieve_host, org_id, api_key)

    # Check each participant
    print("\n" + "=" * 80)
    print("Verification Results:")
    print("=" * 80)

    already_members = []
    not_members = []

    for idx, row in df.iterrows():
        email = str(row.get('Email', '')).strip().lower()
        name = str(row.get('Name', '')).strip()

        if not email or email == 'nan':
            print(f"\n⚠ Skipping row {idx+1}: No email address")
            continue

        if email in existing_members:
            already_members.append({
                'name': name,
                'email': email,
                'member_info': member_details.get(email, {})
            })
            print(f"\n✗ ALREADY A MEMBER: {name} ({email})")
            print(f"    Role: {member_details.get(email, {}).get('role', 'N/A')}")
        else:
            not_members.append({'name': name, 'email': email})
            print(f"\n✓ NOT A MEMBER: {name} ({email})")
            print(f"    Can be invited")

    # Summary
    print("\n" + "=" * 80)
    print("Summary:")
    print(f"  Total participants in test invite: {len(df)}")
    print(f"  Already organization members: {len(already_members)}")
    print(f"  Not members (safe to invite): {len(not_members)}")
    print("=" * 80)

    if already_members:
        print("\n⚠ WARNING: The following participants are already members:")
        for member in already_members:
            print(f"  - {member['name']} ({member['email']})")
        print("\nYou may want to remove them from test_invite.csv before sending invites.")
    else:
        print("\n✓ All participants in test_invite.csv are NOT currently members.")
        print("  It is safe to proceed with sending invites.")

if __name__ == '__main__':
    main()
