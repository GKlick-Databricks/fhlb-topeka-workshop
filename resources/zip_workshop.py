"""Zip a workshop folder for Databricks import — WITH directory entries.

Why this exists: `zipfile.write(path, arcname)` writes only file entries. Databricks' workspace
zip import creates subfolders ONLY from explicit directory entries, so plain zips silently drop
your resources/, 07_app/, data/ subfolders on import. This writer emits the directory entries.

Usage:
    python3 zip_workshop.py <src_dir> <output.zip> [arcroot]
    # arcroot defaults to the src_dir's basename (the top folder name inside the zip)

Verify afterwards:
    zipinfo -1 output.zip | grep '/$'      # should list your subfolders
"""
import os, sys, zipfile

def zip_dir(src_dir, out_zip, arcroot=None, exclude=(".DS_Store",)):
    src_dir = os.path.abspath(src_dir)
    arcroot = arcroot or os.path.basename(src_dir.rstrip("/"))
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(zipfile.ZipInfo(arcroot + "/"), "")                    # root dir entry
        for root, dirs, files in os.walk(src_dir):
            for d in sorted(dirs):
                dfull = os.path.join(root, d)
                z.writestr(zipfile.ZipInfo(os.path.join(arcroot, os.path.relpath(dfull, src_dir)) + "/"), "")
            for fn in sorted(files):
                if fn in exclude:
                    continue
                fp = os.path.join(root, fn)
                z.write(fp, os.path.join(arcroot, os.path.relpath(fp, src_dir)))
    # sanity check: confirm directory entries exist
    with zipfile.ZipFile(out_zip) as z:
        dirs = [n for n in z.namelist() if n.endswith("/")]
    print(f"wrote {out_zip}: {os.path.getsize(out_zip)//1024} KB, {len(dirs)} directory entries")
    if not dirs:
        print("  WARNING: no directory entries — subfolders will not import into Databricks!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    zip_dir(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
