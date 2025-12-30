import json
import os

fixes = {
  "nce2-l86": {
    "intro_3": [{"word": "Speedboat", "pos": "n.", "meaning": "快艇"}],
    "s1": [{"word": "Direction", "pos": "n.", "meaning": "方向"}],
    "s2": [{"word": "Swing", "pos": "v.", "meaning": "摇摆"}],
    "s4": [{"word": "Desperately", "pos": "adv.", "meaning": "拼命地"}],
    "s6": [{"word": "Companion", "pos": "n.", "meaning": "同伴"}],
    "s8": [{"word": "Lifebuoy", "pos": "n.", "meaning": "救生圈"}]
  },
  "nce2-l87": {
    "intro_2": [{"word": "Alibi", "pos": "n.", "meaning": "不在场证明"}],
    "s1": [{"word": "Inspector", "pos": "n.", "meaning": "探长"}],
    "s2": [{"word": "Suspicious", "pos": "adj.", "meaning": "怀疑的"}],
    "s4": [{"word": "Murder", "pos": "v.", "meaning": "谋杀"}],
    "s6": [{"word": "Impossible", "pos": "adj.", "meaning": "不可能的"}],
    "s8": [{"word": "Ignorant", "pos": "adj.", "meaning": "无知的"}]
  },
  "nce2-l88": {
    "intro_2": [{"word": "Trap", "pos": "v.", "meaning": "困住"}],
    "intro_3": [{"word": "Surface", "pos": "n.", "meaning": "表面"}],
    "s1": [{"word": "Explosive", "pos": "n.", "meaning": "炸药"}],
    "s3": [{"word": "Vibration", "pos": "n.", "meaning": "震动"}],
    "s5": [{"word": "Miner", "pos": "n.", "meaning": "矿工"}],
    "s7": [{"word": "Rescue", "pos": "v.", "meaning": "营救"}],
    "s9": [{"word": "Capsule", "pos": "n.", "meaning": "胶囊"}]
  },
  "nce2-l89": {
    "intro_3": [{"word": "Slip", "pos": "n.", "meaning": "滑倒;错误"}],
    "intro_4": [{"word": "Tongue", "pos": "n.", "meaning": "舌头"}],
    "s1": [{"word": "Cinema", "pos": "n.", "meaning": "电影院"}],
    "s3": [{"word": "Artist", "pos": "n.", "meaning": "艺术家"}],
    "s6": [{"word": "Position", "pos": "n.", "meaning": "位置"}],
    "s8": [{"word": "Advertisement", "pos": "n.", "meaning": "广告"}]
  },
  "nce2-l90": {
    "intro_2": [{"word": "Platform", "pos": "n.", "meaning": "钻井平台"}],
    "s1": [{"word": "Terror", "pos": "n.", "meaning": "恐惧"}],
    "s2": [{"word": "Fire", "pos": "n.", "meaning": "火灾"}],
    "s4": [{"word": "Alarm", "pos": "n.", "meaning": "警报"}],
    "s6": [{"word": "Drill", "pos": "v.", "meaning": "钻探"}],
    "s8": [{"word": "Fish", "pos": "n.", "meaning": "鱼"}]
  },
  "nce2-l91": {
    "intro_3": [{"word": "Balloon", "pos": "n.", "meaning": "气球"}],
    "s1": [{"word": "Pilot", "pos": "n.", "meaning": "飞行员"}],
    "s3": [{"word": "Circle", "pos": "v.", "meaning": "盘旋"}],
    "s5": [{"word": "Basket", "pos": "n.", "meaning": "篮子"}],
    "s7": [{"word": "Signal", "pos": "n.", "meaning": "信号"}],
    "s9": [{"word": "Designation", "pos": "n.", "meaning": "目的地"}]
  },
  "nce2-l92": {
    "intro_1": [{"word": "Trouble", "pos": "n.", "meaning": "麻烦"}],
    "s2": [{"word": "Ladder", "pos": "n.", "meaning": "梯子"}],
    "s3": [{"word": "Shed", "pos": "n.", "meaning": "棚子"}],
    "s5": [{"word": "Sarcastic", "pos": "adj.", "meaning": "讽刺的"}],
    "s7": [{"word": "Doorbell", "pos": "n.", "meaning": "门铃"}],
    "s9": [{"word": "Neighbor", "pos": "n.", "meaning": "邻居"}]
  },
  "nce2-l93": {
    "intro_2": [{"word": "Monument", "pos": "n.", "meaning": "纪念碑"}],
    "intro_3": [{"word": "Statue", "pos": "n.", "meaning": "雕像"}],
    "s1": [{"word": "Copper", "pos": "n.", "meaning": "铜"}],
    "s3": [{"word": "Pedestal", "pos": "n.", "meaning": "基座"}],
    "s5": [{"word": "Erect", "pos": "v.", "meaning": "竖立"}],
    "s8": [{"word": "Official", "pos": "adj.", "meaning": "官方的"}]
  },
  "nce2-l94": {
    "intro_4": [{"word": "Expert", "pos": "n.", "meaning": "专家"}],
    "s2": [{"word": "Accustom", "pos": "v.", "meaning": "使习惯"}],
    "s3": [{"word": "Underwater", "pos": "adj.", "meaning": "水下的"}],
    "s4": [{"word": "Tricycle", "pos": "n.", "meaning": "三轮车"}],
    "s6": [{"word": "Pedal", "pos": "v.", "meaning": "踩踏板"}],
    "s8": [{"word": "Champion", "pos": "n.", "meaning": "冠军"}]
  },
  "nce2-l95": {
    "intro_2": [{"word": "Ambassador", "pos": "n.", "meaning": "大使"}],
    "s2": [{"word": "Extinguisher", "pos": "n.", "meaning": "灭火器"}],
    "s3": [{"word": "Embassy", "pos": "n.", "meaning": "大使馆"}],
    "s7": [{"word": "Basement", "pos": "n.", "meaning": "地下室"}],
    "s16": [{"word": "Shot", "pos": "n.", "meaning": "枪声;发射"}],
    "s19": [{"word": "Lunch", "pos": "n.", "meaning": "午餐"}]
  },
  "nce2-l96": {
    "intro_2": [{"word": "Festival", "pos": "n.", "meaning": "节日"}],
    "intro_3": [{"word": "Occasion", "pos": "n.", "meaning": "场合"}],
    "s2": [{"word": "Lantern", "pos": "n.", "meaning": "灯笼"}],
    "s8": [{"word": "Drift", "pos": "v.", "meaning": "漂流"}],
    "s9": [{"word": "Spectacle", "pos": "n.", "meaning": "景象"}]
  }
}

directory = '/Users/phoenix/Documents/workspace-personal/visual-nce/src/data/lessons'

for filename, lesson_data in fixes.items():
    filepath = os.path.join(directory, f"{filename}.json")
    if not os.path.exists(filepath):
        print(f"File not found: {filename}")
        continue
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        modified = False
        for seg in data.get('segments', []):
            if seg['id'] in lesson_data:
                # If analysis is missing or words are empty, update it
                if 'analysis' not in seg or not seg['analysis'] or not seg['analysis'].get('words'):
                    seg['analysis'] = {
                        "words": lesson_data[seg['id']]
                    }
                    modified = True
            elif 'analysis' not in seg and not seg['id'].startswith('intro_'):
                 # For sX segments that are missing analysis but we didn't specify words, give empty structure
                 # so we don't have "missing field" errors in UI if that matters
                 seg['analysis'] = {"words": []}
                 modified = True
            
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated {filename}")
            
    except Exception as e:
        print(f"Error updating {filename}: {e}")

