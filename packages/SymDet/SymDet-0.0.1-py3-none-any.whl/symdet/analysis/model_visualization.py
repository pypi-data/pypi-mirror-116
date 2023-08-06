"""
This program and the accompanying materials are made available under the terms of the
Eclipse Public License v2.0 which accompanies this distribution, and is available at
https://www.eclipse.org/legal/epl-v20.html
SPDX-License-Identifier: EPL-2.0

Copyright Contributors to the Zincware Project.

Model Visualization
===================
Visualize the NN models in different ways
"""
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np


class Visualizer:
    """
    Class for the visualization of NN models

    Attributes
    ----------
    data : tf.Tensor
                data to be visualized by the TSNE
        colour_map : list
                A colour map to be applied to the data so that it matches that of the cluster map.
    """

    def __init__(self, data, colour_map):
        """
        Constructor the visualizer class

        Parameters
        ----------
        data : tf.Tensor
                data to be visualized by the TSNE
        colour_map : list
                A colour map to be applied to the data so that it matches that of the cluster map.
        """

        self.data = data
        self.colour_map = colour_map

    def tsne_visualization(self,
                           perplexity=50,
                           n_components=2,
                           plot: bool = True,
                           save: bool = False) -> np.ndarray:
        """
        Display a TSNE representation of the models embedding layer

        Parameters
        ----------
        perplexity : int
                Perplexity of the tsne representation.
        n_components : int
                Dimensionality of the TSNE representation.
        plot : bool
                If true the TSNE representation will be plotted.
        save : bool
                If true the plot will be saved.

        Returns
        -------
        tsne_representation : np.ndarray
                Returns the tsne representation as an array.
        Notes
        -----
        See the theory documentation for a full overview of these parameters, particularly in the case of the TSNE
        values.
        """
        tsne_model = TSNE(n_components=n_components,
                          perplexity=perplexity,
                          random_state=1)
        tsne_representation = tsne_model.fit_transform(self.data)

        if plot:
            plt.scatter(
                tsne_representation[:, 0],
                tsne_representation[:, 1],
                c=self.colour_map,
                marker='.',
                cmap="viridis",
                vmax=11,
                vmin=-1,
            )
            plt.colorbar()
            if save:
                plt.savefig(
                    f"tsne_representation_{perplexity}_{n_components}.svg",
                    dpi=800,
                    format="svg",
                )
            plt.show()

        return tsne_representation
