from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

CANVAS_W, CANVAS_H = 758, 1024
PADDING = 30
INK = 0
DIVIDER = 180

font_cache = {}

def get_font(size=28, bold=False):
    key = (size, bold)
    if key in font_cache:
        return font_cache[key]
    
    # Try multiple font paths
    font_paths = [
        "./LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",  # Windows
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, size, index=1 if bold else 0)
                font_cache[key] = font
                return font
            except:
                continue
        try:
            font = ImageFont.truetype("arial.ttf", size)
            font_cache[key] = font
            return font
        except:
            font = ImageFont.load_default()
            font_cache[key] = font
            return font

def draw_header(draw, x, y, w, title, subtitle=""):
    font_title = get_font(52, bold=True)      # Was 60
    font_subtitle = get_font(32)              # Was 38
    draw.text((x + PADDING, y), title, fill=INK, font=font_title)
    if subtitle:
        subtitle_w = draw.textlength(subtitle, font=font_subtitle)
        draw.text((x + w - PADDING - subtitle_w, y + 10), subtitle, fill=DIVIDER, font=font_subtitle)
    underline_y = y + 70                      # Was 78
    draw.rectangle((x + PADDING, underline_y, x + w - PADDING, underline_y + 6), fill=INK)
    return y + 90                            # Was 100

def draw_task_row(draw, x, y, w, task, is_urgent=False):
    font_task = get_font(38, bold=bool(is_urgent))  # Was 44
    row_h = 85                                                  # Was 100
    title = task.get("title", "")
    draw.text((x + PADDING, y + 12), title, fill=INK, font=font_task)
    draw.line((x + PADDING, y + row_h - 6, x + w - PADDING, y + row_h - 6), fill=220, width=2)
    return y + row_h

def draw_bottom_bar(draw, battery_pct=None):
    bar_y = 954
    bar_h = 70
    draw.rectangle((0, bar_y, CANVAS_W, bar_y + bar_h), fill=INK)
    font_bar = get_font(36, bold=True)       # Was 42
    text_y = bar_y + (bar_h - 36) // 2
    left_text = []
    if battery_pct is not None:
        left_text.append(f"{battery_pct}%")
    left_text.append(datetime.now().strftime("%I:%M %p"))
    cx = PADDING
    for i, text in enumerate(left_text):
        if i > 0:
            draw.line((cx, bar_y + 14, cx, bar_y + bar_h - 14), fill=140, width=2)
            cx += 20
        draw.text((cx, text_y), text, fill=255, font=font_bar)
        cx += draw.textlength(text, font=font_bar) + 20

def render_todo_dashboard(tasks, battery_pct=None):
    img = Image.new('L', (CANVAS_W, CANVAS_H), 255)
    draw = ImageDraw.Draw(img)
    
    active_tasks = [t for t in tasks if not t.get("done", False)]
    total = len(tasks)
    done = total - len(active_tasks)
    subtitle = f"{done}/{total} done" if total else ""
    
    y = draw_header(draw, 0, 0, CANVAS_W, "To Do", subtitle)
    y += 8
    
    max_tasks = 7                          # Was 6 (fits more tasks now)
    for task in active_tasks[:max_tasks]:
        is_urgent = task.get("priority") == "P0"
        y = draw_task_row(draw, 0, y, CANVAS_W, task, is_urgent)
    
    if not active_tasks:
        font_empty = get_font(48)          # Was 56
        draw.text((CANVAS_W // 2 - 180, 450), "No Tasks to Complete", fill=DIVIDER, font=font_empty)
    
    draw_bottom_bar(draw, battery_pct)
    return img

if __name__ == "__main__":
    test_tasks = [
        {"title": "Buy groceries", "priority": "P0", "done": False},
        {"title": "Vacuum living room", "priority": "P1", "done": False},
        {"title": "Reply to emails", "priority": "P2", "done": False},
        {"title": "Water plants", "priority": "P2", "done": True},
        {"title": "Return library books", "priority": "P1", "done": False},
        {"title": "Fold laundry", "priority": "P3", "done": False},
        {"title": "Take out trash", "priority": "P2", "done": True},
    ]
    img = render_todo_dashboard(test_tasks, battery_pct=78)
    img.save("dashboard.png")
    print("Dashboard saved as dashboard.png")