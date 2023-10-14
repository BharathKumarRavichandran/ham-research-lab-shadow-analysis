import time

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


def visualize_shadow_matrix(sh, hour, minute):
    # f, ax = plt.subplots(dpi=500)
    plt.subplots()
    plt.imshow(sh, cmap='viridis')
    plt.title("%2s" % str(hour).zfill(2) + ":%2s" % str(minute).zfill(2), pad=10, fontsize=15, color="black",
              weight='bold')
    plt.show()
    df = pd.DataFrame(sh)
    df.head()


def save_shadow_matrix_as_image(sh, hour, minute, file_path):
    original_backend = matplotlib.get_backend()
    matplotlib.use('Agg')  # agg to ignore gui related errors in backend

    f, ax = plt.subplots(dpi=500)
    plt.imshow(sh, cmap='viridis')
    plt.title("%2s" % str(hour).zfill(2) + ":%2s" % str(minute).zfill(2),
              pad=10,
              fontsize=15,
              color="black",
              weight='bold')

    plt.savefig(file_path)
    plt.close()

    # Restore original bg
    matplotlib.use(original_backend)
    print(f"Saved image to path {file_path}")
    time.sleep(1)
