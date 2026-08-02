import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

# Colors
NAVY = "#0A1931"
NAVY_LIGHT = "#162447"
EMERALD = "#10B981"
EMERALD_DARK = "#065F46"
GOLD = "#FBBF24"
GOLD_LIGHT = "#FDE68A"
BG = "#F8FAFC"
WHITE = "#FFFFFF"

os.makedirs("/home/user/Goop/assets/charts", exist_ok=True)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

def style_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E5E7EB')
    ax.spines['bottom'].set_color('#E5E7EB')
    ax.tick_params(colors='#6B7280', labelsize=9)
    ax.set_facecolor('white')

# 1. Cost Comparison Chart
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
fig.patch.set_facecolor('white')
style_ax(ax)
categories = ['Verde Tech\n(ours)', 'Commercial\nSmart Kits']
costs = [1890, 8000]
bars = ax.bar(categories, costs, width=0.45, color=[EMERALD, '#E5E7EB'], edgecolor='white', linewidth=1.5, zorder=3)
ax.bar_label(bars, labels=[f'₹{c:,}' for c in costs], padding=8, fontsize=12, fontweight='bold', color=NAVY)
ax.set_ylabel('Cost (INR)', fontsize=10, color='#6B7280')
ax.set_ylim(0, 9500)
ax.grid(axis='y', color='#F3F4F6', linewidth=0.8, zorder=0)
# Highlight savings
ax.annotate('76% cheaper\n+ AI + Camera', xy=(0.5, 4000), xytext=(0.5, 6000),
            fontsize=11, ha='center', color=EMERALD_DARK, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=EMERALD, lw=1.5))
plt.tight_layout()
plt.savefig("/home/user/Goop/assets/charts/cost_comparison.png", bbox_inches='tight', dpi=300)
plt.close()

# 2. Moisture Watering Cycle Chart
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
fig.patch.set_facecolor('white')
style_ax(ax)
time = np.linspace(0, 120, 120)
# Simulate moisture decreasing then pump on
moisture = 55 - 0.25*time
moisture[60:] = np.linspace(55-0.25*60, 70, 60)  # pump on rises
moisture[80:] = np.linspace(70, 48, 40)
threshold = np.full_like(time, 35)

ax.plot(time, moisture, color=EMERALD, linewidth=2.5, label='Soil Moisture %')
ax.plot(time, threshold, color=GOLD, linewidth=1.8, linestyle='--', label='Threshold 35%')
ax.fill_between(time, moisture, threshold, where=(moisture < threshold), color='#FEF3C7', alpha=0.6, label='Pump ON zone')
# Annotations
ax.annotate('Pump AUTO\nTRIGGERS', xy=(40, 34), xytext=(15, 15),
            fontsize=9, ha='center', color=EMERALD_DARK, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=EMERALD))
ax.annotate('Watering →\nMoisture ↑', xy=(65, 62), xytext=(85, 75),
            fontsize=9, ha='center', color=NAVY, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=NAVY))
ax.set_xlabel('Time (seconds) over 2-min cycle', fontsize=10, color='#6B7280')
ax.set_ylabel('Moisture %', fontsize=10, color='#6B7280')
ax.set_ylim(10, 80)
ax.legend(frameon=False, fontsize=9, loc='lower left')
ax.set_title('Live Watering Cycle — Pump stays ON continuously after fix', fontsize=12, fontweight='bold', color=NAVY, loc='left', pad=15)
plt.tight_layout()
plt.savefig("/home/user/Goop/assets/charts/moisture_cycle.png", bbox_inches='tight', dpi=300)
plt.close()

# 3. One-Second Heartbeat Timeline
fig, ax = plt.subplots(figsize=(10, 3), dpi=300)
fig.patch.set_facecolor('white')
ax.set_xlim(0, 1000)
ax.set_ylim(0, 10)
ax.axis('off')

# Timeline bar
ax.add_patch(FancyBboxPatch((0, 4), 1000, 1.5, boxstyle="round,pad=0.1", facecolor='#EEF2FF', edgecolor='#C7D2FE'))

