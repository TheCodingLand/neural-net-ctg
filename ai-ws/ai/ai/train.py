from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division, absolute_import, print_function

import os
from fastText import train_supervised


def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

if __name__ == "__main__":
    train_data = os.path.join(os.getenv("DATADIR", ''), 'emails.train')
    valid_data = os.path.join(os.getenv("DATADIR", ''), 'emails.valid')

    # train_supervised uses the same arguments and defaults as the fastText cli
    model = train_supervised(
        input=train_data, epoch=50, lr=1.0, wordNgrams=3, verbose=2, minCount=1
    )
    print_results(*model.test(valid_data))

    model = train_supervised(
        input=train_data, epoch=50, lr=1.0, wordNgrams=3, verbose=2, minCount=1,
        loss="hs"
    )
    print_results(*model.test(valid_data))
    model.save_model("emails.bin")

    model.quantize(input=train_data, qnorm=True, retrain=True, cutoff=100000)
    print_results(*model.test(valid_data))
    model.save_model("emails.ftz")
