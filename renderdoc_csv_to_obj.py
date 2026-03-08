import csv
import sys
import argparse
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(description="Convert RenderDoc CSV to OBJ")
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("--mode", choices=["triangles", "strips"], default="strips", help="Draw mode")
    parser.add_argument("--flip-winding", action="store_true", help="Flip face winding")
    args = parser.parse_args()

    vertices = {}
    texcoords = {}
    indices = []

    with open(args.input, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        for row in reader:
            idx = int(row['IDX'])
            pos = (float(row['v_Position.x']), float(row['v_Position.y']), float(row['v_Position.z']))
            uv = (float(row['v_TexCoord0.x']), float(row['v_TexCoord0.y']))
            vertices[idx] = pos
            texcoords[idx] = uv
            indices.append(idx)

    # Get unique indices in order
    unique_indices = sorted(set(indices))

    # Map old index to new 0-based
    index_map = {old: new for new, old in enumerate(unique_indices)}

    # Write OBJ
    obj_file = args.input.replace('.csv', '.obj')
    with open(obj_file, 'w') as f:
        # Write vertices
        for idx in unique_indices:
            pos = vertices[idx]
            f.write(f"v {pos[0]} {pos[1]} {pos[2]}\n")

        # Write texcoords
        for idx in unique_indices:
            uv = texcoords[idx]
            f.write(f"vt {uv[0]} {uv[1]}\n")

        # Build faces
        if args.mode == "triangles":
            for i in range(0, len(indices), 3):
                if i + 2 < len(indices):
                    idx0 = index_map[indices[i]]
                    idx1 = index_map[indices[i+1]]
                    idx2 = index_map[indices[i+2]]
                    if args.flip_winding:
                        idx0, idx2 = idx2, idx0
                    f.write(f"f {idx0+1}/{idx0+1} {idx1+1}/{idx1+1} {idx2+1}/{idx2+1}\n")
        elif args.mode == "strips":
            for i in range(len(indices) - 2):
                idx0 = index_map[indices[i]]
                idx1 = index_map[indices[i+1]]
                idx2 = index_map[indices[i+2]]
                if args.flip_winding:
                    if i % 2 == 0:
                        idx0, idx2 = idx2, idx0
                else:
                    if i % 2 == 1:
                        idx0, idx2 = idx2, idx0
                f.write(f"f {idx0+1}/{idx0+1} {idx1+1}/{idx1+1} {idx2+1}/{idx2+1}\n")

    print(f"Converted {args.input} to {obj_file}")

if __name__ == "__main__":
    main()