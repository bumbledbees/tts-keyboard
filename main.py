import argparse
import os.path
import readline  # pylint: disable=W0611  # noqa: F401
import sys
import wave

import piper
import pyaudio
from sanitize_filename import sanitize


def main():
    parser = argparse.ArgumentParser(prog='tts-keyboard',
                                     description='simple voice keyboard')
    parser.add_argument('voice',
                        help='path to a .onnx file containing a piper voice')
    parser.add_argument('-g', '--gain', '--volume',
                        type=float,
                        default=1.0,
                        help='scale factor for output volume')
    parser.add_argument('-s', '--speed',
                        type=float,
                        default=1.0,
                        help='scale factor for rate of speaking')
    parser.add_argument('-av', '--audio-variation',
                        type=float,
                        default=1.0,
                        help='scale factor for audio variation')
    parser.add_argument('-sv', '--speaker-variation',
                        type=float,
                        default=1.0,
                        help='scale factor for speaker variation')
    parser.add_argument('-ra', '--raw-audio',
                        dest='normalize_audio',
                        action='store_false',
                        help='use raw audio from voice')
    parser.add_argument('-d', '--output-device',
                        help='output device name as reported to PyAudio')
    parser.add_argument('--sample-rate',
                        type=int,
                        help=argparse.SUPPRESS)
    args = parser.parse_args()

    voice = piper.PiperVoice.load(args.voice)
    audio = pyaudio.PyAudio()
    stream_kwargs = {}
    if args.output_device:
        for n in range(audio.get_device_count()):
            dev_info = audio.get_device_info_by_index(n)
            if dev_info['name'] == args.output_device:
                stream_kwargs['output_device_index'] = dev_info['index']
        if 'output_device_index' not in stream_kwargs:
            print(f'error: failed to open device {args.output_device}',
                  file=sys.stderr)
            sys.exit(1)
    if args.sample_rate is None:
        args.sample_rate = voice.config.sample_rate
    stream = audio.open(
        format=audio.get_format_from_width(2),
        channels=1,
        rate=args.sample_rate,
        output=True,
        **stream_kwargs
    )
    syn_config = piper.SynthesisConfig(
        volume=args.gain,
        length_scale=args.speed,
        noise_scale=args.audio_variation,
        noise_w_scale=args.speaker_variation,
        normalize_audio=args.normalize_audio
    )

    loop(voice, stream, syn_config)

    stream.close()
    audio.terminate()
    sys.exit(0)


def loop(voice, stream, config):
    while True:
        words = input('(tts-keyboard) ')
        if not words:
            continue
        if words.lower().startswith(':q'):
            return
        if words.startswith(':s '):
            words = words[3:]
            fname = sanitize(words.replace(' ', '_'))[:64] + '.wav'
            if os.path.exists(fname):
                print(f'  File "{fname}" exists.')
                response = input('  Overwrite? (y/N) ')
                if response.lower() != 'y':
                    continue
            with wave.open(fname, 'wb') as outfile:
                print(f'  Saving audio to "{fname}"...')
                voice.synthesize_wav(words, outfile, syn_config=config)
                continue

        chunks = voice.synthesize(words, config)
        for chunk in chunks:
            stream.write(chunk.audio_int16_bytes)


if __name__ == "__main__":
    main()
