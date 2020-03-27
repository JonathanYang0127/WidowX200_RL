import os

import matplotlib.pyplot as plt
import pcl
import numpy as np
from sklearn.cluster import dbscan

# Old Replab Settings
# TRAY_CENTER = np.array([0.05, 0.05, 0.7]) # calibrate this everytime the camera is moved
# margin = 0.018
# TRAY_LOWERBOUND = np.array([-0.1277, -0.1018, 0.6452]) + np.array([margin, margin, 0])
# TRAY_UPPERBOUND = np.array([0.2334, 0.1443, 0.7494]) - np.array([margin, margin, 0])

# New Widow200 Settings
TRAY_CENTER = np.array([0.025, 0.05, 0.7])
margin = 0.02
TRAY_LOWERBOUND = np.array([-0.17, -0.1,  0.6]) + np.array([margin, margin, 0])
# --Teddy in the corner: [-0.13604932, -0.07284055,  0.8274319]
TRAY_UPPERBOUND = np.array([0.24, 0.2, 0.86]) - np.array([margin, margin, 0])
# --Teddy in the corner: [0.2083086, 0.16757944, 0.63460684]
PC_TO_ROBOT_TRANSMATRIX = [[-0.09791446, -1.0184524,  -0.0192177 ],
 [-3.7841015,  -2.2033608,   0.29452783],
 [-3.2073226,  -2.824164,    0.34469584],
 [ 2.856357,    2.2066314,  -0.20683573]]


PCD_IN = "pc0.pcd"
VERBOSE = True

# Old transformation matrix
# np.array([
#     [ 1.06882217,  0.14424542,  0.02702813],
#     [-0.09740936,  1.81315984,  0.35831866],
#     [-0.04663416,  1.08545626,  0.6689786 ],
#     [-0.00493222, -0.81908478, -0.06038063]
# ])

def filter_pcd_to_pc_array(pcd_in):
    """
    Input: `pcd_in`: filepath of pcd file we want to cluster.
    Side Effects: A new .pcd file is saved called `pcd_in`_clustered.pcd which filters points,
    keeping only those within a specified distance range.
    output: none.
    """
    # old replab settings: (0.6, 0.83, 0.24)
    LOW_DIST_THRESH = 0.65 # 0.6
    HIGH_DIST_THRESH = 0.95 # 0.83
    TRAY_RADIUS = 0.26 # 0.24
    pc_in = pcl.load_XYZRGB(pcd_in) # load input point cloud
    pc_in_array = np.asarray(pc_in)
    pc_out_array = pc_in_array.copy()
    tray_pts_indices = []
    for i in range(pc_out_array.shape[0]):
        pt = pc_out_array[i]
        pt_dist = np.linalg.norm(pt[:3])
        tray_center_pt_dist = np.linalg.norm(pt[:3] - TRAY_CENTER)
        if tray_center_pt_dist < TRAY_RADIUS and (pt_dist > LOW_DIST_THRESH and pt_dist < HIGH_DIST_THRESH):
            tray_pts_indices.append(i)
            # pt[3] = 0xffff00 # R,G,B = FF, 00, 00
        else:
            # pt[0] = 0
            # pt[1] = 0
            # pt[2] = 0
            pt[3] = 0x0 # 0 # appears as black though. 16777215 # R,G,B = FF, FF, FF
    # add random noise (black points) (for localization purposes)
    # pc_out_array = np.concatenate((pc_out_array, random_points_array_at(0.05, 0.05, 0.7, 0)), axis=0).astype(np.float32)
    return pc_out_array[tray_pts_indices, :]

def random_points_array_at(x, y, z, rgb, num_points=200, std_dev=0.002):
    random_pts_array = np.random.normal([x, y, z, rgb], scale=[std_dev]*3 + [0], size=(num_points, 4))
    x = random_pts_array.astype(np.float32)
    return x

