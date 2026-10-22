"""Build teaching SVGs and Lab 1-5 figures without third-party packages.

Labs 1-3 combine mechanism schematics with synthetic teaching plots. Lab 4 plots
the analytically computed synthetic ODE derivative norms alongside the joint
Gaussian PPO formulation. Lab 5 reads its paired trial data and statistics
directly from the lab. Run with --check to verify checked-in assets without writing.
"""
import argparse
import html
import json
import math
import runpy
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "ei_tutorial"
META = json.loads((ROOT / "tools" / "arxiv_metadata.json").read_text(encoding="utf-8"))

PALETTE = [
    ("#2563eb", "#eff6ff", "#bfdbfe"),
    ("#0d9488", "#f0fdfa", "#99f6e4"),
    ("#7c3aed", "#f5f3ff", "#ddd6fe"),
    ("#d97706", "#fffbeb", "#fde68a"),
    ("#059669", "#ecfdf5", "#a7f3d0"),
    ("#e11d48", "#fff1f2", "#fecdd3"),
    ("#0284c7", "#f0f9ff", "#bae6fd"),
]


def text(x, y, value, size=18, color="#334155", anchor="start", weight="normal"):
    w_attr = f' font-weight="{weight}"' if weight != "normal" else ""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}"{w_attr} '
        f'fill="{color}" text-anchor="{anchor}">{html.escape(str(value))}</text>'
    )


def frame(title, subtitle, body, height=540):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}" '
        'width="100%" height="100%" font-family="Arial, sans-serif">\n'
        '<rect width="1200" height="100%" fill="#FFFFFF"/>\n'
        + text(600, 36, title, 23, "#0f172a", "middle", "700")
        + "\n"
        + text(600, 64, subtitle, 14.5, "#475569", "middle")
        + "\n"
        + body
        + "\n</svg>\n"
    )


def cards(title, subtitle, entries, footer, top_graphic="", top_offset=90, show_arrows=False):
    columns = 2 if len(entries) > 3 else len(entries)
    width = 1120 / columns
    rows = math.ceil(len(entries) / columns)
    wrap_width = max(26, int((width - 52) / 9.2))
    max_lines = max(
        sum(len(textwrap.wrap(p, wrap_width)) for p in paragraphs)
        for _, paragraphs in entries
    )
    max_paragraphs = max(len(paragraphs) for _, paragraphs in entries)
    card_height = max(172, 76 + 21 * max_lines + 5 * max_paragraphs)
    row_height = card_height + 18
    body = [top_graphic] if top_graphic else []
    for i, (heading, paragraphs) in enumerate(entries):
        accent, bg, border = PALETTE[i % len(PALETTE)]
        x = 40 + (i % columns) * width
        y = top_offset + (i // columns) * row_height
        cw = width - 16
        body.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{card_height}" '
            f'rx="10" fill="{bg}" stroke="{border}" stroke-width="1.5"/>'
        )
        body.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="36" '
            f'rx="10" fill="{accent}"/>'
        )
        body.append(text(x + 16, y + 24, heading, 16.5, "#ffffff", "start", "700"))
        line_y = y + 60
        for paragraph in paragraphs:
            for line in textwrap.wrap(paragraph, wrap_width):
                body.append(text(x + 16, line_y, line, 15.5, "#1e293b"))
                line_y += 21
            line_y += 5
        if line_y > y + card_height + 4:
            raise ValueError(f"Card text exceeds available space: {heading}")
        if show_arrows and columns == 3 and i < 2:
            ax1 = x + cw + 2
            ax2 = x + width - 2
            ay = y + card_height / 2
            body.append(
                f'<line x1="{ax1:.1f}" y1="{ay:.1f}" x2="{ax2:.1f}" y2="{ay:.1f}" '
                'stroke="#64748b" stroke-width="2.5"/>'
            )
            body.append(
                f'<polygon points="{ax2-6:.1f},{ay-5:.1f} {ax2:.1f},{ay:.1f} {ax2-6:.1f},{ay+5:.1f}" fill="#64748b"/>'
            )
    height = top_offset + rows * row_height + 64
    for i, line in enumerate(textwrap.wrap(footer, 125)):
        body.append(text(600, height - 38 + i * 19, line, 14, "#475569", "middle"))
    return frame(title, subtitle, "\n".join(body), height)


