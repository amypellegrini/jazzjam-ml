from parseMusicXMLFile import parseMusicXMLFile
import pandas as pd

paths = [
  'dataset/target-note/bass/2_5_1_progression.musicxml',
  'dataset/target-note/bass/2_5_1_tritone_substitution.musicxml',
  'dataset/target-note/bass/2_5_1_6_progression.musicxml',
  'dataset/target-note/bass/2_5_1_progression_2.musicxml',
  'dataset/target-note/bass/2_5_1_6_half_note_value_chords.musicxml',
  'dataset/target-note/bass/Diatonic_chords_asc.musicxml',
  'dataset/target-note/bass/Diatonic_chords_asc_69.musicxml',
  'dataset/target-note/bass/Repeated_dominants.musicxml',
  'dataset/target-note/bass/Blues_fragments.musicxml'
]

finalResult = {
  'bassHarmonyDF': pd.DataFrame({
    'keyFifths': [],
    'beats': [],
    'beatsType': [],
    'harmonyRootStep': [],
    'harmonyRootAlter': [],
  }),
  'bassSequencesDF': pd.DataFrame({})
}

for path in paths:
    result = parseMusicXMLFile(path)
    finalResult['bassHarmonyDF'] = pd.concat([finalResult['bassHarmonyDF'], result['bassHarmonyDF']])
    finalResult['bassSequencesDF'] = pd.concat([finalResult['bassSequencesDF'], result['bassSequencesDF']])

finalResult.get('bassHarmonyDF').to_csv('dataset/walking-bass-harmony-list.csv', index=False)
finalResult.get('bassSequencesDF').to_csv('dataset/walking-bass-sequence-list.csv', index=False)
