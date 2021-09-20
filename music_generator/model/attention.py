from tensorflow.keras.layers import (
    Activation,
    Concatenate,
    Dense,
    Embedding,
    Input,
    Lambda,
    LSTM,
    Multiply,
    Permute,
    RepeatVector,
    Reshape,
)
import tensorflow.keras.backend as K
from tensorflow.keras.models import Model
from dataclasses import dataclass


@dataclass
class LSTMAttentionSettings:
    notes_size: int
    durations_size: int
    embed_size: int
    lstm_units: int


class LSTMAttention:
    def __init__(self, settings: LSTMAttentionSettings):
        self.settings = settings

    def _create_network(self):
        notes_in = Input(shape=(None,))
        durations_in = Input(shape=(None,))
        x1 = Embedding(
            self.settings.notes_size,
            self.settings.embed_size
        )(notes_in)
        x2 = Embedding(
            self.settings.durations_size,
            self.settings.embed_size
        )(durations_in)
        x = Concatenate()([x1, x2])
        x = LSTM(self.settings.lstm_units, return_sequences=True)(x)
        x = LSTM(self.settings.lstm_units, return_sequences=True)(x)
        e = Dense(1, activation='tanh')(x)
        e = Reshape([-1])(e)
        alpha = Activation('softmax')(e)
        alpha_repeated = Permute([2, 1])(RepeatVector(self.settings.lstm_units)(alpha))
        c = Multiply()([x, alpha_repeated])
        c = Lambda(lambda xin: K.sum(xin, axis=1), output_shape=(self.settings.lstm_units,))(c)

        notes_out = Dense(
            self.settings.notes_size,
            activation='softmax',
            name='pitch'
        )(c)
        durations_out = Dense(
            self.settings.durations_size,
            activation='softmax',
            name='duration'
        )(c)

        _ = Model([notes_in, durations_in], [notes_out, durations_out])
