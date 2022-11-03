# coding=utf-8
import numpy as np

from TTS import text_to_speech
from Updater import BSUpdater, VoiceUpdater
from wav2blendshape import wav2blendshape

bs_updater = BSUpdater(52, '127.0.0.1', port=25001)
bs_updater1 = BSUpdater(52, '127.0.0.1', port=25002)
voice_updater = VoiceUpdater('127.0.0.1', port=25003)


if __name__ == '__main__':
    while True:
        sentence = input('请输入内容：')
        if sentence == 'exit':
            break
        text_to_speech(sentence, actor_name='zh-CN-YunxiNeural', style_degree=2, style='depressful')
        bs = wav2blendshape()
        # np.savez('data.npz', bs)
        # print(bs.shape)
        # break
        print(f'bs_shape: {bs.shape}')
        voice_updater.update()
        bs_updater.update(bs)
        # break
        bs_updater1.update(bs)





