import fs from "fs";
import path from "path";

export default function handler(req, res) {
  const logPath = path.resolve(process.cwd(), "..", "agent_log.json");

  try {
    if (fs.existsSync(logPath)) {
      const data = JSON.parse(fs.readFileSync(logPath, "utf-8"));
      res.status(200).json(data);
    } else {
      res.status(200).json([]);
    }
  } catch (err) {
    res.status(500).json({ error: "Failed to read agent log" });
  }
}
