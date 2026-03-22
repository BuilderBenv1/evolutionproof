import fs from "fs";
import path from "path";

export default function handler(req, res) {
  const candidates = [
    path.resolve(process.cwd(), "agent_state.json"),
    path.resolve(process.cwd(), "..", "agent_state.json"),
    path.resolve(process.cwd(), "data", "agent_state.json"),
  ];

  for (const statePath of candidates) {
    try {
      if (fs.existsSync(statePath)) {
        const data = JSON.parse(fs.readFileSync(statePath, "utf-8"));
        return res.status(200).json(data);
      }
    } catch (err) {
      continue;
    }
  }

  res.status(200).json({});
}
