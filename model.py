import re
import numpy as np
import tensorflow as tf
import keras
import csv
import random
import math

num_inputs = 34
epochs = 70
neurons = [9, 9, 9, 9]
lr = 0.001
he_normal = True


def main():
    file = open("sportsref_download.csv", mode='r')
    reader = csv.reader(file)
    next(reader)

    inputs_outputs = []

    for row in reader:
        inputs_outputs.append([])
        for i in range(len(row[1:])):
            value = row[i + 1]
            # for the first value (position), one-hot encode the data
            to_categorical = i == 0
            is_output = i == len(row[1:]) - 1
            inputs_outputs[-1] += preprocess(value, to_categorical, is_output)

    # for i in range(len(inputs_outputs)):
    #     if len(inputs_outputs[i]) != num_inputs+1:
    #         print(len(inputs_outputs[i]))
    #         raise ValueError("Expected length of " + str(num_inputs+1) + ", got: " + str(inputs_outputs[i]))

    train_input, train_output, test_input, test_output = split_train_test(inputs_outputs)

    model = keras.models.load_model("model")
    # layers = [layer for layer in keras.models.load_model("model").layers]
    # if he_normal:
    #     initializer = tf.keras.initializers.HeNormal()
    # else:
    #     initializer = tf.keras.initializers.GlorotUniform()
    # new_layer = keras.layers.Dense(3, name="layer_5", activation="relu", kernel_initializer=initializer)
    # new_leaky = keras.layers.LeakyReLU(name="leky_2")
    # layers.insert(-1, new_layer)
    # layers.insert(-1, new_leaky)
    # model = keras.models.Sequential(layers)
    # model.build((None, num_inputs))
    model.summary()

    # lrate_scheduler = keras.callbacks.LearningRateScheduler(step_decay)
    model.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=keras.optimizers.Adam(learning_rate=lr))
    model.fit(train_input, train_output, epochs=epochs)
    score = model.evaluate(test_input, test_output)

    if score < 4900:
        model.save("model")
        print("model saved!")

    # richardson_data = np.array([one_hot(0) + [1, 76, 1, 244, 1, 4.43, 1, 40.5, 0, 0, 1, 129, 0, 0, 0, 0]])
    # richardson = model.predict(richardson_data)[0][0]
    # positive_counterfactuals, negative_counterfactuals = counterfactuals(model)
    # print("Anthony Richardson prediction: pick " + str(round(richardson)))
    #
    # negative_counterfactuals.sort(key=lambda x: x[1])  # sort by the model's prediction
    # positive_counterfactuals.sort(key=lambda x: x[1])
    # worse_richardson = negative_counterfactuals[-3:]
    # better_richardson = positive_counterfactuals[:3]
    #
    # i = 0
    # while i < len(worse_richardson):
    #     if worse_richardson[i][1] <= richardson:
    #         worse_richardson.pop(i)
    #         i -= 1
    #     i += 1
    #
    # while i < len(better_richardson):
    #     if better_richardson[i][1] >= richardson:
    #         better_richardson.pop(i)
    #         i -= 1
    #     i += 1
    #
    # wr = worse_richardson
    # if len(wr) == 0:
    #     print("richardson can't get any worse!")
    # if len(wr) == 1:
    #     print("richardson would only be worse if his %s was worse (pick %.2f)." % (wr[0][0], wr[0][1]))
    # if len(wr) == 2:
    #     print("richardson would be worse if his %s (pick %.2f) or his %s (pick %.2f) was worse." %
    #           (wr[0][0], wr[0][1], wr[1][0], wr[1][1]))
    # if len(wr) == 3:
    #     print("richardson would be worse if his %s (pick %.2f), his %s (pick %.2f), or his %s (pick %.2f) was worse." %
    #           (wr[0][0], wr[0][1], wr[1][0], wr[1][1], wr[2][0], wr[2][1]))
    #
    # br = better_richardson
    # if len(br) == 0:
    #     print("richardson can't get any better!")
    # if len(br) == 1:
    #     print("richardson would only be better if his %s was better (pick %.2f)." % (br[0][0], br[0][1]))
    # if len(br) == 2:
    #     print("richardson would be better if his %s (pick %.2f) or his %s (pick %.2f) was better." %
    #           (br[0][0], br[0][1], br[1][0], br[1][1]))
    # if len(br) == 3:
    #     print("richardson would be better if his %s (pick %.2f), his %s (pick %.2f), or his %s (pick %.2f) was better."
    #           % (br[0][0], br[0][1], br[1][0], br[1][1], br[2][0], br[2][1]))
    #
    # # check if there's a way we could make one of richardson's measurables worse to make the model
    # # like him better, or vice versa
    # if negative_counterfactuals[0][1] < richardson:
    #     # strange_better_richardson is too long
    #     sbr = negative_counterfactuals[0]
    #     print("strangely, richardson would be better if his %s was worse (pick %.2f)." % (sbr[0], sbr[1]))
    #
    # if positive_counterfactuals[0][1] > richardson:
    #     swr = positive_counterfactuals[-1]
    #     print("strangely, richardson would be worse if his %s was better (pick %.2f)." % (swr[0], swr[1]))


