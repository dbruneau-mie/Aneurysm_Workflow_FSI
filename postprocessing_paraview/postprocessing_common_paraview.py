import sys
import os


def get_visualization_path(case_path):

    # Finds the visualization path for TurtleFSI simulations
    for file in os.listdir(case_path):
        file_path = os.path.join(case_path, file)
        if os.path.exists(os.path.join(file_path, "1")):
            visualization_path = os.path.join(file_path, "1/Visualization")
        elif os.path.exists(os.path.join(file_path, "Visualization")):
            visualization_path = os.path.join(file_path, "Visualization")
    
    return visualization_path