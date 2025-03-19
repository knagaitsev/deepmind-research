import os
from pathlib import Path

import train

curr_path = Path(os.path.realpath(os.path.dirname(__file__)))
results_dir = curr_path / "results"
results_path = results_dir / "results.csv"
data_path = curr_path / "data/temperature_044/test"

def main():
    file_pattern = os.path.join(str(data_path), 'aggregated*')

    models = [
        {
            "s": "09",
            "time_index": 0
        },
        {
            "s": "08",
            "time_index": 1
        },
        {
            "s": "07",
            "time_index": 2
        },
        {
            "s": "06",
            "time_index": 3
        },
        {
            "s": "05",
            "time_index": 4
        },
        {
            "s": "04",
            "time_index": 5
        },
        {
            "s": "alpha",
            "time_index": 6
        },
        {
            "s": "03",
            "time_index": 7
        },
        {
            "s": "02",
            "time_index": 8
        },
        {
            "s": "01",
            "time_index": 9
        }
    ]

    with open(results_path, 'w') as f:
        f.write("s,time_index,corr_mean,corr_std\n")

    for model in models:
        s_val = model["s"]
        time_index = model["time_index"]

        corr_mean, corr_std = train.apply_model(
            checkpoint_path=f'all_checkpoints/t044_s{s_val}.ckpt',
            file_pattern=file_pattern,
            max_files_to_load=None,
            time_index=time_index
        )

        with open(results_path, 'a') as f:
            f.write(f"{s_val},{time_index},{corr_mean},{corr_std}\n")


if __name__ == '__main__':
    main()
