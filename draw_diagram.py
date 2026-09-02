import argparse
import json
import os
import cv2
import numpy as np

def draw_hud_panel(img, metrics):
    """繪製高階運動科學 HUD 數據面板，提升專業視覺質感"""
    h, w, _ = img.shape
    overlay = img.copy()
    
    # 面板座標與樣式 (右上角)
    box_x1, box_y1, box_x2, box_y2 = w - 420, 40, w - 40, 240
    cv2.rectangle(overlay, (box_x1, box_y1), (box_x2, box_y2), (15, 23, 42), -1)
    cv2.rectangle(img, (box_x1, box_y1), (box_x2, box_y2), (0, 229, 255), 2)
    
    # 內文排版
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(overlay, "SBA SYSTEMIC BIOMECHANICS AUDIT", (box_x1 + 15, box_y1 + 30), font, 0.5, (0, 229, 255), 1, cv2.LINE_AA)
    cv2.line(overlay, (box_x1 + 15, box_y1 + 40), (box_x2 - 15, box_y1 + 40), (100, 100, 100), 1)
    
    texts = [
        f"External Load: {metrics.get('external_load', '180 kg')}",
        f"Ground Reaction (GRF): {metrics.get('grf', '3,200 N')}",
        f"Hip/Knee Moment Ratio: {metrics.get('moment_ratio', '1.85 (Dominant)')}",
        f"L5/S1 Shear Stress: {metrics.get('shear_stress', 'CRITICAL (High)')}",
        f"Status: {metrics.get('status', 'IMMEDIATE CORRECTION REQ.')}"
    ]
    
    for i, text in enumerate(texts):
        color = (0, 0, 255) if "CRITICAL" in text or "IMMEDIATE" in text else (255, 255, 255)
        cv2.putText(overlay, text, (box_x1 + 15, box_y1 + 75 + i * 25), font, 0.45, color, 1, cv2.LINE_AA)
        
    # 融合透明度
    alpha = 0.85
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

def process_image(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    img_name = data.get("image", "IMG_3871.jpeg")
    if not os.path.exists(img_name):
        raise FileNotFoundError(f"找不到對應影像檔案: {img_name}")
        
    img = cv2.imread(img_name)
    h, w, _ = img.shape
    
    # 1. 繪製主外力線 (紅色：External Load)
    start_ext = (int(w * 0.48), int(h * 0.35))
    end_ext = (int(w * 0.48), int(h * 0.75))
    cv2.arrowedLine(img, start_ext, end_ext, (0, 0, 255), 4, tipLength=0.03)
    cv2.putText(img, "External Load (180 kg)", (end_ext[0] + 15, end_ext[1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # 2. 繪製地面反作用力線 (青色：GRF)
    start_grf = (int(w * 0.49), int(h * 0.78))
    end_grf = (int(w * 0.49), int(h * 0.50))
    cv2.arrowedLine(img, start_grf, end_grf, (255, 255, 0), 4, tipLength=0.03)
    cv2.putText(img, "GRF (3,200 N)", (end_grf[0] + 15, end_grf[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    # 3. 繪製腰椎剪切力警示圓圈與力矩臂
    cv2.circle(img, (int(w * 0.48), int(h * 0.58)), 25, (0, 0, 255), 2)
    cv2.putText(img, "L5/S1 Stress Vector", (int(w * 0.48) - 70, int(h * 0.58) - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)

    # 4. 載入動態數據面板
    metrics = data.get("metrics", {
        "external_load": "180 kg",
        "grf": "3,200 N",
        "moment_ratio": "1.85 (Hip Dominant)",
        "shear_stress": "CRITICAL (High)",
        "status": "IMMEDIATE CORRECTION REQ."
    })
    draw_hud_panel(img, metrics)
    
    output_name = "output_sba_analysis.jpeg"
    cv2.imwrite(output_name, img)
    print(f"高階分析圖已成功生成: {output_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SBA Advanced Biomechanical Visualizer")
    parser.add_argument("--json", required=True, help="Path to JSON configuration file")
    args = parser.parse_args()
    process_image(args.json)
