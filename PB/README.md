# WL Pattern Analyzer

## Overview
WL Pattern Analyzer is a sophisticated pattern analysis tool designed to identify, visualize, and predict patterns in win/loss sequences. The application uses advanced statistical methods and multiple analysis algorithms to detect patterns and make predictions based on historical data.

## Features

### Core Features
- Record and analyze Win/Loss sequences
- Multiple prediction algorithms
- Visual result history display
- Detailed pattern statistics
- Save and load data functionality
- Real-time prediction updates

### Analysis Algorithms
1. **Pattern Analysis**: Analyzes sequences of various lengths
2. **Matrix Analysis**: Studies 5x5 matrix patterns
3. **Adaptive Analysis**: Weighted analysis based on trends
4. **Enhanced Analysis**: Advanced geometric and spatial pattern detection
5. **Combined Analysis**: Uses the strongest prediction from all algorithms

### Enhanced Analysis Models
The application includes 12 sophisticated analysis models:

1. **Diagonal Pattern Analysis**: Examines patterns along main diagonal, anti-diagonal, and parallel diagonals
2. **Rectangle/Square Region Analysis**: Analyzes 2x2, 2x3, 3x2, and 3x3 rectangular regions
3. **L-Shape Pattern Analysis**: Identifies L-shaped patterns in multiple orientations
4. **T-Shape Pattern Analysis**: Examines T-shaped patterns in various orientations
5. **Spiral Pattern Analysis**: Analyzes patterns in spiral formation, both outside-in and inside-out
6. **Neighbor Pattern Analysis**: Studies how the 8 neighbors around a cell influence outcomes
7. **Zigzag Pattern Analysis**: Identifies zigzag patterns both horizontally and vertically
8. **Scatter Analysis**: Examines the distribution and clustering of wins and losses
9. **Quadrant Analysis**: Divides the matrix into four quadrants and analyzes relationships
10. **Symmetry Analysis**: Evaluates horizontal, vertical, and diagonal symmetry patterns
11. **Border Analysis**: Compares patterns between border and interior cells
12. **Heatmap Analysis**: Creates density maps of wins and losses to identify hotspots

## Getting Started

### Requirements
- Python 3.6 or higher
- PyQt5
- NumPy

### Installation
1. Install the required packages:
```
pip install PyQt5 numpy
```

2. Clone or download the application files
3. Run the main application:
```
python pattern.py
```

### Usage
1. **Recording Results**:
   - Click the WIN or LOSS buttons to record individual results
   - Use the Bulk Entry field to add multiple results at once (e.g., "W L W L W")

2. **Analyzing Patterns**:
   - Select the desired algorithm from the dropdown menu
   - View predictions in the PREDICTION tab
   - Explore detailed analysis in the ANALYSIS and ENHANCED tabs

3. **Working with Data**:
   - Use SAVE to export your data to a text file
   - Use LOAD to import previously saved data
   - Use DELETE to remove the last result
   - Use CLEAR to reset all data

4. **Configuration**:
   - Set the minimum sample size for statistical significance
   - Adjust pattern length for basic pattern analysis

## Interface Guide

### Main View
- **Left Panel**: Controls for recording data and configuration
- **Right Panel**: Multi-tab display with PREDICTION, HISTORY, ANALYSIS, and ENHANCED tabs

### Enhanced Analysis Tab
Select different analysis types from the dropdown to view detailed statistics for each analysis model. Each model provides:
- Pattern statistics with win/loss percentages
- Color-coded highlighting of significant patterns
- Specialized visualizations for certain analysis types

## Statistical Methodology
The application employs several statistical approaches:
- Pattern frequency and outcome probability analysis
- Spatial relationship analysis in the matrix
- Trend detection and weighting
- Geometric pattern recognition
- Clustering and density analysis

Results with probability greater than 55% are highlighted, and predictions are made based on the pattern with the highest statistical probability and sample size.

## Tips for Optimal Use
1. Record at least 25-30 results for meaningful analysis
2. Experiment with different algorithms to find what works best for your data
3. Pay attention to the sample size - larger samples provide more reliable predictions
4. The Combined Analysis algorithm often provides the most balanced predictions
5. Check the Enhanced tab for deeper insights into complex patterns

## File Formats
Data is saved as simple text files with W and L characters representing wins and losses. Example:
```
W W L W L L W W W L W L W L W W L L W W
```

## License
This software is provided for educational and research purposes only. Always gamble responsibly and in accordance with local laws and regulations.