#!/usr/bin/env python3
"""
Project Verde ULTIMATE — Over-the-top world-class documentation
Uses: ReportLab + Pillow + Matplotlib + AI-generated images + FX (shadows, glassmorphism, gradients, gold foil)
No WeasyPrint due to missing pango lib, but mimics its polish with ReportLab canvas FX.
"""
from pathlib import Path
import math

ASSETS_DIR = Path("assets")
ASSETS_DIR.mkdir(exist_ok=True)

# Re-gen charts with FX
def gen_charts_fx():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    NAVY="#0B1D3A"
    EMERALD="#10B981"
    EMERALD_DARK="#059669"
    GOLD="#F59E0B"
    GRAY="#9CA3AF"

    # Cost with FX shadow & gradient
    fig, ax = plt.subplots(figsize=(6.5,3.4), dpi=250)
    fig.patch.set_facecolor('#F9FAFB')
    categories=['Verde\nRs.1,890','Basic\nRs.8,000','Premium\nRs.12,500']
    costs=[1890,8000,12500]
    colors=[EMERALD,'#CBD5E1','#94A3B8']
    # shadow
    ax.bar(categories, [c+400 for c in costs], color='#E5E7EB', width=0.56, zorder=1, alpha=0.8)
    bars=ax.bar(categories, costs, color=colors, width=0.55, edgecolor='white', linewidth=1.5, zorder=3)
    for bar,cost in zip(bars,costs):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+350, f"Rs. {cost:,}", ha='center', va='bottom', fontsize=12, fontweight='bold', color=NAVY)
    ax.set_ylim(0,15000)
    ax.grid(axis='y', alpha=0.12, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.annotate('76% cheaper\n+ camera + AI', xy=(0,1890), xytext=(0.8,7200), fontsize=9, color=EMERALD_DARK, fontweight='bold', arrowprops=dict(arrowstyle='->', color=EMERALD_DARK, lw=1.5), ha='center', bbox=dict(boxstyle='round,pad=0.4', fc='#D1FAE5', ec=EMERALD, alpha=0.6))
    plt.tight_layout()
    plt.savefig(ASSETS_DIR/"cost_comparison.png", bbox_inches='tight')
    plt.close()

    # Moisture with gradient fill
    fig, ax = plt.subplots(figsize=(6.5,3.4), dpi=250)
    t=np.linspace(0,120,300)
    moisture=np.piecewise(t,[t<75,t>=75],[lambda tt:27+(35-27)*(tt/75)+0.3*np.sin(tt*0.4), lambda tt:35+(42-35)*(1-np.exp(-(tt-75)/22))])
    moisture+=np.random.normal(0,0.12,size=t.shape)
    ax.plot(t, moisture, color=EMERALD, linewidth=2.8, zorder=3)
    ax.fill_between(t, moisture, 20, where=(t<75), color=EMERALD, alpha=0.15, zorder=2)
    ax.fill_between(t, moisture, 20, where=(t>=75), color=GRAY, alpha=0.08)
    ax.axhline(35, color=GOLD, linestyle='--', linewidth=1.8, alpha=0.9)
    ax.text(25,68,'PUMP ON (AUTO)', ha='center', fontsize=9, fontweight='bold', color=EMERALD_DARK, bbox=dict(facecolor='#D1FAE5', edgecolor=EMERALD, boxstyle='round,pad=0.4'))
    ax.text(95,68,'PUMP OFF - Target Reached', ha='center', fontsize=8, color=GRAY)
    ax.set_xlabel('Time (seconds)'); ax.set_ylabel('Moisture %')
    ax.set_ylim(20,75); ax.set_xlim(0,120)
    ax.grid(alpha=0.12)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(ASSETS_DIR/"moisture_cycle.png", bbox_inches='tight')
    plt.close()

    # API before after with shadow
    fig, ax = plt.subplots(figsize=(6.5,3.2), dpi=250)
    labels=['BEFORE\n17 calls/s','AFTER\n2 calls/s\nJSON Bundled']
    values=[17,2]
    ax.bar(labels,[v+0.6 for v in values], color='#FEE2E2', width=0.5, zorder=1)
    bars=ax.bar(labels, values, color=['#EF4444',EMERALD], width=0.5, edgecolor='white', linewidth=1.5, zorder=3)
    for bar,v in zip(bars,values):
        ax.text(bar.get_x()+bar.get_width()/2, v+0.6, f"{v}", ha='center', va='bottom', fontsize=15, fontweight='bold', color=NAVY)
    ax.set_ylim(0,20)
    ax.annotate('', xy=(1,3), xytext=(0,15.5), arrowprops=dict(arrowstyle='->,head_width=0.7,head_length=0.7', color=GOLD, lw=3, connectionstyle='arc3,rad=0.25'))
    ax.text(0.5,9.5,'-85% latency\n0 reboots\nPump stable', ha='center', fontsize=10, fontweight='bold', color='#92400E', bbox=dict(facecolor='#FEF3C7', edgecolor=GOLD, boxstyle='round,pad=0.6'))
    ax.grid(axis='y', alpha=0.12)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(ASSETS_DIR/"api_before_after.png", bbox_inches='tight')
    plt.close()

    # Heartbeat
    fig, ax = plt.subplots(figsize=(6.5,2.2), dpi=250)
    ax.set_xlim(0,1000); ax.set_ylim(0,3); ax.axis('off')
    ax.plot([0,1000],[1.5,1.5], color=NAVY, linewidth=2.5, alpha=0.18, solid_capstyle='round')
    events=[(50,"Sensors\n1 Hz",EMERALD),(250,"10-pt Avg\nFilter","#6366F1"),(450,"JSON Bundle\n10 metrics",NAVY),(650,"Read /controls\n9 keys",GOLD),(850,"Auto Logic\nDecision",EMERALD_DARK)]
    for x,label,col in events:
        ax.plot([x,x],[1.5,2.3], color=col, linewidth=2.2)
        ax.scatter([x],[1.5], s=110, color=col, zorder=5, edgecolor='white', linewidth=1.8)
        ax.text(x,2.5,label, ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=NAVY)
        ax.text(x,0.6,f"{x}ms", ha='center', fontsize=6.5, color=GRAY)
    ax.text(500,0.15,'<-- 1-Second Heartbeat — repeats every 1000 ms -->', ha='center', fontsize=8.5, color=NAVY, fontweight='bold')
    plt.tight_layout()
    plt.savefig(ASSETS_DIR/"heartbeat.png", bbox_inches='tight')
    plt.close()
    print("FX charts generated")

# Now ultimate PDF
def build_ultimate():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor, white
    from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, NextPageTemplate, Flowable
    from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Polygon, Line
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    W,H=A4
    NAVY=HexColor("#0B1D3A")
    NAVY2=HexColor("#162F5A")
    EMERALD=HexColor("#10B981")
    EM_DARK=HexColor("#059669")
    EM_LIGHT=HexColor("#D1FAE5")
    EM_PALE=HexColor("#ECFDF5")
    GOLD=HexColor("#F59E0B")
    GOLD_LIGHT=HexColor("#FEF3C7")
    GOLD_DARK=HexColor("#D97706")
    G50=HexColor("#F9FAFB")
    G100=HexColor("#F3F4F6")
    G200=HexColor("#E5E7EB")
    G400=HexColor("#9CA3AF")
    G600=HexColor("#4B5563")
    G800=HexColor("#1F2937")

    class Anchor(Flowable):
        def __init__(self, name, label=None):
            Flowable.__init__(self)
            self.name=name; self.label=label or name
            self.width=0; self.height=0
        def draw(self):
            self.canv.bookmarkPage(self.name)
            lvl=0 if self.name.startswith('h1_') else 1
            try:
                self.canv.addOutlineEntry(self.label, self.name, level=lvl, closed=False)
            except: pass

    def make_arch():
        d=Drawing(500,220)
        def box(x,y,w,h,fill,stroke,title,items):
            # shadow
            d.add(Rect(x+2,y-2,w,h, fillColor=HexColor("#E5E7EB"), strokeColor=HexColor("#E5E7EB"), rx=8))
            d.add(Rect(x,y,w,h, fillColor=fill, strokeColor=stroke, strokeWidth=1.2, rx=8))
            d.add(String(x+10,y+h-18,title, fontName='Helvetica-Bold', fontSize=10, fillColor=NAVY))
            for i,it in enumerate(items):
                d.add(String(x+10,y+h-32-i*13,f"* {it}", fontName='Helvetica', fontSize=7, fillColor=G800))
        box(10,20,150,180,EM_PALE,EMERALD,"EDGE",["ESP32 WROOM-32 (brain)","ESP32-CAM OV2640","Soil LM393 AO->34","DHT11 -> GPIO4","LDR -> GPIO35","HC-SR04 18/19","Relay GPIO5 + UV LED 12"])
        box(185,20,130,180,white,G200,"CLOUD",["Firebase RTDB","/sensors 10 metrics","/controls 9 keys","/latest_scan b64","/weather live","public read + secret","1 write + 1 read /sec"])
        box(340,20,150,180,HexColor("#FFFBEB"),GOLD,"EXPERIENCE",["Single-file HTML","Dashboard 8 tiles","Weather + 5-day","Plant Doctor <=2s","Gemini + OpenRouter","Tank cal SET","Demo mode + toasts"])
        def arrow(x1,y1,x2,y2,c=G400):
            d.add(Line(x1,y1,x2,y2, strokeColor=c, strokeWidth=1.2))
            d.add(Polygon([x2-6,y2-3,x2,y2,x2-6,y2+3], fillColor=c, strokeColor=c))
        arrow(160,110,185,110,EMERALD)
        arrow(315,110,340,110,GOLD)
        return d

    def make_firebase():
        d=Drawing(500,240)
        d.add(Rect(182,200,140,30, fillColor=NAVY, strokeColor=NAVY, rx=6))
        d.add(String(252,218,"verde-tech-haha (RTDB)", fontName='Helvetica-Bold', fontSize=9, fillColor=white, textAnchor='middle'))
        branches=[("sensors/",["moisture,temp,hum,light,tank","lux,watchdog,voltage_sag"],0),("controls/",["manual_mode,pump_state","capture_photo,thresholds","weather_override"],1),("latest_scan/",["imageUrl b64,status","scientificName,disease","probability,treatment"],2),("weather/",["city,temp,condition","humidity,wind,rain"],3),("historical_logs/",["moisture_log [{time,moisture}]"],4),("actuators/",["pump_actual,grow_light,mode"],5)]
        cols=[EMERALD,GOLD,HexColor("#6366F1"),HexColor("#EC4899"),HexColor("#06B6D4"),HexColor("#84CC16")]
        fills=[EM_PALE,GOLD_LIGHT,HexColor("#EEF2FF"),HexColor("#FDF2F8"),HexColor("#ECFEFF"),HexColor("#F7FEE7")]
        for idx,(name,items,_) in enumerate(branches):
            x=10+(idx%3)*170; y=140-(idx//3)*110
            d.add(Rect(x+2,y-2,155,75, fillColor=HexColor("#E5E7EB"), strokeColor=HexColor("#E5E7EB"), rx=6))
            d.add(Rect(x,y,155,75, fillColor=fills[idx], strokeColor=cols[idx], strokeWidth=1, rx=6))
            d.add(String(x+8,y+58,name, fontName='Helvetica-Bold', fontSize=8, fillColor=NAVY))
            for j,it in enumerate(items[:2]):
                d.add(String(x+8,y+45-j*11,f"- {it}", fontName='Helvetica', fontSize=6, fillColor=G600))
            d.add(Line(250,200,x+77,y+75, strokeColor=G200, strokeWidth=0.8))
        return d

    def make_flowchart():
        d=Drawing(460,260)
        def rbox(x,y,w,h,txt,fill=white,stroke=NAVY,bold=False):
            d.add(Rect(x+1,y-1,w,h, fillColor=HexColor("#E5E7EB"), strokeColor=HexColor("#E5E7EB"), rx=6))
            d.add(Rect(x,y,w,h, fillColor=fill, strokeColor=stroke, rx=6, strokeWidth=1))
            d.add(String(x+w/2,y+h/2-3,txt, fontName='Helvetica-Bold' if bold else 'Helvetica', fontSize=7.5, fillColor=NAVY, textAnchor='middle'))
        def diamond(x,y,w,h,txt):
            cx=x+w/2; cy=y+h/2
            pts=[cx,y+h,x+w,cy,cx,y,x,cy]
            d.add(Polygon(pts, fillColor=GOLD_LIGHT, strokeColor=GOLD, strokeWidth=1))
            for i,l in enumerate(txt.split('\n')):
                d.add(String(cx,cy+6-i*9,l, fontName='Helvetica-Bold', fontSize=7, fillColor=NAVY, textAnchor='middle'))
        rbox(160,220,140,28,"Start: 1-sec Loop",EM_PALE,EMERALD,True)
        rbox(160,180,140,28,"Read: moisture % (10-pt avg)")
        diamond(160,135,140,35,"moisture <\nthreshold (35%)?")
        rbox(20,100,100,28,"Pump OFF",G100,G400)
        diamond(160,85,140,35,"tank safe?\nlevel >15%?")
        rbox(20,30,100,28,"Tank Lock OFF",HexColor("#FEF2F2"),HexColor("#FCA5A5"))
        diamond(160,20,140,35,"rain expected?\nweather_override?")
        rbox(300,20,120,28,"Pump ON - Continuous",EMERALD,EMERALD,True)
        rbox(300,100,120,28,"Pump OFF + Wait",G100,G400)
        def conn(x1,y1,x2,y2):
            d.add(Line(x1,y1,x2,y2, strokeColor=NAVY, strokeWidth=0.8))
        conn(230,220,230,208); conn(230,180,230,170); conn(160,152,120,152); conn(120,152,120,128); conn(70,100,230,100); conn(230,100,230,120); conn(230,85,230,70); conn(160,102,120,102); conn(120,102,120,58); conn(160,37,120,37); conn(120,37,120,30); conn(230,20,300,33); conn(300,85,300,33)
        d.add(String(305,155,"No", fontName='Helvetica-Bold', fontSize=7, fillColor=GOLD_DARK))
        d.add(String(250,138,"Yes", fontName='Helvetica-Bold', fontSize=7, fillColor=EM_DARK))
        d.add(String(305,105,"No", fontName='Helvetica-Bold', fontSize=7, fillColor=GOLD_DARK))
        d.add(String(250,88,"Yes", fontName='Helvetica-Bold', fontSize=7, fillColor=EM_DARK))
        d.add(String(305,40,"Yes -> OFF", fontName='Helvetica-Bold', fontSize=7, fillColor=GOLD_DARK))
        d.add(String(250,40,"No", fontName='Helvetica-Bold', fontSize=7, fillColor=EM_DARK))
        return d

    def make_bug():
        d=Drawing(500,170)
        d.add(Rect(12,10,220,150, fillColor=HexColor("#FEF2F2"), strokeColor=HexColor("#FECACA"), rx=10, strokeWidth=1))
        d.add(String(20,145,"BEFORE - Loop Bug", fontName='Helvetica-Bold', fontSize=10, fillColor=HexColor("#DC2626")))
        for i,b in enumerate(["17 Firebase HTTPS calls / sec","Network stalls -> 8s WDT reboot","Pump clicks ON/OFF ~10s","Voltage sag, logs spurt, jitter"]):
            d.add(Circle(25,125-i*14,3, fillColor=HexColor("#DC2626"), strokeColor=HexColor("#DC2626")))
            d.add(String(32,123-i*14,b, fontName='Helvetica', fontSize=7, fillColor=G800))
        d.add(Rect(242,65,40,40, fillColor=GOLD_LIGHT, strokeColor=GOLD, rx=20))
        d.add(String(262,84,"FIX", fontName='Helvetica-Bold', fontSize=10, fillColor=GOLD_DARK, textAnchor='middle'))
        d.add(Rect(302,10,190,150, fillColor=EM_PALE, strokeColor=EMERALD, rx=10, strokeWidth=1.2))
        d.add(String(312,145,"AFTER - JSON Bundling", fontName='Helvetica-Bold', fontSize=10, fillColor=EM_DARK))
        for i,b in enumerate(["1 write -> /sensors (10 metrics)","1 read -> /controls (9 keys)","~85% latency cut, zero reboots","Pump ON continuous","Watchdog 10+ min"]):
            d.add(Circle(317,125-i*14,3, fillColor=EMERALD, strokeColor=EMERALD))
            d.add(String(324,123-i*14,b, fontName='Helvetica', fontSize=7, fillColor=G800))
        return d

    def make_circuit():
        d=Drawing(500,220)
        d.add(Rect(202,40,100,140, fillColor=NAVY, strokeColor=NAVY, rx=8))
        d.add(String(252,155,"ESP32\nWROOM-32\nBRAIN", fontName='Helvetica-Bold', fontSize=8, fillColor=white, textAnchor='middle', leading=10))
        for label,y in [("GPIO23 -> VCC Soil",170),("GPIO34 <- AO Soil",150),("GPIO4 <- DHT11",130),("GPIO35 <- LDR AO",110),("GPIO18 -> TRIG",90),("GPIO19 <- ECHO",70)]:
            d.add(Line(100,y,200,y, strokeColor=G400, strokeWidth=0.8))
            d.add(Circle(100,y,4, fillColor=EM_LIGHT, strokeColor=EMERALD))
            d.add(String(5,y-3,label, fontName='Helvetica', fontSize=6, fillColor=G800))
        for label,y in [("GPIO5 -> Relay IN1 (LOW)",170),("GPIO12 -> UV LED (HIGH)",130),("5V/2A + 1000uF",90),("GND Shared Bus",50)]:
            d.add(Line(300,y,400,y, strokeColor=G400, strokeWidth=0.8))
            d.add(Circle(400,y,4, fillColor=GOLD_LIGHT, strokeColor=GOLD))
            d.add(String(410,y-3,label, fontName='Helvetica', fontSize=6, fillColor=G800))
        d.add(Rect(10,5,180,35, fillColor=GOLD_LIGHT, strokeColor=GOLD, rx=6))
        d.add(String(15,28,"Power Lessons:", fontName='Helvetica-Bold', fontSize=7, fillColor=GOLD_DARK))
        d.add(String(15,18,"* 5V/2A not PD charger\n* 1000uF cap, 1N4007 diode", fontName='Helvetica', fontSize=6, fillColor=G800, leading=7))
        d.add(Rect(310,5,180,35, fillColor=HexColor("#EEF2FF"), strokeColor=HexColor("#6366F1"), rx=6))
        d.add(String(315,28,"Safety:", fontName='Helvetica-Bold', fontSize=7, fillColor=HexColor("#4338CA")))
        d.add(String(315,18,"* Watchdog 8s, NVS\n* Tank lock, rain, +-2% hyst", fontName='Helvetica', fontSize=6, fillColor=G800, leading=7))
        return d

    # Doc template
    class VerdeDoc(BaseDocTemplate):
        def __init__(self, filename, **kwargs):
            BaseDocTemplate.__init__(self, filename, **kwargs)
            f_cover=Frame(self.leftMargin,self.bottomMargin,self.width,self.height,id='cover')
            f_content=Frame(36,48,523,720,id='content')
            from reportlab.platypus import PageTemplate
            self.addPageTemplates([PageTemplate(id='cover', frames=f_cover, onPage=cover_page), PageTemplate(id='content', frames=f_content, onPage=content_page)])

    def cover_page(canvas, doc):
        canvas.saveState()
        # full bleed AI hero
        try:
            canvas.drawImage(str(ASSETS_DIR/"ai_cover_hero.jpg"), 0,0,width=W,height=H, preserveAspectRatio=False, anchor='c')
        except:
            canvas.setFillColor(NAVY)
            canvas.rect(0,0,W,H,fill=1,stroke=0)
        # overlay gradient: navy 65% + emerald mesh bottom
        canvas.setFillColor(NAVY)
        canvas.setFillAlpha(0.72)
        canvas.rect(0,0,W,H,fill=1,stroke=0)
        canvas.setFillAlpha(1)
        # emerald blob FX
        canvas.setFillColor(EM_DARK)
        canvas.setFillAlpha(0.85)
        canvas.circle(W-80,120,260,fill=1,stroke=0)
        canvas.setFillColor(HexColor("#0E8A5F"))
        canvas.circle(W-150,100,180,fill=1,stroke=0)
        canvas.setFillColor(EMERALD)
        canvas.circle(W-100,180,110,fill=1,stroke=0)
        canvas.setFillAlpha(1)
        # gold foil accent background small
        try:
            canvas.setFillAlpha(0.12)
            canvas.drawImage(str(ASSETS_DIR/"ai_gold_foil.jpg"), 0,H-180,width=W,height=180, preserveAspectRatio=False)
            canvas.setFillAlpha(1)
        except: pass
        # gold top/bottom stripes
        canvas.setFillColor(GOLD)
        canvas.rect(0,H-8,W,8,fill=1,stroke=0)
        canvas.rect(0,0,W,4,fill=1,stroke=0)
        # thin diagonal gold lines FX
        canvas.setStrokeColor(GOLD)
        canvas.setStrokeAlpha(0.35)
        canvas.setLineWidth(0.6)
        for i in range(5):
            y=320+i*90
            canvas.line(0,y,W,y+40)
        canvas.setStrokeAlpha(1)
        # plant stem FX leaf drawing (same as before)
        canvas.setStrokeColor(white)
        canvas.setLineWidth(2.5)
        canvas.line(460,80,460,280)
        canvas.setFillColor(HexColor("#34D399"))
        p=canvas.beginPath()
        p.moveTo(460,220); p.curveTo(400,250,390,200,460,180); p.close()
        canvas.drawPath(p,fill=1,stroke=0)
        p=canvas.beginPath()
        p.moveTo(460,200); p.curveTo(520,230,530,180,460,160); p.close()
        canvas.drawPath(p,fill=1,stroke=0)
        # top tagline sensors
        canvas.setFont("Helvetica-Bold",7)
        canvas.setFillColor(EM_LIGHT)
        canvas.drawString(36,H-22,"ESP32  |  5 SENSORS  |  2 ACTUATORS  |  FIREBASE  |  4 AI APIS  |  Rs. 1,890  |  COMPLETE & DEMO-READY")
        canvas.restoreState()

    def content_page(canvas, doc):
        canvas.saveState()
        # subtle emerald mesh watermark top right
        try:
            canvas.setFillAlpha(0.035)
            canvas.drawImage(str(ASSETS_DIR/"ai_emerald_mesh.jpg"), W-200,H-200,width=200,height=200, preserveAspectRatio=False)
            canvas.setFillAlpha(1)
        except: pass
        # gold top line + bottom light
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(2.8)
        canvas.line(36,H-28,W-36,H-28)
        canvas.setStrokeColor(G200)
        canvas.setLineWidth(0.6)
        canvas.line(36,32,W-36,32)
        canvas.setFont('Helvetica',7)
        canvas.setFillColor(G400)
        canvas.drawString(36,18,"PROJECT VERDE - DAV ACON 5 - 2026 - Aarav & Anuj - Class X - Rs. 1,890 - 5 Sensors - 17->2 Calls - 94%")
        canvas.drawRightString(W-36,18,f"{doc.page} / 31")
        # side emerald dot
        canvas.setFillColor(EMERALD)
        canvas.circle(24,H/2,3,fill=1,stroke=0)
        # left gold accent tiny line per page number even/odd FX
        if doc.page%2==0:
            canvas.setFillColor(GOLD_LIGHT)
            canvas.rect(0,H/2-60,4,120,fill=1,stroke=0)
        canvas.restoreState()

    # Styles
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    styles=getSampleStyleSheet()
    s_title_cover=ParagraphStyle('CoverTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=58, leading=60, textColor=white, spaceAfter=8)
    s_tagline=ParagraphStyle('Tagline', parent=styles['Normal'], fontName='Helvetica', fontSize=14.5, leading=19, textColor=HexColor("#A7F3D0"), spaceAfter=18)
    s_body=ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=15, textColor=G800, spaceAfter=8, alignment=4)
    s_small=ParagraphStyle('Small', parent=s_body, fontSize=9, leading=13)
    s_h1=ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=28, leading=32, textColor=NAVY, spaceBefore=6, spaceAfter=10)
    s_h2=ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=16, leading=19, textColor=EM_DARK, spaceBefore=12, spaceAfter=6)
    s_h3=ParagraphStyle('H3', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4)
    s_kicker=ParagraphStyle('Kicker', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=GOLD_DARK, spaceAfter=4)
    s_quote=ParagraphStyle('Quote', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=11.5, leading=16, textColor=NAVY, leftIndent=14, borderPadding=(10,10,10,12), spaceAfter=10, backColor=HexColor("#F0FDF4"), borderColor=EMERALD)
    s_caption=ParagraphStyle('Caption', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=G400, alignment=1, spaceBefore=4)
    s_cover_meta=ParagraphStyle('CoverMeta', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=HexColor("#CBD5E1"))
    s_white_small=ParagraphStyle('WhiteSmall', parent=s_small, textColor=HexColor("#E5E7EB"))

    def kpi_card(title,value,sub,accent=EMERALD):
        inner=[[Paragraph(f"<font color='{accent.hexval()}'><b>{title}</b></font>", s_kicker)],[Paragraph(f"<b><font size=17 color='#0B1D3A'>{value}</font></b>", s_body)],[Paragraph(f"<font size=8 color='#6B7280'>{sub}</font>", s_small)]]
        t=Table(inner, colWidths=[112])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),white),('BOX',(0,0),(-1,-1),0.8,G200),('LINEABOVE',(0,0),(-1,0),2.2,accent),('ROUNDEDCORNERS',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
        return t

    def shadow_image(path,w,h,r=8):
        # returns table with shadow effect
        try:
            img=Image(str(path), width=w, height=h)
        except:
            img=Paragraph(f"[{path.name}]", s_small)
        # shadow table
        inner=[[img]]
        t=Table(inner, colWidths=[w], rowHeights=[h])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),white),('BOX',(0,0),(-1,-1),0.8,G200),('ROUNDEDCORNERS',(0,0),(-1,-1),r),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
        return t

    OUTPUT="Project_Verde_Definitive_Documentation.pdf"
    story=[]
    story.append(NextPageTemplate('cover'))
    story.append(Spacer(1,62))
    story.append(Paragraph("PROJECT", ParagraphStyle('ck', parent=s_kicker, textColor=GOLD, fontSize=12, leading=14)))
    story.append(Paragraph("VERDE", s_title_cover))
    story.append(Spacer(1,6))
    story.append(Paragraph("The plant that waters itself —<br/>and talks to AI.", s_tagline))
    story.append(Spacer(1,16))
    badge=Table([[Paragraph("<b>COMPLETE & DEMO-READY</b><br/><font size=8>Hardware • Firmware • Cloud • Web App • AI</font>", ParagraphStyle('badge', parent=s_small, textColor=white, fontName='Helvetica-Bold', leading=10))]], colWidths=[230])
    badge.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),EM_DARK),('BOX',(0,0),(-1,-1),0,G200),('ROUNDEDCORNERS',(0,0),(-1,-1),10),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12)]))
    story.append(badge)
    story.append(Spacer(1,24))
    story.append(Paragraph("Aarav Choudhary (Class X) & Anuj (Class X)<br/>DAV ACON 5 — Tech Exhibition, 2026", s_cover_meta))
    story.append(Spacer(1,12))
    story.append(Paragraph("Total Build Cost ~ Rs. 1,890 (~ $23) • All software free tiers • 5 Sensors • 2 Actuators • 2 MCUs • 4 AI APIs • 1-sec Heartbeat", ParagraphStyle('cc', parent=s_white_small, fontSize=8, leading=11, textColor=HexColor("#A7F3D0"))))
    story.append(Spacer(1,110))
    strip=Table([[Paragraph("<b>EDGE</b><br/>ESP32 WROOM-32 + ESP32-CAM", s_white_small), Paragraph("<b>CLOUD</b><br/>Firebase RTDB — source of truth", s_white_small), Paragraph("<b>EXPERIENCE</b><br/>Single-file Web App + AI Doctor", s_white_small)]], colWidths=[160,160,160])
    strip.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor("#11294F")),('ROUNDEDCORNERS',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    story.append(strip)
    story.append(PageBreak())
    story.append(NextPageTemplate('content'))

    # 60 sec with dashboard mockup background
    story.append(Anchor("h1_60sec","The Whole Story in 60 Seconds"))
    story.append(Paragraph("<font color='#D97706'>TL;DR</font> • THE WHOLE STORY IN 60 SECONDS", s_kicker))
    story.append(Paragraph("The Whole Story in 60 Seconds", s_h1))
    story.append(Paragraph("If you read only one page, read this. Urban families kill plants not from neglect, but from <b>lack of information</b>. Verde fixes that with a Rs. 1,890 brain that watches soil, weather, water — and acts. No subscriptions, no black boxes.", s_body))
    story.append(Spacer(1,6))
    # KPI row with shadows
    kpis=[kpi_card("BUILD COST","Rs. 1,890","vs Rs. 8,000+ commercial kits",EMERALD),kpi_card("API CALLS","17 → 2 / sec","-85% latency, 0 reboots",GOLD_DARK),kpi_card("DIAGNOSIS","94%","Plant.id crop.health test",EM_DARK),kpi_card("HEARTBEAT","1 sec","JSON bundled 10 metrics + 9 keys",NAVY)]
    story.append(Table([kpis], colWidths=[124]*4, spaceAfter=8))
    story.append(Paragraph("Three tiers, one heartbeat — over-the-top tested:", s_h3))
    for b in ["<b>EDGE (Hands & Eyes):</b> ESP32 WROOM-32 reads 5 sensors every 1 sec. Soil power-gated 15 ms to prevent corrosion (10-pt avg). ESP32-CAM polls capture_photo every 1.5 s, SVGA JPEG → Vercel raw POST → base64 /latest_scan → app ≤2 s. Sequential boot + 8 MHz XCLK fixed brownout & RF.","<b>CLOUD (Memory):</b> Firebase RTDB — /sensors 10 metrics, /controls 9 keys, /latest_scan b64, /weather live, /historical_logs, /actuators. One write + one read per sec. Not 17. That bug taught us architecture.","<b>EXPERIENCE (Face):</b> Single-file HTML. Four pages via burger. Live tiles + sparklines + hover graphs last-10 ▲/▼, threshold sliders, tank calibration SET EMPTY/FULL, 5-day forecast rain override (ids 2xx/3xx/5xx/6xx), Plant Doctor + Gemini + OpenRouter vision+sensor chats.","<b>INTELLIGENCE:</b> OWM live Delhi, crop.health Plant.id 94% nutrient deficiency treatment, Gemini 2.5 Flash via gemini-flash-latest inline image+telemetry, OpenRouter 8-model text + 5-model vision fallback chains never dead-end (435 models)."]:
        story.append(Paragraph(f"• {b}", s_body))
    story.append(Spacer(1,6))
    story.append(Paragraph("\"The plant that waters itself — and talks to AI.\" Not a slogan. It's what happens when moisture < 35% AND tank >15% AND no rain.", s_quote))
    story.append(Spacer(1,6))
    story.append(shadow_image(ASSETS_DIR/"ai_dashboard_mockup.jpg", 500, 280, 10))
    story.append(Paragraph("AI-generated dashboard mockup — glassmorphism tiles, navy header #0B1D3A, emerald data viz #10B981, gold accents #F59E0B. Single-file HTML but feels like funded startup.", s_caption))
    story.append(PageBreak())

    # Contents with AI mesh
    story.append(Anchor("h1_contents","Contents"))
    story.append(Paragraph("NAVIGATE • HYPERLINKED TOC", s_kicker))
    story.append(Paragraph("Contents", s_h1))
    toc_items=[("01","Why — The Problem Worth Solving","h1_why","Urban death + Rs. 8k gap + no camera/AI"),("02","How It Works — Architecture","h1_arch","EDGE→CLOUD→EXPERIENCE + 1-sec heartbeat FX"),("03","Hardware — 5 Sensors, 2 Actuators, 2 Brains","h1_hardware","BOM, pin map, power lessons + AI bench photo"),("04","Firmware — Bug Story 17→2","h1_firmware","Scheduler, auto flowchart, watchdog + fix"),("05","Cloud — Firebase Schema","h1_cloud","Single source of truth tree"),("06","Web App — Single File, Four Worlds","h1_webapp","Dashboard, Weather, Plant Doctor, AI Assistants"),("07","AI & APIs — 4 Integrations Tested Live","h1_ai","OWM, Plant.id, Gemini, OpenRouter + 94% test"),("08","Features — Everything Live","h1_features","13 live features + tank calibration hack"),("09","Testing — 13-Point PASS Matrix","h1_testing","DHT breathe to 10-min watchdog"),("10","Bugs We Hit & Fixed","h1_bugs","10 war stories = credibility"),("11","Cost & Sustainability","h1_cost","Rs. 1,890 breakdown + comparison chart"),("12","Future — Solar, NPK, Zones, Alerts","h1_future","Roadmap Q2 2026 - Q1 2027"),("13","Judge Tour — 3-Min Demo Script","h1_tour","180-sec wow flow"),("14","Conclusion — Why We Win","h1_conclusion","QR to live demo + hero numbers")]
    toc_data=[]
    for num,title,anchor,desc in toc_items:
        toc_data.append([Paragraph(f"<b><font color='#10B981'>{num}</font></b>", ParagraphStyle('num', parent=s_body, fontSize=10)), Paragraph(f"<a href=\"#{anchor}\" color=\"#0B1D3A\"><b>{title}</b></a><br/><font size=7 color='#6B7280'>{desc}</font>", s_body), Paragraph("<font color='#9CA3AF'>→</font>", s_small)])
    toc_table=Table(toc_data, colWidths=[36,430,18])
    toc_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(0,0),(-1,-2),0.4,G100),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(toc_table)
    story.append(Spacer(1,8))
    story.append(Table([[shadow_image(ASSETS_DIR/"ai_emerald_mesh.jpg",120,80,8), Paragraph("How to use: Judges → 3-min flip via TOC. Parents → any page standalone. Engineers → pin maps + schema. <b>Click any TOC entry to jump (bookmarks).</b> Design: navy #0B1D3A emerald #10B981 gold #F59E0B, 2 fonts, generous white space, authentic AI photos 40% of real estate, pull quotes, infographics.", s_small)]], colWidths=[130,380], spaceBefore=6))
    story.append(PageBreak())

    # Why with AI images
    story.append(Anchor("h1_why","Why"))
    story.append(Paragraph("PART 01 • WHY • PROBLEM + OPPORTUNITY", s_kicker))
    story.append(Paragraph("The Problem Worth Solving", s_h1))
    story.append(Paragraph("Urban families love plants. Plants die anyway. Why? Not cruelty — <b>lack of real-time data</b>. Verde turns guesswork into telemetry.", s_body))
    story.append(Spacer(1,6))
    story.append(Table([[shadow_image(ASSETS_DIR/"ai_cover_hero.jpg",240,180,10), Table([[Paragraph("<b>What we saw in Delhi homes</b>", s_h3), Paragraph("• Mom waters daily → root rot<br/>• Dad forgets week → wilt<br/>• Tank empties mid-pump → burn<br/>• Rain comes, pump still waters → waste<br/>• No camera → disease 10 days late", s_small)],[Paragraph("<b>What market sells Rs. 8k+</b>", s_h3), Paragraph("• Gardena, Xiaomi, no camera<br/>• No AI diagnosis, closed-source<br/>• No tank level, no rain override<br/>• Subscription cloud<br/>• Looks like tech, not teaching", s_small)]], colWidths=[250])]], colWidths=[250,270], spaceAfter=10))
    story.append(Paragraph("\"A Rs. 1,890 plant that texts its mood is more useful than Rs. 12k timer kit.\"", s_quote))
    story.append(Paragraph("Insight: plant must <b>tell us</b> what it needs, and <b>act</b> when we're away. Moisture <35% AND tank safe AND no rain → pump ON. No human needed, but human can always override.", s_body))
    story.append(Spacer(1,8))
    hero=Table([[Paragraph("<font size=22 color='#0B1D3A'><b>70%</b></font><br/><font size=8>urban plants die 3 months</font>", s_small), Paragraph("<font size=22 color='#059669'><b>Rs.1,890</b></font><br/><font size=8>our total vs Rs.8k+ market</font>", s_small), Paragraph("<font size=22 color='#D97706'><b>94%</b></font><br/><font size=8>AI disease ID accuracy</font>", s_small), Paragraph("<font size=22 color='#0B1D3A'><b>1 sec</b></font><br/><font size=8>heartbeat bundled</font>", s_small)]], colWidths=[125]*4)
    hero.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('BOX',(0,0),(-1,-1),0.8,G200)]))
    story.append(hero)
    story.append(PageBreak())

    # Architecture with isometric AI
    story.append(Anchor("h1_arch","Architecture"))
    story.append(Paragraph("PART 02 • ARCHITECTURE • THREE TIERS + ONE HEARTBEAT", s_kicker))
    story.append(Paragraph("How It Works", s_h1))
    story.append(Paragraph("Three tiers, one heartbeat every second. No magic, just disciplined engineering + FX.", s_body))
    story.append(Spacer(1,6))
    story.append(shadow_image(ASSETS_DIR/"ai_architecture_isometric.jpg", 500, 300, 10))
    story.append(Paragraph("AI-generated isometric architecture — left EDGE (brain+eyes), middle CLOUD Firebase, right EXPERIENCE laptop dashboard. Navy/Emerald/Gold palette, clean minimal, startup illustration.", s_caption))
    story.append(Spacer(1,8))
    story.append(make_arch())
    story.append(Paragraph("System architecture vector — EDGE (brain+eyes+5 sensors), CLOUD single source, EXPERIENCE single-file HTML + 4 AI APIs. Flow exact.", s_caption))
    story.append(Spacer(1,8))
    story.append(Paragraph("One-Second Heartbeat Timeline", s_h2))
    story.append(Image(str(ASSETS_DIR/"heartbeat.png"), width=500, height=170))
    story.append(Paragraph("Every 1000 ms: sensors 1 Hz → 10-pt avg soil/LDR + 5-pt + invalid rejection tank → bundle 10-metric JSON → one PUT /sensors → one GET /controls (9 keys) → decision → actuator. Watchdog fed every loop.", s_small))
    story.append(PageBreak())

    # Hardware ultimate with AI bench + macro
    story.append(Anchor("h1_hardware","Hardware"))
    story.append(Paragraph("PART 03 • HARDWARE • 5 SENSORS, 2 ACTUATORS, 2 BRAINS", s_kicker))
    story.append(Paragraph("Everything from Lajpat Nagar + Amazon — Rs. 1,890. Breadboard, so judges see every wire.", s_h1))
    story.append(Spacer(1,4))
    story.append(shadow_image(ASSETS_DIR/"ai_hardware_bench.jpg", 500, 320, 10))
    story.append(Paragraph("AI-generated hardware bench — ESP32 WROOM-32 + ESP32-CAM + soil LM393 + DHT11 + LDR + HC-SR04 + relay + pump + UV LED + breadboard with jumper wires, 1000uF cap + 1N4007 diode, 5V adapter. Photorealistic lab top view.", s_caption))
    story.append(Spacer(1,8))
    bom_data=[["Module","ESP32 Pin","Role & Trick FX"],["Soil LM393","AO→34, VCC→23 gated 15ms","Power-gated 15ms → no corrosion. 10-pt moving avg, gold accent."],["DHT11","DATA→4","Breathe test: blow → spike. Shared GND critical."],["LDR","AO→35","Dark detection. Hysteresis ±2% → no LED flicker."],["HC-SR04","TRIG 18 ECHO 19","Tank level 5-pt filter + invalid rejection. Splash-proof."],["Relay active-LOW","IN1→5","Switches 5V pump, isolated COM/NO own 5V."],["UV LED","12 active-HIGH 220Ω","Photosynthetic, auto on LDR < threshold."],["ESP32-CAM OV2640","Own board + MB","SVGA JPEG, 8MHz XCLK, sequential boot 500ms."],["Power 5V/2A","—","NOT PD charger: PD needs handshake chip ESP32 lacks → 0mA."],["Protection","—","1N4007 flyback diode across pump + 1000uF cap across 5V/GND."]]
    bom_table_data=[[Paragraph(f"<b>{c}</b>", s_small) for c in bom_data[0]]]
    for row in bom_data[1:]:
        bom_table_data.append([Paragraph(c, s_small) for c in row])
    bom_table=Table(bom_table_data, colWidths=[95,90,315], repeatRows=1)
    bom_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),white),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,G50]),('GRID',(0,0),(-1,-1),0.4,G100),('LEFTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(bom_table)
    story.append(PageBreak())
    story.append(Paragraph("Circuit / Wiring — Simplified, not EDA, but every GPIO exact", s_h2))
    story.append(Table([[shadow_image(ASSETS_DIR/"ai_circuit_macro.jpg",240,160,8), make_circuit()]], colWidths=[250,260], spaceAfter=8))
    story.append(Paragraph("Left: AI macro close-up ESP32 pins glowing emerald traces, gold solder, navy PCB. Right: vector wiring map — VCC gated GPIO23 prevents galvanic corrosion, relay LOW, UV HIGH.", s_caption))
    story.append(Spacer(1,8))
    story.append(Paragraph("Power Design — Hard-Won Lessons (Honesty = Credibility)", s_h2))
    power=[["Lesson","We Tried","Failed","Fix FX"],["PD Charger","67W USB-PD laptop brick","PD needs handshake ESP32 lacks → ~0mA starved","5V/2A phone adapter"],["Cap","No cap","Pump+WiFi spike → brownout reboot","1000uF electrolytic across 5V/GND"],["Diode","Pump direct relay","Inductive kick → reset","1N4007 flyback across pump"],["Isolation","Pump+ESP32 same 5V","Noise sag","Relay COM/NO own 5V"],["Rail","Split breadboard","Relay dead no power","Bridge + to +, - to -"],["GND","DHT separate GND","temp=0 always","Shared GND bus GPIO4"]]
    pl_data=[[Paragraph(f"<b>{c}</b>" if i==0 else c, s_small) for c in row] for i,row in enumerate(power)]
    pl_table=Table(pl_data, colWidths=[55,100,145,185], repeatRows=1)
    pl_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor("#FEF3C7")),('GRID',(0,0),(-1,-1),0.4,G200),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,G50]),('LEFTPADDING',(0,0),(-1,-1),5)]))
    story.append(pl_table)
    story.append(Spacer(1,6))
    story.append(Paragraph("Audit spec: thresholds 35% moisture / 15% tank / 35% light. 8 MHz XCLK (was 20 MHz → RF interference). Pins 34,23,4,35,18,19,5,12. All verified live.", ParagraphStyle('audit', parent=s_small, backColor=EM_PALE, borderPadding=(6,6,6,6))))
    story.append(PageBreak())

    # Firmware
    story.append(Anchor("h1_firmware","Firmware"))
    story.append(Paragraph("PART 04 • FIRMWARE • CODE_1 V3.0.7-FINAL", s_kicker))
    story.append(Paragraph("The Brain — Non-Blocking by Design", s_h1))
    story.append(Paragraph("No delay() anywhere. Everything millis() + hardware watchdog 8s fed every loop + NVS thresholds.", s_body))
    story.append(Spacer(1,4))
    fw_table=Table([[Paragraph("<b>Task Scheduler</b>", s_h3), Paragraph("<b>Filtering FX</b>", s_h3)],[Paragraph("• Sensors 1 Hz<br/>• Cloud 1 s<br/>• WiFi 10 s<br/>• Logs 60 s<br/>• WDT fed every loop<br/>• NVS persists thresholds", s_small), Paragraph("• Soil & LDR 10-pt moving avg<br/>• Tank 5-pt + invalid rejection<br/>• ±2% hysteresis light auto<br/>• Splash garbage can't fake empty<br/>• Voltage sag counter", s_small)]], colWidths=[260,260], spaceAfter=8)
    fw_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.6,G200),('BACKGROUND',(0,0),(0,1),EM_PALE)]))
    story.append(fw_table)
    story.append(Paragraph("AUTO Logic — The Core Decision", s_h2))
    story.append(make_flowchart())
    story.append(Paragraph("Flowchart: pump_ON = moisture <35% AND tank >15% AND rain_expected=false. Manual still tank-protected. Fail-safe default.", s_caption))
    story.append(PageBreak())
    story.append(Paragraph("The Bug That Taught Us Engineering", s_h1))
    story.append(Paragraph("Honesty = credibility. We almost failed demo because of one architectural mistake.", s_body))
    story.append(Spacer(1,6))
    story.append(make_bug())
    story.append(Spacer(1,4))
    story.append(Image(str(ASSETS_DIR/"api_before_after.png"), width=500, height=250))
    story.append(Paragraph("FX chart: BEFORE 17 calls/sec → stall → WDT reboot → pump flicker. AFTER 2 calls/sec JSON bundled -85% latency, zero reboots, pump continuous.", s_caption))
    story.append(Spacer(1,6))
    for b in ["<b>Symptoms:</b> AUTO clicked ON/OFF every ~10s. Logs 17 calls/sec. Network stall. 8s WDT reboot. Never stayed ON long enough.","<b>Root:</b> Each metric separate HTTPS. TLS ~150ms ×17 =2.5s blocking → WDT deadlock → reboot → loop.","<b>Fix:</b> One JSON 10 metrics → single PUT /sensors. One GET /controls 9 keys. 2 calls/sec. -85% latency, 0 reboots, pump ON 120s till threshold.","<b>Tested:</b> Pump AUTO 120s no glitch, OFF exactly at threshold 35%, watchdog 10+ min 0 reboots."]:
        story.append(Paragraph(f"• {b}", s_body))
    story.append(Paragraph("\"Don't spam the cloud. Respect the handshake.\"", s_quote))
    story.append(PageBreak())

    # Cloud
    story.append(Anchor("h1_cloud","Cloud"))
    story.append(Paragraph("PART 05 • CLOUD • FIREBASE RTDB", s_kicker))
    story.append(Paragraph("Single Source of Truth", s_h1))
    story.append(Paragraph("One database, no backend server, legacy secret auth, public read validated writes. If Firebase has it, app + ESP32 agree.", s_body))
    story.append(Spacer(1,6))
    story.append(make_firebase())
    story.append(Paragraph("Schema tree: verde-tech-haha RTDB six nodes — Sensors telemetry, Controls intents, Latest_scan vision, Weather live, Logs history, Actuators truth.", s_caption))
    story.append(Spacer(1,8))
    story.append(Table([[Paragraph("<b>/sensors</b> 10 metrics 1Hz", s_small), Paragraph("moisture %, temp C, humidity %, light %, tank %, lux, watchdog_status, voltage_sag, uploads, fails. Filtered avg.", s_small)],[Paragraph("<b>/controls</b> 9 keys", s_small), Paragraph("manual_mode, pump_state, light_manual, grow_light, capture_photo, moisture_threshold, tank_threshold, light_threshold, weather_override", s_small)],[Paragraph("<b>/latest_scan</b> vision", s_small), Paragraph("imageUrl b64, status, captured_at, scientificName, diseaseName, probability 0-100, treatmentPlan", s_small)]], colWidths=[120,380], spaceBefore=6))
    story.append(PageBreak())

    # Web App with dashboard mockup
    story.append(Anchor("h1_webapp","Web App"))
    story.append(Paragraph("PART 06 • WEB APP • SINGLE-FILE HTML", s_kicker))
    story.append(Paragraph("The Face — No React, No Build, Feels Like Product", s_h1))
    story.append(Paragraph("One HTML file any judge can open and understand. But FX: glassmorphism cards, sparklines, toasts, fullscreen demo mode.", s_body))
    story.append(Spacer(1,6))
    story.append(shadow_image(ASSETS_DIR/"ai_dashboard_mockup.jpg",500,280,10))
    story.append(Paragraph("AI dashboard mockup — 8 telemetry tiles + sparklines, moisture history, threshold sliders, predicted actuator states, system strip, toasts. Navy #0B1D3A header, emerald viz, gold accents.", s_caption))
    story.append(Spacer(1,6))
    pages=[("Dashboard","8 tiles + sparklines + hover last-10 ▲/▼, controls, sliders, predicted states, history chart, status strip, toasts, demo mode, uptime"),("Weather","Live Delhi, 5-day chips, auto rain-override 3min countdown → weather_override=1 ids 2xx/3xx/5xx/6xx"),("Plant Doctor","Live CAM ≤2s, CAPTURE, upload-or-CAM modal: photo + crop.health diagnosis + AI chat same image. Flip fix upside-down"),("AI Assistants","Gemini image chat + OpenRouter sensor-aware quick prompts. Tank calibration SET EMPTY/FULL app-side remap no reflash")]
    cards=[]
    for title,desc in pages:
        t=Table([[Paragraph(f"<b>{title}</b>", s_h3)],[Paragraph(desc, s_small)]], colWidths=[115])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),EM_PALE),('BOX',(0,0),(-1,-1),0.6,G200),('ROUNDEDCORNERS',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),6)]))
        cards.append(t)
    story.append(Table([cards], colWidths=[125]*4, spaceAfter=8))
    story.append(Image(str(ASSETS_DIR/"moisture_cycle.png"), width=500, height=270))
    story.append(Paragraph("Moisture watering-cycle chart FX — threshold 35% dashed gold, PUMP ON emerald fill, OFF gray, no flicker, OFF exactly at threshold.", s_caption))
    story.append(PageBreak())

    # AI APIs with plant doctor AI
    story.append(Anchor("h1_ai","AI APIs"))
    story.append(Paragraph("PART 07 • AI & APIS • 4 INTEGRATIONS LIVE-TESTED", s_kicker))
    story.append(Paragraph("Four APIs — No Mock Data, All Live", s_h1))
    story.append(Paragraph("Tested Delhi 35°C, nutrient deficiency @94%, free-tier rotation fallback chains.", s_body))
    story.append(Spacer(1,6))
    story.append(shadow_image(ASSETS_DIR/"ai_plant_doctor.jpg",500,300,10))
    story.append(Paragraph("AI Plant Doctor — macro leaf nutrient deficiency yellow spots, futuristic AI scanning overlay emerald boxes + gold HUD, 94% accuracy + treatment. Biotech startup aesthetic.", s_caption))
    story.append(Spacer(1,6))
    api=[["API","Purpose","Auth","How FX","Accuracy"],["OpenWeatherMap","live weather+5-day → rain override","key in URL","GET weather?q=Delhi; ids 2xx/3xx/5xx/6xx → rain → override=1","Live Delhi 35°C city id 1273294"],["crop.health Plant.id","plant+disease ID","Api-Key header","POST /api/v1/identification b64 image → crop + disease suggestions","Money-plant nutrient deficiency @94% + treatment — real"],["Gemini 2.5 Flash","vision chat on photo","X-goog-api-key AQ","POST gemini-flash-latest:generateContent inline image+diag+telemetry","AQ needs header; flash-latest alias works"],["OpenRouter","sensor chat+vision fallback","Bearer sk-or-v1-…","POST chat/completions OpenAI-compat 8-model text +5-model vision chain","435 models; free rotate → chain never dead-end"]]
    api_data=[[Paragraph(f"<b>{c}</b>", ParagraphStyle('ah', parent=s_small, fontName='Helvetica-Bold', textColor=white)) for c in api[0]]]
    for row in api[1:]:
        api_data.append([Paragraph(c, s_small) for c in row])
    api_table=Table(api_data, colWidths=[68,78,58,138,125], repeatRows=1)
    api_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),0.4,G200),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor("#F8FAFC")]),('LEFTPADDING',(0,0),(-1,-1),5)]))
    story.append(api_table)
    story.append(PageBreak())

    # Features
    story.append(Anchor("h1_features","Features"))
    story.append(Paragraph("PART 08 • FEATURES • EVERYTHING LIVE", s_kicker))
    story.append(Paragraph("No Screenshots, Real Data — 14 Features", s_h1))
    story.append(Spacer(1,4))
    feat=[["Feature","Live?","Demo FX"],["Live soil % +10-pt avg + sparkline","YES","Dunk sensor water → % rises graph ▲ emerald"],["Temp/Humidity DHT11","YES","Breathe → temp/hum spike gold"],["LDR+UV grow LED auto","YES","Cover LDR → dark → LED ON hysteresis ±2%"],["Ultrasonic tank %","YES","Hand over tank → level changes SET EMPTY/FULL"],["Pump AUTO 120s continuous","YES","Set 80% → ON till 80 no flicker"],["Pump OFF at threshold exact","YES","Watch OFF at 35% not early"],["Tank lock protection","YES","Set empty → refuses ON even manual"],["Rain override","YES","Force rainy city override=1 → OFF"],["CAM capture ≤2s","YES","Press CAPTURE → flash → app ≤2s 1.6s avg"],["Plant Doctor 94%","YES","Upload diseased leaf → name+treatment"],["Gemini vision chat","YES","Ask why yellow? sees image+sensors"],["OpenRouter sensor chat","YES","Ask should I water? reads live moisture"],["Watchdog 10+ min 0 reboots","YES","Uptime timer counts"],["Threshold sliders NVS","YES","Drag → persists reboot"]]
    feat_data=[[Paragraph(f"<b>{c}</b>", ParagraphStyle('fh', parent=s_small, fontName='Helvetica-Bold', textColor=white)) for c in feat[0]]]
    for row in feat[1:]:
        feat_data.append([Paragraph(row[0], s_small), Paragraph(row[1], s_small), Paragraph(row[2], s_small)])
    feat_table=Table(feat_data, colWidths=[165,45,275], repeatRows=1)
    feat_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),EM_DARK),('GRID',(0,0),(-1,-1),0.4,G200),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,G50])]))
    story.append(feat_table)
    story.append(Spacer(1,8))
    story.append(Paragraph("Tank calibration — favorite UX hack: ultrasonic raw drifts per bucket. Instead of reflash ESP32, SET EMPTY/FULL in app stores raw_empty/full in localStorage remaps 0-100%. Works any bucket, no code.", s_small))
    story.append(Spacer(1,6))
    story.append(Paragraph("Demo mode + toasts: fullscreen demo hides clutter, enlarges tiles for projector. Toasts show every action: 'Pump ON — AUTO', 'Rain override active 3 min', 'Photo captured'.", s_small))
    story.append(PageBreak())

    # Testing
    story.append(Anchor("h1_testing","Testing"))
    story.append(Paragraph("PART 09 • TESTING • 13-POINT PASS MATRIX", s_kicker))
    story.append(Paragraph("Tested after every fix. Final run signed.", s_h1))
    story.append(Spacer(1,4))
    test=[["#","Test","Method","Expected","Result"],["1","WiFi/boot","5V/2A check serial","Boots ≤3s 3-network fallback","PASS"],["2","DHT11 breathe","Blow warm air","Temp +2-3C hum +5%","PASS"],["3","Moisture dunk","Dunk LM393","0%→~85% 3s avg smooth","PASS"],["4","LDR cover","Cover hand","Light % drops → dark → UV ON","PASS"],["5","Ultrasonic hand","Hand over HC-SR04","Tank % jumps 5-pt rejects splash","PASS"],["6","Pump AUTO 120s","Threshold 80% moist 30%","Pump ON 120s no flicker","PASS"],["7","OFF at threshold","Watch cross 35%","OFF 35.0±0.5","PASS"],["8","Tank lock","Set 5% empty manual ON","Pump refuses toast 'Tank empty'","PASS"],["9","Rain override","OWM rainy id 500","override=1 pump OFF countdown","PASS"],["10","CAM capture ≤2s","Press CAPTURE","Flash→Vercel→app ≤2.0s","PASS 1.6s"],["11","Plant Doctor 94%","Upload leaf","Sci name +94% + treatment","PASS"],["12","AI chats fallback","429 one model next","Gemini+OpenRouter chain","PASS"],["13","Watchdog 10+ min","Leave 12min","0 reboots uptime inc sag 0","PASS"]]
    test_data=[[Paragraph(f"<b>{c}</b>", ParagraphStyle('th', parent=s_small, fontName='Helvetica-Bold', textColor=white)) for c in test[0]]]
    for row in test[1:]:
        test_data.append([Paragraph(c, s_small) for c in row])
    test_table=Table(test_data, colWidths=[18,65,95,135,80], repeatRows=1)
    test_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),0.4,G200),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,G50])]))
    story.append(test_table)
    story.append(Spacer(1,8))
    story.append(Paragraph("[12:43] WiFi HomeNet 72% RSSI<br/>[12:44] Soil 28% → pump AUTO ON tank 67% safe no rain<br/>[12:46] Soil 35.1% → pump OFF exact<br/>[12:47] Capture trigger 1 → CAM flash → upload 1.4s<br/>[12:50] Uptime 634s WDT 0 reboots sag 0", ParagraphStyle('log', parent=s_small, backColor=NAVY, textColor=HexColor("#A7F3D0"), fontName='Courier', borderPadding=(6,6,6,6))))
    story.append(PageBreak())

    # Bugs
    story.append(Anchor("h1_bugs","Bugs"))
    story.append(Paragraph("PART 10 • WAR STORIES • 10 REAL FAILURES", s_kicker))
    story.append(Paragraph("Bugs We Hit & Fixed — Honesty = Credibility", s_h1))
    story.append(Paragraph("Project without bugs is project that didn't run. 10 real failures, fixes, lessons.", s_body))
    story.append(Spacer(1,4))
    bugs=[("AUTO 10s loop","17 calls/sec stall WDT reboot loop","JSON bundling 1+1 calls/sec -85%"),("Camera probe 0x106","OV2640 not found","FPC ribbon unseated → reseat gold-side down + power cycle"),("PSRAM not found","CAM says no PSRAM","Weak power → 5V/2A adapter not PD"),("0x20002 boot crash","ESP32-CAM crash dump","Camera+WiFi surge → sequential boot 500ms"),("RF interference","CAM corrupted WiFi TX","20MHz XCLK too fast → throttle 8MHz"),("67W PD charger starved","Board dim WiFi fails","PD handshake missing → 5V/2A phone adapter"),("Relay dead","Relay never clicks","Split breadboard rails → bridge + to + - to -"),("temp=0 always","DHT returns 0","Wrong pin + separate GND → GPIO4 + shared GND"),("Firebase spurts","Logs bursts","13 calls/sec → one bundled call"),("Compile quote error","missing terminating quote","Copy-paste corruption → re-download fresh")]
    bug_data=[[Paragraph("<b>Bug</b>", ParagraphStyle('bh', parent=s_small, fontName='Helvetica-Bold', textColor=white)), Paragraph("<b>Symptom</b>", ParagraphStyle('bh2', parent=s_small, fontName='Helvetica-Bold', textColor=white)), Paragraph("<b>Fix</b>", ParagraphStyle('bh3', parent=s_small, fontName='Helvetica-Bold', textColor=white))]]
    for t,sy,fx in bugs:
        bug_data.append([Paragraph(f"<b>{t}</b>", s_small), Paragraph(sy, s_small), Paragraph(fx, s_small)])
    bug_table=Table(bug_data, colWidths=[100,160,220], repeatRows=1)
    bug_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor("#7C3AED")),('GRID',(0,0),(-1,-1),0.4,G200),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,G50])]))
    story.append(bug_table)
    story.append(Spacer(1,10))
    story.append(Paragraph("Most valuable bug #1: taught system thinking. Costly calls kill UX. Bundling is architecture, not optimization.", s_quote))
    story.append(PageBreak())

    # Cost
    story.append(Anchor("h1_cost","Cost"))
    story.append(Paragraph("PART 11 • COST & SUSTAINABILITY • Rs.1,890 HOW?", s_kicker))
    story.append(Paragraph("Rs. 1,890 — Fully Itemized, No Hidden", s_h1))
    story.append(Paragraph("Tracked every rupee. No hidden software. All APIs free-tier. Not counting laptop+phone you already have.", s_body))
    story.append(Spacer(1,6))
    cost=[["Category","Items","Cost INR"],["Electronics","ESP32 Rs.320 ESP32-CAM Rs.480 5 sensors Rs.300 relay Rs.70 pump Rs.150","1,320"],["Power protection","5V/2A adapter Rs.150 1000uF Rs.15 1N4007 Rs.5 wires Rs.50","220"],["Mechanical","Breadboard Rs.120 enclosure Rs.150 UV LED Rs.30 misc Rs.50","350"],["Software APIs","Firebase free Vercel hobby OWM 1000/day free Plant.id free Gemini free OpenRouter free","0"],["","","~1,890"]]
    cb_data=[[Paragraph(f"<b>{c}</b>", ParagraphStyle('ch', parent=s_small, fontName='Helvetica-Bold', textColor=white)) for c in cost[0]]]
    for i,row in enumerate(cost[1:]):
        if i==len(cost)-2:
            cb_data.append([Paragraph("", s_small), Paragraph("", s_small), Paragraph(f"<b><font size=13 color='#0B1D3A'>{row[2]}</font></b>", s_small)])
        else:
            cb_data.append([Paragraph(row[0], s_small), Paragraph(row[1], s_small), Paragraph(f"Rs. {row[2]}", s_small)])
    cb_table=Table(cb_data, colWidths=[85,310,80], repeatRows=1)
    cb_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('BACKGROUND',(0,-1),(-1,-1),GOLD_LIGHT),('GRID',(0,0),(-1,-2),0.4,G200),('LINEABOVE',(0,-1),(-1,-1),1.5,NAVY)]))
    story.append(cb_table)
    story.append(Spacer(1,8))
    story.append(Image(str(ASSETS_DIR/"cost_comparison.png"), width=500, height=270))
    story.append(Paragraph("Cost comparison FX — ours vs market 76% cheaper than basic, 85% than premium, yet includes camera+AI they lack plus student-hackable.", s_caption))
    story.append(Spacer(1,8))
    story.append(Table([[shadow_image(ASSETS_DIR/"ai_gold_foil.jpg",120,90,8), Paragraph("<b>Sustainability FX:</b><br/>• Water saved 40% rain override + threshold vs daily timer<br/>• Power 5V/0.6A ~3W 15ms power-gating prevents corrosion years<br/>• Zero subscription free-tier APIs RTDB Vercel hobby<br/>• Repairable breadboard not PCB replace sensor 2min", s_small)]], colWidths=[130,380]))
    story.append(PageBreak())

    # Future
    story.append(Anchor("h1_future","Future"))
    story.append(Paragraph("PART 12 • FUTURE • WHERE VERDE GROWS NEXT", s_kicker))
    story.append(Paragraph("Roadmap Like Startup — Solar, NPK, Zones, Alerts", s_h1))
    story.append(Paragraph("Built finished product but sketched roadmap like startup would. Solar field-deployable, NPK precise, zones real garden, alerts product parents use.", s_body))
    story.append(Spacer(1,6))
    future=[("Solar Autonomy","12V panel + charge controller +18650 battery day charges night runs 3W→5W panel enough Cost +Rs.900","Q3 2026"),("NPK Probe","Replace LM393 with 3-in-1 NPK+pH actual nutrient data → better AI treatment","Q4 2026"),("Multi-Plant Zones","One ESP32 drives 4 relays via mux each zone threshold per plant cactus 20% fern 60%","Q1 2027"),("Telegram/WhatsApp Alerts","Pump ON tank empty disease detected → push Firebase Functions free","Q2 2026 2 days"),("Predictive Watering","Logs → linear regression moisture drop rate water before wilt not after","Q2 2027"),("Next.js Dashboard","Scaffolded migrate single HTML to Next.js + charts + auth + multi-device","Q3 2026")]
    f_data=[[Paragraph("<b>Feature</b>", ParagraphStyle('fhh', parent=s_small, fontName='Helvetica-Bold', textColor=white)), Paragraph("<b>What FX</b>", ParagraphStyle('fhh2', parent=s_small, fontName='Helvetica-Bold', textColor=white)), Paragraph("<b>When</b>", ParagraphStyle('fhh3', parent=s_small, fontName='Helvetica-Bold', textColor=white))]]
    for t,w,when_ in future:
        f_data.append([Paragraph(f"<b>{t}</b>", s_small), Paragraph(w, s_small), Paragraph(when_, s_small)])
    f_table=Table(f_data, colWidths=[100,300,80], repeatRows=1)
    f_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),EM_DARK),('GRID',(0,0),(-1,-1),0.4,G200),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,EM_PALE])]))
    story.append(f_table)
    story.append(Spacer(1,8))
    story.append(Image(str(ASSETS_DIR/"api_before_after.png"), width=500, height=250))
    story.append(Paragraph("Bug fix became principle: fewer richer calls beat many tiny. Applies to future — batch NPK+moisture same JSON.", s_caption))
    story.append(PageBreak())

    # Tour
    story.append(Anchor("h1_tour","Tour"))
    story.append(Paragraph("PART 13 • JUDGE TOUR • 3-MIN DEMO SCRIPT", s_kicker))
    story.append(Paragraph("180 Seconds to Wow — Rehearsed", s_h1))
    story.append(Paragraph("Judges have 180 sec. Exact flow that makes them say wow — with FX cues.", s_body))
    story.append(Spacer(1,6))
    tour=[("0:00-0:20 Hook","Hold plant 'This plant waters itself and talks to AI. Rs.1,890. No subscriptions.' Show cover hero AI image, point 5 sensors glowing."),("0:20-0:50 Live telemetry","Open Dashboard mockup. Point 8 tiles sparklines. Dunk soil sensor → moisture rises live emerald. Cover LDR → UV LED ON gold. Hand over ultrasonic → tank % changes."),("0:50-1:20 Auto logic","Set moisture slider 35→80 watch pump ON continuous FX. 'Before 17 calls flicker every 10s, now 2 calls -85% latency.' Show api_before_after chart."),("1:20-1:50 Plant Doctor","Press CAPTURE flash LED → ≤2s photo appears. 'ESP32-CAM 8MHz XCLK sequential boot.' Upload diseased leaf → 94% nutrient deficiency + treatment. Gemini chat 'why yellow?' sees image+sensors."),("1:50-2:20 Weather Safety","Show weather 5-day chips. 'Rain expected → pump locks even if soil dry.' Demo tank lock: set empty → pump refuses manual ON 'Safe'."),("2:20-2:50 Cost & honesty","Show cost comparison Rs.1,890 vs Rs.8k+ with AI bench photo. 'We failed 10 times. Relay dead split rail, DHT temp=0 GND, CAM 0x106 ribbon. Fix log in doc.'"),("2:50-3:00 Close","QR live demo scan → verde.vercel.app. 'Future solar+NPK+zones. Today demo-ready zero reboots 10+ min watchdog happy. Rs.1,890 plant that texts you.'")]
    tour_data=[[Paragraph("<b>Time</b>", ParagraphStyle('th1', parent=s_small, fontName='Helvetica-Bold', textColor=white)), Paragraph("<b>What to say & do + FX cue</b>", ParagraphStyle('th2', parent=s_small, fontName='Helvetica-Bold', textColor=white))]]
    for tm,desc in tour:
        tour_data.append([Paragraph(f"<b>{tm}</b>", s_small), Paragraph(desc, s_small)])
    tour_table=Table(tour_data, colWidths=[80,400], repeatRows=1)
    tour_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),0.4,G200),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,G50])]))
    story.append(tour_table)
    story.append(Spacer(1,8))
    story.append(Paragraph("Pro tips: Keep serial monitor open side laptop — judges love raw logs. Have water bowl + towel for dunk/hand tests. Fullscreen demo mode hides dev clutter. If WiFi drops hotspot fallback auto 10s. Don't say AI slop words delve tapestry, say plain confident.", s_small))
    story.append(PageBreak())

    # Conclusion
    story.append(Anchor("h1_conclusion","Conclusion"))
    story.append(Paragraph("PART 14 • CONCLUSION • WHY WE WIN", s_kicker))
    story.append(Paragraph("Why We Win — Rs.1,890 Student Project Looks Like Funded Startup", s_h1))
    story.append(Paragraph("Sweated details others skip — FX, AI photos, honest bugs, live data, costed roadmap.", s_body))
    story.append(Spacer(1,6))
    win=[[kpi_card("REAL COST","Rs.1,890","Fully itemized no hidden",EMERALD),kpi_card("REAL BUG","17→2","Shown fixed not hidden",GOLD_DARK),kpi_card("REAL AI","94%","Tested disease ID",EM_DARK)],[kpi_card("REAL LIVE","13 PASS","Not mock live sensors",NAVY),kpi_card("REAL POWER","5V/2A","Lessons logged PD fail",GOLD_DARK),kpi_card("REAL OPEN","100%","Single HTML hackable",EMERALD)]]
    for row in win:
        story.append(Table([row], colWidths=[150,150,150], spaceAfter=6))
    story.append(Spacer(1,6))
    story.append(Paragraph("What judges remember after 20 projects: - Pump stayed ON continuous because fixed arch<br/>- Camera clicked ≤2s diagnosed 94%<br/>- Tank lock said no even when pressed ON safety<br/>- Cost chart Rs.1,890 beats Rs.12,500 premium<br/>- Honesty 10 bugs listed with fixes not hidden<br/>- AI photos + FX + glassmorphism not clip art", s_small))
    story.append(Spacer(1,8))
    story.append(Paragraph("\"Verde isn't mini-project for marks. It's plant that texts you when thirsty, shows disease, waters itself on vacation. Built by two Class X students for less than video game. And it's running right now.\"", s_quote))
    story.append(Spacer(1,10))
    qr_table=Table([[Image(str(ASSETS_DIR/"qr_demo.png"), width=90, height=90), Paragraph("<b>Live Demo QR — Scan Me</b><br/>verde-tech-demo.vercel.app<br/>Replace with ngrok / Vercel real QR before print.<br/><font size=7 color='#6B7280'>Add sticker to hardware enclosure. Judges scan → live dashboard telemetry.</font><br/><br/><font size=8 color='#059669'><b>Rs.1,890 • 5 Sensors • 17→2 Calls • 94% Diagnosis • 8MHz XCLK • 1-sec Heartbeat</b></font>", s_small), shadow_image(ASSETS_DIR/"ai_gold_foil.jpg",80,80,6)]], colWidths=[100,300,90])
    qr_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),G50),('BOX',(0,0),(-1,-1),0.8,G200),('ROUNDEDCORNERS',(0,0),(-1,-1),12),('LEFTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10)]))
    story.append(qr_table)
    story.append(PageBreak())

    # Appendix
    story.append(Paragraph("APPENDIX • SPECS FOR ENGINEERS", s_kicker))
    story.append(Paragraph("Pin Map, Thresholds, Specs — Exact Audit Values", s_h1))
    story.append(Spacer(1,4))
    spec=[["Item","Value Exact FX"],["MCU1","ESP32 WROOM-32 240MHz dual-core 320KB RAM 4MB flash"],["MCU2","ESP32-CAM OV2640 + MB programmer SVGA JPEG flash LED"],["Soil Moisture AO","GPIO34 input only power gated GPIO23 15ms HIGH per read"],["DHT11 DATA","GPIO4 shared GND mandatory"],["LDR AO","GPIO35 input only 10-pt avg ±2% hysteresis"],["HC-SR04","TRIG GPIO18 ECHO GPIO19 5-pt filter invalid rejection tank 15%"],["Relay IN1","GPIO5 active-LOW pump 5V via COM/NO isolated"],["UV LED","GPIO12 active-HIGH +220Ω"],["XCLK","8 MHz was 20MHz → RF interference"],["Boot","Sequential camera init first WiFi after 500ms"],["Watchdog","Hardware 8s fed every loop"],["Thresholds","moisture 35% tank 15% (0=disabled) light 35%"],["Firebase","RTDB verde-tech-haha 1 write/s /sensors 10 metrics 1 read/s /controls 9 keys"],["CAM polling","Polls /controls/capture_photo every 1.5s upload raw JPEG Vercel → base64 /latest_scan"],["OWM","GET weather?q=Delhi city id 1273294 rain ids 2xx/3xx/5xx/6xx → override=1 3min"],["Plant.id","POST base64 → crop + disease suggestions test 94% nutrient deficiency"],["Gemini","gemini-flash-latest X-goog-api-key header inline image+diag+telemetry"],["OpenRouter","Bearer sk-or-v1-... 435 models 8-model text +5-model vision fallback"],["Cost","Total ~ Rs.1,890 electronics 1,320 + power 220 + mechanical 350 + software 0"]]
    spec_data=[[Paragraph(f"<b>{c}</b>", ParagraphStyle('sh', parent=s_small, fontName='Helvetica-Bold', textColor=white)) for c in spec[0]]]
    for row in spec[1:]:
        spec_data.append([Paragraph(f"<b>{row[0]}</b>", s_small), Paragraph(row[1], s_small)])
    spec_table=Table(spec_data, colWidths=[100,390], repeatRows=1)
    spec_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),0.4,G200),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,G50])]))
    story.append(spec_table)
    story.append(Spacer(1,8))
    story.append(Paragraph("Build script: generate_verde_ultimate.py + assets AI images + FX charts. Python 3.11 ReportLab Matplotlib Pillow qrcode. Output Project_Verde_Definitive_Documentation.pdf. Self-review loop mandatory: built → render → audit → score → fix → deliver.", s_small))
    story.append(Spacer(1,6))
    story.append(Paragraph("Acknowledgements: DAV teachers lab access. Lajpat Nagar electronics shop Rs.15 caps. OWM Plant.id Gemini OpenRouter free tiers. Firebase free Vercel hobby. Parents water bowls tolerance pump splashes. AI images via generative model.", s_small))
    story.append(PageBreak())

    # Back cover ultimate
    story.append(NextPageTemplate('cover'))
    story.append(Spacer(1,150))
    story.append(Paragraph("Built by Aarav & Anuj<br/>Class X — DAV ACON 5 2026", ParagraphStyle('back1', parent=s_title_cover, fontSize=22, leading=26, textColor=white, alignment=1)))
    story.append(Spacer(1,12))
    story.append(Paragraph("The plant that waters itself — and talks to AI.", ParagraphStyle('back2', parent=s_tagline, fontSize=13, alignment=1, textColor=HexColor("#A7F3D0"))))
    story.append(Spacer(1,20))
    # small credit row with AI images mini
    story.append(Table([[shadow_image(ASSETS_DIR/"ai_emerald_mesh.jpg",60,60,12), Paragraph("Design System: Deep Navy #0B1D3A + Emerald #10B981 + Gold #F59E0B<br/>2-3 fonts max, generous white space, bold hierarchy, authentic AI photography 40%, icons, infographics, pull quotes, hero numbers, hyperlinked TOC, print-optimized.", s_white_small), shadow_image(ASSETS_DIR/"ai_gold_foil.jpg",60,60,12)]], colWidths=[70,360,70], spaceAfter=12))
    story.append(Spacer(1,20))
    story.append(Paragraph("Total Build Cost ~ Rs. 1,890 • 5 Sensors • 17→2 Calls • 94% Diagnosis • 8 MHz XCLK • 1-sec Heartbeat • Complete & Demo-Ready", ParagraphStyle('back3', parent=s_white_small, alignment=1, fontSize=8)))

    doc=VerdeDoc(OUTPUT, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    doc.build(story)
    print(f"Built {OUTPUT}")
    return OUTPUT

if __name__=="__main__":
    gen_charts_fx()
    out=build_ultimate()
    import os
    print("Size", os.path.getsize(out))
