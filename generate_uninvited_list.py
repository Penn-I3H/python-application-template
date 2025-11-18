#!/usr/bin/env python3

import os
import sys
import pandas as pd
import requests

def load_registration_list(file_path: str) -> pd.DataFrame:
    """Load the registration list from Excel file."""
    print(f"Loading registration list from: {file_path}")
    df = pd.read_excel(file_path)
    print(f"Loaded {len(df)} rows")
    print(f"Columns: {df.columns.tolist()}")
    return df

def get_existing_members(org_id: str, api_key: str):
    """Fetch existing members from Pennsieve API."""
    url = f"https://api.pennsieve.io/organizations/{org_id}/members"
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
        for member in members:
            if 'email' in member:
                existing_emails.add(member['email'].lower())

        print(f"Found {len(existing_emails)} existing members")
        return existing_emails

    except requests.exceptions.RequestException as e:
        print(f"Error fetching members: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        sys.exit(1)

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
    print("Pennsieve Uninvited Members List Generator")
    print("=" * 80)

    # Load environment variables from dev.env if not already set
    env_vars = load_env_file('dev.env')

    # Get environment variables
    # Use local paths instead of Docker paths when running locally
    input_dir = './data/input'
    output_dir = './data/output'
    api_key = os.environ.get('API_KEY', env_vars.get('API_KEY'))
    org_id = "N:organization:388563ac-49b5-4fc1-b6b0-2fba767e54b0"

    if not api_key:
        print("ERROR: API_KEY environment variable not set in dev.env")
        sys.exit(1)

    # Find the Excel file
    excel_files = [f for f in os.listdir(input_dir) if f.endswith('.xlsx')]
    if not excel_files:
        print(f"ERROR: No Excel files found in {input_dir}")
        sys.exit(1)

    excel_file = os.path.join(input_dir, excel_files[0])
    print(f"Using file: {excel_file}\n")

    # Load registration list
    df = load_registration_list(excel_file)

    # Display sample data to understand structure
    print("\nFirst few rows:")
    print(df.head())
    print("\n")

    # Try to identify email column
    email_col = None
    for col in df.columns:
        if 'email' in col.lower():
            email_col = col
            break

    if not email_col:
        print("\nERROR: Could not find email column in the spreadsheet")
        print("Available columns:", df.columns.tolist())
        sys.exit(1)

    print(f"Using column '{email_col}' for email addresses")

    # Get existing members
    existing_members = get_existing_members(org_id, api_key)

    # Debug: Print first few existing member emails
    print(f"\nFirst 5 existing member emails:")
    for i, email in enumerate(list(existing_members)[:5]):
        print(f"  {i+1}. {email}")

    # Filter out members who already have invites
    uninvited_mask = []
    invited_count = 0
    uninvited_count = 0

    for _, row in df.iterrows():
        email = str(row[email_col]).strip().lower() if pd.notna(row[email_col]) else None

        if not email or email == 'nan' or email == '':
            uninvited_mask.append(False)
        else:
            is_uninvited = email not in existing_members
            uninvited_mask.append(is_uninvited)

            if is_uninvited:
                uninvited_count += 1
            else:
                invited_count += 1

    print(f"\nDebug counts:")
    print(f"  Already invited: {invited_count}")
    print(f"  Not yet invited: {uninvited_count}")

    uninvited_df = df[uninvited_mask].copy()

    print(f"\n{'=' * 80}")
    print(f"Total registrations: {len(df)}")
    print(f"Total members in Pennsieve workspace: {len(existing_members)}")
    print(f"Registrations already in workspace: {invited_count}")
    print(f"Registrations needing invites: {len(uninvited_df)}")
    print(f"{'=' * 80}\n")

    if len(uninvited_df) == 0:
        print("No uninvited members found!")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save to CSV
    output_file = os.path.join(output_dir, 'uninvited_members.csv')
    uninvited_df.to_csv(output_file, index=False)

    print(f"Uninvited members list saved to: {output_file}")
    print(f"\nFirst few uninvited members:")
    print(uninvited_df.head(10))

if __name__ == '__main__':
    main()
