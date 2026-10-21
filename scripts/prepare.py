"""Compatibility entry point; exercise source: Ve_nha/Bai_2/cau_hinh_bao_mat.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Ve_nha.Bai_2.cau_hinh_bao_mat import main

if __name__ == '__main__':
    main()
