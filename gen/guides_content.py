# Original guide texts (body HTML). Titles/SEO/related are set in gen.py
GUIDES = [
 ("guide-remove-vocals.html", "How to remove vocals from a song",
  "A practical guide to removing the singer from a song with AI, what to expect, and how to get a clean result.",
  '''<p class="lead">Removing the vocals from a song used to be a studio trick. Today an AI model can do it on a normal computer or phone in a few minutes. This guide explains how it works, what results to expect and how to get the cleanest instrumental possible.</p>
<h2>Why the old trick rarely worked</h2>
<p>For years the common advice was "phase cancellation": invert one stereo channel and subtract it from the other. Lead vocals are usually mixed exactly in the centre, so they cancel out. The problem is that bass, kick drum and often the snare are also in the centre, so they disappear too, and any stereo reverb on the voice stays behind as a ghost. The result sounds thin and hollow.</p>
<h2>What AI separation does differently</h2>
<p>A source separation model has learned from thousands of songs what a voice, a drum kit and a bass guitar look like in the spectrum. Instead of subtracting channels, it estimates each instrument as its own track. That is why you can get a full-sounding backing track with the voice gone, or the voice alone with everything else removed.</p>
<h2>Step by step with Audio Splitter Pro</h2>
<ol><li>Open the splitter and select your song. MP3, WAV, M4A, FLAC and OGG files all work.</li>
<li>Choose <b>No vocals</b> to create only the instrumental parts, or keep <b>All tracks</b> if you also want the vocal track.</li>
<li>Press the split button and keep the tab open. A few minutes of waiting is normal, because the AI runs on your own device.</li>
<li>In the mixer, turn the Karaoke button on to hear the song without the voice, or mute the vocal track yourself.</li>
<li>Export the result as a WAV file.</li></ol>
<h2>Getting the best quality</h2>
<ul><li><b>Start from the best file you have.</b> A lossless or high bitrate source gives the model more detail than a low quality MP3.</li>
<li><b>Choose High quality</b> in the options if you are not in a hurry. It processes the song with more overlap between pieces, which smooths the joins.</li>
<li><b>Expect small leftovers.</b> Backing vocals, heavy reverb and effects can leave faint traces. That is normal for every separation tool.</li>
<li><b>Dense mixes are harder.</b> A thin acoustic recording separates almost perfectly, while a wall of distorted guitars is more challenging.</li></ul>
<h2>What it is good for</h2>
<p>Karaoke nights, practising an instrument along with a backing track, making a cover, creating a clean instrumental for a video you have the rights to, or simply listening to how a song is built. Always make sure you have permission to use the music you process.</p>
<h2>Frequently asked questions</h2>
<h3>Is the result perfect?</h3><p>No separation is perfect. Modern models are very good, but you may hear small artefacts, especially on busy songs.</p>
<h3>Does it work on any language?</h3><p>Yes. The model separates sounds, it does not need to understand the words.</p>
<h3>Is my song uploaded anywhere?</h3><p>No. Everything is processed inside your browser.</p>'''),

 ("guide-make-karaoke-track.html", "How to make a karaoke track from any song",
  "Turn your favourite song into a karaoke backing track in a few minutes, and keep the lead vocal as a guide if you want it.",
  '''<p class="lead">A karaoke track is simply a song with the lead singer taken out. With AI separation you no longer have to hope that someone published a karaoke version: you can make one from the exact recording you love.</p>
<h2>What you need</h2>
<p>An audio file of the song (MP3, WAV, M4A, FLAC or OGG), a modern browser and a few minutes. A computer gives the fastest result, but a recent phone can work for short songs.</p>
<h2>Make the track</h2>
<ol><li>Open the splitter and choose your song.</li>
<li>Select <b>No vocals</b>. The app will create the drums, bass and other instruments, but skip the vocal file.</li>
<li>When processing ends, the mixer opens with one strip per track. Press <b>Karaoke</b> to mute the vocals instantly and bring the instruments to a balanced level.</li>
<li>Press play and sing. Use the loop button to repeat a difficult part, and the five second buttons to jump around.</li>
<li>Use <b>Export</b> to save the backing track as WAV and play it on any device.</li></ol>
<h2>Keep the voice as a guide</h2>
<p>If you are learning a new song, keep all four tracks. Lower the vocal strip to around thirty percent instead of muting it. You can hear the melody and the pronunciation, but your own voice still fits on top. When you feel confident, turn it to zero.</p>
<h2>Tips for a better karaoke night</h2>
<ul><li>Use the highest quality setting for songs you will play for an audience.</li>
<li>Check the whole track once. If a backing vocal remains in one chorus, you will know before the party starts.</li>
<li>Raise the bass track slightly on small speakers so the song keeps its energy without the voice.</li>
<li>Export as WAV for the cleanest sound. Convert to MP3 later if you need a smaller file.</li></ul>
<h2>A note on rights</h2>
<p>Making a karaoke track for personal practice is one thing. Publishing or selling it is another, and requires permission from the rights holders. Use music you own or are allowed to use.</p>'''),

 ("guide-what-are-stems.html", "What are stems? A simple explanation",
  "Stems are the separate groups of instruments inside a song. Learn what they are, why they matter and how they are used.",
  '''<p class="lead">If you have ever heard a producer talk about "pulling up the stems", you may have wondered what they meant. Stems are the building blocks of a finished song, and they are easier to understand than they sound.</p>
<h2>A stem is a group of sounds</h2>
<p>When a song is recorded, there can be dozens of individual tracks: kick, snare, hi-hats, bass, several guitars, keyboards, lead vocal, harmonies. Mixing all of them gives the song you hear. A <b>stem</b> is a smaller bundle of those tracks mixed together, such as "all the drums" or "all the vocals". Most songs are delivered as four stems.</p>
<h2>The four common stems</h2>
<ul><li><b>Vocals:</b> the lead singer and usually the backing vocals.</li>
<li><b>Drums:</b> kick, snare, cymbals and percussion.</li>
<li><b>Bass:</b> the bass guitar or synth bass.</li>
<li><b>Other:</b> everything else, such as guitars, piano, strings and synthesisers.</li></ul>
<h2>Stems versus multitracks</h2>
<p>A multitrack is the full set of original recordings. A stem is a combination of them. Multitracks give the most control but are huge, and are rarely shared. Stems are small enough to share and still let you change the balance of a song.</p>
<h2>Why people want stems</h2>
<ul><li><b>Musicians</b> mute their own instrument and play along with the rest of the band.</li>
<li><b>Singers</b> practise with a backing track and no lead voice.</li>
<li><b>DJs and producers</b> make remixes and mashups, with permission from the rights holders.</li>
<li><b>Teachers and students</b> isolate the bass line or the drum pattern to study it.</li>
<li><b>Listeners</b> are curious and want to hear what each part is doing.</li></ul>
<h2>Where do stems come from now?</h2>
<p>Artists rarely release them, but AI separation models can estimate them from a finished stereo song. They are not identical to the studio stems, though for practice, study and creative play they are often more than good enough.</p>
<h2>Try it</h2>
<p>Pick a song you know well, split it and listen to each stem alone. Hearing the bass or the drums without anything else is one of the fastest ways to understand how a song works.</p>'''),

 ("guide-how-ai-separation-works.html", "How AI music source separation works",
  "A plain-language look at how neural networks separate vocals, drums and bass, and why it runs inside your browser.",
  '''<p class="lead">Taking a finished song and pulling it back into separate instruments sounds almost impossible. After all, the sounds have been added together. Yet modern AI models do it surprisingly well. Here is the idea without the heavy maths.</p>
<h2>The problem</h2>
<p>A stereo song is a single stream of numbers: the air pressure for the left and right speakers, 44,100 times per second. Every instrument has been added into those numbers. There is no mathematical way to subtract one sound exactly, because we do not know what it looked like on its own.</p>
<h2>The idea: learn what instruments look like</h2>
<p>Researchers train a neural network on a large collection of songs for which the separate stems are known. The model is shown the mix and asked to predict the stems. When it is wrong, its internal settings are nudged slightly. After many repetitions it learns the typical patterns of a voice, a kick drum or a bass guitar, and how they overlap.</p>
<h2>Two ways of looking at sound</h2>
<p>Some models look at the <b>waveform</b>, the raw signal over time. Others look at the <b>spectrogram</b>, a picture of which frequencies are present at each moment. The model used here, a Hybrid Transformer Demucs, uses both views and a transformer to compare different parts of the song with each other. A drum pattern that repeats, for example, helps the model recognise the drums every time they appear.</p>
<h2>Why the song is processed in pieces</h2>
<p>The network works on a window of about eight seconds. A long song is cut into overlapping windows, each is separated, and the results are blended together with a gradual crossfade so you never hear a seam. More overlap means smoother joins and a slower job. This is what the quality setting controls.</p>
<h2>Why it runs in your browser</h2>
<p>The model is converted to a portable format called ONNX and executed by a runtime compiled to WebAssembly. That lets the browser do the heavy calculation on your own processor, so your music never has to leave your device. The first visit downloads the model once and keeps it in browser storage.</p>
<h2>Limits you should know about</h2>
<ul><li>The result is an estimate, not the original studio stems.</li>
<li>Very similar sounds, like a lead vocal and a harmony singing the same notes, can be confused.</li>
<li>Phones have less memory and speed than computers, so long songs take longer.</li></ul>
<h2>Where the technology is going</h2>
<p>Separation keeps improving, with models that split more instruments and make fewer artefacts. Running such models locally, privately and for free is becoming normal, and this site is one small example.</p>'''),

 ("guide-better-separation-tips.html", "10 tips for cleaner stem separation",
  "Simple habits that improve the quality of AI vocal removal and stem splitting, from file choice to settings.",
  '''<p class="lead">Two people can run the same song through the same AI and get different results. The difference is usually the input and a few settings. These ten tips help you get the cleanest tracks.</p>
<ol class="tips">
<li><h3>Use a high quality source</h3><p>Lossless files such as WAV or FLAC keep detail that low bitrate MP3 files throw away. The model can only separate what is still in the file.</p></li>
<li><h3>Avoid re-encoded copies</h3><p>A song downloaded from a video site has usually been compressed more than once. If you own the CD or a purchased download, use that instead.</p></li>
<li><h3>Pick High quality for songs that matter</h3><p>The extra overlap smooths the joins between windows. Use Fast only for quick previews.</p></li>
<li><h3>Create only the tracks you need</h3><p>If you only want a karaoke version, choose No vocals. The AI still works on the whole song, but you skip building files you will never use.</p></li>
<li><h3>Do not clip the input</h3><p>An already distorted, very loud master is harder to separate. If you have a quieter version, try it.</p></li>
<li><h3>Listen on headphones first</h3><p>Small artefacts hide on laptop speakers. Headphones let you decide if a result is good enough before you export.</p></li>
<li><h3>Use the mixer instead of fighting leftovers</h3><p>If a trace of vocals remains, lower the other tracks a little or raise the bass. Small mixing changes often hide small artefacts.</p></li>
<li><h3>Keep the tab open and the device awake</h3><p>Processing runs inside the page. Locking the screen or switching apps on a phone can pause it.</p></li>
<li><h3>Close heavy tabs</h3><p>The model needs memory. Closing other tabs gives it room and avoids crashes, especially on phones.</p></li>
<li><h3>Export WAV, convert later</h3><p>WAV is lossless. If you need MP3, convert it once at the end instead of converting between formats several times.</p></li>
</ol>
<h2>When to switch to the app</h2>
<p>If your phone struggles with the browser version, the Android app runs the same kind of model with native code, supports MP3 export and lets you record your voice over the music.</p>'''),
]