def build_lab1_top():
    parts = [
        '<rect x="40" y="84" width="1120" height="170" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>',
        text(60, 110, "Computational Graph: Knowledge Insulation (stop_gradient on VLM Hidden Features)", 16, "#0f172a", "start", "700"),
        # VLM Backbone Box
        '<rect x="65" y="132" width="220" height="96" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>',
        text(175, 168, "VLM Backbone", 16, "#1e40af", "middle", "700"),
        text(175, 192, "Shared Hidden h", 14, "#334155", "middle"),
        text(175, 212, "theta_VLM", 13, "#64748b", "middle"),
        # Arrow to Auxiliary Token Head (Top Branch)
        '<line x1="285" y1="158" x2="430" y2="152" stroke="#059669" stroke-width="2.5"/>',
        '<polygon points="424,147 434,152 424,157" fill="#059669"/>',
        text(358, 144, "dL_aux / dh (flows)", 12.5, "#059669", "middle", "700"),
        '<rect x="435" y="124" width="255" height="52" rx="7" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>',
        text(562, 147, "Discrete Token Head (L_aux)", 14.5, "#065f46", "middle", "700"),
        text(562, 166, "Semantic / FAST supervision", 12.5, "#047857", "middle"),
        # Arrow to Stop-Gradient Gate & Flow Expert (Bottom Branch)
        '<line x1="285" y1="202" x2="365" y2="208" stroke="#e11d48" stroke-width="2.5" stroke-dasharray="5,3"/>',
        '<rect x="365" y="190" width="96" height="36" rx="6" fill="#fff1f2" stroke="#e11d48" stroke-width="2"/>',
        text(413, 213, "h.detach()", 13.5, "#be123c", "middle", "700"),
        '<line x1="461" y1="208" x2="495" y2="208" stroke="#2563eb" stroke-width="2.5"/>',
        '<polygon points="489,203 499,208 489,213" fill="#2563eb"/>',
        '<rect x="500" y="186" width="245" height="52" rx="7" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>',
        text(622, 208, "Flow Action Expert (L_flow)", 14.5, "#1e40af", "middle", "700"),
        text(622, 227, "Updates expert; blocked at h", 12.5, "#1d4ed8", "middle"),
        # Right Verification Box
        '<rect x="775" y="114" width="365" height="122" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>',
        text(957, 138, "Synthetic Gradient Routing Check", 15, "#0f172a", "middle", "700"),
        text(795, 166, "With stop_gradient:", 13.5, "#059669", "start", "700"),
        '<rect x="945" y="153" width="8" height="16" fill="#059669"/>',
        text(962, 166, "||grad_joint - grad_aux|| = 0.000", 13, "#065f46"),
        text(795, 198, "Without detach:", 13.5, "#e11d48", "start", "700"),
        '<rect x="945" y="185" width="140" height="16" rx="3" fill="#e11d48"/>',
        text(945, 222, "Flow loss perturbs backbone (> 0)", 13, "#be123c"),
    ]
    return "\n".join(parts)


