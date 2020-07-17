from numpy import array, float32
import numpy as np
from sklearn.linear_model import LinearRegression
import gym_replab
from sklearn.preprocessing import PolynomialFeatures

rgb_coords = np.array([array([ 33.92592593, 432.81481481]),
array([ 96.        , 436.76470588]),
array([148.95867769, 449.20661157]),
array([ 35.42857143, 274.5       ]),
array([105.89010989, 260.17582418]),
array([151.72972973, 266.32432432]),
array([ 31.59036145, 135.97590361]),
array([ 98.64516129, 129.48387097]),
array([140.54716981, 119.03773585])])

robot_coords = np.array([array([0.16431753, 0.13140975], dtype=float32),
array([0.2641115 , 0.11613164], dtype=float32),
array([0.3092924 , 0.11545982], dtype=float32),
array([ 0.16503447, -0.03309003], dtype=float32),
array([ 0.27562898, -0.03351239], dtype=float32),
array([ 0.31386122, -0.03431487], dtype=float32),
array([ 0.16896546, -0.17180271], dtype=float32),
array([ 0.2618817 , -0.16135776], dtype=float32),
array([ 0.30938584, -0.16271168], dtype=float32)])

poly = PolynomialFeatures(1)
temp = poly.fit_transform(rgb_coords)
print(temp.shape)
matrix = gym_replab.utils.compute_robot_transformation_matrix(np.array(temp), np.array(robot_coords))
print(matrix)
residuals = gym_replab.utils.rgb_to_robot_coords(rgb_coords, matrix) - robot_coords
residuals = [np.linalg.norm(i) for i in residuals]
print(residuals)
