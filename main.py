import asyncio
import os
import shutil
import logging
from pathlib import Path
from argparse import ArgumentParser


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    tasks = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            tasks.append(asyncio.create_task(copy_file(file_path, output_folder)))

    await asyncio.gather(*tasks)

async def copy_file(file_path, output_folder):
    try:
        extension = file_path.suffix.lstrip(".") or "no_extension"
        target_folder = Path(output_folder) / extension
        target_folder.mkdir(parents=True, exist_ok=True)
        target_path = target_folder / file_path.name

        await asyncio.to_thread(shutil.copy2, file_path, target_path)
        logging.info(f"Copied: {file_path} to {target_path}")
    except Exception as e:
        logging.error(f"Failed to copy {file_path}: {e}")

def main():
    parser = ArgumentParser(description="Sort files by extension asynchronously.")
    parser.add_argument("source_folder", type=str, help="Path to the source folder.")
    parser.add_argument("output_folder", type=str, help="Path to the output folder.")

    args = parser.parse_args()
    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.is_dir():
        logging.error(f"Source folder does not exist: {source_folder}")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == "__main__":
    main()