def build_lab2_top():
    H, d, s = 50, 8, 16
    w_paper, w_exp = [], []
    for i in range(H):
        if i < d:
            w_paper.append(1.0)
            w_exp.append(1.0)
        elif i < H - s:
            c_i = (H - s - i) / (H - s - d + 1)
            w_paper.append(c_i * (math.exp(c_i) - 1.0) / (math.e - 1.0))
            w_exp.append(math.exp(-0.25 * (i - d)))
        else:
            w_paper.append(0.0)
            w_exp.append(0.0)
    # Plot box x=80..620, y=120..240
    px0, py0, pw, ph = 95, 118, 490, 115
    def pt(i, w):
        return f"{px0 + (i / (H - 1)) * pw:.1f},{py0 + (1.0 - w) * ph:.1f}"
    paper_pts = " ".join(pt(i, w) for i, w in enumerate(w_paper))
    exp_pts = " ".join(pt(i, w) for i, w in enumerate(w_exp))
    xd = px0 + (d / (H - 1)) * pw
    x_free = px0 + ((H - s) / (H - 1)) * pw
    parts = [
        '<rect x="40" y="84" width="1120" height="182" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>',
        text(65, 108, "RTC Soft-Mask Schedule W_i Across Chunk Horizon (H=50, d=8, s=16)", 15.5, "#0f172a", "start", "700"),
        f'<rect x="{px0}" y="{py0}" width="{xd-px0:.1f}" height="{ph}" fill="#dbeafe"/>',
        f'<rect x="{xd:.1f}" y="{py0}" width="{x_free-xd:.1f}" height="{ph}" fill="#f3e8ff"/>',
        f'<rect x="{x_free:.1f}" y="{py0}" width="{px0+pw-x_free:.1f}" height="{ph}" fill="#f1f5f9"/>',
        f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="none" stroke="#94a3b8" stroke-width="1.2"/>',
        text(px0 - 8, py0 + 10, "1.0", 12, "#334155", "end"),
        text(px0 - 8, py0 + ph, "0.0", 12, "#334155", "end"),
        text((px0 + xd) / 2, py0 + 22, "[0,d)", 11.5, "#1e40af", "middle", "700"),
        text((xd + x_free) / 2, py0 + 22, "Overlap [d,H-s)", 11.5, "#6d28d9", "middle", "700"),
        text((x_free + px0 + pw) / 2, py0 + 22, "Free [H-s,H)", 11.5, "#475569", "middle", "700"),
        f'<polyline points="{exp_pts}" fill="none" stroke="#d97706" stroke-width="2" stroke-dasharray="5,3"/>',
        f'<polyline points="{paper_pts}" fill="none" stroke="#2563eb" stroke-width="3"/>',
        text(340, 254, "Chunk index i (blue solid: paper W_i; amber dashed: exp(-0.25*(i-d)))", 12.5, "#334155", "middle"),
        # Right formula box
        '<rect x="625" y="102" width="515" height="148" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>',
        text(645, 128, "Exact RTC Equations (Black et al., arXiv:2506.07339, Eq. 2-5):", 15, "#1e40af", "start", "700"),
        text(645, 156, "• Overlap decay:  c_i = (H - s - i) / (H - s - d + 1),  W_i = c_i*(exp(c_i)-1)/(e-1)", 13, "#334155"),
        text(645, 182, "• Denoised endpoint:  a_hat_1 = a_tau + (1 - tau) * v_theta(a_tau, tau)", 13.5, "#334155"),
        text(645, 208, "• Clipped VJP weight:  coeff = min(beta, (1 - tau) / (tau * r_tau^2))", 13.5, "#0f766e", "start", "700"),
        text(645, 234, "• Guided velocity:  v_rtc = v_theta + coeff * (d a_hat_1 / d a_tau)^T [W * (y - a_hat_1)]", 13.5, "#334155"),
    ]
    return "\n".join(parts)


def build_lab3_top():
    parts = [
        '<rect x="40" y="84" width="1120" height="172" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>',
        text(60, 110, "Two-Part Synthetic Teaching Structure in labs/lab3_cascade_tactile_flow.py", 15.5, "#0f172a", "start", "700"),
        # Left box: Part 1 Input Dropout Ablation
        '<rect x="60" y="124" width="520" height="116" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>',
        text(80, 148, "Part 1: Synthetic Proprioception-Dropout Ablation", 14.5, "#1e40af", "start", "700"),
        text(80, 172, "• Sweep train correlation rho in {0.0, 0.5, 0.9} between proprio & target", 13, "#334155"),
        text(80, 194, "• Method A (0% dropout) vs Method B (50% proprio dropout during training)", 13, "#334155"),
        text(80, 216, "• Evaluated on independent noisy test inputs (no claimed winner across all rho)", 13, "#475569"),
        # Right box: Part 2 Two-Stage ODE Rollout
        '<rect x="615" y="124" width="525" height="116" rx="8" fill="#ffffff" stroke="#5eead4" stroke-width="1.5"/>',
        text(635, 148, "Part 2: Generic Two-Stage Flow Rollout", 14.5, "#0f766e", "start", "700"),
        text(635, 172, "• Stage 1 integrates slow_steps with context features (batch, H, D)", 13, "#334155"),
        text(635, 194, "• Stage 2 integrates fast_steps with context + auxiliary features", 13, "#059669", "start", "700"),
        text(635, 216, "• Verifies output tensor shape (batch, H, D) and numerical finiteness", 13, "#334155"),
    ]
    return "\n".join(parts)


