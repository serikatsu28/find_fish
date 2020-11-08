import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential, model_from_json
from keras import regularizers
from keras.optimizers import RMSprop
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

img_row = 64
img_col = 32
color = 3

def main():
    nn_model('./image/photos.npz')

def nn_model(data_path):
    input_shape = (img_row, img_col, color)

    photos = np.load(data_path)
    x = photos['x']
    y = photos['y']
    x = x.astype('float32') / 255
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state= 71)

    #画像を回転、反転させて画像枚数を増やす
    x_new = []
    y_new = []

    for i, xi in enumerate(x_train):
        yi = y_train[i]
        for angle in range(-30, 30, 10):
            center = (img_row/2, img_col/2)
            #画像を回転
            rotate = cv2.getRotationMatrix2D(center, angle, 1.0)
            xi_r = cv2.warpAffine(xi, rotate, (img_row,img_col))
            x_new.append(xi_r)
            y_new.append(yi)
            #画像を反転
            xi_f = cv2.flip(xi_r, 1)
            x_new.append(xi_f)
            y_new.append(yi)

    x_train = np.array(x_new)
    y_train = np.array(y_new)

    # モデルの初期化
    model = Sequential()
    # 入力層
    model.add(Conv2D(32, kernel_size=3, padding='same',
                     input_shape=input_shape, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, kernel_size=3, padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Dense(32, activation='relu'))
    # 1次元に変換
    model.add(Flatten())
    model.add(Dense(8, activation='relu', kernel_regularizer=regularizers.l2(0.001))) # 正則化
    model.add(Dropout(0.5))
    # 出力層
    model.add(Dense(1, activation='sigmoid'))

    # モデルをコンパイル
    model.compile(
        loss='binary_crossentropy',
        optimizer=RMSprop(),
        metrics=['accuracy'])

    # 学習を実行
    log = model.fit(x_train, y_train,
              batch_size=96,
              epochs=20,
              verbose=1,
              validation_data=(x_test, y_test))

    # モデルを評価
    score = model.evaluate(x_test, y_test, verbose=1)
    print('正解率=', score[1], 'loss=', score[0])

    # モデルを保存
    open('find_fish_model.json','w').write(model.to_json())
    model.save_weights('find_fish_weight.hdf5')

if __name__=='__main__':
    main()
