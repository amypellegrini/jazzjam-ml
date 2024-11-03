import xml.etree.ElementTree as ET
import pandas as pd
import uuid

def parseMusicXMLFile(filePath):
  bassHarmonyDF = pd.DataFrame({
    'keyFifths': [],
    'beats': [],
    'beatsType': [],
    'divisions': [],
    'harmonyRootStep': [],
    'harmonyRootAlter': [],
  })

  bassSequencesDF = pd.DataFrame({})
  bassPart = None

  # Parse the MusicXML file
  tree = ET.parse(filePath)
  root = tree.getroot()
  partList = root.find('part-list')

  # Find the bass part
  for part in partList:
    bassPartId = None
      
    if part.find('part-name').text == 'Acoustic Bass':
      bassPartId = part.attrib['id']
      
    for element in root.iter('part'):
      if element.attrib['id'] == bassPartId:
        bassPart = element

  flatPart = []

  # Flatten the part to remove the measures
  for measure in bassPart.findall('measure'):
    for child in measure:
      flatPart.append(child)

  attributes = flatPart[0]

  key = attributes.find('key')
  time = attributes.find('time')
  beats = time.find('beats').text
  beatsType = time.find('beat-type').text
  keyFifths = key.find('fifths').text
  divisions = int(attributes.find('divisions').text)
  measureDuration = int(beats) * divisions

  previousDFHarmony = None
  currentDFHarmony = None
  currentDFSequence = None
  currentSequenceList = None

  counter = 0

  for element in flatPart:
    counter += 1

    if element.tag == 'attributes':
      key = element.find('key')
      keyFifths = key.find('fifths').text

    if element.tag == 'harmony':
      if currentDFHarmony is not None and currentDFHarmony.get('harmonyDuration') != '0':
        currentDFSequence['sequence'] = currentSequenceList
        currentDFSequence['id'] = currentDFHarmony.get('sequenceId')

        bassSequencesDF = pd.concat([bassSequencesDF, pd.DataFrame([currentDFSequence])], ignore_index=True)
        previousDFHarmony = currentDFHarmony

      root = element.find('root')
      rootStep = root.find('root-step').text
      rootAlter = root.find('root-alter')
      kind = element.find('kind').text

      if rootAlter is not None:
        rootAlter = rootAlter.text
      else:
        rootAlter = "0"

      currentDFHarmony = {}
      currentDFSequence = {}
      currentSequenceList = []

      currentDFHarmony['harmonyRootStep'] = rootStep
      currentDFHarmony['keyFifths'] = keyFifths
      currentDFHarmony['beats'] = beats
      currentDFHarmony['beatsType'] = beatsType
      currentDFHarmony['harmonyRootAlter'] = rootAlter
      currentDFHarmony['harmonyKind'] = kind
      currentDFHarmony['divisions'] = str(int(divisions))
      currentDFHarmony['harmonyDuration'] = '0'
      currentDFHarmony['sequenceId'] = uuid.uuid4()

    if element.tag == 'note':
      noteDuration = int(element.find('duration').text)

      accumulatedDuration = int(currentDFHarmony.get('harmonyDuration'))
      accumulatedDuration += noteDuration

      currentDFHarmony['harmonyDuration'] = str(int(accumulatedDuration))

      pitchStep = element.find('pitch').find('step').text
      pitchOctave = element.find('pitch').find('octave').text
      pitchAlter = element.find('pitch').find('alter')

      if pitchAlter is not None:
        pitchAlter = pitchAlter.text
      else:
        pitchAlter = "0"

      serializedNote = {}
      serializedNote['duration'] = str(int(noteDuration))
      serializedNote['pitchStep'] = pitchStep
      serializedNote['pitchOctave'] = pitchOctave
      serializedNote['pitchAlter'] = pitchAlter

      if len(currentSequenceList) == 0:
        currentDFHarmony['startPitchStep'] = pitchStep
        currentDFHarmony['startPitchOctave'] = pitchOctave
        currentDFHarmony['startPitchAlter'] = pitchAlter

        if previousDFHarmony is not None:
          previousDFHarmony['targetPitchStep'] = pitchStep
          previousDFHarmony['targetPitchOctave'] = pitchOctave
          previousDFHarmony['targetPitchAlter'] = pitchAlter

          bassHarmonyDF = pd.concat([bassHarmonyDF, pd.DataFrame([previousDFHarmony])], ignore_index=True)
        
      currentSequenceList.append(serializedNote)

    barLine = flatPart[counter].find('bar-style') if counter < len(flatPart) else None
    barStyle = barLine.text if barLine is not None else None
    lastMeasure = barStyle == 'light-heavy' if barStyle is not None else False

    if lastMeasure:
      break

    if currentDFHarmony is not None and currentDFHarmony.get('harmonyDuration') == str(measureDuration):
      currentDFSequence['sequence'] = currentSequenceList
      currentDFSequence['id'] = currentDFHarmony.get('sequenceId')

      bassSequencesDF = pd.concat([bassSequencesDF, pd.DataFrame([currentDFSequence])], ignore_index=True)
      previousDFHarmony = currentDFHarmony

      currentDFHarmony = {}
      currentDFSequence = {}
      currentSequenceList = []

      currentDFHarmony['harmonyRootStep'] = rootStep
      currentDFHarmony['keyFifths'] = keyFifths
      currentDFHarmony['beats'] = beats
      currentDFHarmony['beatsType'] = beatsType
      currentDFHarmony['harmonyRootAlter'] = rootAlter
      currentDFHarmony['harmonyKind'] = kind
      currentDFHarmony['divisions'] = str(int(divisions))
      currentDFHarmony['harmonyDuration'] = '0'
      currentDFHarmony['sequenceId'] = uuid.uuid4()

  result = {
    'bassHarmonyDF': bassHarmonyDF,
    'bassSequencesDF': bassSequencesDF
  }

  return result
