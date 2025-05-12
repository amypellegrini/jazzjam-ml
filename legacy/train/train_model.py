import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import numpy as np

def train_model(model, train_loader, num_epochs=50, learning_rate=0.001, device='cuda' if torch.cuda.is_available() else 'cpu'):
    """
    Training loop for the walking bass generator
    """
    model = model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Loss functions
    pitch_criterion = nn.CrossEntropyLoss()  # For pitch steps (categorical)
    regression_criterion = nn.MSELoss()      # For duration, octave, alter (continuous)
    
    # Training loop
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        num_batches = 0
        
        for batch in train_loader:
            # Move batch to device
            harmonies = batch['harmonies'].to(device)
            sequences = batch['sequences'].to(device)
            lengths = batch['lengths']
            
            # Zero gradients
            optimizer.zero_grad()
            
            # Get model predictions
            predictions = model(harmonies, lengths)
            
            # Calculate losses for each feature
            loss = 0.0
            
            # Pitch step loss (categorical)
            pitch_steps_target = sequences[:, :, 1].long()  # Index 1 is pitch step
            loss += pitch_criterion(
                predictions['pitch_step'].view(-1, 7),  # Reshape to [batch_size * seq_len, num_pitches]
                pitch_steps_target.view(-1)             # Reshape to [batch_size * seq_len]
            )
            
            # Duration loss
            duration_target = sequences[:, :, 0]  # Index 0 is duration
            loss += regression_criterion(
                predictions['duration'].squeeze(-1),
                duration_target
            )
            
            # Octave loss
            octave_target = sequences[:, :, 2]  # Index 2 is octave
            loss += regression_criterion(
                predictions['octave'].squeeze(-1),
                octave_target
            )
            
            # Alter loss
            alter_target = sequences[:, :, 3]  # Index 3 is alter
            loss += regression_criterion(
                predictions['alter'].squeeze(-1),
                alter_target
            )
            
            # Backward pass and optimization
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
        
        # Print epoch statistics
        avg_loss = total_loss / num_batches
        print(f'Epoch {epoch+1}/{num_epochs}, Average Loss: {avg_loss:.4f}')
        
        # Optional: Evaluate on a validation set here
        if (epoch + 1) % 5 == 0:
            evaluate_model(model, batch, device)  # Using last batch for quick evaluation

def evaluate_model(model, batch, device):
    """
    Evaluate model predictions showing input harmony and all note features
    """
    model.eval()
    with torch.no_grad():
        harmonies = batch['harmonies'].to(device)
        sequences = batch['sequences'].to(device)
        lengths = batch['lengths']
        
        predictions = model(harmonies, lengths)
        
        # Get harmony features for first sequence
        harmony = harmonies[0]  # Shape: [harmony_features]
        
        # Create reverse mappings
        pitch_idx_to_note = {0: 'C', 1: 'D', 2: 'E', 3: 'F', 4: 'G', 5: 'A', 6: 'B'}
        harmony_idx_to_kind = {
            0: 'major', 1: 'minor', 2: 'dominant', 3: 'major-seventh',
            4: 'minor-seventh', 5: 'half-diminished', 6: 'diminished',
            7: 'augmented', 8: 'minor-ninth', 9: 'major-sixth',
            10: 'dominant-ninth'
        }
        
        # Decode harmony
        harmony_root = pitch_idx_to_note[int(harmony[3].item())]  # harmonyRootStep
        harmony_root_alter = harmony[4].item()  # harmonyRootAlter
        harmony_kind = harmony_idx_to_kind[int(harmony[6].item())]  # harmonyKind
        
        print("\nInput Harmony:")
        print(f"Key signature (fifths): {harmony[0].item()}")
        print(f"Time signature: {int(harmony[1].item())}/{int(harmony[2].item())}")
        print(f"Harmony root: {harmony_root} (alter: {harmony_root_alter})")
        print(f"Harmony kind: {harmony_kind}")
        print(f"Harmony duration: {harmony[7].item()}")
        print(f"Start pitch: {pitch_idx_to_note[int(harmony[8].item())]} octave {int(harmony[9].item())} (alter: {harmony[10].item()})")
        print(f"Target pitch: {pitch_idx_to_note[int(harmony[11].item())]} octave {int(harmony[12].item())} (alter: {harmony[13].item()})")
        
        # Get predictions for first sequence
        pitch_probs = predictions['pitch_step'][0, :lengths[0]]
        predicted_pitches = torch.argmax(pitch_probs, dim=-1)
        predicted_durations = predictions['duration'][0, :lengths[0]].squeeze(-1)
        predicted_octaves = predictions['octave'][0, :lengths[0]].squeeze(-1)
        predicted_alters = predictions['alter'][0, :lengths[0]].squeeze(-1)
        
        # Get actual values for first sequence
        actual_pitches = sequences[0, :lengths[0], 1]
        actual_durations = sequences[0, :lengths[0], 0]
        actual_octaves = sequences[0, :lengths[0], 2]
        actual_alters = sequences[0, :lengths[0], 3]
        
        print("\nPredicted notes:")
        for i in range(len(predicted_pitches)):
            note_name = pitch_idx_to_note[predicted_pitches[i].item()]
            print(f"Note {i+1}: {note_name}, Octave: {predicted_octaves[i]:.1f}, "
                  f"Duration: {predicted_durations[i]:.1f}, Alter: {predicted_alters[i]:.1f}")
        
        print("\nActual notes:")
        for i in range(len(actual_pitches)):
            note_name = pitch_idx_to_note[int(actual_pitches[i].item())]
            print(f"Note {i+1}: {note_name}, Octave: {actual_octaves[i]:.1f}, "
                  f"Duration: {actual_durations[i]:.1f}, Alter: {actual_alters[i]:.1f}")

# Example usage
if __name__ == "__main__":
    # Assuming you have your dataset and model from previous code
    from jazz_dataset import JazzDataset, collate_fn  # Import your dataset class
    from walking_bass_generator import WalkingBassGenerator      # Import your model class
    
    harmony_csv_path = 'dataset/walking-bass-harmony-list.csv'
    sequence_csv_path = 'dataset/walking-bass-sequence-list.csv'


    # Create dataset and dataloader
    dataset = JazzDataset(harmony_csv_path, sequence_csv_path)
    train_loader = DataLoader(
        dataset,
        batch_size=32,
        shuffle=True,
        collate_fn=collate_fn
    )
    
    # Create model
    model = WalkingBassGenerator()
    
    # Train model
    train_model(model, train_loader)