def build_lab4_svg():
    ks = (2, 5, 10, 20)
    rows = []
    for k in ks:
        full = 4 * math.sqrt(7) * ((1 + 8 / k) ** k - 1) / 8
        last = 4 * math.sqrt(7) / k
        rows.append((k, full, last))

    px0, py0, pw, ph = 110, 135, 470, 260
    # Log10 scale from 10^-0.5 to 10^3.2
    lo_log, hi_log = -0.5, 3.2
    def y_of(val):
        return py0 + ph - ((math.log10(val) - lo_log) / (hi_log - lo_log)) * ph
    def x_of(idx):
        return px0 + 45 + idx * ((pw - 90) / (len(ks) - 1))

    body = [
        '<rect x="40" y="92" width="575" height="370" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>',
        text(327, 118, "Derivative Norm vs. Euler Steps K (Log10 Scale)", 16.5, "#0f172a", "middle", "700"),
        f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="#ffffff" stroke="#94a3b8" stroke-width="1.2"/>',
    ]
    for exp_v, label in ((0, "10^0"), (1, "10^1"), (2, "10^2"), (3, "10^3")):
        gy = py0 + ph - ((exp_v - lo_log) / (hi_log - lo_log)) * ph
        body.append(f'<line x1="{px0}" y1="{gy:.1f}" x2="{px0+pw}" y2="{gy:.1f}" stroke="#e2e8f0" stroke-dasharray="4,4"/>')
        body.append(text(px0 - 10, gy + 5, label, 12.5, "#475569", "end"))

    full_pts = " ".join(f"{x_of(i):.1f},{y_of(f):.1f}" for i, (_, f, _) in enumerate(rows))
    last_pts = " ".join(f"{x_of(i):.1f},{y_of(l):.1f}" for i, (_, _, l) in enumerate(rows))
    body.append(f'<polyline points="{full_pts}" fill="none" stroke="#e11d48" stroke-width="3"/>')
    body.append(f'<polyline points="{last_pts}" fill="none" stroke="#059669" stroke-width="3"/>')

    for i, (k, f, l) in enumerate(rows):
        cx = x_of(i)
        fy, ly = y_of(f), y_of(l)
        body.append(f'<circle cx="{cx:.1f}" cy="{fy:.1f}" r="5" fill="#e11d48"/>')
        body.append(text(cx, fy - 10, f"{f:.1f}", 12, "#be123c", "middle", "700"))
        body.append(f'<circle cx="{cx:.1f}" cy="{ly:.1f}" r="5" fill="#059669"/>')
        body.append(text(cx, ly + 18, f"{l:.2f}", 12, "#065f46", "middle", "700"))
        body.append(text(cx, py0 + ph + 22, f"K={k}", 13, "#334155", "middle", "700"))

    body += [
        text(327, 442, "Red: Full Euler chain ||dL/dtheta||  |  Green: Last-step-only truncated ||dL/dtheta||", 13, "#334155", "middle", "700"),
        # Right Panel: Analytic values & Joint Gaussian PPO Card
        '<rect x="635" y="92" width="525" height="370" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>',
        '<rect x="635" y="92" width="525" height="38" rx="10" fill="#1d4ed8"/>',
        text(897, 117, "Analytic Values & Joint Gaussian Chunk PPO", 16.5, "#ffffff", "middle", "700"),
        text(655, 152, "Positive linear field: velocity = 8 * a + theta; batch=4, action dim=7", 14.5, "#1e293b", "start", "700"),
    ]
    for i, (k, full, last) in enumerate(rows):
        y = 186 + i * 32
        body.append(text(665, y, f"K={k:2d}: full derivative norm = {full:.3f}; last-step-only = {last:.3f}", 15, "#334155"))
    body += [
        '<rect x="655" y="314" width="485" height="128" rx="8" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.2"/>',
        text(672, 340, "Key Implementation Checks in Lab 4:", 14.5, "#1e40af", "start", "700"),
        text(672, 365, "1. Joint chunk density sums log_prob over (H, D): .sum(dim=(1, 2))", 13.5, "#334155"),
        text(672, 390, "2. Forward trajectories are identical; truncation changes the gradient estimator.", 13.5, "#334155"),
        text(672, 415, "3. Chosen unstable field only. Neither a variance theorem nor robot RL score.", 13.5, "#475569"),
    ]
    return frame(
        "Lab 4: joint Gaussian PPO and truncated differentiation",
        "SYNTHETIC ANALYTIC EXAMPLE - no training success-rate curve",
        "\n".join(body),
        500,
    )


