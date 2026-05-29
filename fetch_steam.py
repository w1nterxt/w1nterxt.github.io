"""Steam 数据拉取脚本
用法: python fetch_steam.py
输出: steam_data.json (玩家信息 + 游戏库排行)
"""
import json
import os
import urllib.request

API_KEY = "502DBFF44F5A7BA5782794AC41AC5804"
STEAM_ID = "76561199231046808"
OUTPUT = os.path.join(os.path.dirname(__file__), "steam_data.json")


def fetch(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read())


def main():
    result = {"player": {}, "games": [], "total_games": 0, "total_hours": 0}

    # 1. 玩家概要
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={API_KEY}&steamids={STEAM_ID}"
    player = fetch(url)["response"]["players"][0]
    result["player"] = {
        "name": player["personaname"],
        "avatar": player["avatarfull"],
        "avatar_medium": player.get("avatarmedium", ""),
        "url": player["profileurl"],
    }
    print(f"玩家: {player['personaname']}")

    # 2. 全部游戏 (含免费游戏)
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={API_KEY}&steamid={STEAM_ID}&include_appinfo=true&include_played_free_games=true"
    raw = fetch(url)["response"].get("games", [])
    print(f"游戏总数: {len(raw)}")

    all_games = []
    total_minutes = 0
    for g in raw:
        mins = g.get("playtime_forever", 0)
        total_minutes += mins
        all_games.append(
            {
                "appid": g["appid"],
                "name": g["name"],
                "hours": round(mins / 60, 1),
                "icon": (
                    f"https://media.steampowered.com/steamcommunity/public/images/apps/{g['appid']}/{g['img_icon_url']}.jpg"
                    if g.get("img_icon_url")
                    else ""
                ),
                "header": (
                    f"https://steamcdn-a.akamaihd.net/steam/apps/{g['appid']}/header.jpg"
                ),
                "last_played": g.get("rtime_last_played", 0),
            }
        )

    # 按时长排序
    all_games.sort(key=lambda g: g["hours"], reverse=True)
    result["games"] = all_games
    result["total_games"] = len(all_games)
    result["total_hours"] = round(total_minutes / 60, 1)

    # 写入
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"已写入: {OUTPUT}")
    print(f"时长排行 TOP 10:")
    for g in all_games[:10]:
        print(f"  {g['name'][:30]:30s} {g['hours']:>8.1f}h")


if __name__ == "__main__":
    main()
