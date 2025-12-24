from simulation import run_simulation

if __name__ == "__main__":
    try:
        run_simulation(steps=10, seed=221)
    except Exception as e:
        print(f"ERROR: {e}")