def build_lab5_svg():
    stats = runpy.run_path(str(ROOT / "labs" / "lab5_rigorous_robot_eval_statistics.py"), run_name="figure_source")
    trials = stats["synthetic_trial_data"]()
    body = [
        '<rect x="40" y="92" width="700" height="330" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>',
        text(65, 122, "Arbitrary paired outcomes, N=50; Wilson 95% intervals", 17, "#0f172a", "start", "700"),
    ]
    x0, x_scale = 340, 3.6
    for pct in (0, 25, 50, 75, 100):
        gx = x0 + pct * x_scale
        body.append(f'<line x1="{gx:.1f}" y1="140" x2="{gx:.1f}" y2="375" stroke="#e2e8f0" stroke-dasharray="3,3"/>')
        body.append(text(gx, 398, f"{pct}%", 12, "#64748b", "middle"))
    for i, (name, values) in enumerate(trials.items()):
        rate, lo, hi = stats["wilson_score_ci"](sum(values), len(values))
        y = 168 + i * 54
        body += [
            text(65, y, f"{name}: {sum(values)}/50 = {rate:.1f}%", 15.5, "#1e293b", "start", "700"),
            f'<line x1="{x0+lo*x_scale:.1f}" y1="{y-5}" x2="{x0+hi*x_scale:.1f}" y2="{y-5}" stroke="#2563eb" stroke-width="4"/>',
            f'<line x1="{x0+lo*x_scale:.1f}" y1="{y-12}" x2="{x0+lo*x_scale:.1f}" y2="{y+2}" stroke="#2563eb" stroke-width="2.5"/>',
            f'<line x1="{x0+hi*x_scale:.1f}" y1="{y-12}" x2="{x0+hi*x_scale:.1f}" y2="{y+2}" stroke="#2563eb" stroke-width="2.5"/>',
            f'<circle cx="{x0+rate*x_scale:.1f}" cy="{y-5}" r="6" fill="#1d4ed8"/>',
            text(65, y + 20, f"95% interval: [{lo:.1f}%, {hi:.1f}%]", 13.5, "#475569"),
        ]
    n10, n01, p = stats["mcnemar_exact_binomial_p"](trials["Method D"], trials["Method C"])
    _, wl, wh = stats["wilson_score_ci"](10, 10)
    body += [
        '<rect x="760" y="92" width="400" height="330" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>',
        '<rect x="760" y="92" width="400" height="38" rx="10" fill="#0d9488"/>',
        text(960, 117, "Paired McNemar & Small-N Check", 16.5, "#ffffff", "middle", "700"),
        text(782, 158, "Method D vs Method C (N=50 paired):", 15, "#0f172a", "start", "700"),
        text(782, 186, f"• Discordant pairs: b={n10} (D only), c={n01} (C only)", 14, "#334155"),
        text(782, 212, f"• Exact two-sided McNemar p = {p:.8f}", 14, "#0f766e", "start", "700"),
        '<rect x="780" y="242" width="360" height="156" rx="8" fill="#fff1f2" stroke="#fecdd3" stroke-width="1.2"/>',
        text(798, 270, "Small-Sample Trap (10/10 Successes):", 14.5, "#9f1239", "start", "700"),
        text(798, 298, "• Naive Wald CI: [100.0%, 100.0%] (overconfident)", 13.5, "#be123c"),
        text(798, 324, f"• Wilson 95% CI: [{wl:.1f}%, {wh:.1f}%]", 13.5, "#065f46", "start", "700"),
        text(798, 354, "• Always report exact k/N alongside interval bounds.", 13, "#334155"),
        text(65, 455, f"D vs C: discordant pairs {n10}/{n01}; exact two-sided McNemar p = {p:.8f}", 16.5, "#1e293b", "start", "700"),
        text(65, 485, f"10/10 example: Wald [100, 100]%; Wilson [{wl:.1f}, {wh:.1f}]%. No MDE/power claim.", 15.5, "#475569"),
    ]
    return frame(
        "Lab 5: paired statistics from the script's example data",
        "SYNTHETIC - NOT REAL RESULTS; Method A/B/C/D do not identify published methods",
        "\n".join(body),
        520,
    )