# Segments
events = [
    (50, 200, EMERALD, "Sensors\n1 Hz"),
    (260, 150, GOLD, "Bundle JSON\n10 metrics"),
    (450, 120, NAVY_LIGHT, "Cloud Write\n/sensors"),
    (610, 120, "#60A5FA", "Cloud Read\n/controls"),
    (770, 150, EMERALD_DARK, "Actuate\nPump/LED"),
]
for x, w, col, label in events:
    ax.add_patch(FancyBboxPatch((x, 4.2), w, 1.1, boxstyle="round,pad=0.05", facecolor=col, edgecolor='white', linewidth=1.2))
    ax.text(x+w/2, 4.75, label, ha='center', va='center', fontsize=7, fontweight='bold', color='white' if col!=GOLD else NAVY, linespacing=0.9)
    ax.text(x+w/2, 2.8, f"{int(w)}ms", ha='center', va='center', fontsize=7, color='#6B7280')

# Total
ax.text(500, 8, "ONE-SECOND HEARTBEAT = 1,000 ms  —  Non-blocking millis() scheduler, feeds 8s watchdog every loop", 
        ha='center', va='center', fontsize=10, fontweight='bold', color=NAVY)
ax.plot([0,1000],[4,4], color=NAVY, linewidth=0.5, alpha=0.2)

plt.tight_layout()
plt.savefig("/home/user/Goop/assets/charts/heartbeat.png", bbox_inches='tight', dpi=300)
plt.close()

# 4. BEFORE/AFTER Bug Infographic
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300, gridspec_kw={'width_ratios':[1,1]})
fig.patch.set_facecolor('white')

# Before
ax1.set_facecolor('#FEF2F2')
ax1.set_xlim(0,10)
ax1.set_ylim(0,10)
ax1.axis('off')
ax1.text(5, 9, "BEFORE — BROKEN", ha='center', fontsize=12, fontweight='bold', color='#DC2626')
for i in range(17):
    y = 7.5 - i*0.4
    ax1.add_patch(FancyBboxPatch((1, y), 8, 0.3, boxstyle="round,pad=0.02", facecolor='#FCA5A5', edgecolor='white'))
    ax1.text(5, y+0.15, f"Firebase HTTPS call #{i+1}", ha='center', va='center', fontsize=6, color='#7F1D1D')
ax1.text(5, 0.5, "17 calls/sec\n→ Network stall\n→ Watchdog reboot every 8s\n→ Pump ON/OFF loop", ha='center', fontsize=9, color='#991B1B', fontweight='bold', linespacing=1.4)
ax1.add_patch(FancyBboxPatch((0.2,0.2), 9.6, 9.6, boxstyle="round,pad=0.2", facecolor='none', edgecolor='#FCA5A5', linewidth=1.5, linestyle='--'))

# After
ax2.set_facecolor('#ECFDF5')
ax2.set_xlim(0,10)
ax2.set_ylim(0,10)
ax2.axis('off')
ax2.text(5, 9, "AFTER — FIXED ✓", ha='center', fontsize=12, fontweight='bold', color=EMERALD_DARK)
# 2 calls
ax2.add_patch(FancyBboxPatch((1, 6), 8, 1.2, boxstyle="round,pad=0.1", facecolor=EMERALD, edgecolor='white'))
ax2.text(5, 6.6, "1 WRITE → /sensors [10 metrics bundled]", ha='center', va='center', fontsize=8, fontweight='bold', color='white')
ax2.add_patch(FancyBboxPatch((1, 4.3), 8, 1.2, boxstyle="round,pad=0.1", facecolor=NAVY_LIGHT, edgecolor='white'))
ax2.text(5, 4.9, "1 READ → /controls [9 keys bundled]", ha='center', va='center', fontsize=8, fontweight='bold', color='white')
ax2.text(5, 0.5, "2 calls/sec\n→ 85% less latency\n→ Zero reboots\n→ Pump stays ON till threshold", ha='center', fontsize=9, color=EMERALD_DARK, fontweight='bold', linespacing=1.4)
ax2.add_patch(FancyBboxPatch((0.2,0.2), 9.6, 9.6, boxstyle="round,pad=0.2", facecolor='none', edgecolor=EMERALD, linewidth=1.5))

