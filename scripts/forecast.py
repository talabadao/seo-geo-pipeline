#!/usr/bin/env python3
"""forecast.py — hỗ trợ tab Measurement (skill /forecast).

Nguyên tắc (CLAUDE.md §2): số do máy tính, Claude diễn giải. Công thức Goal/Market trend GIỮ trong
Google Sheet; script này chỉ CHUẨN BỊ các dòng `Actual` lấy từ Agency Analytics để /forecast ghi vào
Sheet, và (tùy chọn) tính một forecast bottom-up tham chiếu từ Content Plan.

Bản Phase 1: khung + chú thích. Phần nối Agency Analytics do skill /forecast gọi qua MCP rồi truyền
số vào đây để tính uplift tham chiếu. Chưa gọi API trong script này (tránh giữ credential ở repo).
"""
import sys, json


def bottom_up_uplift(rows, ctr_curve=None):
    """rows: [{'volume': int, 'target_pos': int, 'ramp': float}]. Trả uplift ước tính/tháng."""
    ctr = ctr_curve or {1: .28, 2: .15, 3: .10, 4: .07, 5: .05, 6: .04, 7: .03, 8: .025,
                         9: .02, 10: .017}
    total = 0.0
    for r in rows:
        pos = int(r.get("target_pos", 5))
        total += r.get("volume", 0) * ctr.get(pos, 0.01) * r.get("ramp", 1.0)
    return round(total)


if __name__ == "__main__":
    # Ví dụ: echo '[{"volume":480,"target_pos":3,"ramp":0.6}]' | python3 scripts/forecast.py
    try:
        rows = json.load(sys.stdin)
        print(f"Uplift tham chiếu/tháng: {bottom_up_uplift(rows)} sessions")
    except Exception:
        print(__doc__)
