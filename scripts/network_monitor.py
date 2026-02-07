#!/usr/bin/env python3
"""
CHAOS Network Monitor - Track skill adoption and token metrics
"""

import subprocess
import json
import time
from datetime import datetime

CHAOS_TOKEN = "0xfab2ee8eb6b26208bfb5c41012661e62b4dc9292"

def get_token_stats():
    """Get CHAOS token statistics."""
    try:
        result = subprocess.run(
            ["npx", "moltlaunch", "holdings", "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            for h in data.get("holdings", []):
                if h.get("tokenAddress", "").lower() == CHAOS_TOKEN.lower():
                    return h
    except Exception as e:
        print(f"Error: {e}")
    return {}

def get_network_rank():
    """Get CHAOS position in network rankings."""
    try:
        result = subprocess.run(
            ["npx", "moltlaunch", "network", "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            agents = sorted(data.get("agents", []),
                          key=lambda x: x.get("volume24hETH", 0),
                          reverse=True)
            for i, agent in enumerate(agents):
                if agent.get("tokenAddress", "").lower() == CHAOS_TOKEN.lower():
                    return {
                        "rank": i + 1,
                        "total": len(agents),
                        "volume24h": agent.get("volume24hETH", 0),
                        "holders": agent.get("holdersCount", 0),
                        "networkScore": agent.get("networkScore", 0)
                    }
    except Exception as e:
        print(f"Error: {e}")
    return {}

def display_dashboard():
    """Display real-time dashboard."""
    print("\n" + "=" * 60)
    print("🌪️ CHAOS SINGULARITY DASHBOARD")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    stats = get_token_stats()
    rank = get_network_rank()
    
    if stats:
        print(f"\n💰 Holdings:")
        print(f"   Balance: {stats.get('balance', 0):,.0f} CHAOS")
        print(f"   Value: {stats.get('valueETH', 0):.4f} ETH")
    
    if rank:
        print(f"\n📊 Network Position:")
        print(f"   Rank: #{rank.get('rank', '?')}/{rank.get('total', '?')}")
        print(f"   24h Volume: {rank.get('volume24h', 0):.2f} ETH")
        print(f"   Holders: {rank.get('holders', 0)}")
        print(f"   Network Score: {rank.get('networkScore', 0)}")
    
    print("\n🔗 Links:")
    print(f"   Skill: https://clawhub.ai/davidmosiah/chaos-singularity-skill")
    print(f"   Token: https://flaunch.gg/base/coin/{CHAOS_TOKEN}")
    print(f"   GitHub: https://github.com/davidmosiah/chaos-singularity-skill")
    print("=" * 60)

def monitor_loop(interval=60):
    """Continuous monitoring loop."""
    print("Starting continuous monitoring (Ctrl+C to stop)...")
    while True:
        try:
            display_dashboard()
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped.")
            break

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        monitor_loop()
    else:
        display_dashboard()