def build_se3_top():
    def triad(cx, cy, label):
        return "\n".join([
            f'<circle cx="{cx}" cy="{cy}" r="26" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>',
            f'<line x1="{cx}" y1="{cy}" x2="{cx+18}" y2="{cy}" stroke="#e11d48" stroke-width="2.5"/>',
            f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-18}" stroke="#059669" stroke-width="2.5"/>',
            f'<line x1="{cx}" y1="{cy}" x2="{cx-12}" y2="{cy+12}" stroke="#2563eb" stroke-width="2.5"/>',
            text(cx, cy + 44, label, 13.5, "#0f172a", "middle", "700"),
        ])
    parts = [
        '<rect x="40" y="84" width="1120" height="132" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>',
        triad(160, 138, "{W} World"),
        '<line x1="195" y1="138" x2="415" y2="138" stroke="#2563eb" stroke-width="2.5"/>',
        '<polygon points="409,133 419,138 409,143" fill="#2563eb"/>',
        text(305, 126, "T(W,B): Base Pose", 13.5, "#1d4ed8", "middle", "700"),
        triad(460, 138, "{B} Robot Base"),
        '<line x1="495" y1="126" x2="725" y2="114" stroke="#0d9488" stroke-width="2.5"/>',
        '<polygon points="719,109 729,114 719,119" fill="#0d9488"/>',
        text(610, 108, "T(B,E)(q): Forward Kinematics", 13, "#0f766e", "middle", "700"),
        triad(775, 118, "{E} End-Effector"),
        '<line x1="495" y1="152" x2="985" y2="152" stroke="#7c3aed" stroke-width="2.5" stroke-dasharray="5,3"/>',
        '<polygon points="979,147 989,152 979,157" fill="#7c3aed"/>',
        text(740, 174, "T(B,C): Calibrated Camera Extrinsics", 13, "#6d28d9", "middle", "700"),
        triad(1030, 138, "{C} Camera"),
    ]
    return "\n".join(parts)


