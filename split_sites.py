%%writefile split_sites.py
import pandas as pd, os, hashlib, pathlib, shutil

SRC = pathlib.Path("data/full")
DEST = pathlib.Path("data/sites")
if DEST.exists(): shutil.rmtree(DEST)
DEST.mkdir(parents=True)

patients = pd.read_csv(SRC/"patients.csv")
patients["site"] = patients["Id"].apply(
    lambda x: int(hashlib.sha1(x.encode()).hexdigest(), 16) % 5
)

for site_id in range(5):
    site_dir = DEST/f"site_{site_id}"
    site_dir.mkdir()
    p_ids = set(patients.loc[patients["site"]==site_id, "Id"])
    for fn in SRC.glob("*.csv"):
        df = pd.read_csv(fn)
        if "PATIENT" in df.columns:
            df[df["PATIENT"].isin(p_ids)].to_csv(site_dir/fn.name, index=False)
