import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

class WalkingBassGenerator(nn.Module):
    def __init__(self, 
                 harmony_dim=14,      # Input features from harmony
                 hidden_dim=64,       # Size of hidden layers
                 num_layers=2):       # Number of LSTM layers
        super(WalkingBassGenerator, self).__init__()
        
        # Harmony encoder
        self.harmony_encoder = nn.Sequential(
            nn.Linear(harmony_dim, hidden_dim),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim)
        )
        
        # LSTM decoder
        self.lstm = nn.LSTM(
            input_size=hidden_dim,    # Input size matches encoder output
            hidden_size=hidden_dim,   # Hidden state size
            num_layers=num_layers,    # Number of LSTM layers
            batch_first=True,         # Batch is first dimension
            dropout=0.1               # Dropout between LSTM layers
        )
        
        # Output layers for each note feature
        self.note_decoders = nn.ModuleDict({
            'pitch_step': nn.Linear(hidden_dim, 7),     # 7 possible pitch steps
            'duration': nn.Linear(hidden_dim, 1),       # Duration value
            'octave': nn.Linear(hidden_dim, 1),         # Octave value
            'alter': nn.Linear(hidden_dim, 1)           # Alter value
        })
        
    def forward(self, harmony, lengths):
        """
        Args:
            harmony: Tensor of shape [batch_size, harmony_dim]
            lengths: Tensor of shape [batch_size] with sequence lengths
        """
        batch_size = harmony.shape[0]
        max_seq_len = lengths.max().item()
        
        # Encode harmony
        harmony_encoded = self.harmony_encoder(harmony)  # [batch_size, hidden_dim]
        
        # Repeat encoded harmony for each time step
        harmony_sequence = harmony_encoded.unsqueeze(1).repeat(1, max_seq_len, 1)
        
        # Pack sequence for LSTM (handles variable lengths efficiently)
        packed_input = pack_padded_sequence(
            harmony_sequence, 
            lengths.cpu(), 
            batch_first=True,
            enforce_sorted=False
        )
        
        # Run LSTM
        lstm_output, _ = self.lstm(packed_input)
        
        # Unpack LSTM output
        output_unpacked, _ = pad_packed_sequence(lstm_output, batch_first=True)
        
        # Generate predictions for each note feature
        predictions = {
            'pitch_step': torch.softmax(self.note_decoders['pitch_step'](output_unpacked), dim=-1),
            'duration': self.note_decoders['duration'](output_unpacked),
            'octave': self.note_decoders['octave'](output_unpacked),
            'alter': self.note_decoders['alter'](output_unpacked)
        }
        
        return predictions

# Test the model
if __name__ == "__main__":
    # Create sample batch
    batch_size = 2
    harmony_dim = 14
    max_seq_len = 3
    
    # Sample inputs
    harmony = torch.randn(batch_size, harmony_dim)
    lengths = torch.tensor([3, 2])  # Two sequences, length 3 and 2
    
    # Initialize model
    model = WalkingBassGenerator()
    
    # Get predictions
    predictions = model(harmony, lengths)
    
    # Print shapes
    print("\nModel Output Shapes:")
    for key, value in predictions.items():
        print(f"{key}: {value.shape}")
    
    # Verify predictions align with sequence lengths
    print("\nPrediction Probabilities for Pitch Steps:")
    print(predictions['pitch_step'][0, :lengths[0]])  # First sequence
    print(predictions['pitch_step'][1, :lengths[1]])  # Second sequence