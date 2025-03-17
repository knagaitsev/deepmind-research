import os
from pathlib import Path

import train

curr_path = Path(os.path.realpath(os.path.dirname(__file__)))
bench_path = Path.resolve(curr_path / "bench")
results_dir = curr_path / "results"
results_path = results_dir / "results_ablation.csv"
data_path = curr_path / "data/temperature_044/test"

def main():
    file_pattern = os.path.join(str(data_path), 'aggregated*')

    models = [
        {
            "s": "09",
            "time_index": 0
        },
        {
            "s": "alpha",
            "time_index": 6
        },
        {
            "s": "01",
            "time_index": 9
        }
    ]

    with open(results_path, 'w') as f:
        f.write("s,time_index,shell_index,compared_output\n")

    for model in models:
        s_val = model["s"]
        time_index = model["time_index"]

        compared_outputs = train.apply_model_ablation(
            checkpoint_path=f'all_checkpoints/t044_s{s_val}.ckpt',
            file_pattern=file_pattern,
            max_files_to_load=None,
            time_index=time_index
        )

        with open(results_path, 'a') as f:
            for (i, v) in enumerate(compared_outputs):
                f.write(f"{s_val},{time_index},{i},{v}\n")


if __name__ == '__main__':
    main()
