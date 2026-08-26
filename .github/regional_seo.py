import runpy
import subprocess
import sys

# Keep the established regional SEO implementation untouched, then add the
# approved social-link preview as the final presentation/metadata pass.
runpy.run_path(".github/regional_seo_core.py", run_name="__main__")

try:
    import PIL  # noqa: F401
except ModuleNotFoundError:
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--quiet",
        "Pillow",
    ])

runpy.run_path(".github/social_preview.py", run_name="__main__")
