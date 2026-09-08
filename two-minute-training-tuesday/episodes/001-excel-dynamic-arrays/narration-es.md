# Narration — episode 001

The rendered cut (`TMTT-001-Excel-Dynamic-Arrays.mp4`) ships silent with
burned-in captions. This is the voiceover script for it, generated directly from
the video's caption track, so **the timings below are the video's real timings**
— not the estimates in `script.md`.

153 words over 109 seconds — about 84 words per minute, a
deliberately slow, clear pace for a technical demo.

This file is generated. Edit the wording in `render/episode.html` (the
`CAPTIONS` array), then run `python make_narration.py` and re-render the video.

## The fastest path: Clipchamp text to speech

Clipchamp has an AI voiceover generator built in, so you do not have to record
anything or own a microphone.

1. Open the MP4 in Clipchamp and drop it on the timeline.
2. **Record & create → Text to speech.**
3. Pick a language and voice. Preview a few — the voice carries the whole
   episode, so it is worth two minutes of listening. Prefer a calm, mid-paced
   English voice over an enthusiastic one; this is instruction, not marketing.
4. Paste the **continuous read** below, generate, and drop it on the timeline.
5. Nudge the audio clip so the first word lands at 0:02.5, right as the title
   card ends.
6. Adjust **speed** in the properties panel until the read tracks the picture.
   If a line drifts, split the audio clip there and slide the piece.
7. Once the voice is in, decide about captions. The burned-in ones match this
   script word for word, so they are safe to keep. If you would rather use
   Clipchamp's auto-captions, re-render a clean picture first:
   `python render/make_video.py --no-captions`.

Pitch and pace are adjustable, natural pauses are supported, and it handles up
to ten minutes of audio, so a two-minute episode is well inside the limit.

## Continuous read

Paste this whole block into text to speech for one continuous take. It matches
the on-screen captions word for word.

> Bienvenidos a Two-Minute Training Tuesday. Este es un export de costos del ERP. Trescientas ochenta líneas. Necesitas los proveedores, sin duplicados. En vez de copiar, pegar, Quitar duplicados Hay algo mejor. Una fórmula: UNICOS, y la columna de proveedor. Excel escribe la referencia por ti. Quince proveedores, de trescientas ochenta líneas. Nunca le dije quince. Tomó el espacio que necesitaba. Toda esa lista pertenece a la fórmula en B5. Eso es un rango desbordado. No está ordenada. Envuélvela en ORDENAR. Una función más por fuera. Nada más cambia. Alfabético. Sigue siendo una fórmula. Ahora la más potente. FILTRAR: dale toda la tabla... ...y la regla: centro de costo igual a esta celda. Ciento treinta y seis líneas: tu informe, filtrado. Como una tabla dinámica. Y lo importante: Cambia el centro de costo... ...y el informe se vuelve a dibujar solo. Sin copiar, pegar ni reordenar. La próxima semana: adjuntos de Outlook en segundos.

## Beat-by-beat, with the video's real timings

Use this if you would rather generate one clip per beat and place each at its
timecode. More work, much tighter sync.

| Starts at | Window | Words | Line |
| --- | --- | --- | --- |
| 0.3 | 3.3s | 5 | Bienvenidos a Two-Minute Training Tuesday. |
| 3.7 | 3.0s | 8 | Este es un export de costos del ERP. |
| 6.8 | 4.0s | 3 | Trescientas ochenta líneas. |
| 11.0 | 3.4s | 5 | Necesitas los proveedores, sin duplicados. |
| 14.5 | 3.8s | 7 | En vez de copiar, pegar, Quitar duplicados |
| 18.4 | 1.7s | 3 | Hay algo mejor. |
| 21.0 | 4.5s | 8 | Una fórmula: UNICOS, y la columna de proveedor. |
| 25.6 | 4.3s | 6 | Excel escribe la referencia por ti. |
| 30.7 | 5.2s | 6 | Quince proveedores, de trescientas ochenta líneas. |
| 36.0 | 5.4s | 9 | Nunca le dije quince. Tomó el espacio que necesitaba. |
| 41.5 | 4.9s | 9 | Toda esa lista pertenece a la fórmula en B5. |
| 46.5 | 2.7s | 5 | Eso es un rango desbordado. |
| 49.3 | 5.2s | 6 | No está ordenada. Envuélvela en ORDENAR. |
| 54.6 | 4.3s | 8 | Una función más por fuera. Nada más cambia. |
| 59.7 | 3.8s | 5 | Alfabético. Sigue siendo una fórmula. |
| 63.6 | 3.1s | 4 | Ahora la más potente. |
| 66.8 | 6.2s | 5 | FILTRAR: dale toda la tabla... |
| 73.1 | 7.8s | 10 | ...y la regla: centro de costo igual a esta celda. |
| 82.0 | 5.5s | 8 | Ciento treinta y seis líneas: tu informe, filtrado. |
| 87.6 | 3.3s | 7 | Como una tabla dinámica. Y lo importante: |
| 91.6 | 3.9s | 5 | Cambia el centro de costo... |
| 97.0 | 4.5s | 8 | ...y el informe se vuelve a dibujar solo. |
| 101.6 | 3.9s | 5 | Sin copiar, pegar ni reordenar. |
| 105.9 | 3.2s | 8 | La próxima semana: adjuntos de Outlook en segundos. |

## If you would rather record it yourself

A human voice beats synthesis for internal comms, because people recognise a
colleague and trust it more.

1. Open the MP4 in Clipchamp, **Record & create → Audio.**
2. Watch the picture and read the lines above as each beat arrives. Do not chase
   the timings on the first pass — get a clean read, then slide the audio.
3. When you fumble, pause two seconds and redo the sentence. The silence is
   visible in the waveform, so the retake is trivial to cut.
4. Use a headset mic, not the laptop mic, and close the door.

See [`../../production/recording-sop.md`](../../production/recording-sop.md) for
the full audio setup.

## Also here

`TMTT-001-captions.srt` — the same caption track as a sidecar file, from the same
source. Useful if you upload somewhere that wants captions separately, or want to
edit the wording without re-rendering the video.
