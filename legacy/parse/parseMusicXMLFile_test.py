from parseMusicXMLFile import parseMusicXMLFile

def test_matches_chords_with_sequences(snapshot):
    output = parseMusicXMLFile('__tests__/fixtures/2_5_1_progression.musicxml')
    outputHarmonyListString = output.get('bassHarmonyDF').drop('sequenceId', axis=1).to_string()
    outputSequencesListString = output.get('bassSequencesDF').drop('id', axis=1).to_string()
    
    snapshot.assert_match(outputHarmonyListString, '2_5_1_progression_harmony_list.txt')
    snapshot.assert_match(outputSequencesListString, '2_5_1_progression_sequences_list.txt')

def test_handles_key_change(snapshot):
    output = parseMusicXMLFile('__tests__/fixtures/key_change.musicxml')
    outputHarmonyListString = output.get('bassHarmonyDF').drop('sequenceId', axis=1).to_string()
    
    snapshot.assert_match(outputHarmonyListString, 'key_change.txt')

def test_handles_empty_chords(snapshot):
    output = parseMusicXMLFile('__tests__/fixtures/empty_chord_symbol.musicxml')
    outputHarmonyListString = output.get('bassHarmonyDF').drop('sequenceId', axis=1).to_string()
    
    snapshot.assert_match(outputHarmonyListString, 'empty_chord_symbol.txt')

def test_handles_eight_note_durations(snapshot):
    output = parseMusicXMLFile('__tests__/fixtures/quarter_eight_durations.musicxml')
    outputHarmonyListString = output.get('bassHarmonyDF').drop('sequenceId', axis=1).to_string()
    outputSequencesListString = output.get('bassSequencesDF').drop('id', axis=1).to_string()
    
    snapshot.assert_match(outputHarmonyListString, 'harmony_quarter_eigth_durations.txt')
    snapshot.assert_match(outputSequencesListString, 'sequences_quarter_eigth_durations.txt')

def test_handles_half_note_chord_durations(snapshot):
    output = parseMusicXMLFile('__tests__/fixtures/half_note_chords.musicxml')
    outputHarmonyListString = output.get('bassHarmonyDF').drop('sequenceId', axis=1).to_string()
    outputSequencesListString = output.get('bassSequencesDF').drop('id', axis=1).to_string()
    
    snapshot.assert_match(outputHarmonyListString, 'harmony_half_note_chord_durations.txt')
    snapshot.assert_match(outputSequencesListString, 'sequences_half_note_chord_durations.txt')
