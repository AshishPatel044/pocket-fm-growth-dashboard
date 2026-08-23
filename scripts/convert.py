#!/usr/bin/env python3
"""Auto-update index.html with new CSV data from the data/ folder."""

import csv, json, re, sys
from datetime import datetime
from pathlib import Path

CSV_CPS   = Path('data/CPS New Sheet - Master Sheet (CPS).csv')
CSV_SCALE = Path('data/CPS New Sheet - New Scalling Ads .csv')
HTML_PATH = Path('index.html')

CPS_KEYS = [
    'adset_name','show_name','base_asset','selected_promos','video_type',
    'adset_id','show_id','start_date','end_date','delivery',
    'meta_installs','cpi_usd','cpi_inr','activation','vc25','vc50','vc75','vc95',
    'cpm','cti','octr',
    'f_qs_installs','f_cpi_qs','f_ldau','f_10min','f_30min','f_ssd0act',
    'f_act_ldau','f_conv_d0','f_rec_d0','f_adopt_d0','f_d0h2','f_d0h4',
    'f_ssd3act','f_d3h4','f_d3h5','f_conv_d3','f_rec_d3','f_adopt_d3',
    'f_bing_d3','f_sbing_d3',
    'f_ssd7act','f_d7h4','f_d7h5','f_d7h10','f_conv_d7','f_rec_d7',
    'f_adopt_d7','f_bing_d7','f_sbing_d7',
    'n_qs_installs','n_ldau','n_10min','n_30min','n_ssd0act',
    'n_conv_d0','n_rec_d0','n_d0h2','n_d0h4',
    'n_ssd3act','n_d3h4','n_d3h5','n_conv_d3','n_rec_d3','n_bing_d3','n_sbing_d3',
    'n_ssd7act','n_d7h4','n_d7h5','n_d7h10','n_conv_d7','n_rec_d7',
    'n_bing_d7','n_sbing_d7',
]
CPS_TEXT = set(range(10))

SCALE_KEYS = [
    'show_name','show_id','adset_id','promo','adset_name','asset_link','time',
    'cpi_inr','cost_usd','show_drr',
    'installs','act','recovery','conversion','bingers','arpu','arppu',
    'whales','swhales','h1','h4','h5','h10','h20',
    'd3_installs','d3_act','d3_recovery','d3_conversion','d3_bingers',
    'd3_arpu','d3_arppu','d3_whales','d3_swhales',
    'd3_h1','d3_h4','d3_h5','d3_h5h1','d3_h10','d3_h20','d3_h30',
    'cpd3_h20','cpd3_h30','cpwd3','cpswd3',
    'd7_installs','d7_act','d7_recovery','d7_conversion','d7_bingers',
    'd7_arpu','d7_arppu','d7_whales','d7_swhales',
    'd7_h1','d7_h4','d7_h5','d7_h5h1','d7_h10','d7_h20','d7_h30',
    'cpd7_h20','cpd7_h30','cpwd7','cpswd7',
    'd15_installs','d15_act','d15_recovery','d15_conversion','d15_bingers',
    'd15_arpu','d15_arppu','d15_whales','d15_swhales',
    'd15_h1','d15_h4','d15_h5','d15_h5h1','d15_h10','d15_h20','d15_h30',
    'cpd15_h20','cpd15_h30','cpwd15','cpswd15',
]
SCALE_TEXT = set(range(7))


def parse_val(v):
    v = v.strip()
    if not v:
        return None
    if v.startswith('$'):
        f = float(v[1:].replace(',', ''))
        return int(f) if f == int(f) else round(f, 8)
    if v.endswith('%'):
        return round(float(v[:-1].replace(',', '')) / 100.0, 8)
    v2 = v.replace(',', '')
    try:
        return int(v2) if '.' not in v2 else round(float(v2), 8)
    except (ValueError, OverflowError):
        return v or None


def csv_to_rows(path, keys, text_cols, skip):
    rows = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for _ in range(skip):
            next(reader)
        for raw in reader:
            if not any(c.strip() for c in raw):
                continue
            row = {}
            for i, key in enumerate(keys):
                cell = raw[i].strip() if i < len(raw) else ''
                if i in text_cols:
                    row[key] = cell if cell else None
                else:
                    row[key] = parse_val(cell)
            rows.append(row)
    return rows


def main():
    for p in (CSV_CPS, CSV_SCALE, HTML_PATH):
        if not p.exists():
            print(f'ERROR: {p} not found', file=sys.stderr)
            sys.exit(1)

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    db_idx = next(
        (i for i, l in enumerate(lines) if l.strip().startswith('const DB = {')),
        None,
    )
    if db_idx is None:
        print('ERROR: could not find "const DB = {" line in index.html', file=sys.stderr)
        sys.exit(1)

    db_str = lines[db_idx].strip().rstrip(';')
    db_str = db_str[len('const DB = '):]
    db = json.loads(db_str)

    # Replace rows only — columns are never touched
    cps_rows   = csv_to_rows(CSV_CPS,   CPS_KEYS,   CPS_TEXT,   skip=3)
    scale_rows = csv_to_rows(CSV_SCALE, SCALE_KEYS, SCALE_TEXT, skip=2)
    db['cps']['rows']     = cps_rows
    db['scaling']['rows'] = scale_rows

    lines[db_idx] = (
        'const DB = '
        + json.dumps(db, ensure_ascii=False, separators=(',', ':'))
        + ';\n'
    )

    d = datetime.utcnow()
    today = f"{d.day} {d.strftime('%b')} {d.year}"
    pattern = re.compile(r'(<span class="udate">)[^<]*(</span>)')
    lines = [pattern.sub(rf'\g<1>{today}\2', l) for l in lines]

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f'Done: {len(cps_rows)} CPS rows, {len(scale_rows)} Scaling rows. Date: {today}')


if __name__ == '__main__':
    main()
