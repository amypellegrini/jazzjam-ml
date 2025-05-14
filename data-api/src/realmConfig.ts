import Realm from "realm";
import {
  HarmonyKind,
  HarmonyRootAlter,
  PitchOctave,
  Step,
  StepAlter,
} from "./types";

export class Note extends Realm.Object {
  static schema = {
    name: "Note",
    properties: {
      duration: "int",
      pitchStep: "string?",
      pitchOctave: "int?",
      pitchAlter: "int?",
      rest: "bool?",
      chord: "bool?",
    },
  };
}

export class BassPartAbsoluteHarmony extends Realm.Object {
  _id!: number;
  beats!: number;
  beatsType!: number;
  divisions!: number;
  harmonyDuration!: number;
  harmonyKind!: HarmonyKind;
  harmonyRootAlter!: HarmonyRootAlter;
  harmonyRootStep!: Step;
  startPitchStep!: Step;
  startPitchOctave!: PitchOctave;
  startPitchAlter!: StepAlter;
  sequenceId!: string;
  style!: string;

  static schema = {
    name: "BassPartAbsoluteHarmony",
    properties: {
      _id: "int",
      beats: "int",
      beatsType: "int",
      divisions: "int",
      harmonyDuration: "int",
      harmonyKind: "string",
      harmonyRootAlter: "int",
      harmonyRootStep: "string",
      startPitchStep: "string",
      startPitchOctave: "int",
      startPitchAlter: "int",
      sequenceId: "string",
      style: "string",
    },
  };
}

export class PianoPartAbsoluteHarmony extends Realm.Object {
  _id!: number;
  keyFifths!: number;
  beats!: number;
  beatsType!: number;
  divisions!: number;
  harmonyDuration!: number;
  harmonyKind!: HarmonyKind;
  harmonyRootAlter!: HarmonyRootAlter;
  harmonyRootStep!: Step;
  sequenceId!: string;
  bassStep: Step | undefined;
  bassAlter: StepAlter | undefined;
  style!: string;

  static schema = {
    name: "PianoPartAbsoluteHarmony",
    properties: {
      _id: "int",
      keyFifths: "int",
      beats: "int",
      beatsType: "int",
      divisions: "int",
      harmonyDuration: "int",
      harmonyKind: "string",
      harmonyRootAlter: "int",
      harmonyRootStep: "string",
      sequenceId: "string",
      bassStep: "string?",
      bassAlter: "int?",
      style: "string",
    },
  };
}

export class PianoSequence extends Realm.Object {
  _id!: string;
  leftHand!: Realm.List<Note>;
  rightHand!: Realm.List<Note>;

  static schema = {
    name: "PianoSequence",
    properties: {
      _id: "string",
      leftHand: "Note[]",
      rightHand: "Note[]",
    },
  };
}

export class WalkingBassSequence extends Realm.Object {
  _id!: string;
  sequence!: Realm.List<Note>;

  static schema = {
    name: "WalkingBassSequence",
    properties: {
      _id: "string",
      sequence: "Note[]",
    },
  };
}

export class WalkingBassHarmony extends Realm.Object {
  _id!: number;
  keyFifths!: number;
  beats!: number;
  beatsType!: number;
  harmonyRootStep!: Step;
  harmonyRootAlter!: HarmonyRootAlter;
  harmonyKind!: HarmonyKind;
  divisions!: number;
  startPitchStep!: Step;
  startPitchOctave!: PitchOctave;
  startPitchAlter!: StepAlter;
  targetPitchStep!: Step;
  targetPitchOctave!: PitchOctave;
  targetPitchAlter!: StepAlter;
  harmonyDuration!: number;
  sequenceId!: string;
  bassStep: Step | undefined;
  bassAlter: StepAlter | undefined;
  style!: string;

  static schema = {
    name: "WalkingBassHarmony",
    properties: {
      _id: "int",
      keyFifths: "int",
      beats: "int",
      beatsType: "int",
      harmonyRootStep: "string",
      divisions: "int",
      harmonyRootAlter: "int",
      harmonyKind: "string",
      harmonyDuration: "int",
      sequenceId: "string",
      startPitchStep: "string",
      startPitchOctave: "int",
      startPitchAlter: "int",
      targetPitchStep: "string",
      targetPitchOctave: "int",
      targetPitchAlter: "int",
      bassStep: "string?",
      bassAlter: "int?",
      style: "string",
    },
  };
}

const realmConfig = {
  schema: [
    WalkingBassHarmony,
    Note,
    PianoSequence,
    PianoPartAbsoluteHarmony,
    WalkingBassSequence,
    BassPartAbsoluteHarmony,
  ],
  schemaVersion: 19,
  path: "bundle.realm",
};

export { realmConfig };
