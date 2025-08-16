# tts-keyboard

quick and dirty voice keyboard using Piper for vocal synthesis and PyAudio for playback.

## setup
navigate to the directory where `tts-keyboard` is installed.

install dependencies by running `pip install .`

download voice files from [https://huggingface.co/rhasspy/piper-voices/tree/main](https://huggingface.co/rhasspy/piper-voices/tree/main). make sure to download both the `.onnx` and `.onnx.json` files for the voices you wish to use.

to run, type `python3 main.py {PATH-TO-VOICE-FILE}`, replacing `{PATH-TO-VOICE-FILE}` with the path to the `.onnx` voice file.

## general usage
type a message then press `<Enter>` and your message will be spoken aloud.

type `:q` then `<Enter>` to quit.

type `:s` before your message for it to be written to a file.

## command line arguments
syntax:
```
tts-keyboard [-h, --help]
             [-g, --gain, --volume GAIN]
             [-s, --speed SPEED]
             [-av, --audio-variation AUDIO_VARIATION]
             [-sv, --speaker-variation SPEAKER_VARIATION]
             [-ra, --raw-audio]
             [-d, --output-device OUTPUT_DEVICE]
             voice
```

### positional arguments
#### `voice`
> path to a `.onnx` file containing a piper voice. note that in the same directory as the `.onnx` file, there must be a file with the same name and the suffix `.onnx.json`.

### optional arguments
#### `-h, --help`
> show this help message and exit

#### `-g, --gain, --volume GAIN`
> scale factor for output volume

#### `-s, --speed SPEED`
> scale factor for rate of speaking

#### `-av, --audio-variation AUDIO_VARIATION`
> scale factor for audio variation

#### `-sv, --speaker-variation SPEAKER_VARIATION`
> scale factor for speaker variation

#### `-ra, --raw-audio`
> use raw audio from voice

#### `-d, --output-device OUTPUT_DEVICE`
> output device name as reported to PyAudio

## known issues
- on Linux, if there are no unusual errors and no sound, it may be due to PyAudio using ALSA and selecting the wrong output device. try specifying one of the following output devices with `-d`/`--output-device` depending on your system configuration:
  - `pulse`
  - `pipewire`
  - `jack`

## additional links
- [Piper project page](https://github.com/rhasspy/piper1-gpl)
- [Piper voice files](https://huggingface.co/rhasspy/piper-voices)
- [Piper voice samples](https://rhasspy.github.io/piper-samples)
- [PyAudio documentation](https://people.csail.mit.edu/hubert/pyaudio/docs)
