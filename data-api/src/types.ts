export type Style = "swing" | "bossa-nova";

export type Step = "C" | "D" | "E" | "F" | "G" | "A" | "B";

export type StepAlter = -2 | -1 | 0 | 1 | 2;

export type HarmonyKind =
  | "augmented"
  | "augmented-seventh"
  | "diminished"
  | "diminished-seventh"
  | "dominant"
  | "dominant-11th"
  | "dominant-13th"
  | "dominant-ninth"
  | "half-diminished"
  | "major"
  | "major-11th"
  | "major-13th"
  | "major-minor"
  | "major-ninth"
  | "major-seventh"
  | "major-sixth"
  | "minor"
  | "minor-11th"
  | "minor-13th"
  | "minor-ninth"
  | "minor-seventh"
  | "minor-sixth"
  | "none"
  | "suspended-fourth"
  | "suspended-second";

export type HarmonyRootAlter = -1 | 0 | 1;

export type PitchOctave = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;

export interface BaseHarmony {
  keyFifths: number;
  beats: number;
  beatsType: number;
  harmonyRootStep: string;
  harmonyRootAlter: number;
  divisions: number;
  harmonyKind: HarmonyKind;
  harmonyDuration: number;
  bassStep: Step | undefined;
  bassAlter: StepAlter | undefined;
}

export interface Note {
  pitchStep?: Step;
  pitchAlter?: StepAlter;
  pitchOctave?: PitchOctave;
  duration: number;
  chord?: boolean;
  rest?: boolean;
}

export interface Sequence {
  notes: Note[];
}

export interface HarmonySequencePair<T extends BaseHarmony> {
  harmony: T;
  sequence: Sequence;
}

export interface PianoHarmonySequencePair {
  harmony: BaseHarmony;
  sequence: {
    rightHand: Note[];
    leftHand: Note[];
  };
}
