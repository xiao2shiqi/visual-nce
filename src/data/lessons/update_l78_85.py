import json
import os

fixes = {
  "nce2-l78": {
    "intro_1": [{"word": "Smoke", "pos": "v.", "meaning": "吸烟"}],
    "intro_2": [{"word": "Retire", "pos": "v.", "meaning": "退休"}],
    "intro_3": [{"word": "Problem", "pos": "n.", "meaning": "问题"}],
    "intro_4": [{"word": "Chance", "pos": "n.", "meaning": "机会"}],
    "s1": [{"word": "Grandmother", "pos": "n.", "meaning": "祖母"}],
    "s2": [{"word": "Collect", "pos": "v.", "meaning": "收集"}, {"word": "Stamp", "pos": "n.", "meaning": "邮票"}],
    "s3": [{"word": "Garden", "pos": "n.", "meaning": "花园"}],
    "s4": [{"word": "Artist", "pos": "n.", "meaning": "艺术家"}],
    "s5": [{"word": "Paint", "pos": "v.", "meaning": "画画"}],
    "s6": [{"word": "Determined", "pos": "adj.", "meaning": "坚决的"}],
    "s7": [{"word": "Successful", "pos": "adj.", "meaning": "成功的"}],
    "s8": [{"word": "Cigarette", "pos": "n.", "meaning": "香烟"}]
  },
  "nce2-l79": {
    "intro_1": [{"word": "Travel", "pos": "v.", "meaning": "旅行"}],
    "intro_3": [{"word": "Exciting", "pos": "adj.", "meaning": "令人兴奋的"}],
    "s1": [{"word": "Journey", "pos": "n.", "meaning": "旅程"}],
    "s3": [{"word": "Usually", "pos": "adv.", "meaning": "通常"}],
    "s5": [{"word": "Familiar", "pos": "adj.", "meaning": "熟悉的"}],
    "s6": [{"word": "Strange", "pos": "adj.", "meaning": "奇怪的"}],
    "s8": [{"word": "Opportunity", "pos": "n.", "meaning": "机会"}]
  },
  "nce2-l80": {
    "intro_2": [{"word": "Crystal", "pos": "n.", "meaning": "水晶"}, {"word": "Palace", "pos": "n.", "meaning": "宫殿"}],
    "intro_3": [{"word": "Different", "pos": "adj.", "meaning": "不同的"}],
    "s1": [{"word": "Building", "pos": "n.", "meaning": "建筑物"}],
    "s2": [{"word": "Exhibition", "pos": "n.", "meaning": "展览"}],
    "s4": [{"word": "Machinery", "pos": "n.", "meaning": "机器"}],
    "s6": [{"word": "Furniture", "pos": "n.", "meaning": "家具"}],
    "s8": [{"word": "Destroy", "pos": "v.", "meaning": "毁坏"}]
  },
  "nce2-l81": {
    "intro_3": [{"word": "Prisoner", "pos": "n.", "meaning": "囚犯"}],
    "intro_4": [{"word": "Escape", "pos": "v.", "meaning": "逃跑"}],
    "s1": [{"word": "Camp", "pos": "n.", "meaning": "营地"}],
    "s3": [{"word": "Uniform", "pos": "n.", "meaning": "制服"}],
    "s4": [{"word": "Rifle", "pos": "n.", "meaning": "步枪"}],
    "s5": [{"word": "Shoulder", "pos": "n.", "meaning": "肩膀"}],
    "s7": [{"word": "March", "pos": "v.", "meaning": "行军"}],
    "s9": [{"word": "Inspect", "pos": "v.", "meaning": "视察"}]
  },
  "nce2-l82": {
    "intro_1": [{"word": "Monster", "pos": "n.", "meaning": "怪物"}],
    "intro_3": [{"word": "Fisherman", "pos": "n.", "meaning": "渔民"}],
    "s1": [{"word": "Creature", "pos": "n.", "meaning": "生物"}],
    "s3": [{"word": "Directly", "pos": "adv.", "meaning": "直接地"}],
    "s5": [{"word": "Peculiar", "pos": "adj.", "meaning": "奇怪的"}],
    "s7": [{"word": "Laugh", "pos": "v.", "meaning": "笑"}],
    "s8": [{"word": "Mistake", "pos": "n.", "meaning": "错误"}]
  },
  "nce2-l83": {
    "intro_3": [{"word": "Election", "pos": "n.", "meaning": "选举"}],
    "intro_4": [{"word": "Former", "pos": "adj.", "meaning": "以前的"}],
    "s1": [{"word": "Defeat", "pos": "v.", "meaning": "击败"}],
    "s2": [{"word": "Fanatical", "pos": "adj.", "meaning": "狂热的"}],
    "s3": [{"word": "Opponent", "pos": "n.", "meaning": "对手"}],
    "s4": [{"word": "Argument", "pos": "n.", "meaning": "争论"}],
    "s8": [{"word": "Result", "pos": "n.", "meaning": "结果"}]
  },
  "nce2-l84": {
    "intro_2": [{"word": "Strike", "pos": "n.", "meaning": "罢工"}],
    "intro_3": [{"word": "Busman", "pos": "n.", "meaning": "公交车司机"}],
    "s1": [{"word": "State", "pos": "v.", "meaning": "说明"}],
    "s2": [{"word": "Agreement", "pos": "n.", "meaning": "协议"}],
    "s4": [{"word": "Pressure", "pos": "n.", "meaning": "压力"}],
    "s6": [{"word": "Refuse", "pos": "v.", "meaning": "拒绝"}],
    "s7": [{"word": "Passenger", "pos": "n.", "meaning": "乘客"}]
  },
  "nce2-l85": {
    "intro_2": [{"word": "Decide", "pos": "v.", "meaning": "决定"}],
    "intro_4": [{"word": "Message", "pos": "n.", "meaning": "消息"}],
    "s1": [{"word": "Headmaster", "pos": "n.", "meaning": "校长"}],
    "s3": [{"word": "Request", "pos": "n.", "meaning": "请求"}],
    "s4": [{"word": "Former", "pos": "adj.", "meaning": "以前的"}],
    "s6": [{"word": "Devote", "pos": "v.", "meaning": "致力于"}]
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
            # Also just add a default empty analysis structure if it's missing entirely but we don't have data
            elif 'analysis' not in seg:
                 seg['analysis'] = {"words": []}
                 modified = True
            
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated {filename}")
            
    except Exception as e:
        print(f"Error updating {filename}: {e}")

