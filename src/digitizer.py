import json
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button

IMAGE_FILE = "Nightingale-mortality.jpg"
PROGRESS_FILE = "progress.json"
OUTPUT_CSV = "output_data.csv"

MONTHS_CHART1 = [
    "1854-04","1854-05","1854-06","1854-07",
    "1854-08","1854-09","1854-10","1854-11",
    "1854-12","1855-01","1855-02","1855-03"
]
MONTHS_CHART2 = [
    "1855-04","1855-05","1855-06","1855-07",
    "1855-08","1855-09","1855-10","1855-11",
    "1855-12","1856-01","1856-02","1856-03"
]
ALL_MONTHS = MONTHS_CHART1 + MONTHS_CHART2
LAYERS = ["blue", "red", "black"]
LAYER_COLORS = {"blue": "cyan", "red": "orange", "black": "white"}
LAYER_NAMES = {"blue": "DISEASE (blue)", "red": "WOUNDS (red)", "black": "OTHER (black)"}

def empty_data():
    return {m: {"blue": None, "red": None, "black": None} for m in ALL_MONTHS}

def compute_radius(center, point):
    return float(np.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2))

def save_progress(state):
    payload = {
        "center_right":   state["center_right"],
        "center_left":    state["center_left"],
        "data":           state["data"],
        "capture_index":  state["capture_index"],
        "layer_index":    state["layer_index"],
        "setting_center": state["setting_center"],
    }
    with open(PROGRESS_FILE, "w") as f:
        json.dump(payload, f, indent=2)

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return None
    with open(PROGRESS_FILE) as f:
        return json.load(f)

def export_csv(state):
    data = state["data"]
    cr = state["center_right"]
    cl = state["center_left"]
    incomplete = [m for m in ALL_MONTHS if any(v is None for v in data[m].values())]
    if incomplete:
        print(f"WARNING: {len(incomplete)} month(s) incomplete: {incomplete}")
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "month",
            "center_right_x", "center_right_y",
            "center_left_x",  "center_left_y",
            "disease_radius", "wounds_radius", "other_radius"
        ])
        for m in ALL_MONTHS:
            b = round(data[m]["blue"],  2) if data[m]["blue"]  is not None else ""
            r = round(data[m]["red"],   2) if data[m]["red"]   is not None else ""
            k = round(data[m]["black"], 2) if data[m]["black"] is not None else ""
            crx = round(cr[0], 2) if cr else ""
            cry = round(cr[1], 2) if cr else ""
            clx = round(cl[0], 2) if cl else ""
            cly = round(cl[1], 2) if cl else ""
            writer.writerow([m, crx, cry, clx, cly, b, r, k])
    print(f"\nExported to {OUTPUT_CSV}")
    print(f"\n{'Month':<12} {'Disease':>10} {'Wounds':>10} {'Other':>10}")
    for m in ALL_MONTHS:
        b = f"{data[m]['blue']:.1f}"  if data[m]["blue"]  is not None else "---"
        r = f"{data[m]['red']:.1f}"   if data[m]["red"]   is not None else "---"
        k = f"{data[m]['black']:.1f}" if data[m]["black"] is not None else "---"
        print(f"{m:<12} {b:>10} {r:>10} {k:>10}")

