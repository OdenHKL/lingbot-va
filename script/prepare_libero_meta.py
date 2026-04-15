import json
import os
import argparse
from pathlib import Path

def process_episodes_jsonl(dataset_dir):
    meta_dir = Path(dataset_dir) / "meta"
    episodes_file = meta_dir / "episodes.jsonl"
    
    if not episodes_file.exists():
        raise FileNotFoundError(f"Cannot find {episodes_file}. Make sure the dataset is in LeRobot format.")
    
    out_lines = []
    updated_count = 0
    
    with open(episodes_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            data = json.loads(line)
            
            # Check if action_config already exists
            if "action_config" not in data:
                # In LIBERO, an episode usually corresponds to a single task
                # We can use the first task description as the action_text
                task_desc = data.get("tasks", [""])[0] if data.get("tasks") else ""
                length = data.get("length", 0)
                
                # Add action_config mapping the whole episode to the task description
                data["action_config"] = [
                    {
                        "start_frame": 0,
                        "end_frame": length,
                        "action_text": task_desc
                    }
                ]
                updated_count += 1
            
            out_lines.append(json.dumps(data, ensure_ascii=False))
            
    # Write back to episodes.jsonl
    with open(episodes_file, 'w', encoding='utf-8') as f:
        for line in out_lines:
            f.write(line + '\n')
            
    print(f"✅ Successfully updated {updated_count} episodes in {episodes_file} with 'action_config'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add action_config to LeRobot dataset for LingBot-VA")
    parser.add_argument("--dataset_dir", type=str, required=True, help="Path to the LeRobot dataset directory")
    args = parser.parse_args()
    
    process_episodes_jsonl(args.dataset_dir)
