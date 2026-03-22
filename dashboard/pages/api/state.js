import fs from "fs";
import path from "path";

export default function handler(req, res) {
  const statePath = path.resolve(process.cwd(), "..", "agent_state.json");

  try {
    if (fs.existsSync(statePath)) {
      const data = JSON.parse(fs.readFileSync(statePath, "utf-8"));
      res.status(200).json(data);
    } else {
      res.status(200).json({});
    }
  } catch (err) {
    res.status(500).json({ error: "Failed to read agent state" });
  }
}
