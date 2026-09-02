import json
import os
import cv2
import matplotlib.pyplot as plt

def render_sba_force_diagram(json_file):
    # 確保輸出目錄存在
    os.makedirs("./outputs", exist_ok=True)
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # 1. 載入原始影像底圖
    img = cv2.imread(data['metadata']['image_path'])
    if img is None:
        raise FileNotFoundError(f"找不到底圖檔案：{data['metadata']['image_path']}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    fig, ax = plt.subplots(figsize=(12, 6.75), dpi=data['canvas_config']['dpi'])
    ax.imshow(img)
    
    # 2. 繪製力量向量箭頭 (Force Vectors)
    for v in data['force_vectors']:
        origin = next(k['xy'] for k in data['keypoints'] if k['id'] == v['origin_keypoint'])
        ax.quiver(origin[0], origin[1], v['vector_xy'][0], v['vector_xy'][1], 
                  angles='xy', scale_units='xy', scale=1, color=v['color'], width=0.008)
        ax.text(origin[0] + v['vector_xy'][0]*0.5, origin[1] + v['vector_xy'][1]*0.5, 
                v['label'], color=v['color'], fontsize=12, fontweight='bold')
        
    # 3. 繪製受傷關鍵力臂 (Moment Arms)
    for ma in data['moment_arms']:
        pass
        
    plt.axis('off')
    plt.tight_layout()
    output_path = "./outputs/case_05_larry_wheels_sba.png"
    plt.savefig(output_path, bbox_inches='tight')
    print(f"SBA 力線圖已成功生成於：{output_path}")

# 程式啟動入口
if __name__ == "__main__":
    json_path = "case_05_larry_wheels.json"
    render_sba_force_diagram(json_path)
