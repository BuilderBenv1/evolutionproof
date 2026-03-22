import fs from "fs";
import path from "path";

export default function handler(req, res) {
  // Try multiple paths for agent_log.json
  const candidates = [
    path.resolve(process.cwd(), "agent_log.json"),
    path.resolve(process.cwd(), "..", "agent_log.json"),
    path.resolve(process.cwd(), "data", "agent_log.json"),
  ];

  for (const logPath of candidates) {
    try {
      if (fs.existsSync(logPath)) {
        const data = JSON.parse(fs.readFileSync(logPath, "utf-8"));
        return res.status(200).json(data);
      }
    } catch (err) {
      continue;
    }
  }

  // Return empty array if no log found
  res.status(200).json([]);
}
