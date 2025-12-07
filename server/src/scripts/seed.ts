import fs from 'fs';
import path from 'path';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

async function run() {
  const seedPath = path.join(path.resolve(), 'db', 'seed.sql');
  const sql = fs.readFileSync(seedPath, 'utf-8');
  const dbPath = process.env.SQLITE_PATH || './data.sqlite';
  const db = await open({ filename: dbPath, driver: sqlite3.Database });
  await db.exec(sql);
  await db.close();
  console.log('Seeded SQLite at', dbPath);
}

run();
