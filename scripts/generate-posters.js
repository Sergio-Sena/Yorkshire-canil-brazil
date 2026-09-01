import { execSync } from 'child_process';
import { readdirSync, existsSync, mkdirSync } from 'fs';
import { join, basename, extname } from 'path';

const FFMPEG = 'C:\\ffmpeg\\bin\\ffmpeg.exe';
const VIDEOS_DIR = join('src', 'videos', 'famosos');
const POSTERS_DIR = join('src', 'images', 'posters');

if (!existsSync(POSTERS_DIR)) mkdirSync(POSTERS_DIR, { recursive: true });

const videos = readdirSync(VIDEOS_DIR).filter(f => extname(f) === '.mp4');

for (const video of videos) {
  const name = basename(video, '.mp4');
  const poster = join(POSTERS_DIR, `${name}.webp`);

  if (existsSync(poster)) {
    console.log(`✓ já existe: ${name}.webp`);
    continue;
  }

  const input = join(VIDEOS_DIR, video);
  execSync(`"${FFMPEG}" -i "${input}" -ss 00:00:01 -vframes 1 -q:v 80 "${poster}" -y`, { stdio: 'pipe' });
  console.log(`✔ gerado: ${name}.webp`);
}