def load_and_display():
    saved = load_progress()
    state = {
        "center_right":   saved["center_right"]   if saved else None,
        "center_left":    saved["center_left"]     if saved else None,
        "data":           saved["data"]            if saved else empty_data(),
        "capture_index":  saved["capture_index"]   if saved else 0,
        "layer_index":    saved["layer_index"]     if saved else 0,
        "setting_center": saved["setting_center"]  if saved else "right",
        "markers": [],
        "lines":   [],
    }

    img = mpimg.imread(IMAGE_FILE)
    fig, ax = plt.subplots(figsize=(16, 9))
    plt.subplots_adjust(bottom=0.10)
    ax.imshow(img)
    ax.axis("off")

    status_text = ax.text(
        0.01, 0.01, "", transform=ax.transAxes,
        fontsize=10, color="yellow",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="black", alpha=0.7),
        verticalalignment="bottom"
    )

    def update_status():
        if state["setting_center"] == "right":
            status_text.set_text("SETUP: Click the CENTER of the RIGHT chart (April 1854)")
        elif state["setting_center"] == "left":
            status_text.set_text("SETUP: Click the CENTER of the LEFT chart (April 1855)")
        else:
            idx  = state["capture_index"]
            lidx = state["layer_index"]
            if idx >= len(ALL_MONTHS):
                status_text.set_text("ALL DONE - click Export CSV")
                fig.canvas.draw_idle()
                return
            month = ALL_MONTHS[idx]
            layer = LAYERS[lidx]
            done  = sum(1 for m in ALL_MONTHS for v in state["data"][m].values() if v is not None)
            total = len(ALL_MONTHS) * 3
            status_text.set_text(
                f"[{done}/{total}]  Month: {month}  |  Layer: {LAYER_NAMES[layer]}  |  Click outer edge"
            )
        fig.canvas.draw_idle()

    def on_click(event):
        if event.inaxes != ax:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata

        if state["setting_center"] == "right":
            state["center_right"] = [x, y]
            state["setting_center"] = "left"
            sc = ax.scatter(x, y, s=100, color="lime", edgecolors="black", zorder=7)
            state["markers"].append(sc)
            save_progress(state)
            update_status()
            print(f"Center RIGHT set: ({x:.1f}, {y:.1f})")
            return

        if state["setting_center"] == "left":
            state["center_left"] = [x, y]
            state["setting_center"] = "done"
            sc = ax.scatter(x, y, s=100, color="lime", edgecolors="black", zorder=7)
            state["markers"].append(sc)
            save_progress(state)
            update_status()
            print(f"Center LEFT set: ({x:.1f}, {y:.1f})")
            return

        idx  = state["capture_index"]
        lidx = state["layer_index"]
        if idx >= len(ALL_MONTHS):
            return

        month = ALL_MONTHS[idx]
        layer = LAYERS[lidx]
        center = state["center_right"] if idx < 12 else state["center_left"]
        r = compute_radius(center, [x, y])

        if r < 3:
            print(f"Click ignored: radius {r:.1f} too small")
            return

        state["data"][month][layer] = r
        color = LAYER_COLORS[layer]
        sc = ax.scatter(x, y, s=60, color=color, edgecolors="black", linewidths=0.8, zorder=6)
        ln, = ax.plot([center[0], x], [center[1], y], color=color, linewidth=1.0, alpha=0.6, zorder=5)
        state["markers"].append(sc)
        state["lines"].append(ln)
        print(f"{month} | {layer:5s} | r = {r:.1f} px")

        state["layer_index"] += 1
        if state["layer_index"] >= len(LAYERS):
            state["layer_index"]   = 0
            state["capture_index"] += 1

        save_progress(state)
        update_status()
        fig.canvas.draw_idle()

    def undo(event=None):
        if state["setting_center"] != "done":
            print("Nothing to undo during center setup.")
            return
        idx  = state["capture_index"]
        lidx = state["layer_index"]
        if lidx == 0 and idx == 0:
            print("Nothing to undo.")
            return
        if lidx == 0:
            state["capture_index"] -= 1
            state["layer_index"]    = len(LAYERS) - 1
        else:
            state["layer_index"] -= 1
        month = ALL_MONTHS[state["capture_index"]]
        layer = LAYERS[state["layer_index"]]
        state["data"][month][layer] = None
        if state["markers"]:
            state["markers"].pop().remove()
        if state["lines"]:
            state["lines"].pop().remove()
        save_progress(state)
        update_status()
        fig.canvas.draw_idle()
        print(f"Undone: {month} | {layer}")

    def on_key(event):
        if event.key == "z":
            undo()

    ax_undo   = plt.axes([0.01, 0.02, 0.08, 0.04])
    ax_export = plt.axes([0.11, 0.02, 0.10, 0.04])
    btn_undo   = Button(ax_undo,   "Undo (Z)",   color="0.85")
    btn_export = Button(ax_export, "Export CSV", color="0.7")
    btn_undo.on_clicked(undo)
    btn_export.on_clicked(lambda event: export_csv(state))

    fig.canvas.mpl_connect("button_press_event", on_click)
    fig.canvas.mpl_connect("key_press_event", on_key)
    update_status()

    print("\n=== NIGHTINGALE DIGITIZER ===")
    print("1. Click center of RIGHT chart, then LEFT chart")
    print("2. For each month: click blue outer edge, then red, then black")
    print("3. Press Z or Undo button to correct mistakes")
    print("4. Click Export CSV when done\n")

    plt.show()

if __name__ == "__main__":
    load_and_display()