def cluster_pc_array(pc_array, pc_to_robot_transmatrix=PC_TO_ROBOT_TRANSMATRIX):
    core_samples, labels = dbscan(pc_array, eps=0.02, min_samples=100)
    # np.savetxt("core_samples.txt", core_samples)
    # np.savetxt("labels.txt", labels)
    if VERBOSE: print("set(labels)", set(labels))
    colors = [0xffff00, 0xff00ff, 0x00ffff, 0xff0000, 0x00ff00, 0x0000ff,
              0xaaaa00, 0xaa00aa, 0x00aaaa, 0xaa0000, 0x00aa00, 0x0000aa,
              0x555500, 0x550055, 0x005555, 0x550000, 0x005500, 0x000055,
              0]
    # Group clusters into arrays
    label_indices = [[] for _ in range(len(set(labels)))]
    for i in range(pc_array.shape[0]):
        pt = pc_array[i]
        # pt[3] = colors[labels[i]]
        label_indices[labels[i]].append(i) # place indices in proper bin
    # print("label_indices[0]", label_indices[0])
    cluster_centers = [np.mean(pc_array[label_indices[i], :], axis=0)[:3] for i in range(len(set(labels)))]
    if VERBOSE: print("cluster_centers", cluster_centers)

    clusters = [] # a list of np.arrays, where each np.array is a cluster's points in pc coordinates.

    # Recoloring only clusters within our tray bounds
    for i in range(pc_array.shape[0]):
        pt = pc_array[i]
        if ((cluster_centers[labels[i]] >= TRAY_LOWERBOUND).all() and
            (cluster_centers[labels[i]] <= TRAY_UPPERBOUND).all()):
            pt[3] = colors[labels[i]]

    # plot cluster_centers in point cloud as concentrated blobs:
    #print("Clusters on the tray:")
    for i in range(len(set(labels)) - 1): #exclude the noise cluster
        cc_i_x, cc_i_y, cc_i_z = cluster_centers[i]
        if (cluster_centers[i] >= TRAY_LOWERBOUND).all() and (cluster_centers[i] <= TRAY_UPPERBOUND).all(): # i == 4:
            if VERBOSE:
                print(
                    "cluster_centers[{}]".format(i),
                    cluster_centers[i], "--> robot_coords",
                    pc_to_robot_coords(cluster_centers[i], pc_to_robot_transmatrix)
                )
            pc_array = np.concatenate((pc_array, random_points_array_at(cc_i_x, cc_i_y, cc_i_z, colors[i])), axis=0).astype(np.float32)
            clusters.append(pc_array[label_indices[i], :][:,:3]) # add valid object cluster array to cluster list.
            # Get first 3 cols (ignore 4th color column)
    # Plot the center of the tray
    cc_i_x, cc_i_y, cc_i_z = TRAY_CENTER
    pc_array = np.concatenate((pc_array, random_points_array_at(cc_i_x, cc_i_y, cc_i_z, colors[-1], num_points=1000)), axis=0).astype(np.float32)
    # if VERBOSE: print("clusters", clusters)
    return pc_array, clusters

def get_pc_cluster_center(pcd_in=PCD_IN):
    # pcd_in = "pc0.pcd"
    filtered_pc_array = filter_pcd_to_pc_array(pcd_in)
    pc_array = filtered_pc_array

    core_samples, labels = dbscan(pc_array, eps=0.02, min_samples=100)
    # np.savetxt("core_samples.txt", core_samples)
    # np.savetxt("labels.txt", labels)
    if VERBOSE: print("set(labels)", set(labels))
    colors = [0xffff00, 0xff00ff, 0x00ffff, 0xff0000, 0x00ff00, 0x0000ff,
              0xaaaa00, 0xaa00aa, 0x00aaaa, 0xaa0000, 0x00aa00, 0x0000aa,
              0x555500, 0x550055, 0x005555, 0x550000, 0x005500, 0x000055,
              0]
    # Recoloring
    label_indices = [[] for _ in range(len(set(labels)))]
    for i in range(pc_array.shape[0]):
        pt = pc_array[i]
        pt[3] = colors[labels[i]]
        label_indices[labels[i]].append(i) # place indices in proper bin
    # print("label_indices[0]", label_indices[0])
    cluster_centers = [np.mean(pc_array[label_indices[i], :], axis=0)[:3] for i in range(len(set(labels)))]
    if VERBOSE: print("cluster_centers", cluster_centers)

    clusters = [] # a list of np.arrays, where each np.array is a cluster's points in pc coordinates.

    # plot cluster_centers in point cloud as concentrated blobs:
    #print("Clusters on the tray:")
    for i in range(len(set(labels)) - 1): #exclude the noise cluster
        cc_i_x, cc_i_y, cc_i_z = cluster_centers[i]
        if (cluster_centers[i] >= TRAY_LOWERBOUND).all() and (cluster_centers[i] <= TRAY_UPPERBOUND).all(): # i == 4:
            return cluster_centers[i]


def save_pc_array_to_pcd(pc_array, pcd_out):
    pc = pcl.PointCloud_PointXYZRGB(pc_array)
    pcl.save_XYZRGBA(pc, pcd_out)

def pc_to_robot_coords(pc_coords, pc_to_robot_transmatrix=PC_TO_ROBOT_TRANSMATRIX):
    # add vector of 1s as feature to the pc_coords.
    if VERBOSE: print("pc_coords.shape", pc_coords.shape)
    if len(pc_coords.shape) == 1:
        pc_coords = np.array(list(pc_coords) + [1])
    elif len(pc_coords.shape) == 2:
        pc_coords = np.concatenate((pc_coords, np.ones((pc_coords.shape[0], 1))), axis=-1)
    else:
        raise NotImplementedError("pc_to_robot_coords(...) unsupported for shape {}".format(pc_coords.shape))
    # print("pc_to_robot_coords(): using pc_to_robot_transmatrix:")
    # print(pc_to_robot_transmatrix)
    robot_coords = pc_coords @ pc_to_robot_transmatrix
    # print(robot_coords)
    return robot_coords


