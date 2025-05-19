import Realm from "realm";
import express, { Request, Response } from "express";
import bodyParser from "body-parser";
import cors from "cors";
import {
  realmConfig,
  WalkingBassHarmony,
  WalkingBassSequence,
} from "./realmConfig";

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(cors());

const realm = new Realm(realmConfig);

app.get("/walking-bass-sequences", async (req: Request, res: Response) => {
  try {
    const sequences = realm.objects(WalkingBassSequence);
    res.json(sequences);
  } catch (error) {
    console.error("Error fetching sequences:", error);
    res.status(500).json({ error: "Failed to fetch sequences" });
  }
});

app.get("/walking-bass-harmonies", async (req: Request, res: Response) => {
  try {
    const harmonies = realm.objects(WalkingBassHarmony);
    res.json(harmonies);
  } catch (error) {
    console.error("Error fetching harmonies:", error);
    res.status(500).json({ error: "Failed to fetch harmonies" });
  }
});

app.get("/walking-bass-harmonies/:id", async (req: Request, res: Response) => {
  const id = parseInt(req.params.id);
  try {
    // Replace this with your actual Realm DB fetching logic
    // const harmony = await getWalkingBassHarmonyById(id);
    const harmony = { _id: id /* Your mock data or Realm data */ };
    if (harmony) {
      res.json(harmony);
    } else {
      res.status(404).json({ error: "Harmony not found" });
    }
  } catch (error) {
    console.error("Error fetching harmony:", error);
    res.status(500).json({ error: "Failed to fetch harmony" });
  }
});

app.listen(port, () => {
  console.log(`REST API server listening at http://localhost:${port}`);
});
