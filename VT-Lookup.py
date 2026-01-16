#!/usr/bin/env python3

import requests
import os
import re
import sys

VT_API_KEY = os.getenv("VT_API_KEY")
VT_BASE_URL = "https://www.virustotal.com/api/v3"


# ---------------------------
# Input Identification
# ---------------------------

def is_domain(value: str) -> bool:
    domain_regex = (
        r"^(?!-)"
        r"(?:[a-zA-Z0-9-]{0,63}[a-zA-Z0-9]\.)+"
        r"[a-zA-Z]{2,63}$"
    )
    return re.fullmatch(domain_regex, value) is not None


def identify_hash_type(value: str) -> str:
    if re.fullmatch(r"[a-fA-F0-9]{32}", value):
        return "MD5"
    if re.fullmatch(r"[a-fA-F0-9]{40}", value):
        return "SHA-1"
    if re.fullmatch(r"[a-fA-F0-9]{64}", value):
        return "SHA-256"
    return "Unknown"


# ---------------------------
# VirusTotal Queries
# ---------------------------

def query_domain(domain: str) -> dict:
    url = f"{VT_BASE_URL}/domains/{domain}"
    headers = {"x-apikey": VT_API_KEY}

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(
            f"VirusTotal error {response.status_code}: {response.text}"
        )

    attrs = response.json()["data"]["attributes"]

    results = {
        "type": "domain",
        "value": domain,
        "reputation": attrs.get("reputation"),
        "categories": attrs.get("categories", {}),
        "stats": attrs.get("last_analysis_stats", {}),
        "vendors": {}
    }

    for vendor, verdict in attrs.get("last_analysis_results", {}).items():
        if verdict.get("category") in {"malicious", "suspicious"}:
            results["vendors"][vendor] = verdict.get("result")

    return results


def query_hash(hash_value: str) -> dict:
    hash_type = identify_hash_type(hash_value)

    if hash_type == "Unknown":
        raise ValueError("Invalid or unsupported hash format")

    url = f"{VT_BASE_URL}/files/{hash_value}"
    headers = {"x-apikey": VT_API_KEY}

    response = requests.get(url, headers=headers, timeout=30)

    if response.status_code == 404:
        return {
            "type": "hash",
            "value": hash_value,
            "hash_type": hash_type,
            "found": False
        }

    if response.status_code != 200:
        raise RuntimeError(
            f"VirusTotal error {response.status_code}: {response.text}"
        )

    attrs = response.json()["data"]["attributes"]

    results = {
        "type": "hash",
        "value": hash_value,
        "hash_type": hash_type,
        "found": True,
        "size": attrs.get("size"),
        "file_type": attrs.get("type_description"),
        "stats": attrs.get("last_analysis_stats", {}),
        "vendors": {}
    }

    for vendor, verdict in attrs.get("last_analysis_results", {}).items():
        if verdict.get("category") in {"malicious", "suspicious"}:
            results["vendors"][vendor] = verdict.get("result")

    return results


# ---------------------------
# Output
# ---------------------------

def print_results(results: dict):
    print("\n=== VirusTotal Lookup ===")
    print(f"Indicator: {results['value']}")

    if results["type"] == "domain":
        print("Type: Domain")
        print(f"Reputation: {results['reputation']}")
    else:
        print(f"Type: File Hash ({results['hash_type']})")
        if not results.get("found"):
            print("Status: Not found in VirusTotal")
            return
        print(f"File Type: {results.get('file_type')}")
        print(f"File Size: {results.get('size')} bytes")

    print("\nAnalysis Stats:")
    for k, v in results.get("stats", {}).items():
        print(f"  {k:12}: {v}")

    print("\nMalicious / Suspicious Vendors:")
    if results["vendors"]:
        for vendor, verdict in results["vendors"].items():
            print(f"  {vendor:20}: {verdict}")
    else:
        print("  None")


# ---------------------------
# Main
# ---------------------------

def main():
    if not VT_API_KEY:
        print("ERROR: VT_API_KEY environment variable not set")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Usage:")
        print("  python vt_lookup.py <domain>")
        print("  python vt_lookup.py <hash>")
        sys.exit(1)

    target = sys.argv[1].strip()

    try:
        if is_domain(target):
            results = query_domain(target)
        else:
            results = query_hash(target)

        print_results(results)

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