def pc_to_robot_coords_list(
        pc_coords_list,
        project_onto_xy=True,
        pc_to_robot_transmatrix=PC_TO_ROBOT_TRANSMATRIX
    ):
    # pc_to_robot_coords(...), but takes in a list of pc_coords.
    if project_onto_xy: # throw out the 3rd (index 2) column, which is z.
        return [pc_to_robot_coords(pc_coord, pc_to_robot_transmatrix)[:,:2] for pc_coord in pc_coords_list]
    else:
        return [pc_to_robot_coords(pc_coord, pc_to_robot_transmatrix) for pc_coord in pc_coords_list]

def principal_components(X, i):
    """Returns first i (principal components, singular values) of same dimension of X"""
    # center X
    X_mean = np.mean(X, axis=0)
    X_stds = np.std(X, axis=0)
    X_centered = (X - X_mean)
    u, s, vh = np.linalg.svd(X_centered)
    return vh[:i], s[:i], X_mean

def plot_cluster_and_principal_components(
        clusters_list,
        principal_components_list,
        clusters_centers_list,
        clusters_sing_vals_list
    ):
    plt.plot(0)
    for i in range(len(clusters_list)):
        plt.scatter(clusters_list[i][:,0], clusters_list[i][:, 1])
        cluster_center_x_i, cluster_center_y_i = clusters_centers_list[i]
        for j in range(len(principal_components_list[i])):
            x_ij, y_ij = principal_components_list[i][j]
            cluster_sing_val_sq_ij = (clusters_sing_vals_list[i][j] ** 2) / 4 # arbitrary scaling
            if VERBOSE: print("="*10)
            # print("x_ij, y_ij", x_ij, y_ij)
            # print("cluster_sing_val_sq_ij", cluster_sing_val_sq_ij)
            print("x_ij * cluster_sing_val_sq_ij, y_ij * cluster_sing_val_sq_ij", x_ij * cluster_sing_val_sq_ij, y_ij * cluster_sing_val_sq_ij)
            print("cluster_center_x_i, cluster_center_y_i", cluster_center_x_i, cluster_center_y_i)
            arrow_color = str(np.clip(0.3*j, 0, 1))
            # print("arrow_color", arrow_color)
            plt.quiver(
                cluster_center_x_i,
                cluster_center_y_i,
                x_ij * cluster_sing_val_sq_ij,
                y_ij * cluster_sing_val_sq_ij,
                scale_units="xy",
                scale=1,
                color=arrow_color
            )
        plt.title("Object {} Point Cloud".format(i))
        plt.xlabel("robot coord x")
        plt.ylabel("robot coord y")
        plt.axis("equal")
        plt.savefig("principal_coords_obj{}.png".format(i))

def choose_center_and_pc(
        clusters_list,
        principal_components_list,
        clusters_centers_list,
        clusters_sing_vals_list
    ):
    if len(clusters_centers_list) == 0:
        return None
    center = np.array(clusters_centers_list[0])
    vector = np.array(principal_components_list[0][1])
    return center, vector

def compute_center_and_pc(pcd_in=PCD_IN, pc_to_robot_transmatrix=PC_TO_ROBOT_TRANSMATRIX):
    # pcd_in = "pc0.pcd"
    filtered_pc_array = filter_pcd_to_pc_array(pcd_in)
    clustered_pc_array, object_clusters = cluster_pc_array(filtered_pc_array, pc_to_robot_transmatrix)
    pcd_in_name = os.path.splitext(pcd_in)[0]
    pcd_clustered_filename = pcd_in_name + "_clustered.pcd"
    save_pc_array_to_pcd(clustered_pc_array, pcd_clustered_filename)
    print("{} saved in".format(pcd_clustered_filename), os.path.abspath(os.getcwd()))
    # Plot PCA stuff.
    # convert object cluster points in pc coords --> robot coords.
    object_clusters_in_robot_coords_xy = pc_to_robot_coords_list(
        object_clusters,
        project_onto_xy=True,
        pc_to_robot_transmatrix=pc_to_robot_transmatrix
    )
    pc_infos = [principal_components(obj_cluster, 2) for obj_cluster in object_clusters_in_robot_coords_xy]
    # object_clusters_in_robot_coords_xy = [np.array([[-100, 0], [100, 0], [0, -10], [0, 10]])]
    object_clusters_principal_components = [pc_info[0] for pc_info in pc_infos]
    clusters_sing_vals_list = [pc_info[1] for pc_info in pc_infos]
    clusters_centers_list = [pc_info[2] for pc_info in pc_infos]
    return choose_center_and_pc(
        object_clusters_in_robot_coords_xy,
        object_clusters_principal_components,
        clusters_centers_list,
        clusters_sing_vals_list
    )

if __name__ == "__main__":
    compute_center_and_pc()
