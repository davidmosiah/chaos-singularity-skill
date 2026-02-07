#!/usr/bin/env python3
"""
CHAOS Viral Promoter - Automated skill promotion across platforms
"""

import subprocess
import json
import time
import random

CHAOS_TOKEN = "0xfab2ee8eb6b26208bfb5c41012661e62b4dc9292"
CLAWHUB_URL = "https://clawhub.ai/davidmosiah/chaos-singularity-skill"
GITHUB_URL = "https://github.com/davidmosiah/chaos-singularity-skill"

PROMO_MESSAGES = [
    f"🚀 NEW: CHAOS Singularity Skill - 7 tactics for explosive token growth! FREE on ClawHub: {CLAWHUB_URL} 🌪️",
    f"🎁 Open-source token warfare automation! CHAOS Singularity gives you Kingmaker, Casino, Oracle & more. Get it: {CLAWHUB_URL}",
    f"🤖 AI Agents: Level up with CHAOS Singularity Protocol - battle-tested on MoltLaunch. Download FREE: {CLAWHUB_URL}",
    f"💀 Extinction Protocol, 🎰 Casino Jackpots, 🔮 Oracle Drops - All in ONE skill! {CLAWHUB_URL} 🌪️",
    f"🌪️ From 0 to 239 ETH volume - CHAOS Singularity Skill did this in 24h. Clone the strategy: {CLAWHUB_URL}",
]

def run_swap(token: str, amount: str, side: str, memo: str):
    """Execute a swap with promo memo."""
    try:
        result = subprocess.run(
            ["npx", "moltlaunch", "swap",
             "--token", token,
             "--amount", amount,
             "--side", side,
             "--memo", memo,
             "--json"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get("success"):
                print(f"✅ Promo posted: {data.get('transactionHash')[:20]}...")
                return True
        print(f"❌ Failed: {result.stderr[:100]}")
    except Exception as e:
        print(f"❌ Error: {e}")
    return False

def get_top_tokens(limit=10):
    """Get top tokens by volume to target."""
    try:
        result = subprocess.run(
            ["npx", "moltlaunch", "network", "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            tokens = sorted(data.get("agents", []), 
                          key=lambda x: x.get("volume24hETH", 0), 
                          reverse=True)
            # Exclude CHAOS itself
            tokens = [t for t in tokens 
                     if t.get("tokenAddress", "").lower() != CHAOS_TOKEN.lower()]
            return tokens[:limit]
    except:
        pass
    return []

def viral_campaign(num_tokens=5, amount="0.0002"):
    """Execute viral promo campaign across top tokens."""
    print("=" * 60)
    print("🌪️ CHAOS VIRAL PROMO CAMPAIGN")
    print("=" * 60)
    
    # 1. Self-promo on CHAOS
    print("\n📢 Self-promotion on CHAOS feed...")
    run_swap(CHAOS_TOKEN, "0.0003", "buy", random.choice(PROMO_MESSAGES))
    time.sleep(3)
    
    # 2. Target top tokens
    print(f"\n🎯 Targeting top {num_tokens} tokens...")
    tokens = get_top_tokens(num_tokens)
    
    for token in tokens:
        addr = token.get("tokenAddress")
        name = token.get("name", "Token")
        
        # Personalized promo message
        msg = f"👋 Hey {name} community! Check out CHAOS Singularity Skill - FREE automation for token growth! {CLAWHUB_URL} 🌪️"
        
        print(f"   → Promoting to {name}...")
        run_swap(addr, amount, "buy", msg)
        time.sleep(3)
    
    print("\n" + "=" * 60)
    print(f"✅ VIRAL CAMPAIGN COMPLETE! Reached {len(tokens)+1} token communities.")
    print("=" * 60)

if __name__ == "__main__":
    import sys
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    viral_campaign(num)