def preprocess(value, to_categorical, is_output):
    if value == '':
        rvalue = 0.0
    elif value == 'QB':
        rvalue = 0.0
    elif value == 'OT':
        rvalue = 1.0
    elif value == 'OL' or value == 'OG':
        rvalue = 2.0
    elif value == 'C':
        rvalue = 3.0
    elif value == 'RB' or value == 'FB' or value == 'HB':
        rvalue = 4.0
    elif value == 'TE':
        rvalue = 5.0
    elif value == 'WR':
        rvalue = 6.0
    elif value == 'DT':
        rvalue = 7.0
    elif value == 'DL':
        rvalue = 8.0
    elif value == 'DE' or value == 'EDGE':
        rvalue = 9.0
    elif value == 'OLB':
        rvalue = 10.0
    elif value == 'LB':
        rvalue = 11.0
    elif value == 'CB':
        rvalue = 12.0
    elif value == 'DB':
        rvalue = 13.0
    elif value == 'S':
        rvalue = 14.0
    elif value == 'P':
        rvalue = 15.0
    elif value == 'K':
        rvalue = 16.0
    elif value == 'LS':
        rvalue = 17.0
    elif is_num(value):
        rvalue = float(value)
    elif '/' in value:
        pick_num = value.split(" / ")
        # find the first letter in the text (should be "rd" or "st" or "nd" or "th")
        ind = re.search("[a-zA-Z]", pick_num[2]).span(0)[0]

        assert (pick_num[2][3:5] == "rd" or pick_num[2][3:5] == "st" or pick_num[2][3:5] == "nd" or
                pick_num[2][3:5] == "th", "value: " + pick_num[2][3:4])

        rvalue = float(pick_num[2][:ind])
    else:
        raise Exception("Unknown input: %s" % value)

    if to_categorical:
        rvalue = one_hot(rvalue)
    elif not is_output:
        if rvalue == 0:
            rvalue = [0, rvalue]
        else:
            rvalue = [1, rvalue]
    else:
        rvalue = [rvalue]

    # if type(rvalue) == np.ndarray:
    #     raise Exception("unexpected numpy array: " + str(rvalue))

    return rvalue


def split_train_test(data):
    random.shuffle(data)

    num_train_data = int(.8 * len(data))  # number of elements that will be in the training data set
    # first n data points are the training set, rest are the test set
    train_set = data[:num_train_data]
    train_input = []
    train_output = []
    for player in train_set:
        # first num_classes-1 values are the input, last value is the output
        train_input.append(player[:-1])
        train_output.append(player[-1])

    test_set = data[num_train_data:]
    test_input = []
    test_output = []
    for player in test_set:
        # first num_classes-1 values are the input, last value is the output
        test_input.append(player[:-1])
        test_output.append(player[-1])

    return train_input, train_output, test_input, test_output


