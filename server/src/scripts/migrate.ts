import fs from 'fs';
import path from 'path';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

async function run() {
  const schemaPath = path.join(path.resolve(), 'db', 'schema.sql');
  const sql = fs.readFileSync(schemaPath, 'utf-8');
  const dbPath = process.env.SQLITE_PATH || './data.sqlite';
  const db = await open({ filename: dbPath, driver: sqlite3.Database });
  await db.exec(sql.replace(/JSONB/g, 'JSON').replace(/SERIAL PRIMARY KEY/g, 'INTEGER PRIMARY KEY AUTOINCREMENT'));
  await db.close();
  console.log('SQLite schema applied at', dbPath);
}

run();
