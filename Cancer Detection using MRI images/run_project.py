import os
import sys
import subprocess
import pandas as pd

def run_cmd(cmd, description):
    print(f"\n>>> Running: {description}...")
    print(f"Command: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {e}")
        sys.exit(1)

def setup_dependencies():
    print("Checking and installing dependencies...")
    
    # List of required packages
    required_packages = ["torch", "torchvision", "tensorboardX", "h5py", "torchsummary"]
    missing_packages = []
    
    for pkg in required_packages:
        try:
            __import__(pkg)
        except ImportError:
            missing_packages.append(pkg)
            
    if missing_packages:
        print(f"Missing packages detected: {missing_packages}")
        # Standard install command
        if "torch" in missing_packages or "torchvision" in missing_packages:
            print("Installing PyTorch CPU version...")
            run_cmd("pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu", "Installing PyTorch")
            # Remove from generic install list since we handled it
            missing_packages = [p for p in missing_packages if p not in ["torch", "torchvision"]]
            
        if missing_packages:
            run_cmd(f"pip install {' '.join(missing_packages)}", "Installing remaining packages")
    else:
        print("All dependencies are already installed.")

def generate_dummy_data_if_needed():
    csv_path = os.path.join("dataset_csv", "dummy_dataset.csv")
    dummy_data_dir = os.path.join("dummy_data", "DUMMY_DATA_DIR")
    dataset_dir = os.path.join("dummy_data", "DATASET_DIR")
    
    # Read unique slide IDs
    df = pd.read_csv(csv_path)
    slide_ids = df["slide_id"].dropna().unique()
    
    # Check if files already exist
    all_exist = True
    for slide_id in slide_ids[:5]:  # sample check
        if not os.path.exists(os.path.join(dummy_data_dir, f"{slide_id}.pt")):
            all_exist = False
            break
            
    if all_exist and os.path.exists(dummy_data_dir) and len(os.listdir(dummy_data_dir)) >= len(slide_ids):
        print("Dummy feature files already exist. Skipping generation.")
        return
        
    print(f"Generating mock feature files (.pt) for {len(slide_ids)} slides...")
    os.makedirs(dummy_data_dir, exist_ok=True)
    os.makedirs(dataset_dir, exist_ok=True)
    
    import torch
    for slide_id in slide_ids:
        features = torch.randn(10, 1024)
        torch.save(features, os.path.join(dummy_data_dir, f"{slide_id}.pt"))
        torch.save(features, os.path.join(dataset_dir, f"{slide_id}.pt"))
        
    print("Dummy feature generation completed!")

def main():
    # 1. Ensure working directory is the TOAD folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory set to: {script_dir}")
    
    # 2. Setup environment
    setup_dependencies()
    
    # 3. Create mock dataset features
    generate_dummy_data_if_needed()
    
    # 4. Run training script
    train_cmd = (
        "python main_mtl_concat.py "
        "--drop_out --early_stopping --lr 2e-4 --k 1 "
        "--exp_code dummy_mtl_sex --task dummy_mtl_concat "
        "--log_data --data_root_dir dummy_data --max_epochs 5"
    )
    run_cmd(train_cmd, "Model Training (5 epochs)")
    
    # 5. Run evaluation script
    eval_cmd = (
        "python eval_mtl_concat.py "
        "--drop_out --k 1 "
        "--models_exp_code dummy_mtl_sex_s1 --save_exp_code dummy_mtl_sex_s1_eval "
        "--task dummy_mtl_concat --results_dir results --data_root_dir dummy_data"
    )
    run_cmd(eval_cmd, "Model Evaluation")
    
    print("\n==============================================")
    print("TOAD execution finished successfully!")
    print("Checkpoints saved in: results/dummy_mtl_sex_s1/")
    print("Evaluation summary saved in: eval_results/EVAL_dummy_mtl_sex_s1_eval/summary.csv")
    print("==============================================")

if __name__ == "__main__":
    main()
