import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
import json
import ast  # For safely evaluating the string representation of the list of dictionaries

harmony_csv_path = 'dataset/walking-bass-harmony-list.csv'
sequence_csv_path = 'dataset/walking-bass-sequence-list.csv'

class JazzDataset(Dataset):
    def __init__(self, harmony_csv_path, sequence_csv_path):
        # Load the data
        self.harmonies = pd.read_csv(harmony_csv_path)
        sequences_df = pd.read_csv(sequence_csv_path)
        
        # Convert sequence string to actual Python objects and create a dictionary
        # keyed by sequence ID for faster lookup
        self.sequences = {
            row['id']: ast.literal_eval(row['sequence'])
            for _, row in sequences_df.iterrows()
        }
        
        # Create mappings for categorical variables
        self.pitch_step_to_idx = {
            'C': 0, 'D': 1, 'E': 2, 'F': 3, 
            'G': 4, 'A': 5, 'B': 6
        }
        
        self.harmony_kind_to_idx = {
            'major': 0, 
            'minor': 1, 
            'dominant': 2,
            'major-seventh': 3,
            'minor-seventh': 4,
            'half-diminished': 5,
            'diminished': 6,
            'augmented': 7,
            'minor-ninth': 8,
            'major-sixth': 9,
            'dominant-ninth': 10
        }
    
    def __len__(self):
        return len(self.harmonies)
    
    def __getitem__(self, idx):
        # Get harmony features
        harmony = self.harmonies.iloc[idx]
        sequence = self.sequences[harmony['sequenceId']]
        
        # Convert harmony to feature vector
        harmony_features = [
            harmony['keyFifths'],
            harmony['beats'],
            harmony['beatsType'],
            self.pitch_step_to_idx[harmony['harmonyRootStep']],
            harmony['harmonyRootAlter'],
            harmony['divisions'],
            self.harmony_kind_to_idx[harmony['harmonyKind']],
            harmony['harmonyDuration'],
            self.pitch_step_to_idx[harmony['startPitchStep']],
            harmony['startPitchOctave'],
            harmony['startPitchAlter'],
            self.pitch_step_to_idx[harmony['targetPitchStep']],
            harmony['targetPitchOctave'],
            harmony['targetPitchAlter']
        ]
        
        # Convert sequence to feature vectors
        sequence_features = []
        for note in sequence:
            note_features = [
                int(note['duration']),
                self.pitch_step_to_idx[note['pitchStep']],
                int(note['pitchOctave']),
                int(note['pitchAlter'])
            ]
            sequence_features.append(note_features)
            
        return {
            'harmony': torch.tensor(harmony_features, dtype=torch.float32),
            'sequence': torch.tensor(sequence_features, dtype=torch.float32),
            'sequence_length': len(sequence_features)
        }

def collate_fn(batch):
    """
    Custom collate function to handle variable-length sequences:
    - Stacks harmony tensors
    - Pads sequence tensors to the longest sequence in the batch
    - Returns sequence lengths for unpacking later
    """
    # Sort batch by sequence length (descending) for packed sequence
    batch = sorted(batch, key=lambda x: x['sequence_length'], reverse=True)
    
    # Separate harmonies and sequences
    harmonies = torch.stack([item['harmony'] for item in batch])
    sequences = [item['sequence'] for item in batch]
    lengths = torch.tensor([item['sequence_length'] for item in batch])
    
    # Pad sequences to longest sequence in batch
    sequences_padded = pad_sequence(sequences, batch_first=True)
    
    return {
        'harmonies': harmonies,                    # Shape: [batch_size, harmony_features]
        'sequences': sequences_padded,             # Shape: [batch_size, max_seq_length, sequence_features]
        'lengths': lengths                         # Shape: [batch_size]
    }

# Test the batching
if __name__ == "__main__":
    # Example usage with sample data
    import tempfile
    
    # Create sample data with different sequence lengths
    harmony_data = """keyFifths,beats,beatsType,harmonyRootStep,harmonyRootAlter,divisions,harmonyKind,harmonyDuration,sequenceId,startPitchStep,startPitchOctave,startPitchAlter,targetPitchStep,targetPitchOctave,targetPitchAlter
0,4,4,D,0,1,minor-seventh,4,id1,D,3,0,G,3,0
0,4,4,G,0,1,dominant,4,id2,G,3,0,C,3,0"""

    sequence_data = """sequence,id
"[{'duration': '1', 'pitchStep': 'D', 'pitchOctave': '3', 'pitchAlter': '0'}, {'duration': '1', 'pitchStep': 'F', 'pitchOctave': '3', 'pitchAlter': '0'}]",id1
"[{'duration': '1', 'pitchStep': 'G', 'pitchOctave': '3', 'pitchAlter': '0'}, {'duration': '1', 'pitchStep': 'B', 'pitchOctave': '3', 'pitchAlter': '0'}, {'duration': '1', 'pitchStep': 'D', 'pitchOctave': '4', 'pitchAlter': '0'}]",id2"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f_harmony:
        f_harmony.write(harmony_data)
        harmony_path = f_harmony.name
        
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f_sequence:
        f_sequence.write(sequence_data)
        sequence_path = f_sequence.name
    
    # Create dataset and dataloader
    dataset = JazzDataset(harmony_path, sequence_path)
    dataloader = DataLoader(
        dataset,
        batch_size=2,
        shuffle=True,
        collate_fn=collate_fn
    )
    
    # Get a batch
    batch = next(iter(dataloader))
    print("Harmonies shape:", batch['harmonies'].shape)
    print("Sequences shape:", batch['sequences'].shape)
    print("Sequence lengths:", batch['lengths'])