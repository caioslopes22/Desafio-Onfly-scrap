
from poke_pipeline.main import run

if __name__ == "__main__":
    run(limit=100, offset=0, output_dir="/app/outputs", request_delay=0.05)
