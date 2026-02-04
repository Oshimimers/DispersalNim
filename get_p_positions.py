from pathlib import Path
import sys

# get_p_positions.py

def filter_zero_lines(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8", errors="replace") as src, \
         output_path.open("w", encoding="utf-8") as dst:
        for line in src:
            if ": 0" in line:
                dst.write(line)

def main():
    base_dir = Path(__file__).parent.resolve()

    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        fname = input("Enter memo filename in this directory (e.g. memo.txt): ").strip()

    input_path = (base_dir / fname).resolve()
    if not input_path.exists():
        print(f"File not found: {input_path}")
        return

    out_name = input_path.stem + "_p_positions" + input_path.suffix
    output_path = base_dir / out_name

    filter_zero_lines(input_path, output_path)
    print(f"Wrote filtered lines to: {output_path}")

if __name__ == "__main__":
    main()