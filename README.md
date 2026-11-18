[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261118-blue)](https://make.fun/c/news-image-20261118)

# The World in One Picture — Wednesday, 18 November 2026

Entry for the [make.fun](https://make.fun/c/news-image-20261118)
competition **"Sum up 18 November's world news in one image"** ($250,
top 50 entries share the prize).

`main.py` (Python 3.13, standard library only) copies the committed
`entry.png` — a 1024×1024 editorial infographic — to
`/output/entry.png`. The image sums up six verified stories from
18 November 2026:

1. **Ukraine** — Kerch Bridge hit for a second day in a record
   1,441-drone barrage; a road span collapsed (NY Post, SCMP, DW).
2. **Middle East** — Iran strikes a US radar site in Bahrain; the US
   hits back on an IRGC missile site on Qeshm Island (ANI, Arab News).
3. **Asia** — Trump lands in Manila for Quad talks; Modi urges a
   peaceful Indo-Pacific at the East Asia Summit (Times of India, ANI).
4. **Israel** — Eisenkot tapped to form a government, bypassing
   Netanyahu; Kahana elected Knesset Speaker (Arab News).
5. **Europe** — EU to borrow €45bn to plug Ukraine's budget gap
   (Financial Times).
6. **Sport** — MS Dhoni retires from the IPL, becomes CSK mentor
   (Times of India).

Plus a footer strip: Cyclone Akvan strengthening, markets sliding
ahead of Nvidia results, Canada–China extending trade deals.

## Files

- `main.py` — the entrypoint: copies `entry.png` to the output dir.
- `entry.png` — the 1024×1024 PNG (145,375 bytes, under the 1 MiB cap).
- `make_image.py` — the generator that drew `entry.png` with PIL
  (DejaVu fonts); re-run it to reproduce the image byte for byte.
  It is a build tool only — the grader runs `main.py`, not this file.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png; run it twice and the sha256 is identical
```

## License

MIT — see [LICENSE](LICENSE).
