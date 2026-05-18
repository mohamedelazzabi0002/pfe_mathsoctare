#!/usr/bin/env python3
"""Utility to create a user with hashed password in the local DB.
Usage: python mathsocrate_pfe\create_user.py --full-name "Name" --email a@b.com --password secret --role eleve --class-name "3A"
"""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Service.login_service import _hash_password
from Database.db import execute_query


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--full-name', required=True)
    p.add_argument('--email', required=True)
    p.add_argument('--password', required=True)
    p.add_argument('--role', choices=['eleve','enseignant'], default='eleve')
    p.add_argument('--class-name', default=None)
    p.add_argument('--cognitive-profile', choices=['normal','hesitant','error_prone'], default='normal')

    args = p.parse_args()

    pwd_hash = _hash_password(args.password)

    execute_query(
        "INSERT INTO users (full_name, email, password, role, class_name, cognitive_profile) VALUES (?, ?, ?, ?, ?, ?)",
        (args.full_name, args.email, pwd_hash, args.role, args.class_name, args.cognitive_profile),
    )

    print("Utilisateur créé avec succès.")


if __name__ == '__main__':
    main()