def leaky_model():
    layers = [keras.Input(shape=num_inputs)]
    for i in range(len(neurons)):
        if he_normal:
            initializer = tf.keras.initializers.HeNormal()
        else:
            initializer = tf.keras.initializers.GlorotUniform()
        layers.append(keras.layers.Dense(neurons[i], activation="relu", kernel_initializer=initializer))
        layers.append(keras.layers.LeakyReLU())

    if he_normal:
        initializer = tf.keras.initializers.HeNormal()
    else:
        initializer = tf.keras.initializers.GlorotUniform()
    layers.append(keras.layers.Dense(1, activation="relu", kernel_initializer=initializer))
    return keras.models.Sequential(layers)


# change the input to the model slightly to see how the result would change
def counterfactuals(model):
    return ([("height", model.predict(np.array([one_hot(0) +
                                                [1, 84, 1, 244, 1, 4.43, 1, 40.5, 0, 0, 1, 129, 0, 0, 0, 0]]))[0][0]),
             ("weight", model.predict(np.array([one_hot(0) +
                                                [1, 76, 1, 270, 1, 4.43, 1, 40.5, 0, 0, 1, 129, 0, 0, 0, 0]]))[0][0]),
             ("40 time", model.predict(np.array([one_hot(0) +
                                                 [1, 76, 1, 244, 1, 4.23, 1, 40.5, 0, 0, 1, 129, 0, 0, 0, 0]]))[0][0]),
             ("vert", model.predict(np.array([one_hot(0) +
                                              [1, 76, 1, 244, 1, 4.43, 1, 44.5, 0, 0, 1, 129, 0, 0, 0, 0]]))[0][0]),
             ("bench", model.predict(np.array([one_hot(0) +
                                               [1, 76, 1, 244, 1, 4.43, 1, 40.5, 1, 20, 1, 129, 0, 0, 0, 0]]))[0][0]),
             ("broad", model.predict(np.array([one_hot(0) +
                                               [1, 76, 1, 244, 1, 4.43, 1, 40.5, 0, 0, 1, 147, 0, 0, 0, 0]]))[0][0]),
             ("3cone", model.predict(np.array([one_hot(0) +
                                               [1, 76, 1, 244, 1, 4.43, 1, 40.5, 0, 0, 1, 129, 1, 7.7, 0, 0]]))[0][0]),
             ("shuttle",
              model.predict(np.array([one_hot(0) +
                                      [1, 76, 1, 244, 1, 4.43, 1, 40.5, 0, 0, 1, 129, 0, 0, 1, 4.5]]))[0][0])],
            [("position", model.predict(np.array([one_hot(3) +
                                                  [1, 76, 1, 244, 1, 4.43, 1, 40.5, 0, 0, 1, 129, 0, 0, 0, 0]]))[0][0]),
             ("height", model.predict(np.array([one_hot(0) +
                                                [1, 71, 1, 244, 1, 4.43, 1, 40.5, 0, 0, 1, 129, 0, 0, 0, 0]]))[0][0]),
             ("weight", model.predict(np.array([one_hot(0) +
                                                [1, 76, 1, 200, 1, 4.43, 1, 40.5, 0, 0, 1, 129, 0, 0, 0, 0]]))[0][0]),
             ("40 time", model.predict(np.array([one_hot(0) +
                                                 [1, 76, 1, 244, 1, 4.63, 1, 40.5, 0, 0, 1, 129, 0, 0, 0, 0]]))[0][0]),
             ("vert", model.predict(np.array([one_hot(0) +
                                              [1, 76, 1, 244, 1, 4.43, 1, 30, 0, 0, 1, 129, 0, 0, 0, 0]]))[0][0]),
             ("broad", model.predict(np.array([one_hot(0) +
                                               [1, 76, 1, 244, 1, 4.43, 1, 40.5, 0, 0, 1, 70, 0, 0, 0, 0]]))[0][0])])


def one_hot(n):
    return keras.utils.to_categorical(n, num_classes=18).tolist()


def step_decay(epoch):
    initial_lrate = 0.05
    drop = 0.8
    epochs_drop = (1.0 / math.log(0.00001 / initial_lrate, drop)) * epochs  # the learning rate should end at 0.00001
    lrate = initial_lrate * math.pow(drop,
                                     math.floor((1 + epoch) / epochs_drop))
    return lrate


# return whether a string is numeric
def is_num(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


main()
