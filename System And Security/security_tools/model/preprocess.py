"""
Data Preprocessing Module for Zero-Day Ransomware Detection
Handles loading RISS dataset, feature selection, and data preparation
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, chi2
import joblib

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    RAW_DATA_DIR, PROCESSED_DATA_DIR, N_FEATURES,
    FEATURE_SCALER_PATH, FEATURE_SELECTOR_PATH, SELECTED_FEATURES_PATH,
    TRAIN_FAMILIES, TEST_FAMILIES, FAMILY_NAMES
)


class DataPreprocessor:
    """Preprocessor for the RISS ransomware dataset."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.selector = None
        self.selected_feature_names = None
        self.n_features = N_FEATURES
        
    def load_dataset(self, data_path=None):
        """
        Load the RISS dataset from CSV file.
        
        The RISS dataset format:
        - Column 0: Sample ID
        - Column 1: Family ID (0=Goodware, 1-11=Ransomware families)
        - Column 2+: Behavioral features
        
        Returns:
            X: Feature matrix
            y: Binary labels (0=Benign, 1=Ransomware)
            family_ids: Original family IDs for zero-day splitting
        """
        print("[INFO] Loading RISS dataset...")
        
        # Find the data file
        if data_path is None:
            possible_paths = [
                os.path.join(RAW_DATA_DIR, "RansomwareData.csv"),
                os.path.join(RAW_DATA_DIR, "ransomwaredata.csv"),
            ]
            for root, dirs, files in os.walk(RAW_DATA_DIR):
                for f in files:
                    if f.lower().endswith('.csv'):
                        possible_paths.append(os.path.join(root, f))
            
            data_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    data_path = path
                    break
                    
            if data_path is None:
                raise FileNotFoundError(
                    f"Dataset not found. Please run data/download_data.py first."
                )
        
        print(f"[INFO] Loading from: {data_path}")
        
        # Load the CSV file WITHOUT header (RISS dataset has no header row)
        df = pd.read_csv(data_path, header=None)
        print(f"[INFO] Dataset shape: {df.shape}")
        print(f"[INFO] Columns: {len(df.columns)}")
        
        # RISS Dataset structure:
        # Column 0: Sample ID (we'll ignore this)
        # Column 1: Family ID (0=Goodware, 1-11=Ransomware)
        # Columns 2+: Features
        
        # Extract family IDs from column 1
        family_ids = df.iloc[:, 1].values.astype(int)
        
        # Create binary labels: 0=Goodware (family 0), 1=Ransomware (family 1-11)
        y = (family_ids > 0).astype(int)
        
        # Extract features (all columns from index 2 onwards)
        X = df.iloc[:, 2:].values.astype(float)
        
        # Create feature names
        feature_cols = [f"feature_{i}" for i in range(X.shape[1])]
        
        # Handle any non-numeric values
        X = np.nan_to_num(X, nan=0, posinf=0, neginf=0)
        
        print(f"\n[INFO] Dataset Statistics:")
        print(f"       Total samples: {len(y)}")
        print(f"       Benign samples (Goodware): {np.sum(y == 0)}")
        print(f"       Ransomware samples: {np.sum(y == 1)}")
        print(f"       Feature dimensions: {X.shape[1]}")
        
        # Print family distribution
        print(f"\n[INFO] Family Distribution:")
        unique_families = np.unique(family_ids)
        for fam_id in sorted(unique_families):
            count = np.sum(family_ids == fam_id)
            name = FAMILY_NAMES.get(int(fam_id), f"Unknown-{fam_id}")
            print(f"       {name}: {count} samples")
        
        return X, y, family_ids, feature_cols
    
    def select_features(self, X, y, feature_names=None):
        """
        Select top-K features using chi-squared test.
        Following Cui et al. paper methodology.
        """
        print(f"\n[INFO] Performing feature selection (top {self.n_features} features)...")
        
        # Ensure non-negative values for chi-squared test
        X_positive = X - X.min(axis=0)
        
        # Apply SelectKBest with chi-squared
        self.selector = SelectKBest(chi2, k=min(self.n_features, X.shape[1]))
        X_selected = self.selector.fit_transform(X_positive, y)
        
        # Get selected feature indices
        selected_indices = self.selector.get_support(indices=True)
        
        if feature_names is not None:
            self.selected_feature_names = [feature_names[i] for i in selected_indices]
            print(f"[INFO] Selected features: {self.selected_feature_names[:10]}...")
        else:
            self.selected_feature_names = [f"feature_{i}" for i in selected_indices]
        
        # Get feature scores
        scores = self.selector.scores_
        top_scores = sorted(zip(range(len(scores)), scores), key=lambda x: x[1], reverse=True)[:10]
        
        print(f"\n[INFO] Top 10 Feature Scores:")
        for idx, score in top_scores:
            name = feature_names[idx] if feature_names else f"feature_{idx}"
            print(f"       {name}: {score:.2f}")
        
        print(f"\n[INFO] Selected features shape: {X_selected.shape}")
        
        return X_selected
    
    def normalize_features(self, X_train, X_test=None):
        """Normalize features using StandardScaler."""
        print("\n[INFO] Normalizing features...")
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled
    
    def zero_day_split(self, X, y, family_ids):
        """
        Split data for zero-day evaluation.
        Training: Goodware + known ransomware families
        Testing: Goodware + unseen ransomware families
        """
        print("\n[INFO] Performing zero-day data split...")
        print(f"       Training families: {[FAMILY_NAMES.get(f, f) for f in TRAIN_FAMILIES]}")
        print(f"       Test families (Zero-day): {[FAMILY_NAMES.get(f, f) for f in TEST_FAMILIES]}")
        
        # Get indices for training and testing
        train_mask = np.isin(family_ids, [0] + TRAIN_FAMILIES)  # Goodware + training families
        test_mask = np.isin(family_ids, [0] + TEST_FAMILIES)    # Goodware + test families
        
        # For goodware (family 0), split between train and test
        goodware_mask = family_ids == 0
        goodware_indices = np.where(goodware_mask)[0]
        
        np.random.seed(42)
        np.random.shuffle(goodware_indices)
        
        n_goodware = len(goodware_indices)
        n_train_goodware = int(0.8 * n_goodware)
        
        train_goodware_idx = goodware_indices[:n_train_goodware]
        test_goodware_idx = goodware_indices[n_train_goodware:]
        
        # Get ransomware indices for train/test
        train_ransomware_mask = np.isin(family_ids, TRAIN_FAMILIES)
        test_ransomware_mask = np.isin(family_ids, TEST_FAMILIES)
        
        # Combine indices
        train_indices = np.concatenate([
            train_goodware_idx,
            np.where(train_ransomware_mask)[0]
        ])
        
        test_indices = np.concatenate([
            test_goodware_idx,
            np.where(test_ransomware_mask)[0]
        ])
        
        # Extract data
        X_train = X[train_indices]
        y_train = y[train_indices]
        X_test = X[test_indices]
        y_test = y[test_indices]
        
        print(f"\n[INFO] Training set: {len(y_train)} samples")
        print(f"       - Benign: {np.sum(y_train == 0)}")
        print(f"       - Ransomware: {np.sum(y_train == 1)}")
        
        print(f"\n[INFO] Test set (Zero-day): {len(y_test)} samples")
        print(f"       - Benign: {np.sum(y_test == 0)}")
        print(f"       - Ransomware: {np.sum(y_test == 1)}")
        
        return X_train, X_test, y_train, y_test
    
    def save_preprocessors(self):
        """Save the fitted scaler and selector for inference."""
        os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
        
        print("\n[INFO] Saving preprocessors...")
        joblib.dump(self.scaler, FEATURE_SCALER_PATH)
        print(f"       Scaler saved to: {FEATURE_SCALER_PATH}")
        
        if self.selector is not None:
            joblib.dump(self.selector, FEATURE_SELECTOR_PATH)
            print(f"       Selector saved to: {FEATURE_SELECTOR_PATH}")
        
        if self.selected_feature_names is not None:
            joblib.dump(self.selected_feature_names, SELECTED_FEATURES_PATH)
            print(f"       Feature names saved to: {SELECTED_FEATURES_PATH}")
    
    def load_preprocessors(self):
        """Load previously saved scaler and selector."""
        print("\n[INFO] Loading preprocessors...")
        
        if os.path.exists(FEATURE_SCALER_PATH):
            self.scaler = joblib.load(FEATURE_SCALER_PATH)
            print(f"       Scaler loaded from: {FEATURE_SCALER_PATH}")
        
        if os.path.exists(FEATURE_SELECTOR_PATH):
            self.selector = joblib.load(FEATURE_SELECTOR_PATH)
            print(f"       Selector loaded from: {FEATURE_SELECTOR_PATH}")
        
        if os.path.exists(SELECTED_FEATURES_PATH):
            self.selected_feature_names = joblib.load(SELECTED_FEATURES_PATH)
            print(f"       Feature names loaded from: {SELECTED_FEATURES_PATH}")
    
    def preprocess_for_training(self, data_path=None):
        """
        Complete preprocessing pipeline for training.
        
        Returns:
            X_train, X_test, y_train, y_test: Preprocessed data splits
        """
        print("=" * 60)
        print("Data Preprocessing Pipeline")
        print("=" * 60)
        
        # Load dataset
        X, y, family_ids, feature_names = self.load_dataset(data_path)
        
        # Feature selection
        X_selected = self.select_features(X, y, feature_names)
        
        # Zero-day split
        X_train, X_test, y_train, y_test = self.zero_day_split(
            X_selected, y, family_ids
        )
        
        # Normalize
        X_train, X_test = self.normalize_features(X_train, X_test)
        
        # Save preprocessors
        self.save_preprocessors()
        
        # Reshape for CNN (add channel dimension)
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
        
        print("\n" + "=" * 60)
        print("Preprocessing Complete!")
        print(f"Training data shape: {X_train.shape}")
        print(f"Test data shape: {X_test.shape}")
        print("=" * 60)
        
        return X_train, X_test, y_train, y_test
    
    def transform_for_inference(self, features):
        """
        Transform features for real-time inference.
        
        Args:
            features: Raw feature vector or array
            
        Returns:
            Transformed features ready for model prediction
        """
        # Load preprocessors if not loaded
        if self.selector is None or self.scaler is None:
            self.load_preprocessors()
        
        features = np.array(features).reshape(1, -1)
        
        # Ensure non-negative for chi-squared (apply same shift as training)
        features = features - features.min()
        
        # Apply feature selection
        if self.selector is not None:
            features = self.selector.transform(features)
        
        # Apply scaling
        features = self.scaler.transform(features)
        
        # Reshape for CNN
        features = features.reshape(1, features.shape[1], 1)
        
        return features


def main():
    """Run the preprocessing pipeline."""
    preprocessor = DataPreprocessor()
    
    try:
        X_train, X_test, y_train, y_test = preprocessor.preprocess_for_training()
        
        # Save processed data
        np.savez(
            os.path.join(PROCESSED_DATA_DIR, "processed_data.npz"),
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test
        )
        print(f"\n[INFO] Processed data saved to: {PROCESSED_DATA_DIR}/processed_data.npz")
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("[INFO] Please run data/download_data.py first to download the dataset.")
        sys.exit(1)


if __name__ == "__main__":
    main()
