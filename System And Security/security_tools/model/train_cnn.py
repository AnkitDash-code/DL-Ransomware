"""
1D-CNN Model Training for Zero-Day Ransomware Detection
Based on the CVAE + 1D-CNN approach from Cui et al. (simplified)
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    roc_curve, auc, precision_recall_curve
)

# TensorFlow imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF warnings
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import (
    Conv1D, MaxPooling1D, Flatten, Dense, Dropout, 
    BatchNormalization, Input
)
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    MODEL_PATH, PROCESSED_DATA_DIR, N_FEATURES,
    EPOCHS, BATCH_SIZE, EARLY_STOPPING_PATIENCE, VALIDATION_SPLIT
)
from model.preprocess import DataPreprocessor


class RansomwareCNN:
    """1D-CNN model for ransomware detection."""
    
    def __init__(self, input_shape=None):
        self.model = None
        self.history = None
        self.input_shape = input_shape or (N_FEATURES, 1)
        
    def build_model(self):
        """
        Build the 1D-CNN architecture.
        Architecture follows the approach from the CVAE+1D-CNN paper.
        """
        print("\n[INFO] Building 1D-CNN model...")
        
        n_features = self.input_shape[0]
        
        model = Sequential([
            # Input layer
            Input(shape=self.input_shape),
            
            # First Conv Block
            Conv1D(filters=64, kernel_size=3, activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling1D(pool_size=2),
            
            # Second Conv Block
            Conv1D(filters=128, kernel_size=3, activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling1D(pool_size=2),
            
            # Third Conv Block
            Conv1D(filters=256, kernel_size=3, activation='relu', padding='same'),
            BatchNormalization(),
            
            # Flatten and Dense layers
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(64, activation='relu'),
            Dropout(0.3),
            
            # Output layer
            Dense(1, activation='sigmoid')
        ])
        
        # Compile the model
        optimizer = Adam(learning_rate=0.001)
        model.compile(
            loss='binary_crossentropy',
            optimizer=optimizer,
            metrics=['accuracy', 
                     tf.keras.metrics.Precision(name='precision'),
                     tf.keras.metrics.Recall(name='recall'),
                     tf.keras.metrics.AUC(name='auc')]
        )
        
        self.model = model
        print("\n[INFO] Model Architecture:")
        model.summary()
        
        return model
    
    def get_callbacks(self):
        """Get training callbacks."""
        callbacks = [
            # Early stopping to prevent overfitting
            EarlyStopping(
                monitor='val_loss',
                patience=EARLY_STOPPING_PATIENCE,
                restore_best_weights=True,
                verbose=1
            ),
            # Save best model
            ModelCheckpoint(
                MODEL_PATH,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            # Reduce learning rate on plateau
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-6,
                verbose=1
            )
        ]
        return callbacks
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Train the model.
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
        """
        if self.model is None:
            self.build_model()
        
        print("\n" + "=" * 60)
        print("Training 1D-CNN Ransomware Detector")
        print("=" * 60)
        print(f"Training samples: {len(X_train)}")
        print(f"Epochs: {EPOCHS}")
        print(f"Batch size: {BATCH_SIZE}")
        print(f"Early stopping patience: {EARLY_STOPPING_PATIENCE}")
        
        # Prepare validation data
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
            print(f"Validation samples: {len(X_val)}")
        else:
            validation_data = None
            print(f"Validation split: {VALIDATION_SPLIT}")
        
        print("\n[INFO] Starting training...")
        
        # Train the model
        self.history = self.model.fit(
            X_train, y_train,
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            validation_split=VALIDATION_SPLIT if validation_data is None else 0,
            validation_data=validation_data,
            callbacks=self.get_callbacks(),
            verbose=1
        )
        
        print("\n[INFO] Training complete!")
        return self.history
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on test data.
        
        Returns:
            Dictionary with evaluation metrics
        """
        print("\n" + "=" * 60)
        print("Evaluating on Zero-Day Test Set")
        print("=" * 60)
        
        # Get predictions
        y_pred_proba = self.model.predict(X_test, verbose=0).flatten()
        y_pred = (y_pred_proba >= 0.5).astype(int)
        
        # Calculate metrics using sklearn for reliability
        from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        try:
            auc_score = roc_auc_score(y_test, y_pred_proba)
        except:
            auc_score = 0.0
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'auc': auc_score,
            'loss': 0.0
        }
        
        print("\n[RESULTS] Model Performance:")
        print(f"          Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        print(f"          Precision: {metrics['precision']:.4f}")
        print(f"          Recall: {metrics['recall']:.4f}")
        print(f"          AUC: {metrics['auc']:.4f}")
        
        # Classification report
        print("\n[INFO] Classification Report:")
        print(classification_report(y_test, y_pred, 
                                    target_names=['Benign', 'Ransomware']))
        
        # Store for visualization
        self.y_test = y_test
        self.y_pred = y_pred
        self.y_pred_proba = y_pred_proba
        
        return metrics
    
    def plot_training_history(self, save_path=None):
        """Plot training history."""
        if self.history is None:
            print("[WARNING] No training history available.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Accuracy
        axes[0, 0].plot(self.history.history['accuracy'], label='Train')
        axes[0, 0].plot(self.history.history['val_accuracy'], label='Validation')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        axes[0, 1].plot(self.history.history['loss'], label='Train')
        axes[0, 1].plot(self.history.history['val_loss'], label='Validation')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Precision
        axes[1, 0].plot(self.history.history['precision'], label='Train')
        axes[1, 0].plot(self.history.history['val_precision'], label='Validation')
        axes[1, 0].set_title('Model Precision')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Recall
        axes[1, 1].plot(self.history.history['recall'], label='Train')
        axes[1, 1].plot(self.history.history['val_recall'], label='Validation')
        axes[1, 1].set_title('Model Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"[INFO] Training history plot saved to: {save_path}")
        
        plt.show()
    
    def plot_confusion_matrix(self, save_path=None):
        """Plot confusion matrix."""
        if not hasattr(self, 'y_test'):
            print("[WARNING] Run evaluate() first.")
            return
        
        cm = confusion_matrix(self.y_test, self.y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Benign', 'Ransomware'],
                    yticklabels=['Benign', 'Ransomware'])
        plt.title('Confusion Matrix - Zero-Day Ransomware Detection')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"[INFO] Confusion matrix saved to: {save_path}")
        
        plt.show()
    
    def plot_roc_curve(self, save_path=None):
        """Plot ROC curve."""
        if not hasattr(self, 'y_pred_proba'):
            print("[WARNING] Run evaluate() first.")
            return
        
        fpr, tpr, _ = roc_curve(self.y_test, self.y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                 label=f'ROC curve (AUC = {roc_auc:.4f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve - Zero-Day Ransomware Detection')
        plt.legend(loc='lower right')
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"[INFO] ROC curve saved to: {save_path}")
        
        plt.show()
    
    def save_model(self, path=None):
        """Save the trained model."""
        save_path = path or MODEL_PATH
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        self.model.save(save_path)
        print(f"[INFO] Model saved to: {save_path}")
    
    def load_model(self, path=None):
        """Load a trained model."""
        load_path = path or MODEL_PATH
        if os.path.exists(load_path):
            self.model = load_model(load_path)
            print(f"[INFO] Model loaded from: {load_path}")
            return True
        else:
            print(f"[ERROR] Model not found at: {load_path}")
            return False
    
    def predict(self, X):
        """
        Make predictions on new data.
        
        Args:
            X: Feature array (already preprocessed)
            
        Returns:
            Probability of ransomware (0 to 1)
        """
        if self.model is None:
            self.load_model()
        
        if self.model is None:
            raise ValueError("Model not loaded. Train or load a model first.")
        
        # Ensure correct shape
        if len(X.shape) == 2:
            X = X.reshape(X.shape[0], X.shape[1], 1)
        elif len(X.shape) == 1:
            X = X.reshape(1, X.shape[0], 1)
        
        return self.model.predict(X, verbose=0).flatten()


def main():
    """Main training pipeline."""
    print("=" * 60)
    print("Zero-Day Ransomware Detection - Model Training")
    print("=" * 60)
    
    # Load preprocessed data or preprocess from scratch
    processed_data_path = os.path.join(PROCESSED_DATA_DIR, "processed_data.npz")
    
    if os.path.exists(processed_data_path):
        print("\n[INFO] Loading preprocessed data...")
        data = np.load(processed_data_path)
        X_train = data['X_train']
        X_test = data['X_test']
        y_train = data['y_train']
        y_test = data['y_test']
    else:
        print("\n[INFO] No preprocessed data found. Running preprocessing...")
        preprocessor = DataPreprocessor()
        X_train, X_test, y_train, y_test = preprocessor.preprocess_for_training()
    
    print(f"\n[INFO] Data shapes:")
    print(f"       X_train: {X_train.shape}")
    print(f"       X_test: {X_test.shape}")
    print(f"       y_train: {y_train.shape}")
    print(f"       y_test: {y_test.shape}")
    
    # Initialize and build model
    input_shape = (X_train.shape[1], 1)
    model = RansomwareCNN(input_shape=input_shape)
    model.build_model()
    
    # Train model
    model.train(X_train, y_train)
    
    # Evaluate on zero-day test set
    metrics = model.evaluate(X_test, y_test)
    
    # Save the model
    model.save_model()
    
    # Plot results
    print("\n[INFO] Generating visualizations...")
    
    plot_dir = os.path.join(PROCESSED_DATA_DIR, "plots")
    os.makedirs(plot_dir, exist_ok=True)
    
    model.plot_training_history(os.path.join(plot_dir, "training_history.png"))
    model.plot_confusion_matrix(os.path.join(plot_dir, "confusion_matrix.png"))
    model.plot_roc_curve(os.path.join(plot_dir, "roc_curve.png"))
    
    print("\n" + "=" * 60)
    print("Training Pipeline Complete!")
    print("=" * 60)
    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Plots saved to: {plot_dir}")
    print(f"\nFinal Zero-Day Detection Accuracy: {metrics['accuracy']*100:.2f}%")
    
    return model, metrics


if __name__ == "__main__":
    model, metrics = main()