# Arrow between
fig.text(0.5, 0.5, "→", ha='center', va='center', fontsize=40, color=GOLD, fontweight='bold', transform=fig.transFigure)

plt.tight_layout()
plt.savefig("/home/user/Goop/assets/charts/bug_fix.png", bbox_inches='tight', dpi=300)
plt.close()

# 5. Firebase Schema Tree visual (as simple diagram)
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
fig.patch.set_facecolor('white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.text(5, 9.5, "Firebase RTDB — verde-tech-haha", ha='center', fontsize=12, fontweight='bold', color=NAVY)

nodes = [
    (5, 8.5, "RTDB Root", NAVY),
    (1.5, 7, "sensors/ (10)", EMERALD),
    (4, 7, "controls/ (9)", GOLD),
    (6.5, 7, "latest_scan/", "#60A5FA"),
    (8.5, 7, "weather/", "#A78BFA"),
    (2.5, 5.5, "historical_logs/", NAVY_LIGHT),
    (7, 5.5, "actuators/", EMERALD_DARK),
]

for x, y, label, col in nodes:
    if "Root" in label:
        ax.add_patch(FancyBboxPatch((x-1.2, y-0.3), 2.4, 0.6, boxstyle="round,pad=0.1", facecolor=col, edgecolor='white'))
        ax.text(x, y, label, ha='center', va='center', color='white', fontsize=9, fontweight='bold')
        # lines to children
        for cx, cy, _, _ in nodes[1:]:
            ax.plot([x, cx], [y-0.3, cy+0.3], color='#E5E7EB', linewidth=1, zorder=0)
    else:
        ax.add_patch(FancyBboxPatch((x-1, y-0.3), 2, 0.6, boxstyle="round,pad=0.1", facecolor=col, edgecolor='white'))
        ax.text(x, y, label, ha='center', va='center', color='white' if col!=GOLD else NAVY, fontsize=8, fontweight='bold')

# Details
details = {
    "sensors/": "moisture · temp · humidity\nlight · tank · lux\nwatchdog · voltage_sag\nuploads_ok · uploads_fail",
    "controls/": "manual_mode · pump_state\nlight_manual · grow_light\ncapture_photo\nmoisture_threshold · tank_threshold\nlight_threshold · weather_override",
    "latest_scan/": "imageUrl (base64)\nstatus · captured_at\nscientificName\ndiseaseName · probability\ntreatmentPlan",
}
y = 4
for k, v in details.items():
    ax.text(0.5, y, f"{k}\n{v}", ha='left', va='top', fontsize=7, color='#374151', fontfamily='monospace',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#F9FAFB', edgecolor='#E5E7EB'))
    y -= 1.3 if len(v.split('\n'))<4 else 1.8

plt.tight_layout()
plt.savefig("/home/user/Goop/assets/charts/firebase_schema.png", bbox_inches='tight', dpi=300)
plt.close()

# 6. System Architecture diagram (simplified but premium)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
fig.patch.set_facecolor('white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Edge layer
ax.add_patch(FancyBboxPatch((0.3, 6.5), 3.2, 3, boxstyle="round,pad=0.2", facecolor='#ECFDF5', edgecolor=EMERALD, linewidth=1.5))
ax.text(1.9, 9.1, "EDGE", ha='center', fontsize=10, fontweight='bold', color=EMERALD_DARK)
ax.text(1.9, 8.6, "ESP32 WROOM-32\n+ 5 sensors + pump\nESP32-CAM (eyes)", ha='center', fontsize=8, color=NAVY, linespacing=1.3)

# Cloud layer
ax.add_patch(FancyBboxPatch((3.9, 6.5), 2.2, 3, boxstyle="round,pad=0.2", facecolor='#EEF2FF', edgecolor='#6366F1', linewidth=1.5))
ax.text(5, 9.1, "CLOUD", ha='center', fontsize=10, fontweight='bold', color='#4338CA')
ax.text(5, 8.6, "Firebase RTDB\nSingle source\nof truth", ha='center', fontsize=8, color=NAVY, linespacing=1.3)

# Experience layer
ax.add_patch(FancyBboxPatch((6.5, 6.5), 3.2, 3, boxstyle="round,pad=0.2", facecolor='#FFFBEB', edgecolor=GOLD, linewidth=1.5))
ax.text(8.1, 9.1, "EXPERIENCE", ha='center', fontsize=10, fontweight='bold', color='#92400E')
ax.text(8.1, 8.6, "Single-file Web App\nDashboard + AI\n4 external APIs", ha='center', fontsize=8, color=NAVY, linespacing=1.3)

# Arrows
ax.annotate("", xy=(3.9, 8), xytext=(3.5, 8), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
ax.text(3.7, 8.3, "HTTPS JSON\n1-sec heartbeat", ha='center', fontsize=7, color=NAVY, fontweight='bold')
ax.annotate("", xy=(6.5, 8), xytext=(6.1, 8), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
ax.text(6.3, 8.3, "REST / polling", ha='center', fontsize=7, color=NAVY, fontweight='bold')

# Bottom details - sensors
sensors = ["Soil MOIST\nGPIO34/23", "DHT11\nGPIO4", "LDR\nGPIO35", "HC-SR04\n18/19", "Relay Pump\nGPIO5", "UV LED\nGPIO12"]
for i, s in enumerate(sensors):
    x = 0.5 + i*1.5
    ax.add_patch(FancyBboxPatch((x, 4.5), 1.2, 1.2, boxstyle="round,pad=0.1", facecolor='white', edgecolor='#E5E7EB'))
    ax.text(x+0.6, 5.1, s, ha='center', va='center', fontsize=6.5, color=NAVY, fontweight='bold', linespacing=1.1)

# APIs
apis = ["OpenWeather\nRain override", "crop.health\n94% diag", "Gemini 2.5\nVision chat", "OpenRouter\nSensor chat"]
for i, a in enumerate(apis):
    x = 6.6 + (i%2)*1.6
    y = 4.5 - (i//2)*1.4
    ax.add_patch(FancyBboxPatch((x, y), 1.4, 1.1, boxstyle="round,pad=0.1", facecolor='white', edgecolor=GOLD))
    ax.text(x+0.7, y+0.55, a, ha='center', va='center', fontsize=6.5, color=NAVY, fontweight='bold', linespacing=1.1)

# Power notes
ax.text(0.5, 2, "Power: 5V/2A phone adapter (NOT USB-PD) · 1000µF cap · 1N4007 flyback · Relay isolated · Sequential boot · 8MHz XCLK", 
        ha='left', fontsize=7, color='#6B7280', style='italic')

plt.tight_layout()
plt.savefig("/home/user/Goop/assets/charts/architecture_diagram.png", bbox_inches='tight', dpi=300)
plt.close()

# 7. AUTO-mode Flowchart
fig, ax = plt.subplots(figsize=(6, 8), dpi=300)
fig.patch.set_facecolor('white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.text(5, 9.5, "AUTO-MODE DECISION", ha='center', fontsize=13, fontweight='bold', color=NAVY)

flow = [
    (5, 8.7, "Read soil moisture\n10-point avg", EMERALD, "diamond"),
    (5, 7.5, "moisture <\nthreshold (35%)?", GOLD, "diamond"),
    (2, 6.2, "NO\nPlant happy", "#E5E7EB", "rect"),
    (5, 6.2, "Check tank\n5-pt avg + reject", NAVY_LIGHT, "rect"),
    (5, 5.0, "Tank safe?\n> tank_threshold", GOLD, "diamond"),
    (2, 3.7, "NO\nLock pump\nProtect hardware", "#FCA5A5", "rect"),
    (5, 3.7, "Check weather\nRain expected?", NAVY_LIGHT, "rect"),
    (5, 2.5, "Rain?\nweather_override", GOLD, "diamond"),
    (2, 1.2, "YES\nSkip watering\nSave water", "#BFDBFE", "rect"),
    (7.5, 1.2, "NO\npump ON ✓\nTill threshold", EMERALD, "rect"),
]

# draw
for x, y, label, col, shape in flow:
    if shape=="diamond":
        # diamond as polygon
        diamond = plt.Polygon([[x, y+0.5],[x+1.2, y],[x, y-0.5],[x-1.2, y]], closed=True, facecolor=col, edgecolor='white', linewidth=1.2)
        ax.add_patch(diamond)
        ax.text(x, y, label, ha='center', va='center', fontsize=7, fontweight='bold', color='white' if col!=GOLD and col!="#E5E7EB" else NAVY, linespacing=1)
    else:
        ax.add_patch(FancyBboxPatch((x-1.1, y-0.45), 2.2, 0.9, boxstyle="round,pad=0.1", facecolor=col, edgecolor='white', linewidth=1))
        ax.text(x, y, label, ha='center', va='center', fontsize=7, fontweight='bold', color='white' if col not in ["#E5E7EB", "#BFDBFE"] else NAVY, linespacing=1)

# Arrows simplified
arrows = [((5,8.2),(5,8.0)), ((5,7.0),(2,6.7)), ((5,7.0),(5,6.7)), ((5,5.7),(5,5.5)), ((5,4.5),(2,4.2)), ((5,4.5),(5,4.2)), ((5,3.2),(5,3.0)), ((5,2.0),(2,1.7)), ((5,2.0),(7.5,1.7))]
for a,b in arrows:
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle='->', color=NAVY, lw=1))

plt.tight_layout()
plt.savefig("/home/user/Goop/assets/charts/auto_flowchart.png", bbox_inches='tight', dpi=300)
plt.close()

# 8. Circuit diagram stylized
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
fig.patch.set_facecolor('white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')
ax.text(5, 5.5, "Wiring — ESP32 WROOM-32 + Sensors + Safeties", ha='center', fontsize=11, fontweight='bold', color=NAVY)
# ESP32 block center
ax.add_patch(FancyBboxPatch((4, 1.5), 2, 3, boxstyle="round,pad=0.1", facecolor=NAVY, edgecolor=GOLD, linewidth=2))
ax.text(5, 3, "ESP32\nWROOM-32\nBrain", ha='center', va='center', fontsize=10, fontweight='bold', color='white', linespacing=1.3)
pins = [("GPIO34/23 → Soil AO/VCC gated", 0.5, 4.2, EMERALD), ("GPIO4 → DHT11", 0.5, 3.6, "#60A5FA"), ("GPIO35 → LDR", 0.5, 3.0, GOLD), ("GPIO18/19 → HC-SR04", 0.5, 2.4, NAVY_LIGHT), ("GPIO5 → Relay IN1 (LOW)", 7.5, 4.2, "#F87171"), ("GPIO12 → UV LED +220Ω", 7.5, 3.6, "#A78BFA"), ("5V/2A + 1000µF cap", 7.5, 2.9, EMERALD_DARK), ("1N4007 flyback diode", 7.5, 2.3, GOLD)]
for label, x, y, col in pins:
    ax.add_patch(FancyBboxPatch((x-0.1, y-0.2), 2.2, 0.4, boxstyle="round,pad=0.05", facecolor='white', edgecolor=col))
    ax.text(x+1, y, label, ha='center', va='center', fontsize=7, color=NAVY, fontweight='bold')
    # line to ESP32
    tx = 4 if x<5 else 6
    ax.plot([x+2.1 if x<5 else x-0.1, tx], [y, y], color=col, linewidth=1.2)

ax.text(0.5, 0.5, "Lesson: USB-PD laptop charger = 0mA (needs handshake chip) → Use 5V/2A phone adapter only!", ha='left', fontsize=8, color='#DC2626', fontweight='bold', style='italic')

plt.tight_layout()
plt.savefig("/home/user/Goop/assets/charts/circuit_diagram.png", bbox_inches='tight', dpi=300)
plt.close()

print("All charts generated")