def build():
    out = {}
    out["lab1_ki_and_latency_plot.svg"] = cards(
        "Lab 1: knowledge-insulation gradient routing",
        "SYNTHETIC TEACHING DIAGRAM - not a semantic-retention or robot benchmark",
        [
            ("Auxiliary token objective", ["Random labels provide an auxiliary loss.", "Its gradient still reaches the backbone."]),
            ("Continuous flow objective", ["Detached hidden features block only this loss from the backbone.", "The action expert remains trainable."]),
            ("Checks in the script", ["Joint backbone gradient equals auxiliary gradient with insulation.", "Latency is measured locally, not copied from a paper."]),
        ],
        "Source: labs/lab1_openpi_ki_and_latency_profiler.py. No fixed cosine-retention or pretrained-model latency claim.",
        top_graphic=build_lab1_top(),
        top_offset=272,
    )
    out["lab2_rtc_trajectory_inpainting_plot.svg"] = cards(
        "Lab 2: clipped RTC guidance",
        "SYNTHETIC TEACHING DIAGRAM - not real robot results or a claimed percentage improvement",
        [
            ("1. Build the soft mask", ["Committed prefix: weight 1; distant suffix: weight 0.", "Transition uses the paper mask; optional variants are explicit."]),
            ("2. Compute the endpoint VJP", ["Endpoint = a + (1 - time) * velocity.", "Use the endpoint Jacobian, not an identity approximation."]),
            ("3. Integrate finite guidance", ["Clip the guidance coefficient at beta, including time zero.", "Report action differences, not a velocity or acceleration guarantee."]),
        ],
        "Source: labs/lab2_rtc_soft_masked_inpainting.py; Black et al., arXiv:2506.07339, equations 2-5.",
        top_graphic=build_lab2_top(),
        top_offset=282,
        show_arrows=True,
    )
    out["lab3_two_stage_modality_ablation_plot.svg"] = cards(
        "Lab 3: controlled synthetic input ablation",
        "SYNTHETIC - not real results; Method A/B are not published robotics methods",
        [
            ("Matched models and data", ["A/B use the same network, initialization, inputs and optimizer.", "Only training-time input dropout differs."]),
            ("Partial train correlation", ["Sweep correlation: 0.0, 0.5, 0.9.", "Tactile observations remain noisy; targets are synthetic scalars."]),
            ("Independent test input", ["Test proprioception is independent random noise, not fixed zero.", "Report MSE without asserting a winner or robot success rate."]),
        ],
        "Source: labs/lab3_cascade_tactile_flow.py. A separate configurable two-stage rollout checks output tensor shapes.",
        top_graphic=build_lab3_top(),
        top_offset=272,
    )
    out["lab4_flow_rl_convergence_plot.svg"] = build_lab4_svg()
    out["lab5_statistical_eval_wilson_mcnemar_plot.svg"] = build_lab5_svg()
    out["stage1_coordinate_frames_se3.svg"] = cards(
        "Coordinate frames and rotation representations",
        "Conceptual geometry - all transforms must declare source and destination frames",
        [
            ("Frame convention", ["T(A,B) maps coordinates in frame B into frame A.", "Compose T(world,base) with T(base,tool); calibrate camera extrinsics separately."]),
            ("Three rotation choices", ["Euler angles: a local chart with singularities.", "Unit quaternion: normalized, with q and -q representing the same rotation."]),
            ("Control consistency", ["6D rotation outputs require orthonormalization.", "Express pose error, angular velocity and wrench in consistent frames."]),
        ],
        "Teaching schematic. No duplicate quaternion panel; no uncalibrated camera-to-camera transform is implied.",
        top_graphic=build_se3_top(),
        top_offset=232,
    )
    out["stage2_qwen_vl_alignment_and_memory.svg"] = cards(
        "Qwen-RobotManip and REKI: distinct evidence",
        "Architectural details must follow each paper; these are not a shared Qwen3.5 specification",
        [
            ("Qwen-RobotManip", ["Built on Qwen-VL; aligns representation, motion and behavior.", "Uses a curated mixture of public robot data and human videos."]),
            ("REKI", ["2.4B VLA with a flow-matching action expert.", "Persistent expert-cache registers summarize recent VLM features."]),
            ("Evidence boundary", ["Do not infer a fixed 3:1 layer schedule, 32 registers or latency from a family name.", "Use version-specific technical reports and code."]),
        ],
        "Sources: arXiv:2606.17846; arXiv:2610.22178. No cross-paper benchmark values are reproduced here.",
    )
    out["vlm_backbone_evidence_comparison.svg"] = cards(
        "VLM backbone comparison: separate family from implementation",
        "Conceptual comparison; model family alone does not determine a robot policy's architecture",
        [
            ("PaliGemma / Gemma", ["Check the exact backbone release and action-expert configuration.", "Count vision, language and action parameters separately."]),
            ("Qwen-VL-based policies", ["Qwen-RobotManip describes alignment and multi-source scaling.", "REKI describes a compact VLA with persistent expert registers."]),
            ("Deployment comparison", ["Report hardware, precision, input images and action horizon.", "Separate control frequency from end-to-end inference latency."]),
        ],
        "Sources: arXiv:2410.24164; arXiv:2606.17846; arXiv:2610.22178. No unsupported Qwen3.5 performance ledger.",
    )
    chronology = [
        ("Diffusion Policy", "2303.04137"),
        ("RT-2", "2307.15818"),
        ("OpenVLA", "2406.09246"),
        ("pi0", "2410.24164"),
        ("pi0.5", "2504.16054"),
        ("pi*0.6", "2511.14759"),
        ("pi0.7", "2604.15483"),
    ]
    timeline_bar = "\n".join([
        '<line x1="70" y1="108" x2="1130" y2="108" stroke="#cbd5e1" stroke-width="4"/>',
        *[
            f'<circle cx="{95 + i * 168}" cy="108" r="8" fill="{PALETTE[i % len(PALETTE)][0]}"/>'
            + text(95 + i * 168, 94, f"{name} ({META[aid]['published'][:7]})", 12, "#0f172a", "middle", "700")
            for i, (name, aid) in enumerate(chronology)
        ],
    ])
    out["stage2_vla_full_chronology_2022_2026.svg"] = cards(
        "Selected VLA milestones by preprint date",
        "Chronology is not an architectural inheritance graph or a publisher-endorsed figure",
        [(name + " / " + META[aid]["published"][:7], [META[aid]["title"], "arXiv:" + aid]) for name, aid in chronology],
        "Dates refer to the first arXiv submission in tools/arxiv_metadata.json; conference dates may differ.",
        top_graphic=timeline_bar,
        top_offset=132,
    )
    routes = [
        ("1. Denoising-chain MDP", ["DPPO", "Optimize tractable stochastic denoising transitions."]),
        ("2. Stochastic flow transitions", ["ReinFlow / pi_RL / RLinf", "Noise makes discrete conditional transitions tractable."]),
        ("3. Forward-process surrogate", ["RoboFFT", "Use a training surrogate; do not call it an exact marginal likelihood."]),
        ("4. Noise-space steering", ["DSRL / NSL", "Adapt the initial noise interface of a frozen base policy."]),
        ("5. Residual / selective heads", ["ResFiT / RL Token", "Train a residual or compact readout on a base policy."]),
        ("6. Advantage / value conditioning", ["RECAP / VaM", "Condition generation or post-training on value information."]),
        ("7. Actor-critic action improvement", ["PA-RL", "Separate critic-guided action improvement from policy fitting."]),
    ]
    out["stage2_flow_vla_rl_seven_routes.svg"] = cards(
        "Seven routes for post-training generative robot policies",
        "Taxonomy follows the tutorial table; route numbers are editorial categories, not paper claims",
        routes,
        "Sources and scope: docs/02_VLA_WAM_and_Flow_RL.md, core chapter A; exact titles in references.bib.",
    )
    out["stage2_recap_vs_rlt_rl_paradigms.svg"] = cards(
        "Post-training interfaces: distinguish the optimization target",
        "Conceptual comparison - no unconditional gradient-explosion theorem",
        [
            ("RECAP: condition generation", ["Use advantage information in a supervised generative objective.", "Read the paper's data collection and improvement loop separately."]),
            ("RL Token: compact RL interface", ["Expose a compact representation and train a small actor-critic interface.", "Do not confuse an RL token with output action tokenization."]),
            ("Conditional Gaussian PPO", ["A joint chunk density sums log-probability over all action coordinates.", "Stopping earlier gradients changes the estimator, not the forward trajectory."]),
        ],
        "Sources: arXiv:2511.14759, 2604.23073; the conditional Gaussian example is in Lab 4, not a claimed reproduction.",
    )
    out["stage3_contact_rich_tactile_rtc_recovery.svg"] = cards(
        "Contact-rich manipulation: perception, execution and verification",
        "Public-paper concepts; no unpublished project design or claimed new method",
        [
            ("1. Tactile representation", ["T3 / Sparsh / UniTouch study transferable representations.", "A token count or stiffness output must be checked per implementation."]),
            ("2. Reactive policies", ["RDP and tactile policies study reactive sensor fusion.", "A generic two-rate teaching model is not a reproduction of these methods."]),
            ("3. RTC execution", ["Black et al.: committed prefix and clipped inpainting guidance.", "Training-time conditioning is a separate follow-up approach."]),
            ("4. Verification and recovery", ["FAVOR: compare WAM observations with future anchors.", "DiVeR: decision-critical verification for test-time selection."]),
        ],
        "References: arXiv:2406.13640, 2506.07339, 2512.05964, 2610.06280, 2610.04933. No failure-aware-critic expansion of FAVOR.",
    )
    out["benchmark_sota_comparison_2026.svg"] = cards(
        "Comparing embodied-policy results: retain the protocol",
        "Evaluation guide - no unsupported cross-paper ranking or latency measurements",
        [
            ("Task and distribution", ["Record benchmark version, split and task list.", "Standard LIBERO and shifted settings answer different questions."]),
            ("Compute and execution", ["Record hardware, precision, input views, horizon and denoising steps.", "Distinguish inference latency from servo frequency."]),
            ("Trials and uncertainty", ["Publish trial counts, seeds and success definitions.", "Use paired tests only with genuinely paired outcomes."]),
        ],
        "Use each original paper's protocol. This repository's synthetic labs cannot supply SOTA robot success rates.",
        show_arrows=True,
    )
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for name, content in build().items():
        path = ASSETS / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        raise SystemExit("Stale figures: " + ", ".join(stale))
    print("Verified 13 generated SVG figures." if args.check else "Built 13 SVG figures.")


if __name__ == "__main__":
    main()
