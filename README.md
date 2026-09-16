# IELTS Focus

IELTS Listening Part 3 focused training site for **option preloading / 选项上膛**.

## Training modes

- 3-option single choice
- 5-option Choose TWO
- Matching with shared options
- Timed option-preload stage before listening
- Browser English TTS at adjustable speed
- Session review, accuracy and preload-rate tracking

All practice material is original and does not reproduce Cambridge IELTS test text.

## Cloud sync

The site uses Supabase Auth + Postgres. Progress is cached locally and merged with the signed-in user's cloud state, so the same account can continue on another device.

RLS is enabled on the cloud tables: authenticated users can only read and write rows whose `user_id` matches their own account.

## Deploy

The repository includes a GitHub Pages workflow. The intended site URL is:

`https://yueert1997ai-sys.github.io/IELTS-focus/`
