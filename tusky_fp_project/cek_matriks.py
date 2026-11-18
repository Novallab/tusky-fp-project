"""Skrip bantu: cetak matriks fungsi x aplikasi beserta file:baris pemanggilan."""
import glob, re, os
import fplib
fungsi = [n for n in dir(fplib) if n.startswith("fp_")]
apps = sorted(glob.glob(os.path.join("apps", "app*.py")))
pemakaian = {f: {} for f in fungsi}
for a in apps:
    for no, baris in enumerate(open(a, encoding="utf-8"), 1):
        if baris.startswith(("from", "import", "                   ")) and "fp_" in baris:
            continue
        for f in fungsi:
            if re.search(rf"\b{f}\(", baris):
                pemakaian[f].setdefault(os.path.basename(a), []).append(no)
for f in fungsi:
    p = pemakaian[f]
    status = "OK" if len(p) >= 3 else "KURANG"
    print(f"{f:18} {len(p)}/5 {status}  " + "; ".join(f"{k}:{v[0]}" for k, v in p.items()))
